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
  
  return isAuthenticated ? children : <Navigate to="/login" replace />
}

function AppContent() {
  const { isDark, toggleTheme } = useTheme()
  const { isAuthenticated, user, logout } = useAuth()

  return (
    <Router>
      <div className="app">
        {isAuthenticated && (
          <nav className="navbar">
            <div className="nav-container">
              <div className="nav-left">
                <h1 className="logo">💻 AlgoMentor</h1>
              </div>
              <div className="nav-right">
                <div className="nav-links">
                  <Link to="/">Home</Link>
                  <Link to="/roadmap">Roadmap</Link>
                  <Link to="/code-check">Code Check</Link>
                </div>
                <div className="user-info">
                  <span className="username">👤 {user?.username}</span>
                  <button className="logout-button" onClick={logout}>Logout</button>
                </div>
                <button className="theme-toggle" onClick={toggleTheme} aria-label="Toggle theme">
                  {isDark ? '☀️' : '🌙'}
                </button>
              </div>
            </div>
          </nav>
        )}

        <main className="main-content">
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/" element={<ProtectedRoute><HomePage /></ProtectedRoute>} />
            <Route path="/roadmap" element={<ProtectedRoute><RoadmapPage /></ProtectedRoute>} />
            <Route path="/roadmap/:pointId/learn" element={<ProtectedRoute><LearningPage /></ProtectedRoute>} />
            <Route path="/quiz/:knowledgePointId" element={<ProtectedRoute><QuizPage /></ProtectedRoute>} />
            <Route path="/code-check" element={<ProtectedRoute><CodeCheckPage /></ProtectedRoute>} />
            <Route path="/code-check/:questionId" element={<ProtectedRoute><CodeCheckPage /></ProtectedRoute>} />
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

