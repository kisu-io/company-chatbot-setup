---
name: training-system
description: "Employee training system: learning paths, progress tracking, quizzes, certifications."
version: 1.0.0
author: Hermes Agent (for Keezhu)
license: MIT
metadata:
  hermes:
    tags: [training, education, quizzes, progress-tracking, employee-onboarding]
    category: devops
    related_skills: [llm-wiki, native-mcp]
---

# Employee Training System

Build and operate an AI-powered employee training platform using Lark Wiki content and Hermes Agent.

## When This Skill Activates

Use this skill when the user:
- Wants to train employees using company wiki content
- Needs to create learning paths from existing documentation
- Wants to generate quizzes from source materials
- Needs progress tracking and certification system
- Asks about employee onboarding automation
- Wants compliance tracking and reporting

## System Architecture

```
Lark Wiki → Sync → Local Markdown → Training DB → Telegram Bot → Employees
                              ↓
                        Quiz Generator (AI)
                              ↓
                        Progress Tracking
                              ↓
                        Manager Dashboard
```

## Quick Start

### 1. Initialize Database

```bash
python3 ~/projects/company-chatbot/scripts/training_db.py
```

### 2. Create First Learning Path

```bash
python3 -c "
from training_db import create_learning_path, create_module

# Create path
create_learning_path(
    path_id='new-hire-onboarding',
    title='New Hire Onboarding',
    description='Essential knowledge for all new employees',
    target_audience=['all'],
    estimated_hours=8,
    required=True
)

# Add modules
create_module(
    module_id='company-mission',
    path_id='new-hire-onboarding',
    title='Company Mission & Values',
    module_type='read',
    source='raw/lark/company-handbook.md',
    order_index=1,
    estimated_minutes=30
)

create_module(
    module_id='security-basics',
    path_id='new-hire-onboarding',
    title='Security Fundamentals',
    module_type='read+quiz',
    source='raw/lark/security-policy.md',
    order_index=2,
    estimated_minutes=60,
    quiz_required=True,
    passing_score=80
)
"
```

### 3. Generate Quiz Questions

Use the `generate-quiz-questions` function below to auto-create quizzes from source docs.

### 4. Test with Training Bot

```bash
python3 ~/projects/company-chatbot/scripts/training_bot.py
```

## Core Functions

### Create Learning Path

```python
from training_db import create_learning_path, create_module

create_learning_path(
    path_id='engineer-onboarding',
    title='Engineer Onboarding',
    description='Technical onboarding for engineering team',
    target_audience=['engineer', 'developer'],
    estimated_hours=16,
    required=True
)

create_module(
    module_id='dev-environment',
    path_id='engineer-onboarding',
    title='Development Environment Setup',
    module_type='read',
    source='raw/lark/dev-setup.md',
    order_index=1,
    estimated_minutes=90
)
```

### Generate Quiz Questions (AI-Powered)

```python
def generate_quiz_questions(source_text: str, module_id: str, 
                           num_questions: int = 10,
                           difficulty: str = 'medium'):
    """
    Generate quiz questions from source material using AI.
    
    Args:
        source_text: The learning content (markdown)
        module_id: Target module ID
        num_questions: Number of questions to generate
        difficulty: easy, medium, or hard
    """
    import requests
    
    prompt = f"""
Generate {num_questions} multiple-choice quiz questions from this content.
Difficulty: {difficulty}

For each question, provide:
- question_id: unique identifier (e.g., "sec-001")
- question_text: the question
- options: 4 answer choices (A, B, C, D)
- correct_answer: the correct option text
- explanation: why the answer is correct
- points: 10 for easy, 20 for medium, 30 for hard
- difficulty: easy/medium/hard

Content:
{source_text[:5000]}  # Truncate to avoid token limits

Output as JSON array.
"""
    
    # Call LLM (using Hermes or direct API)
    response = requests.post(
        'http://localhost:18789/chat',
        json={'message': prompt},
        headers={'Authorization': 'Bearer YOUR_TOKEN'}
    )
    
    questions = response.json()
    
    # Save to database
    from training_db import create_quiz_question
    
    for q in questions:
        create_quiz_question(
            question_id=q['question_id'],
            module_id=module_id,
            question_text=q['question_text'],
            question_type='multiple_choice',
            options=q['options'],
            correct_answer=q['correct_answer'],
            explanation=q['explanation'],
            points=q['points'],
            difficulty=q['difficulty']
        )
    
    return len(questions)
```

### Enroll Employee

```python
from training_db import create_or_update_employee, enroll_employee

# Register employee
create_or_update_employee(
    employee_id='telegram_566009262',
    name='Keezhu',
    role='engineer',
    department='Engineering',
    manager_id='telegram_123456'
)

# Enroll in path
enroll_employee('telegram_566009262', 'new-hire-onboarding')
```

### Track Progress

```python
from training_db import update_module_progress, get_employee_enrollments

# Complete module
update_module_progress(
    employee_id='telegram_566009262',
    module_id='company-mission',
    status='completed',
    time_spent_minutes=28
)

# Get progress
enrollments = get_employee_enrollments('telegram_566009262')
for e in enrollments:
    print(f"{e['path_title']}: {e['status']}")
```

