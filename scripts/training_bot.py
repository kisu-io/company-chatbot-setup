#!/usr/bin/env python3
"""
Training Bot — Main Integration
Integrates with Hermes Agent to deliver training via Telegram.
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from training_db import (
    init_database, create_or_update_employee, get_employee,
    enroll_employee, get_employee_enrollments, get_learning_path,
    get_modules_for_path, update_module_progress, get_module_progress,
    get_quiz_questions, record_quiz_attempt, award_badge, get_employee_badges,
    update_employee_points, update_streak, list_learning_paths
)

class TrainingBot:
    """Main training bot logic."""
    
    def __init__(self):
        init_database()
    
    def register_employee(self, telegram_id: str, name: str, role: str = None,
                         department: str = None, manager_id: str = None):
        """Register or update employee."""
        create_or_update_employee(telegram_id, name, role, department, manager_id)
        return f"✅ {name} registered successfully!"
    
    def list_paths(self, employee_id: str):
        """List available learning paths."""
        employee = get_employee(employee_id)
        role = employee.get('role') if employee else None
        
        paths = list_learning_paths(role)
        
        if not paths:
            return "📚 No learning paths available yet."
        
        response = "📚 **Available Learning Paths**\n\n"
        
        for path in paths:
            required = "🔴 Required" if path['required'] else "🟢 Optional"
            hours = f"⏱️ {path['estimated_hours']}h" if path['estimated_hours'] else ""
            
            response += f"**{path['title']}**\n"
            response += f"{path['description']}\n"
            response += f"{required} {hours}\n\n"
        
        response += "\n_Enroll with: /enroll [path_name]_"
        
        return response
    
    def enroll(self, employee_id: str, path_id: str):
        """Enroll employee in a learning path."""
        path = get_learning_path(path_id)
        
        if not path:
            return f"❌ Learning path '{path_id}' not found."
        
        enroll_employee(employee_id, path_id)
        update_employee_points(employee_id, 25)  # Bonus for enrolling
        
        return f"""🎉 Enrolled in **{path['title']}**!

📊 Path Details:
{path['description']}

⏱️ Estimated: {path['estimated_hours']} hours
📖 Modules: {len(get_modules_for_path(path_id))}

Start with: /continue"""
    
    def continue_learning(self, employee_id: str):
        """Continue current learning."""
        enrollments = get_employee_enrollments(employee_id)
        
        # Find first in-progress enrollment
        active = next((e for e in enrollments if e['status'] == 'in_progress'), None)
        
        if not active:
            return "🎉 You have no active learning paths!\n\nBrowse available: /paths"
        
        # Get modules for this path
        modules = get_modules_for_path(active['path_id'])
        
        # Find first incomplete module
        for module in modules:
            progress = get_module_progress(employee_id, module['module_id'])
            if not progress or progress['status'] != 'completed':
                return self._present_module(employee_id, module, active)
        
        # All modules complete, mark path as complete
        return f"🎉 You've completed all modules in {active['path_title']}!\n\nUse /certificate to get your certificate."
    
    def _present_module(self, employee_id: str, module: dict, enrollment: dict):
        """Present a module to the employee."""
        response = f"""📖 **{module['title']}**

📚 Path: {enrollment['path_title']}
⏱️ Estimated: {module['estimated_minutes']} minutes
📄 Source: {module['source']}

"""
        
        if module['quiz_required']:
            response += """
**Instructions:**
1. Read the source material
2. Mark as complete: /complete [module_id]
3. Take quiz: /quiz [module_id]

"""
        else:
            response += """
**Instructions:**
1. Read the source material
2. Mark as complete: /complete [module_id]

"""
        
        response += f"\n_Commands: /complete {module['module_id']} | /quiz {module['module_id']} | /skip_"
        
        return response
    
    def complete_module(self, employee_id: str, module_id: str, time_spent: int = 30):
        """Mark module as complete."""
        update_module_progress(employee_id, module_id, 'completed', time_spent)
        update_employee_points(employee_id, 50)  # Points for completing module
        update_streak(employee_id)
        
        # Check for badges
        self._check_badges(employee_id)
        
        return f"""✅ Module completed!

🎯 Points earned: +50
⏱️ Time spent: {time_spent} minutes

Next: /continue"""
    
    def start_quiz(self, employee_id: str, module_id: str):
        """Start a quiz for a module."""
        questions = get_quiz_questions(module_id)
        
        if not questions:
            return "❌ No quiz available for this module."
        
        # Store quiz state in session (would use Redis in production)
        quiz_state = {
            'employee_id': employee_id,
            'module_id': module_id,
            'questions': questions,
            'current_question': 0,
            'score': 0,
            'answers': []
        }
        
        # Return first question
        return self._present_question(quiz_state)
    
    def _present_question(self, quiz_state: dict):
        """Present a quiz question."""
        q = quiz_state['questions'][quiz_state['current_question']]
        total = len(quiz_state['questions'])
        
        options = '\n'.join([f"{chr(65+i)}) {opt}" for i, opt in enumerate(q['options'])])
        
        response = f"""📝 **Question {quiz_state['current_question'] + 1}/{total}**

{q['question_text']}

{options}

