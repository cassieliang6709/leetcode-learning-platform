import { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { api } from '../services/api'
import './HomePage.css'

const HomePage = () => {
  const [questions, setQuestions] = useState([])
  const [expandedCard, setExpandedCard] = useState(null)
  const [selectedAnswers, setSelectedAnswers] = useState({})
  const [answeredQuestions, setAnsweredQuestions] = useState({})
  const [progress, setProgress] = useState({ answered_count: 0, correct_count: 0, total_questions: 3 })
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const navigate = useNavigate()
  const { isAuthenticated, user } = useAuth()
  
  const userId = user?.id

  useEffect(() => {
    loadDailyQuiz()
  }, [])

  const loadDailyQuiz = async () => {
    if (!isAuthenticated) {
      setLoading(false)
      return
    }
    
    setLoading(true)
    try {
      const response = await api.getDailyQuiz(userId)
      setQuestions(response.data.questions)
      setProgress({
        answered_count: response.data.answered_count,
        correct_count: response.data.correct_count,
        total_questions: response.data.total_questions
      })
    } catch (error) {
      console.error('Error loading daily quiz:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleCardClick = (questionId) => {
    if (answeredQuestions[questionId]) return
    setExpandedCard(expandedCard === questionId ? null : questionId)
  }

  const handleOptionSelect = (questionId, optionIndex) => {
    setSelectedAnswers({
      ...selectedAnswers,
      [questionId]: optionIndex
    })
  }

  const handleSubmitAnswer = async (questionId) => {
    const selectedOption = selectedAnswers[questionId]
    if (selectedOption === undefined) {
      alert('Please select an answer first')
      return
    }

    setSubmitting(true)
    try {
      const response = await api.submitAnswer(userId, questionId, selectedOption)
      
      setAnsweredQuestions({
        ...answeredQuestions,
        [questionId]: {
          isCorrect: response.data.is_correct,
          message: response.data.message
        }
      })
      
      setProgress(prev => ({
        ...prev,
        answered_count: prev.answered_count + 1,
        correct_count: prev.correct_count + (response.data.is_correct ? 1 : 0)
      }))
      
      setExpandedCard(null)
      alert(response.data.message)
    } catch (error) {
      console.error('Error submitting answer:', error)
      alert('Submission failed, please try again')
    } finally {
      setSubmitting(false)
    }
  }

  const getDifficultyColor = (difficulty) => {
    switch (difficulty?.toLowerCase()) {
      case 'easy': return '#10b981'
      case 'medium': return '#f59e0b'
      case 'hard': return '#ef4444'
      default: return '#6b7280'
    }
  }

  const getDifficultyLabel = (difficulty) => {
    switch (difficulty?.toLowerCase()) {
      case 'easy': return 'Easy'
      case 'medium': return 'Medium'
      case 'hard': return 'Hard'
      default: return 'Unknown'
    }
  }

  if (loading) {
    return (
      <div className="home-page">
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Loading...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="home-page">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">
            <span className="gradient-text">AI-Powered</span> Algorithm Learning Platform
          </h1>
          <p className="hero-subtitle">
            Master LeetCode algorithms systematically - from knowledge assessment to personalized learning paths
          </p>
        </div>

        {/* Feature Cards */}
        <div className="feature-cards">
          <div className="feature-card">
            <div className="feature-icon">🎯</div>
            <h3 className="feature-title">Personalized Learning Path</h3>
            <p className="feature-desc">
              AI-generated custom study plans based on your knowledge assessment
            </p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">💡</div>
            <h3 className="feature-title">Multi-Level Hints</h3>
            <p className="feature-desc">
              Strategy hints → Code examples → Video tutorials
            </p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🤖</div>
            <h3 className="feature-title">AI Code Review</h3>
            <p className="feature-desc">
              Instant feedback with precise problem identification and optimization suggestions
            </p>
          </div>
        </div>
      </section>

      {/* Guest Mode Notice */}
      {!isAuthenticated && (
        <section className="guest-notice-section" style={{
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          borderRadius: '12px',
          padding: '2rem',
          marginBottom: '2rem',
          color: 'white',
          textAlign: 'center'
        }}>
          <h2 style={{ marginBottom: '1rem', fontSize: '1.5rem' }}>👋 Welcome to AlgoMentor!</h2>
          <p style={{ marginBottom: '1.5rem', opacity: 0.9 }}>
            You are browsing as a guest. Sign in to save your progress, view personal stats, and unlock more features.
          </p>
          <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
            <Link
              to="/login"
              style={{
                padding: '0.75rem 1.5rem',
                background: 'white',
                color: '#667eea',
                borderRadius: '8px',
                textDecoration: 'none',
                fontWeight: '600',
                transition: 'transform 0.2s'
              }}
            >
              Sign In
            </Link>
            <Link
              to="/register"
              style={{
                padding: '0.75rem 1.5rem',
                background: 'rgba(255, 255, 255, 0.2)',
                color: 'white',
                border: '2px solid white',
                borderRadius: '8px',
                textDecoration: 'none',
                fontWeight: '600',
                transition: 'transform 0.2s'
              }}
            >
              Sign Up
            </Link>
          </div>
        </section>
      )}

      {/* Daily Challenge Section */}
      <section className="challenge-section">
        <div className="section-header">
          <h2 className="section-title">📅 Daily Knowledge Challenge</h2>
          <p className="section-subtitle">3 curated problems daily to strengthen your algorithm foundation</p>
        </div>
        
        {!isAuthenticated ? (
          <div style={{
            textAlign: 'center',
            padding: '3rem',
            background: 'var(--bg-primary)',
            borderRadius: '12px',
            border: '1px solid var(--border-color)'
          }}>
            <p style={{ marginBottom: '1rem', color: 'var(--text-secondary)' }}>
              💡 Sign in to participate in the daily challenge and save your progress
            </p>
            <Link
              to="/login"
              style={{
                display: 'inline-block',
                padding: '0.75rem 1.5rem',
                background: 'var(--accent-primary)',
                color: 'white',
                borderRadius: '8px',
                textDecoration: 'none',
                fontWeight: '600'
              }}
            >
              Sign In Now
            </Link>
          </div>
        ) : (

        <div className="challenge-container">
          {/* Progress Sidebar */}
          <aside className="progress-sidebar">
            <div className="progress-card">
              <h3 className="progress-title">Today's Progress</h3>
              
              <div className="circular-progress">
                <svg className="progress-ring" viewBox="0 0 120 120">
                  <circle
                    className="progress-ring-bg"
                    cx="60"
                    cy="60"
                    r="50"
                  />
                  <circle
                    className="progress-ring-fill"
                    cx="60"
                    cy="60"
                    r="50"
                    style={{
                      strokeDasharray: `${(progress.answered_count / progress.total_questions) * 314} 314`
                    }}
                  />
                </svg>
                <div className="progress-text">
                  <span className="progress-number">{progress.answered_count}</span>
                  <span className="progress-divider">/</span>
                  <span className="progress-total">{progress.total_questions}</span>
                </div>
              </div>

              <div className="progress-stats">
                <div className="stat-item">
                  <span className="stat-label">Completed</span>
                  <span className="stat-value">{progress.answered_count}</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">Correct</span>
                  <span className="stat-value correct">{progress.correct_count}</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">Accuracy</span>
                  <span className="stat-value">
                    {progress.answered_count > 0 
                      ? Math.round((progress.correct_count / progress.answered_count) * 100) 
                      : 0}%
                  </span>
                </div>
              </div>

              {progress.answered_count === progress.total_questions && (
                <div className="completion-badge">
                  <span className="badge-icon">🎉</span>
                  <span className="badge-text">Completed Today!</span>
                </div>
              )}
            </div>
          </aside>

          {/* Questions List */}
          <div className="questions-list">
            {questions.map((question, index) => {
              const isAnswered = answeredQuestions[question.id]
              const isExpanded = expandedCard === question.id
              const selectedOption = selectedAnswers[question.id]

              return (
                <div 
                  key={question.id} 
                  className={`question-card ${isAnswered ? 'answered' : ''} ${isExpanded ? 'expanded' : ''}`}
                >
                  {/* Card Header */}
                  <div 
                    className="card-header"
                    onClick={() => handleCardClick(question.id)}
                  >
                    <div className="card-left">
                      <span className="question-number">#{index + 1}</span>
                      <div className="question-info">
                        <h3 className="question-title">{question.title}</h3>
                        {question.knowledge_point_name && (
                          <span className="knowledge-tag">{question.knowledge_point_name}</span>
                        )}
                      </div>
                    </div>
                    <div className="card-right">
                      <span 
                        className="difficulty-badge"
                        style={{ backgroundColor: getDifficultyColor(question.difficulty) }}
                      >
                        {getDifficultyLabel(question.difficulty)}
                      </span>
                      {isAnswered ? (
                        <span className={`status-icon ${isAnswered.isCorrect ? 'correct' : 'incorrect'}`}>
                          {isAnswered.isCorrect ? '✅' : '❌'}
                        </span>
                      ) : (
                        <span className="expand-icon">{isExpanded ? '▼' : '▶'}</span>
                      )}
                    </div>
                  </div>

                  {/* Card Body (Expanded) */}
                  {isExpanded && !isAnswered && (
                    <div className="card-body">
                      <p className="question-description">{question.description}</p>
                      
                      <div className="options-container">
                        {question.options.map((option, optionIndex) => (
                          <button
                            key={optionIndex}
                            className={`option-button ${selectedOption === optionIndex ? 'selected' : ''}`}
                            onClick={() => handleOptionSelect(question.id, optionIndex)}
                          >
                            <span className="option-letter">{String.fromCharCode(65 + optionIndex)}</span>
                            <span className="option-text">{option}</span>
                          </button>
                        ))}
                      </div>

                      <button
                        className="submit-button"
                        onClick={() => handleSubmitAnswer(question.id)}
                        disabled={selectedOption === undefined || submitting}
                      >
                        {submitting ? 'Submitting...' : 'Submit Answer'}
                      </button>
                    </div>
                  )}

                  {/* Answered State */}
                  {isAnswered && (
                    <div className="card-result">
                      <p className={`result-message ${isAnswered.isCorrect ? 'correct' : 'incorrect'}`}>
                        {isAnswered.message}
                      </p>
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        </div>
        )}
      </section>

      {/* Quick Actions */}
      <section className="actions-section">
        <button className="action-btn primary" onClick={() => navigate('/roadmap')}>
          📚 View Learning Path
        </button>
        <button className="action-btn secondary" onClick={() => navigate('/quiz')}>
          💻 Start Practice
        </button>
      </section>
    </div>
  )
}

export default HomePage
