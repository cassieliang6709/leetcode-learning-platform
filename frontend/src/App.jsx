import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom'
import { ThemeProvider, useTheme } from './contexts/ThemeContext'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import HomePage from './pages/HomePage'
import RoadmapPage from './pages/RoadmapPage'
import LearningPage from './pages/LearningPage'
import QuizPage from './pages/QuizPage'
import CodeCheckPage from './pages/CodeCheckPage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import './App.css'
import './styles/skeleton.css'

function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = useAuth()
  
  if (loading) {
    return <div className="loading-screen">Loading...</div>
  }
  
  if (!isAuthenticated) {
    return (
      <div style={{ padding: '2rem', textAlign: 'center' }}>
        <h2>需要登录</h2>
        <p>此功能需要登录后才能使用</p>
        <Link to="/login" style={{ marginRight: '1rem' }}>登录</Link>
        <Link to="/register">注册</Link>
      </div>
    )
  }
  
  return children
}

function AppContent() {
  const { isDark, toggleTheme } = useTheme()
  const { isAuthenticated, user, logout } = useAuth()

  return (
    <Router>
      <div className="app">
        <nav className="navbar">
          <div className="nav-container">
            <div className="nav-left">
              <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
                <h1 className="logo">💻 AlgoMentor</h1>
              </Link>
            </div>
            <div className="nav-right">
              <div className="nav-links">
                <Link to="/">Home</Link>
                <Link to="/roadmap">Roadmap</Link>
                <Link to="/code-check">Code Check</Link>
              </div>
              {isAuthenticated ? (
                <div className="user-info">
                  <span className="username">👤 {user?.username}</span>
                  <button className="logout-button" onClick={logout}>Logout</button>
                </div>
              ) : (
                <div className="auth-links">
                  <Link to="/login" className="login-link">Login</Link>
                  <Link to="/register" className="register-link">Sign Up</Link>
                </div>
              )}
              <button className="theme-toggle" onClick={toggleTheme} aria-label="Toggle theme">
                {isDark ? '☀️' : '🌙'}
              </button>
            </div>
          </div>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            {/* 游客模式：大部分页面无需登录 */}
            <Route path="/" element={<HomePage />} />
            <Route path="/roadmap" element={<RoadmapPage />} />
            <Route path="/roadmap/:pointId/learn" element={<LearningPage />} />
            <Route path="/quiz/:knowledgePointId" element={<QuizPage />} />
            <Route path="/code-check" element={<CodeCheckPage />} />
            <Route path="/code-check/:questionId" element={<CodeCheckPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

function App() {
  return (
    <AuthProvider>
      <ThemeProvider>
        <AppContent />
      </ThemeProvider>
    </AuthProvider>
  )
}

export default App

