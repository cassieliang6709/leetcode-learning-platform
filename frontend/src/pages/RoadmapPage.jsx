import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../services/api'
import './RoadmapPage.css'

const RoadmapPage = () => {
  const [knowledgePoints, setKnowledgePoints] = useState([])
  const [loading, setLoading] = useState(true)
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

  const getDifficultyClass = (difficulty) => {
    return `difficulty ${difficulty.toLowerCase()}`
  }

  const handleSelectTopic = (pointId) => {
    navigate(`/quiz/${pointId}`)
  }

  if (loading) {
    return <div className="loading">Loading roadmap...</div>
  }

  return (
    <div className="roadmap-page">
      <div className="roadmap-header">
        <h1>🗺️ Your Learning Roadmap</h1>
        <p>Select a knowledge point to start practicing</p>
      </div>

      <div className="roadmap-grid">
        {knowledgePoints.map((point, index) => (
          <div 
            key={point.id} 
            className="knowledge-card"
            onClick={() => handleSelectTopic(point.id)}
          >
            <div className="card-header">
              <span className="card-number">{index + 1}</span>
              <span className={getDifficultyClass(point.difficulty)}>
                {point.difficulty}
              </span>
            </div>
            <h3>{point.name}</h3>
            <p className="card-description">{point.description}</p>
            <div className="card-footer">
              <span className="category-tag">{point.category}</span>
              <button className="btn-start">Start →</button>
            </div>
          </div>
        ))}
      </div>

      <div className="roadmap-tips">
        <h3>💡 Learning Tips</h3>
        <ul>
          <li>Complete topics in order for best results</li>
          <li>Practice at least 3 problems per topic</li>
          <li>Use hints strategically - try solving first!</li>
          <li>Review your mistakes and learn from them</li>
        </ul>
      </div>
    </div>
  )
}

export default RoadmapPage

