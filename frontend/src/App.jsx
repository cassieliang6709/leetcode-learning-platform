import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import { ThemeProvider, useTheme } from './contexts/ThemeContext'
import HomePage from './pages/HomePage'
import RoadmapPage from './pages/RoadmapPage'
import QuizPage from './pages/QuizPage'
import CodeCheckPage from './pages/CodeCheckPage'
import './App.css'
import './styles/skeleton.css'

function AppContent() {
  const { isDark, toggleTheme } = useTheme()

  return (
    <Router>
      <div className="app">
        <nav className="navbar">
          <div className="nav-container">
            <div className="nav-left">
              <h1 className="logo">💻 LeetCode Master</h1>
            </div>
            <div className="nav-right">
              <div className="nav-links">
                <Link to="/">Home</Link>
                <Link to="/roadmap">Roadmap</Link>
                <Link to="/code-check">Code Check</Link>
              </div>
              <button className="theme-toggle" onClick={toggleTheme} aria-label="Toggle theme">
                {isDark ? '☀️' : '🌙'}
              </button>
            </div>
          </div>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/roadmap" element={<RoadmapPage />} />
            <Route path="/quiz/:knowledgePointId" element={<QuizPage />} />
            <Route path="/code-check" element={<CodeCheckPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

function App() {
  return (
    <ThemeProvider>
      <AppContent />
    </ThemeProvider>
  )
}

export default App

