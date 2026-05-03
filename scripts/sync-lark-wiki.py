#!/usr/bin/env python3
"""
Lark Wiki Sync Script
Syncs Feishu/Lark Wiki docs to local markdown files for Hermes Agent.

Usage: python ~/.hermes/scripts/sync-lark-wiki.py
"""

import os
import sys
import requests
import hashlib
import json
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path.home() / ".hermes/.env")

# Configuration
LARK_APP_ID = os.getenv("LARK_APP_ID")
LARK_APP_SECRET = os.getenv("LARK_APP_SECRET")
LARK_TENANT_KEY = os.getenv("LARK_TENANT_KEY", "")
WIKI_PATH = Path(os.getenv("WIKI_PATH", "~/company-wiki")).expanduser()

# API endpoints
LARK_AUTH_URL = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
LARK_DOCS_URL = "https://open.feishu.cn/open-apis/docx/v1/documents"

def get_tenant_access_token():
    """Get Lark tenant access token for API calls."""
    if not LARK_APP_ID or not LARK_APP_SECRET:
        raise Exception("Missing LARK_APP_ID or LARK_APP_SECRET in ~/.hermes/.env")
    
    payload = {
        "app_id": LARK_APP_ID,
        "app_secret": LARK_APP_SECRET
    }
    response = requests.post(LARK_AUTH_URL, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    if data.get("code") != 0:
        raise Exception(f"Lark auth failed: {data}")
    return data["tenant_access_token"]

def fetch_all_documents(token):
    """Fetch all documents from Lark Wiki."""
    headers = {"Authorization": f"Bearer {token}"}
    documents = []
    page_token = None
    
    while True:
        params = {"page_size": 50}
        if page_token:
            params["page_token"] = page_token
        
        response = requests.get(LARK_DOCS_URL, headers=headers, params=params, timeout=60)
        response.raise_for_status()
        data = response.json()
        
        if data.get("code") != 0:
            raise Exception(f"Lark API error: {data}")
        
        items = data.get("data", {}).get("items", [])
        documents.extend(items)
        
        # Check for more pages
        has_more = data.get("data", {}).get("has_more", False)
        if not has_more:
            break
        page_token = data.get("data", {}).get("page_token")
        
        # Rate limiting protection
        time.sleep(0.5)
    
    return documents

def fetch_document_content(token, doc_id):
    """Fetch full content of a single document."""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{LARK_DOCS_URL}/{doc_id}/raw_content",
        headers=headers,
        params={"document_type": "markdown"},
        timeout=60
    )
    response.raise_for_status()
    data = response.json()
    return data.get("data", {}).get("content", "")

def compute_sha256(content):
    """Compute SHA256 hash of content for change detection."""
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def save_document_to_wiki(doc, content, raw_dir):
    """Save a document to the local wiki."""
    # Create safe filename
    title = doc.get("title", "untitled")
    safe_title = "".join(c if c.isalnum() else "-" for c in title).lower()
    doc_id = doc.get("document_id", "unknown")
    filename = f"{safe_title}-{doc_id[:8]}.md"
    filepath = raw_dir / filename
    
    # Compute hash for change detection
    content_hash = compute_sha256(content)
    
    # Check if file exists and content unchanged
    if filepath.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            existing = f.read()
        # Simple check: if hash in existing file, skip
        if content_hash in existing:
            print(f"⏭️  Skipped (unchanged): {title}")
            return filepath, False
    
    # Create frontmatter
    frontmatter = f"""---
source_url: https://feishu.cn/docs/{doc_id}
ingested: {datetime.now().strftime('%Y-%m-%d')}
sha256: {content_hash}
lark_title: {title}
lark_id: {doc_id}
---

"""
    
    # Write file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(frontmatter)
        f.write(content)
        f.write("\n\n---\n")
        f.write(f"_Synced from Lark on {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n")
    
    print(f"✅ Saved: {title}")
    return filepath, True

def update_index_md(wiki_path, documents):
    """Update the wiki index.md file."""
    index_path = wiki_path / "index.md"
    
    # Build index content
    lines = [
        "# Company Wiki Index",
        "",
        "> Content catalog synced from Lark Wiki",
        f"> Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"> Total documents: {len(documents)}",
        "",
        "## Documents",
        "",
    ]
    
    for doc in sorted(documents, key=lambda x: x.get("title", "")):
        title = doc.get("title", "Untitled")
        doc_id = doc.get("document_id", "")
        updated = doc.get("updated_at", "")
        lines.append(f"- [[{title}]] — Updated: {updated}")
    
    lines.append("")
    lines.append("---")
    lines.append(f"_Auto-generated by sync-lark-wiki.py_")
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    
    print(f"📑 Updated index.md with {len(documents)} documents")

def update_log_md(wiki_path, new_count, skipped_count):
    """Append to log.md."""
    log_path = wiki_path / "log.md"
    
    # Create if doesn't exist
    if not log_path.exists():
        log_path.write_text("# Wiki Sync Log\n\n")
    
    entry = f"""## [{datetime.now().strftime('%Y-%m-%d')}] sync | Lark Wiki
- New/updated documents: {new_count}
- Skipped (unchanged): {skipped_count}
- Total documents in wiki: {new_count + skipped_count}

"""
    
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(entry)

def main():
    """Main sync function."""
    print(f"🚀 Starting Lark Wiki sync...")
    print(f"📁 Wiki path: {WIKI_PATH}")
    
    # Ensure directories exist
    raw_dir = WIKI_PATH / "raw" / "lark"
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    # Get access token
    try:
        token = get_tenant_access_token()
        print("🔑 Got Lark access token")
    except Exception as e:
        print(f"❌ Auth failed: {e}")
        print("💡 Check LARK_APP_ID and LARK_APP_SECRET in ~/.hermes/.env")
        sys.exit(1)
    
    # Fetch all documents
    try:
        print("📚 Fetching document list...")
        documents = fetch_all_documents(token)
        print(f"📄 Found {len(documents)} documents")
    except Exception as e:
        print(f"❌ Failed to fetch documents: {e}")
        sys.exit(1)
    
    # Sync each document
    new_count = 0
    skipped_count = 0
    
    for i, doc in enumerate(documents, 1):
        print(f"[{i}/{len(documents)}] Processing: {doc.get('title', 'Untitled')}")
        
        try:
            content = fetch_document_content(token, doc.get("document_id"))
            filepath, is_new = save_document_to_wiki(doc, content, raw_dir)
            
            if is_new:
                new_count += 1
            else:
                skipped_count += 1
            
            # Rate limiting protection
            time.sleep(1)
                
        except Exception as e:
            print(f"⚠️  Error syncing {doc.get('title')}: {e}")
            continue
    
    # Update index and log
    update_index_md(WIKI_PATH, documents)
    update_log_md(WIKI_PATH, new_count, skipped_count)
    
    # Summary
    print(f"\n✅ Sync complete!")
    print(f"   New/updated: {new_count}")
    print(f"   Skipped: {skipped_count}")
    print(f"   Total: {len(documents)}")
    print(f"   Location: {WIKI_PATH}")

if __name__ == "__main__":
    main()