_Reply with the letter (A, B, C, or D)_"""
        
        return response
    
    def submit_answer(self, quiz_state: dict, answer: str):
        """Submit quiz answer."""
        q = quiz_state['questions'][quiz_state['current_question']]
        answer = answer.upper().strip()
        
        # Check if correct
        is_correct = answer == q['correct_answer'].upper().strip()
        points = q['points'] if is_correct else 0
        
        # Record attempt
        record_quiz_attempt(
            quiz_state['employee_id'],
            q['question_id'],
            answer,
            is_correct,
            points
        )
        
        # Store result
        quiz_state['answers'].append({
            'question_id': q['question_id'],
            'correct': is_correct,
            'points': points
        })
        
        if is_correct:
            quiz_state['score'] += points
            feedback = f"✅ Correct! (+{points} points)"
        else:
            feedback = f"❌ Incorrect. The answer was: {q['correct_answer']}"
        
        # Next question or finish
        quiz_state['current_question'] += 1
        
        if quiz_state['current_question'] >= len(quiz_state['questions']):
            return self._finish_quiz(quiz_state)
        else:
            next_q = self._present_question(quiz_state)
            return f"{feedback}\n\n{next_q}"
    
    def _finish_quiz(self, quiz_state: dict):
        """Finish quiz and show results."""
        total_questions = len(quiz_state['questions'])
        correct = sum(1 for a in quiz_state['answers'] if a['correct'])
        total_points = sum(a['points'] for a in quiz_state['answers'])
        percentage = (correct / total_questions) * 100
        
        # Update module progress with quiz score
        update_module_progress(
            quiz_state['employee_id'],
            quiz_state['module_id'],
            'completed',
            quiz_score=int(percentage)
        )
        
        # Award points
        update_employee_points(quiz_state['employee_id'], total_points)
        update_streak(quiz_state['employee_id'])
        
        # Check for badges
        if percentage == 100:
            award_badge(quiz_state['employee_id'], 'quiz-master')
        
        # Determine pass/fail
        passed = percentage >= 70  # Default passing score
        
        response = f"""📊 **Quiz Results**

✅ Correct: {correct}/{total_questions}
📈 Score: {percentage:.0f}%
🎯 Points earned: {total_points}

"""
        
        if passed:
            response += "🎉 **PASSED!** Well done!"
        else:
            response += "❌ **Not passed.** You can retry after 24 hours."
        
        response += "\n\n/continue to keep learning"
        
        return response
    
    def get_progress(self, employee_id: str):
        """Get employee progress dashboard."""
        employee = get_employee(employee_id)
        
        if not employee:
            return "❌ Employee not found. Register with /start"
        
        enrollments = get_employee_enrollments(employee_id)
        badges = get_employee_badges(employee_id)
        
        completed = sum(1 for e in enrollments if e['status'] == 'completed')
        in_progress = sum(1 for e in enrollments if e['status'] == 'in_progress')
        
        response = f"""📊 **Your Progress**

👤 {employee['name']}
💼 {employee.get('role', 'N/A')} | {employee.get('department', 'N/A')}

📚 **Learning Stats:**
✅ Completed paths: {completed}
🔄 In progress: {in_progress}
🎯 Total points: {employee['total_points']}
🔥 Current streak: {employee['streak_days']} days

🏆 **Badges:** {len(badges)}
"""
        
        for badge in badges[:5]:  # Show first 5 badges
            response += f"\n{badge['icon']} {badge['name']}"
        
        if len(badges) > 5:
            response += f"\n... and {len(badges) - 5} more"
        
        response += "\n\n/paths to browse learning paths"
        
        return response
    
    def _check_badges(self, employee_id: str):
        """Check and award badges based on achievements."""
        employee = get_employee(employee_id)
        enrollments = get_employee_enrollments(employee_id)
        
        # First module completed
        completed_modules = sum(
            1 for e in enrollments 
            if e['status'] in ['completed', 'in_progress']
        )
        
        if completed_modules == 1:
            award_badge(employee_id, 'first-week')
        
        if completed_modules >= 10:
            award_badge(employee_id, 'bookworm')
        
        # First path completed
        completed_paths = sum(1 for e in enrollments if e['status'] == 'completed')
        if completed_paths == 1:
            award_badge(employee_id, 'path-finder')
        
        # Streak badges
        if employee['streak_days'] >= 7:
            award_badge(employee_id, 'week-streak')


# CLI interface for testing
if __name__ == "__main__":
    bot = TrainingBot()
    
    # Test commands
    print("🎓 Training Bot — Test Mode")
    print("\nCommands:")
    print("  register [id] [name] [role] [dept]")
    print("  paths [employee_id]")
    print("  enroll [employee_id] [path_id]")
    print("  continue [employee_id]")
    print("  complete [employee_id] [module_id]")
    print("  quiz [employee_id] [module_id]")
    print("  progress [employee_id]")
    print("  quit")
    
    while True:
        try:
            cmd = input("\n> ").strip()
            if not cmd or cmd.lower() == 'quit':
                break
            
            parts = cmd.split()
            action = parts[0].lower()
            
            if action == 'register' and len(parts) >= 3:
                result = bot.register_employee(parts[1], parts[2], 
                                              parts[3] if len(parts) > 3 else None,
                                              parts[4] if len(parts) > 4 else None)
                print(result)
            
            elif action == 'paths' and len(parts) >= 2:
                result = bot.list_paths(parts[1])
                print(result)
            
            elif action == 'enroll' and len(parts) >= 3:
                result = bot.enroll(parts[1], parts[2])
                print(result)
            
            elif action == 'continue' and len(parts) >= 2:
                result = bot.continue_learning(parts[1])
                print(result)
            
            elif action == 'progress' and len(parts) >= 2:
                result = bot.get_progress(parts[1])
                print(result)
            
            else:
                print("Unknown command. Try: register, paths, enroll, continue, complete, quiz, progress")
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")
