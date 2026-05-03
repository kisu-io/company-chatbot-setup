#!/usr/bin/env python3
"""
Employee Training System — Database Manager
Handles SQLite database for progress tracking, quizzes, and certifications.
"""

import sqlite3
import json
from datetime import datetime, date
from pathlib import Path
from typing import Optional, List, Dict, Any

DB_PATH = Path.home() / ".hermes" / "training.db"

def get_connection():
    """Get database connection with row factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize database schema."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Employees table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            employee_id TEXT PRIMARY KEY,
            name TEXT,
            role TEXT,
            department TEXT,
            hire_date DATE,
            manager_id TEXT,
            level TEXT,
            total_points INTEGER DEFAULT 0,
            streak_days INTEGER DEFAULT 0,
            streak_last_active DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Learning paths table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS learning_paths (
            path_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            target_audience TEXT,
            estimated_hours REAL,
            required BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Modules table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS modules (
            module_id TEXT PRIMARY KEY,
            path_id TEXT,
            title TEXT NOT NULL,
            type TEXT,
            source TEXT,
            order_index INTEGER,
            estimated_minutes INTEGER,
            quiz_required BOOLEAN DEFAULT FALSE,
            passing_score INTEGER DEFAULT 70,
            FOREIGN KEY (path_id) REFERENCES learning_paths(path_id)
        )
    """)
    
    # Enrollments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS enrollments (
            employee_id TEXT,
            path_id TEXT,
            status TEXT,
            started_at TIMESTAMP,
            completed_at TIMESTAMP,
            PRIMARY KEY (employee_id, path_id),
            FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
            FOREIGN KEY (path_id) REFERENCES learning_paths(path_id)
        )
    """)
    
    # Module progress table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS module_progress (
            employee_id TEXT,
            module_id TEXT,
            status TEXT,
            completed_at TIMESTAMP,
            time_spent_minutes INTEGER,
            quiz_score INTEGER,
            quiz_attempts INTEGER DEFAULT 0,
            PRIMARY KEY (employee_id, module_id),
            FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
            FOREIGN KEY (module_id) REFERENCES modules(module_id)
        )
    """)
    
    # Quiz questions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_questions (
            question_id TEXT PRIMARY KEY,
            module_id TEXT,
            question_text TEXT NOT NULL,
            question_type TEXT,
            options TEXT,
            correct_answer TEXT,
            explanation TEXT,
            points INTEGER DEFAULT 10,
            difficulty TEXT,
            FOREIGN KEY (module_id) REFERENCES modules(module_id)
        )
    """)
    
    # Badges table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS badges (
            badge_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            icon TEXT,
            requirement TEXT
        )
    """)
    
    # Employee badges table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employee_badges (
            employee_id TEXT,
            badge_id TEXT,
            earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (employee_id, badge_id),
            FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
            FOREIGN KEY (badge_id) REFERENCES badges(badge_id)
        )
    """)
    
    # Quiz attempts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_attempts (
            attempt_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT,
            question_id TEXT,
            selected_answer TEXT,
            is_correct BOOLEAN,
            points_earned INTEGER,
            attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
            FOREIGN KEY (question_id) REFERENCES quiz_questions(question_id)
        )
    """)
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully")

# Employee Operations
def create_or_update_employee(employee_id: str, name: str = None, role: str = None, 
                             department: str = None, manager_id: str = None, level: str = None):
    """Create or update employee record."""
    conn = get_connection()
    cursor = conn.cursor()
    
    if name:
        cursor.execute("""
            INSERT INTO employees (employee_id, name, role, department, manager_id, level)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(employee_id) DO UPDATE SET
                name = excluded.name,
                role = excluded.role,
                department = excluded.department,
                manager_id = excluded.manager_id,
                level = excluded.level
        """, (employee_id, name, role, department, manager_id, level))
    else:
        cursor.execute("""
            INSERT OR IGNORE INTO employees (employee_id) VALUES (?)
        """, (employee_id,))
    
    conn.commit()
    conn.close()

