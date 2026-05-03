# 🎓 Employee Training System — Architecture

**For:** Keezhu • Company AI Learning Chatbot  
**Version:** 1.0  
**Created:** 2026-05-04

---

## 🎯 System Overview

Transform the Lark Wiki chatbot into an active training platform that:

1. **Onboards** new employees with structured learning paths
2. **Tracks** progress and completion
3. **Tests** knowledge with quizzes
4. **Certifies** employees for compliance/role readiness
5. **Recommends** personalized next steps
6. **Reports** to managers on team progress

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      EMPLOYEE TRAINING SYSTEM                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │  Learning    │    │   Progress   │    │    Quiz &    │      │
│  │    Paths     │    │   Tracking   │    │  Assessment  │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │  Personalized│    │  Manager     │    │ Certification│      │
│  │  Recommendations│  │  Dashboard   │    │   & Badges   │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│                         DATA LAYER                               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   SQLite     │    │   Memory     │    │    Lark      │      │
│  │  (Progress)  │    │  (Sessions)  │    │    Wiki      │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Telegram Bot   │
                    │  (User Interface)│
                    └─────────────────┘
```

---

## 📊 Data Models

### Employee Profile
```json
{
  "employee_id": "telegram_user_id",
  "name": "Employee Name",
  "role": "engineer|sales|marketing|hr|operations",
  "department": "Engineering",
  "hire_date": "2026-01-15",
  "manager_id": "telegram_user_id",
  "level": "junior|mid|senior|lead",
  "enrolled_paths": ["new-hire-onboarding", "security-compliance"],
  "completed_paths": ["intro-to-product"],
  "badges": ["first-week", "security-certified"],
  "streak_days": 5,
  "total_points": 450
}
```

### Learning Path
```json
{
  "path_id": "new-hire-onboarding",
  "title": "New Hire Onboarding",
  "description": "Essential knowledge for all new employees",
  "target_audience": ["all"],
  "prerequisites": [],
  "estimated_hours": 8,
  "required": true,
  "modules": [
    {
      "module_id": "company-mission",
      "title": "Company Mission & Values",
      "type": "read",
      "source": "raw/lark/company-handbook.md",
      "order": 1,
      "estimated_minutes": 30
    },
    {
      "module_id": "security-basics",
      "title": "Security Fundamentals",
      "type": "read+quiz",
      "source": "raw/lark/security-policy.md",
      "order": 2,
      "estimated_minutes": 60,
      "quiz_required": true,
      "passing_score": 80
    }
  ]
}
```

### Progress Tracking
```json
{
  "employee_id": "566009262",
  "path_id": "new-hire-onboarding",
  "status": "in_progress|completed|not_started",
  "started_at": "2026-05-04T10:00:00Z",
  "completed_at": null,
  "modules_completed": [
    {
      "module_id": "company-mission",
      "completed_at": "2026-05-04T10:30:00Z",
      "time_spent_minutes": 28,
      "quiz_score": null
    }
  ],
  "current_module": "security-basics",
  "overall_progress_percent": 50
}
```

### Quiz Question
```json
{
  "question_id": "sec-001",
  "module_id": "security-basics",
  "question_text": "What is the minimum password length required by company policy?",
  "question_type": "multiple_choice|true_false|short_answer",
  "options": ["8 characters", "12 characters", "16 characters", "20 characters"],
  "correct_answer": "12 characters",
  "explanation": "Per security policy section 3.2, all passwords must be at least 12 characters.",
  "points": 10,
  "difficulty": "easy"
}
```

---

## 🎯 Core Features

### 1. Learning Paths

Pre-defined curricula for different roles/goals:

| Path | Target | Duration | Required |
|------|--------|----------|----------|
| New Hire Onboarding | All employees | 8 hours | ✅ Yes |
| Security Compliance | All employees | 4 hours | ✅ Yes |
| Engineer Onboarding | Engineering team | 16 hours | ✅ Yes |
| Sales Fundamentals | Sales team | 12 hours | ✅ Yes |
| Product Deep Dive | All customer-facing | 6 hours | Optional |
| Leadership Training | Managers | 20 hours | Optional |

### 2. Progress Tracking

- ✅ Module completion tracking
- ✅ Time spent per module
- ✅ Quiz scores & attempts
- ✅ Overall path progress (%)
- ✅ Streak tracking (daily learning)
- ✅ Points/gamification

### 3. Quiz System

- Multiple choice questions
- True/False questions
- Short answer (AI-graded)
- Passing score thresholds
- Unlimited retries (with cooldown)
- Explanations for each answer

### 4. Certifications

- Auto-generate certificates on path completion
- Badge system for achievements
- Compliance tracking (who completed what + when)
- Expiry dates for certs that need renewal

### 5. Manager Dashboard

- Team progress overview
- Identify employees behind on required training
- Compliance reports
- Learning recommendations per employee

### 6. Personalized Recommendations

AI-powered suggestions based on:
- Role and level
- Completed paths
- Knowledge gaps (quiz performance)
- Career goals (if provided)
- Popular paths for similar employees

---

## 💬 User Commands (Telegram)

### Employee Commands

```
/start — Welcome message + current progress
/paths — List available learning paths
/path [name] — View path details + enroll
/continue — Resume current learning path
/quiz [module] — Take module quiz
/progress — Show personal progress dashboard
/badges — View earned badges & certificates
/streak — Check learning streak
/leaderboard — See team rankings
/recommend — Get personalized next steps
/certificate [path] — Download completion certificate
```

### Manager Commands

```
/team — View team progress overview
/team/[employee] — Individual employee progress
/compliance — Compliance report (who's missing required training)
/assign [path] [@employee] — Assign learning path to employee
/remind [@employee] — Send learning reminder
```

### Admin Commands

```
/analytics — Platform-wide analytics
/create-path — Create new learning path (interactive)
/create-quiz — Add quiz questions to module
/export — Export progress data (CSV)
/broadcast — Send announcement to all employees
```

---

## 🎮 Gamification System

### Points

| Action | Points |
|--------|--------|
| Complete module | +50 |
| Pass quiz (first try) | +100 |
| Pass quiz (>80%) | +50 |
| Complete learning path | +500 |
| 7-day streak | +200 |
| 30-day streak | +1000 |
| Help colleague (peer review) | +25 |

### Badges

| Badge | Requirement |
|-------|-------------|
| 🌱 First Week | Complete first module |
| 📚 Bookworm | Complete 10 modules |
| 🎯 Quiz Master | Pass 5 quizzes with 100% |
| 🔥 7-Day Streak | Learn 7 days in a row |
| 🏆 Path Finder | Complete first learning path |
| 🛡️ Security Certified | Pass security compliance |
| 🚀 Fast Learner | Complete path in <50% estimated time |
| 🌟 Top Performer | Top 10% on leaderboard |

### Leaderboards

- Weekly top learners
- Monthly top learners
- All-time top learners
- Department rankings
- New hire rankings

---

## 📈 Analytics Dashboard

### Employee View
- Personal progress
- Time spent learning
- Quiz average score
- Streak status
- Badges earned
- Next recommended actions

### Manager View
- Team completion rates
- Employees behind on required training
- Average quiz scores by team
- Time to competency (new hires)
- Learning engagement trends

### Admin View
- Platform-wide adoption
- Most popular paths
- Quiz difficulty analysis
- ROI metrics (time to productivity)
- Compliance status

---

## 🔧 Implementation Phases

### Phase 1: Core Training (Week 1)
- [ ] Learning path data structure
- [ ] Module completion tracking
- [ ] Basic progress commands (/progress, /paths)
- [ ] SQLite database for persistence

### Phase 2: Quiz System (Week 2)
- [ ] Quiz question bank
- [ ] Quiz delivery via Telegram
- [ ] Auto-grading
- [ ] Pass/fail tracking

### Phase 3: Gamification (Week 3)
- [ ] Points system
- [ ] Badge earning logic
- [ ] Leaderboard
- [ ] Streak tracking

### Phase 4: Manager Features (Week 4)
- [ ] Team progress views
- [ ] Compliance reports
- [ ] Path assignment
- [ ] Reminder system

### Phase 5: Advanced Features (Month 2)
- [ ] AI-powered recommendations
- [ ] Certificate generation (PDF)
- [ ] Export/analytics
- [ ] Multi-language support

---

## 🗄️ Database Schema (SQLite)

```sql
-- Employees
CREATE TABLE employees (
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
);

-- Learning Paths
CREATE TABLE learning_paths (
    path_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    target_audience TEXT, -- JSON array
    estimated_hours REAL,
    required BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Modules
CREATE TABLE modules (
    module_id TEXT PRIMARY KEY,
    path_id TEXT,
    title TEXT NOT NULL,
    type TEXT, -- read, read+quiz, video, interactive
    source TEXT, -- file path or URL
    order_index INTEGER,
    estimated_minutes INTEGER,
    quiz_required BOOLEAN DEFAULT FALSE,
    passing_score INTEGER DEFAULT 70,
    FOREIGN KEY (path_id) REFERENCES learning_paths(path_id)
);

-- Enrollments
CREATE TABLE enrollments (
    employee_id TEXT,
    path_id TEXT,
    status TEXT, -- not_started, in_progress, completed
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    PRIMARY KEY (employee_id, path_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    FOREIGN KEY (path_id) REFERENCES learning_paths(path_id)
);

-- Module Progress
CREATE TABLE module_progress (
    employee_id TEXT,
    module_id TEXT,
    status TEXT, -- not_started, in_progress, completed
    completed_at TIMESTAMP,
    time_spent_minutes INTEGER,
    quiz_score INTEGER,
    quiz_attempts INTEGER DEFAULT 0,
    PRIMARY KEY (employee_id, module_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    FOREIGN KEY (module_id) REFERENCES modules(module_id)
);

-- Quiz Questions
CREATE TABLE quiz_questions (
    question_id TEXT PRIMARY KEY,
    module_id TEXT,
    question_text TEXT NOT NULL,
    question_type TEXT, -- multiple_choice, true_false, short_answer
    options TEXT, -- JSON array
    correct_answer TEXT,
    explanation TEXT,
    points INTEGER DEFAULT 10,
    difficulty TEXT, -- easy, medium, hard
    FOREIGN KEY (module_id) REFERENCES modules(module_id)
);

-- Badges
CREATE TABLE badges (
    badge_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    icon TEXT, -- emoji
    requirement TEXT -- JSON condition
);

-- Employee Badges
CREATE TABLE employee_badges (
    employee_id TEXT,
    badge_id TEXT,
    earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (employee_id, badge_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    FOREIGN KEY (badge_id) REFERENCES badges(badge_id)
);

-- Quiz Attempts
CREATE TABLE quiz_attempts (
    attempt_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id TEXT,
    question_id TEXT,
    selected_answer TEXT,
    is_correct BOOLEAN,
    points_earned INTEGER,
    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    FOREIGN KEY (question_id) REFERENCES quiz_questions(question_id)
);
```

---

## 🤖 AI Integration Points

### 1. Content Summarization
- Auto-summarize long Lark docs into module content
- Generate key takeaways
- Create study guides

### 2. Quiz Generation
- Auto-generate quiz questions from source docs
- Vary difficulty levels
- Generate explanations

### 3. Personalized Recommendations
- Analyze employee progress + role
- Suggest next best modules
- Identify knowledge gaps

### 4. Short Answer Grading
- Grade open-ended quiz responses
- Provide feedback
- Detect plagiarism/copying

### 5. Learning Path Creation
- Auto-create paths from wiki structure
- Suggest prerequisites
- Estimate completion times

---

## 📱 Sample Conversation Flows

### New Employee Onboarding

```
Bot: Welcome to the company! 🎉 I'm your learning assistant.
     Let's get you started with onboarding.

Employee: /start

Bot: Hi John! I see you're joining as a Software Engineer.
     You have 3 required learning paths:
     
     1. 📋 New Hire Onboarding (8 hours) — Required
     2. 🛡️ Security Compliance (4 hours) — Required
     3. 👨‍💻 Engineer Onboarding (16 hours) — Required
     
     Would you like to start with New Hire Onboarding?
     [Yes, let's go!] [View all paths] [Remind me later]
```

### Daily Learning

```
Bot: Good morning! ☀️ You're on a 5-day learning streak! 🔥
     Continue where you left off?
     
     📖 Security Fundamentals — Module 3 of 8
     ⏱️ Estimated: 45 minutes
     
     [Continue] [Take Quiz] [Skip for now]
```

### Quiz Experience

```
Bot: 📝 Quiz: Security Fundamentals
     Passing score: 80% | Questions: 10
     
     Question 1/10:
     What is the minimum password length required?
     
     A) 8 characters
     B) 12 characters
     C) 16 characters
     D) 20 characters
     
     [A] [B] [C] [D]
```

### Completion & Certification

```
Bot: 🎉 Congratulations! You've completed Security Compliance!
     
     📊 Your score: 95%
     ⏱️ Total time: 3.5 hours
     🏆 Badge earned: Security Certified
     
     Would you like to:
     [Download Certificate] [Share Achievement] [Continue Learning]
```

---

## 🔐 Security & Privacy

- Employee data encrypted at rest
- Manager access limited to their direct reports
- Compliance data retained per legal requirements
- Anonymous analytics aggregation
- GDPR/privacy compliance for personal data

---

## 📊 Success Metrics

| Metric | Target |
|--------|--------|
| New hire time-to-productivity | < 2 weeks |
| Required training completion rate | > 95% |
| Daily active learners | > 60% |
| Quiz pass rate (first attempt) | > 75% |
| Employee satisfaction (learning) | > 4.5/5 |

---

**Next Step:** Create the actual implementation files and Hermes skills for this training system.
