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
    { id: 'all', name: 'All Topics', icon: '📚' },
    { id: 'array', name: 'Arrays', icon: '📊' },
    { id: 'string', name: 'Strings', icon: '📝' },
    { id: 'tree', name: 'Trees', icon: '🌳' },
    { id: 'graph', name: 'Graphs', icon: '🕸️' },
    { id: 'dp', name: 'Dynamic Programming', icon: '🎯' },
    { id: 'other', name: 'Advanced', icon: '🔧' }
  ]

  const filteredPoints = selectedCategory === 'all' 
    ? knowledgePoints 
    : knowledgePoints.filter(point => point.category === selectedCategory)

  const handleSelectTopic = (pointId) => {
    navigate(`/roadmap/${pointId}/learn`)
  }

  if (loading) {
    return (
      <div className="roadmap-container">
        <div className="roadmap-header">
          <div className="skeleton skeleton-header"></div>
          <div className="skeleton skeleton-subtitle"></div>
        </div>

        <div className="skeleton-filter">
          {[1, 2, 3, 4, 5, 6, 7].map(i => (
            <div key={i} className="skeleton skeleton-filter-btn"></div>
          ))}
        </div>

        <div className="topics-grid">
          {[1, 2, 3, 4, 5, 6].map(i => (
            <div key={i} className="topic-card skeleton-card">
              <div className="skeleton-card-header">
                <div className="skeleton skeleton-number"></div>
                <div className="skeleton skeleton-difficulty"></div>
              </div>
              <div className="skeleton skeleton-title"></div>
              <div className="skeleton skeleton-desc"></div>
              <div className="skeleton skeleton-desc"></div>
              <div className="skeleton skeleton-footer"></div>
            </div>
          ))}
        </div>
      </div>
    )
  }

  const completedCount = 0 // TODO: Track user progress
  const totalCount = knowledgePoints.length

  return (
    <div className="roadmap-container">
      {/* Header */}
      <div className="roadmap-header">
        <h1>
          <span className="gradient-text">Learning Roadmap</span>
        </h1>
        <p>Master algorithms and data structures step by step with guided learning</p>
      </div>

      {/* Progress Summary */}
      <div className="progress-summary-section">
        <div className="progress-summary-card">
          <div className="progress-text">
            <div className="progress-label">Your Progress</div>
            <div className="progress-numbers">
              <span className="completed">{completedCount}</span>
              <span style={{ opacity: 0.7 }}> / {totalCount}</span>
            </div>
          </div>
          <div className="progress-visual">
            <svg width="80" height="80" viewBox="0 0 80 80">
              <circle
                cx="40"
                cy="40"
                r="36"
                fill="none"
                stroke="rgba(255, 255, 255, 0.2)"
                strokeWidth="6"
              />
              <circle
                cx="40"
                cy="40"
                r="36"
                fill="none"
                stroke="white"
                strokeWidth="6"
                strokeLinecap="round"
                strokeDasharray={`${(completedCount / totalCount) * 226}, 226`}
                transform="rotate(-90 40 40)"
              />
              <text
                x="40"
                y="45"
                textAnchor="middle"
                fill="white"
                fontSize="20"
                fontWeight="700"
              >
                {Math.round((completedCount / totalCount) * 100)}%
              </text>
            </svg>
          </div>
        </div>
      </div>

      {/* Category Filter */}
      <div className="categories-filter">
        {categories.map(category => {
          const count = category.id === 'all' 
            ? knowledgePoints.length 
            : knowledgePoints.filter(p => p.category === category.id).length
          
          return (
            <button
              key={category.id}
              className={`category-filter-btn ${selectedCategory === category.id ? 'active' : ''}`}
              onClick={() => setSelectedCategory(category.id)}
            >
              <span className="category-icon">{category.icon}</span>
              <span>{category.name}</span>
              <span className="category-count">{count}</span>
            </button>
          )
        })}
      </div>

      {/* Topics Grid */}
      {filteredPoints.length > 0 ? (
        <div className="topics-grid">
          {filteredPoints.map((point, index) => (
            <div 
              key={point.id} 
              className="topic-card"
              onClick={() => handleSelectTopic(point.id)}
            >
              <div className="topic-header">
                <div className="topic-number">{index + 1}</div>
                <span className={`difficulty difficulty-${point.difficulty?.toLowerCase() || 'medium'}`}>
                  <span className="difficulty-dot" />
                  {point.difficulty || 'Medium'}
                </span>
              </div>
              
              <h3 className="topic-title">{point.name}</h3>
              <p className="topic-description">
                {point.description || 'Master this essential data structure and algorithm pattern'}
              </p>
              
              <div className="topic-footer">
                <div className="topic-category">
                  {point.category || 'algorithm'}
                </div>
                <button className="topic-start-btn">
                  <span>Start Learning</span>
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                    <path d="M6 3L11 8L6 13" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </button>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="empty-state">
          <p>No topics found in this category</p>
        </div>
      )}
    </div>
  )
}

export default RoadmapPage