def get_employee(employee_id: str) -> Optional[Dict]:
    """Get employee by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE employee_id = ?", (employee_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def update_employee_points(employee_id: str, points: int):
    """Add points to employee."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE employees SET total_points = total_points + ?
        WHERE employee_id = ?
    """, (points, employee_id))
    conn.commit()
    conn.close()

def update_streak(employee_id: str):
    """Update learning streak."""
    conn = get_connection()
    cursor = conn.cursor()
    today = date.today().isoformat()
    
    cursor.execute("SELECT streak_last_active, streak_days FROM employees WHERE employee_id = ?", 
                   (employee_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return
    
    last_active = row['streak_last_active']
    current_streak = row['streak_days'] or 0
    
    if last_active == today:
        # Already active today, don't update
        pass
    elif last_active and (date.today() - date.fromisoformat(last_active)).days == 1:
        # Consecutive day
        current_streak += 1
    else:
        # Reset streak
        current_streak = 1
    
    cursor.execute("""
        UPDATE employees SET streak_days = ?, streak_last_active = ?
        WHERE employee_id = ?
    """, (current_streak, today, employee_id))
    
    conn.commit()
    conn.close()

# Learning Path Operations
def create_learning_path(path_id: str, title: str, description: str = None,
                        target_audience: List[str] = None, estimated_hours: float = None,
                        required: bool = False):
    """Create a new learning path."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT OR REPLACE INTO learning_paths 
        (path_id, title, description, target_audience, estimated_hours, required)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (path_id, title, description, 
          json.dumps(target_audience) if target_audience else None,
          estimated_hours, required))
    
    conn.commit()
    conn.close()

def get_learning_path(path_id: str) -> Optional[Dict]:
    """Get learning path by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM learning_paths WHERE path_id = ?", (path_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        result = dict(row)
        result['target_audience'] = json.loads(result['target_audience']) if result['target_audience'] else []
        return result
    return None

def list_learning_paths(employee_role: str = None) -> List[Dict]:
    """List all learning paths, optionally filtered by employee role."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM learning_paths ORDER BY required DESC, title")
    rows = cursor.fetchall()
    conn.close()
    
    paths = []
    for row in rows:
        path = dict(row)
        path['target_audience'] = json.loads(path['target_audience']) if path['target_audience'] else []
        
        # Filter by role if provided
        if employee_role and path['target_audience']:
            if employee_role not in path['target_audience'] and 'all' not in path['target_audience']:
                continue
        
        paths.append(path)
    
    return paths

# Module Operations
def create_module(module_id: str, path_id: str, title: str, module_type: str = "read",
                 source: str = None, order_index: int = 0, estimated_minutes: int = 30,
                 quiz_required: bool = False, passing_score: int = 70):
    """Create a module in a learning path."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT OR REPLACE INTO modules 
        (module_id, path_id, title, type, source, order_index, estimated_minutes, 
         quiz_required, passing_score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (module_id, path_id, title, module_type, source, order_index, 
          estimated_minutes, quiz_required, passing_score))
    
    conn.commit()
    conn.close()

def get_modules_for_path(path_id: str) -> List[Dict]:
    """Get all modules for a learning path."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM modules WHERE path_id = ? ORDER BY order_index
    """, (path_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# Enrollment Operations
def enroll_employee(employee_id: str, path_id: str):
    """Enroll employee in a learning path."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT OR REPLACE INTO enrollments 
        (employee_id, path_id, status, started_at)
        VALUES (?, ?, 'in_progress', CURRENT_TIMESTAMP)
    """, (employee_id, path_id))
    
    conn.commit()
    conn.close()

def get_employee_enrollments(employee_id: str) -> List[Dict]:
    """Get all enrollments for an employee."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.*, lp.title as path_title, lp.description, lp.estimated_hours
        FROM enrollments e
        JOIN learning_paths lp ON e.path_id = lp.path_id
        WHERE e.employee_id = ?
        ORDER BY e.started_at DESC
    """, (employee_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def complete_enrollment(employee_id: str, path_id: str):
    """Mark enrollment as completed."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE enrollments SET status = 'completed', completed_at = CURRENT_TIMESTAMP
        WHERE employee_id = ? AND path_id = ?
    """, (employee_id, path_id))
    conn.commit()
    conn.close()

# Module Progress Operations
def update_module_progress(employee_id: str, module_id: str, status: str = "completed",
                          time_spent_minutes: int = None, quiz_score: int = None):
    """Update module progress."""
    conn = get_connection()
    cursor = conn.cursor()
    
    if time_spent_minutes is not None:
        cursor.execute("""
            UPDATE module_progress SET 
                status = ?, time_spent_minutes = ?, completed_at = CURRENT_TIMESTAMP
            WHERE employee_id = ? AND module_id = ?
        """, (status, time_spent_minutes, employee_id, module_id))
    elif quiz_score is not None:
        cursor.execute("""
            UPDATE module_progress SET 
                status = ?, quiz_score = ?, completed_at = CURRENT_TIMESTAMP
            WHERE employee_id = ? AND module_id = ?
        """, (status, quiz_score, employee_id, module_id))
    else:
        cursor.execute("""
            INSERT OR REPLACE INTO module_progress 
            (employee_id, module_id, status, completed_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (employee_id, module_id, status))
    
    conn.commit()
    conn.close()

def get_module_progress(employee_id: str, module_id: str) -> Optional[Dict]:
    """Get progress for a specific module."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM module_progress WHERE employee_id = ? AND module_id = ?
    """, (employee_id, module_id))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

