import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import HomePage from './pages/HomePage'
import RoadmapPage from './pages/RoadmapPage'
import QuizPage from './pages/QuizPage'
import CodeCheckPage from './pages/CodeCheckPage'
import './App.css'

function App() {
  return (
    <Router>
      <div className="app">
        <nav className="navbar">
          <div className="nav-container">
            <h1 className="logo">🎯 LeetCode Learning Platform</h1>
            <div className="nav-links">
              <Link to="/">Home</Link>
              <Link to="/roadmap">Roadmap</Link>
              <Link to="/code-check">Code Check</Link>
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

export default App

