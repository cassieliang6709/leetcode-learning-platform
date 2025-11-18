import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../services/api'
import './RoadmapPage.css'

const RoadmapPage = () => {
  const [knowledgePoints, setKnowledgePoints] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedCategory, setSelectedCategory] = useState('all')
  const navigate = useNavigate()

  useEffect(() => {
    loadKnowledgePoints()
  }, [])

  const loadKnowledgePoints = async () => {
    try {
      const response = await api.getKnowledgePoints()
      setKnowledgePoints(response.data)
    } catch (error) {
      console.error('Error loading knowledge points:', error)
    } finally {
      setLoading(false)
    }
  }

  const categories = [
    { id: 'all', name: 'All Topics', icon: '📚', count: 0 },
    { id: 'array', name: 'Arrays & More', icon: '📊', count: 0 },
    { id: 'string', name: 'Strings', icon: '📝', count: 0 },
    { id: 'tree', name: 'Trees & Tries', icon: '🌳', count: 0 },
    { id: 'graph', name: 'Graphs', icon: '🕸️', count: 0 },
    { id: 'dp', name: 'Dynamic Programming', icon: '🎯', count: 0 },
    { id: 'other', name: 'Advanced Topics', icon: '🔧', count: 0 }
  ]

  const filteredPoints = selectedCategory === 'all' 
    ? knowledgePoints 
    : knowledgePoints.filter(point => point.category === selectedCategory)

  const getDifficultyClass = (difficulty) => {
    return `difficulty difficulty-${difficulty?.toLowerCase() || 'medium'}`
  }

  const getDifficultyColor = (difficulty) => {
    const colors = {
      easy: 'var(--success)',
      medium: 'var(--warning)',
      hard: 'var(--danger)'
    }
    return colors[difficulty?.toLowerCase()] || colors.medium
  }

  const handleSelectTopic = (pointId) => {
    navigate(`/quiz/${pointId}`)
  }

  if (loading) {
    return (
      <div className="roadmap-container">
        {/* Sidebar Skeleton */}
        <aside className="roadmap-sidebar">
          <div className="sidebar-header">
            <div className="skeleton skeleton-text skeleton-title"></div>
          </div>
          <nav className="category-nav">
            {[1, 2, 3, 4, 5, 6, 7].map(i => (
              <div key={i} className="category-item skeleton-category">
                <span className="skeleton skeleton-icon"></span>
                <span className="skeleton skeleton-text" style={{ flex: 1 }}></span>
                <span className="skeleton skeleton-count"></span>
              </div>
            ))}
          </nav>
        </aside>

        {/* Main Content Skeleton */}
        <main className="roadmap-main">
          <div className="roadmap-header">
            <div className="header-content">
              <div className="skeleton skeleton-text skeleton-heading"></div>
              <div className="skeleton skeleton-text skeleton-subtitle"></div>
            </div>
            <div className="progress-summary">
              <div className="skeleton skeleton-circle"></div>
              <div className="skeleton skeleton-text skeleton-label"></div>
            </div>
          </div>

          <div className="topics-grid">
            {[1, 2, 3, 4, 5, 6].map(i => (
              <div key={i} className="topic-card skeleton-card">
                <div className="topic-header">
                  <div className="skeleton skeleton-number"></div>
                  <div className="skeleton skeleton-difficulty"></div>
                </div>
                <div className="skeleton skeleton-text skeleton-card-title"></div>
                <div className="skeleton skeleton-text skeleton-card-desc"></div>
                <div className="skeleton skeleton-text skeleton-card-desc" style={{ width: '80%' }}></div>
                <div className="topic-footer">
                  <div className="skeleton skeleton-tag"></div>
                  <div className="skeleton skeleton-button"></div>
                </div>
              </div>
            ))}
          </div>
        </main>
      </div>
    )
  }

  const completedCount = 0 // TODO: 从后端获取
  const totalCount = knowledgePoints.length

  return (
    <div className="roadmap-container">
      {/* Sidebar */}
      <aside className="roadmap-sidebar">
        <div className="sidebar-header">
          <h2>Categories</h2>
        </div>
        <nav className="category-nav">
          {categories.map(category => {
            const count = category.id === 'all' 
              ? knowledgePoints.length 
              : knowledgePoints.filter(p => p.category === category.id).length
            
            return (
              <button
                key={category.id}
                className={`category-item ${selectedCategory === category.id ? 'active' : ''}`}
                onClick={() => setSelectedCategory(category.id)}
              >
                <span className="category-icon">{category.icon}</span>
                <span className="category-name">{category.name}</span>
                <span className="category-count">{count}</span>
              </button>
            )
          })}
        </nav>
      </aside>

      {/* Main Content */}
      <main className="roadmap-main">
        <div className="roadmap-header">
          <div className="header-content">
            <h1>Learning Roadmap</h1>
            <p>Master algorithms and data structures step by step</p>
          </div>
          <div className="progress-summary">
            <div className="progress-circle">
              <svg viewBox="0 0 36 36" className="circular-chart">
                <path
                  className="circle-bg"
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                />
                <path
                  className="circle"
                  strokeDasharray={`${(completedCount / totalCount) * 100}, 100`}
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                />
              </svg>
              <div className="progress-text">
                <span className="progress-num">{completedCount}</span>
                <span className="progress-total">/ {totalCount}</span>
              </div>
            </div>
            <div className="progress-label">Completed</div>
          </div>
        </div>

        <div className="topics-grid">
          {filteredPoints.map((point, index) => (
            <div 
              key={point.id} 
              className="topic-card"
              onClick={() => handleSelectTopic(point.id)}
            >
              <div className="topic-header">
                <div className="topic-number">{index + 1}</div>
                <span className={getDifficultyClass(point.difficulty)}>
                  <span 
                    className="difficulty-dot" 
                    style={{ backgroundColor: getDifficultyColor(point.difficulty) }}
                  />
                  {point.difficulty || 'Medium'}
                </span>
              </div>
              
              <h3 className="topic-title">{point.name}</h3>
              <p className="topic-description">{point.description}</p>
              
              <div className="topic-footer">
                <div className="topic-meta">
                  <span className="topic-category">{point.category}</span>
                  <span className="topic-problems">0 / 5 problems</span>
                </div>
                <button className="topic-start-btn">
                  <span>Start</span>
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                    <path d="M6 3L11 8L6 13" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </button>
              </div>
            </div>
          ))}
        </div>

        {filteredPoints.length === 0 && (
          <div className="empty-state">
            <p>No topics found in this category</p>
          </div>
        )}
      </main>
    </div>
  )
}

export default RoadmapPage