# Quiz Operations
def create_quiz_question(question_id: str, module_id: str, question_text: str,
                        question_type: str = "multiple_choice", options: List[str] = None,
                        correct_answer: str = None, explanation: str = None,
                        points: int = 10, difficulty: str = "medium"):
    """Create a quiz question."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT OR REPLACE INTO quiz_questions 
        (question_id, module_id, question_text, question_type, options, 
         correct_answer, explanation, points, difficulty)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (question_id, module_id, question_text, question_type,
          json.dumps(options) if options else None,
          correct_answer, explanation, points, difficulty))
    
    conn.commit()
    conn.close()

def get_quiz_questions(module_id: str) -> List[Dict]:
    """Get all quiz questions for a module."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM quiz_questions WHERE module_id = ? ORDER BY question_id
    """, (module_id,))
    rows = cursor.fetchall()
    conn.close()
    
    questions = []
    for row in rows:
        q = dict(row)
        q['options'] = json.loads(q['options']) if q['options'] else []
        questions.append(q)
    
    return questions

def record_quiz_attempt(employee_id: str, question_id: str, selected_answer: str,
                       is_correct: bool, points_earned: int):
    """Record a quiz attempt."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO quiz_attempts 
        (employee_id, question_id, selected_answer, is_correct, points_earned)
        VALUES (?, ?, ?, ?, ?)
    """, (employee_id, question_id, selected_answer, is_correct, points_earned))
    
    conn.commit()
    conn.close()

# Badge Operations
def create_badge(badge_id: str, name: str, description: str = None, 
                icon: str = "🏆", requirement: str = None):
    """Create a badge."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT OR REPLACE INTO badges (badge_id, name, description, icon, requirement)
        VALUES (?, ?, ?, ?, ?)
    """, (badge_id, name, description, icon, requirement))
    
    conn.commit()
    conn.close()

def award_badge(employee_id: str, badge_id: str):
    """Award a badge to an employee."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if already has badge
    cursor.execute("""
        SELECT * FROM employee_badges WHERE employee_id = ? AND badge_id = ?
    """, (employee_id, badge_id))
    
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO employee_badges (employee_id, badge_id)
            VALUES (?, ?)
        """, (employee_id, badge_id))
        
        # Award points for badge (default 50 points)
        cursor.execute("""
            UPDATE employees SET total_points = total_points + 50
            WHERE employee_id = ?
        """, (employee_id,))
    
    conn.commit()
    conn.close()

def get_employee_badges(employee_id: str) -> List[Dict]:
    """Get all badges for an employee."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.*, eb.earned_at
        FROM badges b
        JOIN employee_badges eb ON b.badge_id = eb.badge_id
        WHERE eb.employee_id = ?
        ORDER BY eb.earned_at DESC
    """, (employee_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# Analytics Operations
def get_team_progress(manager_id: str) -> List[Dict]:
    """Get progress overview for manager's team."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.employee_id, e.name, e.role, 
               COUNT(DISTINCT ep.path_id) as paths_completed,
               e.total_points, e.streak_days
        FROM employees e
        LEFT JOIN enrollments ep ON e.employee_id = ep.employee_id AND ep.status = 'completed'
        WHERE e.manager_id = ?
        GROUP BY e.employee_id
        ORDER BY e.total_points DESC
    """, (manager_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_compliance_report() -> List[Dict]:
    """Get compliance report for required training."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.employee_id, e.name, e.department, lp.path_id, lp.title,
               e.status as enrollment_status
        FROM employees e
        CROSS JOIN learning_paths lp
        LEFT JOIN enrollments e ON e.employee_id = e.employee_id AND e.path_id = lp.path_id
        WHERE lp.required = 1
        ORDER BY e.department, e.name, lp.title
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# Initialize default badges
def init_default_badges():
    """Initialize default badge set."""
    badges = [
        ("first-week", "🌱 First Week", "Complete your first module", "🌱"),
        ("bookworm", "📚 Bookworm", "Complete 10 modules", "📚"),
        ("quiz-master", "🎯 Quiz Master", "Pass 5 quizzes with 100%", "🎯"),
        ("week-streak", "🔥 7-Day Streak", "Learn 7 days in a row", "🔥"),
        ("path-finder", "🏆 Path Finder", "Complete your first learning path", "🏆"),
        ("security-certified", "🛡️ Security Certified", "Pass security compliance", "🛡️"),
        ("fast-learner", "🚀 Fast Learner", "Complete path in <50% estimated time", "🚀"),
    ]
    
    for badge_id, name, description, icon in badges:
        create_badge(badge_id, name, description, icon)

if __name__ == "__main__":
    # Initialize database
    init_database()
    init_default_badges()
    print("✅ Training database ready!")
