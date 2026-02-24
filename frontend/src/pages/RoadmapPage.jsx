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

  // Category display config — maps DB category slug to display name + icon
  const CATEGORY_META = {
    array:                { name: 'Array & Hash',     icon: '📊' },
    two_pointers:         { name: 'Two Pointers',     icon: '👆' },
    sliding_window:       { name: 'Sliding Window',   icon: '🪟' },
    binary_search:        { name: 'Binary Search',    icon: '🔍' },
    linked_list:          { name: 'Linked List',      icon: '🔗' },
    stack:                { name: 'Stack',             icon: '📚' },
    tree:                 { name: 'Trees',             icon: '🌳' },
    dynamic_programming:  { name: 'DP',               icon: '🎯' },
    graph:                { name: 'Graphs',            icon: '🕸️' },
    greedy:               { name: 'Greedy',            icon: '💡' },
    backtracking:         { name: 'Backtracking',      icon: '🔄' },
    heap:                 { name: 'Heap',              icon: '🏔️' },
    bit:                  { name: 'Bit Manipulation',  icon: '⚡' },
  }

  // Derive unique categories that actually exist in the loaded data
  const usedCategories = [...new Set(knowledgePoints.map(p => p.category).filter(Boolean))]
  const categories = [
    { id: 'all', name: 'All Topics', icon: '📖' },
    ...usedCategories
      .sort((a, b) => {
        const order = Object.keys(CATEGORY_META)
        return order.indexOf(a) - order.indexOf(b)
      })
      .map(id => ({
        id,
        name: CATEGORY_META[id]?.name || id,
        icon: CATEGORY_META[id]?.icon || '📌',
      }))
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

  return (
    <div className="roadmap-container">
      {/* Header */}
      <div className="roadmap-header">
        <h1>
          <span className="gradient-text">Learning Roadmap</span>
        </h1>
        <p>Master algorithms and data structures step by step with guided learning</p>
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
