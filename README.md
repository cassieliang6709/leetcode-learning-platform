<div align="center">

# 🎯 AlgoMentor

### AI-Powered Algorithm Learning System with Real-Time Code Execution

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![React 18.2](https://img.shields.io/badge/react-18.2-61dafb.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.115-009688.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/postgresql-14+-336791.svg)](https://www.postgresql.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[Features](#-features) • [Demo](#-demo) • [Quick Start](#-quick-start) • [Tech Stack](#-tech-stack) • [Documentation](#-documentation)

</div>

---

## 📖 Overview

A comprehensive learning platform that combines **LeetCode Hot 100** problems with AI-powered assistance, real-time code execution, and intelligent feedback system. Designed to help developers master data structures and algorithms through guided practice and personalized learning paths.

### 🎥 Demo

> **Live Platform**: Experience the full-featured learning environment with:
> - 🚀 Real-time code execution across multiple languages
> - 🤖 AI-powered code review and optimization suggestions
> - 💡 Multi-level progressive hint system
> - 📊 Visual learning roadmap with 9 core topics

## ✨ Features

### 🎯 Core Learning Experience

| Feature | Description |
|---------|-------------|
| **LeetCode Hot 100** | Curated collection of the most popular algorithm problems |
| **Real-Time Execution** | Run and test code instantly with Piston API integration |
| **Multi-Language Support** | Python, JavaScript, Java, C++ code execution |
| **Smart Test Cases** | Comprehensive test suites with detailed output |

### 🤖 AI-Powered Assistance

- **Failure Analysis**: Automatic debugging suggestions when tests fail
- **Optimization Advice**: Get performance improvements for passing solutions
- **Interactive AI Chat**: Ask questions about problems and get instant help
- **Code Review**: Intelligent feedback on code quality and best practices

### 💡 Progressive Hint System

Three-tier learning support designed to preserve your problem-solving skills:

1. **Level 1 - Strategy Hint**: High-level approach and algorithm selection
2. **Level 2 - Code Hint**: Implementation guidance with pseudocode
3. **Level 3 - Video Tutorial**: Visual explanation with YouTube integration

### 📊 Learning Path & Progress

- **Knowledge Assessment**: Initial quiz to evaluate your skill level
- **AI-Generated Study Plan**: Personalized learning recommendations
- **Visual Roadmap**: Navigate through 9 algorithm topics with progress tracking
- **Daily Challenges**: Curated problems to maintain consistency

### 🎨 Modern UI/UX

- **NeetCode-Inspired Interface**: Clean, professional code editor layout
- **Monaco Editor**: VSCode-quality editing experience
- **Split-Pane Design**: Problem description, code editor, and console
- **Expandable Results**: Maximize test results for detailed analysis
- **Dark/Light Theme**: Comfortable viewing in any environment

## 🏗️ Tech Stack

### Backend Architecture

```
FastAPI (Python 3.12+)
├── SQLAlchemy ORM (Async)
├── PostgreSQL Database
├── Piston API Integration (Code Execution)
├── SiliconFlow AI (Code Analysis)
└── asyncpg (High-Performance Driver)
```

**Key Technologies:**
- **FastAPI**: Modern async web framework with automatic API docs
- **SQLAlchemy 2.0**: Advanced ORM with async support
- **PostgreSQL**: Robust relational database
- **Pydantic**: Data validation and settings management
- **CORS Middleware**: Secure cross-origin requests

### Frontend Stack

```
React 18 + Vite
├── React Router v6 (Navigation)
├── Monaco Editor (Code Editing)
├── Axios (API Client)
├── React Markdown (Rich Content)
└── Context API (State Management)
```

**UI Components:**
- **Monaco Editor**: Professional code editing with syntax highlighting
- **React Markdown**: Render formatted problem descriptions and AI responses
- **Custom Components**: Reusable UI elements for consistent design

### AI & External Services

- **SiliconFlow AI**: Natural language processing for code analysis
- **Piston API**: Secure sandboxed code execution
- **YouTube Integration**: Embedded video tutorials

## 🚀 Quick Start

### Prerequisites

Ensure you have the following installed:

- **Python 3.12+** ([Download](https://www.python.org/downloads/))
- **Node.js 18+** ([Download](https://nodejs.org/))
- **PostgreSQL 14+** ([Download](https://www.postgresql.org/download/))

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/cassieliang6709/leetcode-learning-platform.git
cd leetcode-learning-platform
```

#### 2. Database Setup

```bash
# Create PostgreSQL database
psql -d postgres -c "CREATE DATABASE leetcode_learning;"
```

#### 3. Backend Setup

```bash
cd backend

# Create virtual environment
python3.12 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp env.template .env
# Edit .env and add your DATABASE_URL and SILICONFLOW_API_KEY
```

#### 4. Initialize Database

```bash
cd ..
python scripts/init_db.py
python scripts/init_leetcode_hot100_complete.py
```

#### 5. Frontend Setup

```bash
cd frontend
npm install
```

### Running the Application

#### Development Mode

**Terminal 1 - Backend Server:**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend Server:**
```bash
cd frontend
npm run dev
```

#### Using Scripts (Recommended)

```bash
# Start both frontend and backend
./scripts/start_all.sh

# Stop all services
./scripts/stop_all.sh
```

### Access Points

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:5173 | Main application interface |
| **Backend API** | http://localhost:8000 | REST API endpoints |
| **API Docs** | http://localhost:8000/docs | Interactive API documentation |
| **Health Check** | http://localhost:8000/health | System status endpoint |

## 📁 Project Structure

```
leetcode-learning-platform/
│
├── backend/                      # FastAPI Backend
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/          # API Endpoints
│   │   │       ├── auth.py      # Authentication
│   │   │       ├── code_check.py        # Code review
│   │   │       ├── code_execution.py    # Run code
│   │   │       ├── ai_assistant.py      # AI features
│   │   │       ├── quiz.py              # Quizzes
│   │   │       └── knowledge.py         # Learning paths
│   │   ├── services/            # Business Logic
│   │   │   ├── siliconflow_ai.py       # AI integration
│   │   │   ├── code_executor.py        # Piston API
│   │   │   └── auth_service.py         # Authentication
│   │   ├── database.py          # DB configuration
│   │   ├── models.py            # SQLAlchemy models
│   │   └── schemas.py           # Pydantic schemas
│   ├── main.py                  # Application entry
│   ├── requirements.txt         # Python dependencies
│   └── .env                     # Environment variables
│
├── frontend/                    # React Frontend
│   ├── src/
│   │   ├── pages/              # Page Components
│   │   │   ├── HomePage.jsx           # Landing & Assessment
│   │   │   ├── RoadmapPage.jsx        # Learning roadmap
│   │   │   ├── LearningPage.jsx       # Daily practice
│   │   │   ├── QuizPage.jsx           # Quiz interface
│   │   │   ├── CodeCheckPage.jsx      # Code editor
│   │   │   ├── LoginPage.jsx          # Authentication
│   │   │   └── RegisterPage.jsx       # User registration
│   │   ├── contexts/           # State Management
│   │   │   ├── AuthContext.jsx        # User auth state
│   │   │   └── ThemeContext.jsx       # UI theme
│   │   ├── services/
│   │   │   └── api.js          # API client
│   │   ├── styles/             # Global styles
│   │   │   ├── skeleton.css          # Loading states
│   │   │   └── NeetCodeStyle.css     # Code editor styles
│   │   ├── App.jsx             # Root component
│   │   └── main.jsx            # Application entry
│   ├── package.json            # Node dependencies
│   └── vite.config.js          # Vite configuration
│
└── scripts/                     # Utility Scripts
    ├── init_db.py              # Initialize database
    ├── init_leetcode_hot100_complete.py  # Load problems
    ├── start_all.sh            # Start services
    └── stop_all.sh             # Stop services
```

## 🎮 User Guide

### Getting Started

1. **Register Account** → Create your learning profile
2. **Take Assessment** → Complete the initial knowledge quiz
3. **Get Study Plan** → Receive AI-generated recommendations
4. **Follow Roadmap** → Navigate through 9 algorithm topics

### Using the Code Editor

#### Problem Solving Workflow

```
1. Read Problem → 2. Request Hints → 3. Write Code → 4. Run Tests → 5. Get Feedback
```

#### Available Features

- **Monaco Editor**: Professional code editing with IntelliSense
- **Language Selection**: Switch between Python, JavaScript, Java, C++
- **Split View**: Adjustable panes for description and code
- **Console Output**: Real-time test results and error messages
- **Maximize Results**: Expand test output for detailed analysis

#### Hint System Usage

```javascript
// Request hints progressively as needed
Level 1 (Strategy) → Level 2 (Code) → Level 3 (Video)
```

**Best Practice**: Try solving independently before requesting hints to maximize learning.

### AI Assistant Features

#### 1. Automatic Failure Analysis
When tests fail, AI automatically analyzes your code and provides:
- Error explanation
- Debugging suggestions
- Edge cases you missed
- Corrected implementation examples

#### 2. Optimization Suggestions
When all tests pass, AI reviews your code for:
- Time complexity improvements
- Space complexity optimization
- Code quality best practices
- Alternative approaches

#### 3. Interactive Chat
Click the AI button to:
- Ask about problem concepts
- Request implementation help
- Clarify confusing requirements
- Get debugging assistance

## 📊 Database Schema

### Core Tables

| Table | Description | Key Fields |
|-------|-------------|------------|
| `users` | User accounts | email, hashed_password, created_at |
| `knowledge_points` | Algorithm topics (9 categories) | name, description, difficulty |
| `quiz_questions` | LeetCode Hot 100 problems | title, description, difficulty, test_cases |
| `code_submissions` | Code history & feedback | user_id, code, language, ai_feedback |
| `quiz_attempts` | Problem-solving records | user_id, question_id, is_correct |
| `knowledge_tests` | Assessment results | user_id, score, weak_points |
| `learning_plans` | Personalized study plans | user_id, recommended_path |

### Relationships

```
users ─┬─→ code_submissions
       ├─→ quiz_attempts
       ├─→ knowledge_tests
       └─→ learning_plans

knowledge_points → quiz_questions → quiz_attempts
```

## 🔧 Configuration

### Environment Variables

Create `backend/.env`:

```env
# Database
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/leetcode_learning

# AI Service (SiliconFlow)
SILICONFLOW_API_KEY=your_api_key_here

# Security (Optional)
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend Configuration

Create `frontend/.env` (optional):

```env
VITE_API_URL=http://localhost:8000/api
```

## 🚀 Deployment

### Deploy to Production

The platform can be deployed to:

- **Backend**: Render, Railway, or any Python hosting service
- **Frontend**: Vercel, Netlify, or any static hosting
- **Database**: Railway, Supabase, or managed PostgreSQL

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

### Production Checklist

- [ ] Set production environment variables
- [ ] Configure CORS for your domain
- [ ] Use production database credentials
- [ ] Enable HTTPS
- [ ] Set up monitoring and logging

## 🐛 Troubleshooting

### Common Issues

#### Python Version Compatibility

```bash
# If using Python 3.13, switch to 3.12
brew install python@3.12
python3.12 -m venv venv
```

#### Port Already in Use

```bash
# Kill process on port 8000 (backend)
lsof -ti:8000 | xargs kill -9

# Kill process on port 5173 (frontend)
lsof -ti:5173 | xargs kill -9
```

#### Database Connection Failed

```bash
# Check PostgreSQL status
brew services list

# Start PostgreSQL service
brew services start postgresql@14

# Verify connection
psql -d leetcode_learning
```

#### Missing Dependencies

```bash
# Backend
cd backend
source venv/bin/activate
pip install -r requirements.txt --upgrade

# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Getting Help

- 📖 Check [START_HERE.md](START_HERE.md) for setup guide
- 🔧 See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed fixes
- 💬 Open an issue on GitHub
- 📧 Contact the maintainers

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Contribution Process

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint configuration for JavaScript
- Write descriptive commit messages
- Add tests for new features
- Update documentation as needed

### Areas for Contribution

- 🐛 Bug fixes and error handling
- ✨ New features and enhancements
- 📝 Documentation improvements
- 🎨 UI/UX enhancements
- 🧪 Test coverage expansion
- 🌐 Internationalization (i18n)

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 👥 Authors & Acknowledgments

### Core Team

- **Cassie Liang** - [@cassieliang6709](https://github.com/cassieliang6709) - Project Lead & Full-Stack Development

### Special Thanks

- **LeetCode** - For problem inspiration and learning resources
- **NeetCode** - UI/UX design inspiration
- **FastAPI Community** - Excellent framework and documentation
- **React Community** - Amazing tools and ecosystem
- **SiliconFlow** - AI-powered code analysis capabilities
- **Piston API** - Secure code execution infrastructure

## 🌟 Star History

If you find this project helpful, please consider giving it a ⭐!

[![Star History Chart](https://api.star-history.com/svg?repos=cassieliang6709/leetcode-learning-platform&type=Date)](https://star-history.com/#cassieliang6709/leetcode-learning-platform&Date)

## 📞 Support & Community

### Get Support

- 💬 [GitHub Issues](https://github.com/cassieliang6709/leetcode-learning-platform/issues) - Bug reports and feature requests
- 📖 [Documentation](START_HERE.md) - Comprehensive setup guide
- 🔧 [Troubleshooting](TROUBLESHOOTING.md) - Common problems and solutions

### Stay Updated

- ⭐ Star this repository to follow updates
- 👀 Watch for new releases and features
- 🍴 Fork to create your own version

---

<div align="center">

**Made with ❤️ for algorithm learners worldwide**

[Report Bug](https://github.com/cassieliang6709/leetcode-learning-platform/issues) • [Request Feature](https://github.com/cassieliang6709/leetcode-learning-platform/issues) • [Documentation](START_HERE.md)

</div>