### Award Badges

```python
from training_db import award_badge, create_badge

# Create custom badge
create_badge(
    badge_id='security-expert',
    name='Security Expert',
    description='Complete security training with 95%+ score',
    icon='🛡️'
)

# Award to employee
award_badge('telegram_566009262', 'security-expert')
```

## Telegram Bot Commands

### Employee Commands

| Command | Description |
|---------|-------------|
| `/start` | Register + welcome message |
| `/paths` | List available learning paths |
| `/enroll [path]` | Enroll in a learning path |
| `/continue` | Resume current learning |
| `/complete [module]` | Mark module complete |
| `/quiz [module]` | Start module quiz |
| `/progress` | View personal progress |
| `/badges` | View earned badges |
| `/streak` | Check learning streak |
| `/certificate [path]` | Get completion certificate |

### Manager Commands

| Command | Description |
|---------|-------------|
| `/team` | View team progress |
| `/team/[employee]` | Individual employee progress |
| `/compliance` | Compliance report |
| `/assign [path] [@emp]` | Assign path to employee |
| `/remind [@employee]` | Send learning reminder |

## Quiz Generation Templates

### Multiple Choice

```python
question = {
    "question_id": "sec-001",
    "question_text": "What is the minimum password length?",
    "question_type": "multiple_choice",
    "options": [
        "8 characters",
        "12 characters", 
        "16 characters",
        "20 characters"
    ],
    "correct_answer": "12 characters",
    "explanation": "Per security policy section 3.2, all passwords must be at least 12 characters.",
    "points": 20,
    "difficulty": "medium"
}
```

### True/False

```python
question = {
    "question_id": "sec-002",
    "question_text": "Two-factor authentication is optional for all employees.",
    "question_type": "true_false",
    "options": ["True", "False"],
    "correct_answer": "False",
    "explanation": "2FA is mandatory per security policy section 4.1.",
    "points": 10,
    "difficulty": "easy"
}
```

### Short Answer (AI-Graded)

```python
question = {
    "question_id": "sec-003",
    "question_text": "What are the three pillars of information security?",
    "question_type": "short_answer",
    "options": [],  # Empty for short answer
    "correct_answer": "Confidentiality, Integrity, Availability",
    "explanation": "The CIA triad is the foundation of information security.",
    "points": 30,
    "difficulty": "hard"
}
```

## Gamification System

### Points

| Action | Points |
|--------|--------|
| Enroll in path | +25 |
| Complete module | +50 |
| Pass quiz (first try) | +100 |
| Pass quiz (>80%) | +50 |
| Complete learning path | +500 |
| 7-day streak | +200 |
| 30-day streak | +1000 |

### Default Badges

| Badge ID | Name | Requirement |
|----------|------|-------------|
| `first-week` | 🌱 First Week | Complete first module |
| `bookworm` | 📚 Bookworm | Complete 10 modules |
| `quiz-master` | 🎯 Quiz Master | Pass 5 quizzes with 100% |
| `week-streak` | 🔥 7-Day Streak | Learn 7 days in a row |
| `path-finder` | 🏆 Path Finder | Complete first path |
| `security-certified` | 🛡️ Security Certified | Pass security compliance |

## Certificate Generation

```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

def generate_certificate(employee_name: str, path_title: str, 
                        completion_date: str, output_path: str):
    """Generate PDF certificate."""
    c = canvas.Canvas(output_path, pagesize=letter)
    
    # Title
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(300, 700, "Certificate of Completion")
    
    # Employee name
    c.setFont("Helvetica", 24)
    c.drawCentredString(300, 600, "This certifies that")
    c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(300, 550, employee_name)
    
    # Path title
    c.setFont("Helvetica", 24)
    c.drawCentredString(300, 450, "has successfully completed")
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(300, 400, path_title)
    
    # Date
    c.setFont("Helvetica", 18)
    c.drawCentredString(300, 300, f"Completed on {completion_date}")
    
    c.save()
    return output_path
```

## Analytics & Reporting

### Team Progress

```python
from training_db import get_team_progress, get_compliance_report

# Manager view
team = get_team_progress(manager_id='telegram_123456')
for emp in team:
    print(f"{emp['name']}: {emp['paths_completed']} paths, {emp['total_points']} pts")

# Compliance report
compliance = get_compliance_report()
missing = [r for r in compliance if r['enrollment_status'] != 'completed']
print(f"⚠️ {len(missing)} employees missing required training")
```

## Pitfalls

- **Don't skip database initialization** — Always run `training_db.py` first
- **Validate quiz answers case-insensitively** — Users may type "a" or "A"
- **Rate limit quiz retries** — Prevent gaming with 24-hour cooldown
- **Encrypt employee data** — Use encryption at rest for compliance
- **Manager access control** — Only show direct reports, not entire company
- **Backup database regularly** — `training.db` contains all progress data
- **Test quiz generation** — AI may generate incorrect questions, review before deploying

## Related Tools

- `llm-wiki` — Knowledge base structure
- `native-mcp` — Lark API integration
- `training_db.py` — Database operations
- `training_bot.py` — Bot logic
