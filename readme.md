# 🎯 LeetCode Learning Platform

An AI-powered algorithm learning platform that helps students systematically master LeetCode problems through personalized learning paths, intelligent hints, and code review.

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/react-18.2-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.115-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/postgresql-14+-blue.svg)](https://www.postgresql.org/)

## ✨ Features

- 🎯 **Personalized Learning Path** - AI-generated study plans based on knowledge assessment
- 💡 **Multi-Level Hint System** - Progressive hints (Strategy → Code → Video)
- 🤖 **AI Code Review** - Instant feedback on your code submissions
- 📊 **Progress Tracking** - Monitor your learning journey
- 🗺️ **Visual Roadmap** - Navigate through 9 core algorithm topics
- 📝 **Interactive Quizzes** - Practice with curated LeetCode problems

## 🏗️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM and async database operations
- **PostgreSQL** - Relational database
- **asyncpg** - High-performance PostgreSQL driver

### Frontend
- **React** - UI library with hooks
- **Vite** - Next-generation build tool
- **React Router** - Client-side routing
- **Axios** - HTTP client

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Node.js 18+
- PostgreSQL 14+

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/leetcode-learning-platform.git
cd leetcode-learning-platform

# Create database
psql -d postgres -c "CREATE DATABASE leetcode_learning;"

# Setup backend
cd backend
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Initialize database
cd ..
python scripts/init_db.py

# Setup frontend
cd frontend
npm install
```

### Running the Application

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Access the Application

- **Frontend**: http://localhost:5173
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📁 Project Structure

```
leetcode-learning-platform/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/routes/     # API endpoints
│   │   ├── services/       # Business logic
│   │   ├── database.py     # Database configuration
│   │   ├── models.py       # SQLAlchemy models
│   │   └── schemas.py      # Pydantic schemas
│   ├── main.py             # Application entry point
│   └── requirements.txt    # Python dependencies
├── frontend/               # React frontend
│   ├── src/
│   │   ├── pages/         # Page components
│   │   ├── services/      # API client
│   │   └── App.jsx        # Main application
│   ├── package.json       # Node dependencies
│   └── vite.config.js     # Vite configuration
└── scripts/               # Utility scripts
    ├── init_db.py         # Database initialization
    └── create_db.sh       # Database creation script
```

## 🎮 How to Use

1. **Take the Assessment** - Complete a quick quiz on the home page
2. **Get Your Plan** - Receive AI-generated personalized learning recommendations
3. **Follow the Roadmap** - Navigate through 9 algorithm topics
4. **Practice Problems** - Solve curated LeetCode questions
5. **Use Smart Hints** - Get progressive help when stuck:
   - Level 1: Algorithm strategy (text description)
   - Level 2: Code example with solution
   - Level 3: YouTube video explanation
6. **Submit Code** - Get AI feedback on your implementations

## 📊 Database Schema

The application uses 7 tables:

- `users` - User accounts
- `knowledge_points` - Algorithm topics (9 pre-loaded)
- `knowledge_tests` - Assessment records
- `learning_plans` - Personalized study plans
- `quiz_questions` - Practice problems
- `quiz_attempts` - Solution attempts
- `code_submissions` - Code submissions and AI feedback

## 🔧 Configuration

Create `backend/.env` file:

```env
DATABASE_URL=postgresql+asyncpg://YOUR_USER@localhost:5432/leetcode_learning
OPENAI_API_KEY=your_openai_api_key_here  # Optional
```

## 📚 Documentation

- [Quick Start Guide](QUICKSTART.md)
- [Detailed Setup](README_DEMO.md)
- [Troubleshooting](TROUBLESHOOTING.md)
- [Quick Fixes](QUICK_FIX.md)
- [Startup Instructions](START_HERE.md)

## 🐛 Troubleshooting

### Python 3.13 Compatibility Issues
Use Python 3.12 instead:
```bash
brew install python@3.12
python3.12 -m venv venv
```

### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 5173
lsof -ti:5173 | xargs kill -9
```

### Database Connection Issues
```bash
# Check PostgreSQL status
brew services list

# Start PostgreSQL
brew services start postgresql@14
```

For more help, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

## 🎯 Current Features

- ✅ Knowledge assessment system
- ✅ AI-powered learning plan generation
- ✅ Interactive roadmap with 9 topics
- ✅ Three-level hint system
- ✅ Code submission and review
- ✅ Progress tracking
- ⏳ Real OpenAI API integration (coming soon)
- ⏳ User authentication (coming soon)
- ⏳ Extended problem library (coming soon)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- LeetCode for problem inspiration
- FastAPI for the excellent web framework
- React community for amazing tools and libraries

## 📞 Support

For questions or issues:
- Open an issue on GitHub
- Check the [documentation](README_DEMO.md)
- Review [troubleshooting guide](TROUBLESHOOTING.md)

---

**Made with ❤️ for algorithm learners**
