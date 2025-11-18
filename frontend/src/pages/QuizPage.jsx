import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { api } from '../services/api'
import './QuizPage.css'

const QuizPage = () => {
  const { knowledgePointId } = useParams()
  const [questions, setQuestions] = useState([])
  const [currentQuestion, setCurrentQuestion] = useState(null)
  const [selectedQuestionIndex, setSelectedQuestionIndex] = useState(0)
  const [hints, setHints] = useState([])
  const [currentHintLevel, setCurrentHintLevel] = useState(0)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadQuestions()
  }, [knowledgePointId])

  useEffect(() => {
    if (questions.length > 0) {
      setCurrentQuestion(questions[selectedQuestionIndex])
    }
  }, [selectedQuestionIndex, questions])

  const loadQuestions = async () => {
    try {
      const response = await api.getQuizzesByKnowledge(knowledgePointId)
      setQuestions(response.data)
      if (response.data.length > 0) {
        setCurrentQuestion(response.data[0])
      }
    } catch (error) {
      console.error('Error loading questions:', error)
    } finally {
      setLoading(false)
    }
  }

  const requestHint = async (level) => {
    if (!currentQuestion) return

    try {
      const response = await api.getHint(currentQuestion.id, level)
      setHints([...hints, response.data])
      setCurrentHintLevel(level)
    } catch (error) {
      console.error('Error getting hint:', error)
      alert('Failed to get hint')
    }
  }

  const markComplete = async () => {
    if (!currentQuestion) return

    try {
      await api.submitQuizAttempt(currentQuestion.id, 1, true, currentHintLevel)
      alert('Great job! Moving to next question...')
      
      if (selectedQuestionIndex < questions.length - 1) {
        setSelectedQuestionIndex(selectedQuestionIndex + 1)
        setHints([])
        setCurrentHintLevel(0)
      } else {
        alert('Congratulations! You completed all questions in this topic!')
      }
    } catch (error) {
      console.error('Error submitting attempt:', error)
    }
  }

  if (loading) {
    return <div className="loading">Loading questions...</div>
  }

  if (!currentQuestion) {
    return <div className="no-questions">No questions available for this topic</div>
  }

  return (
    <div className="quiz-page">
      <div className="quiz-sidebar">
        <h3>Questions</h3>
        <div className="question-list">
          {questions.map((q, index) => (
            <div
              key={q.id}
              className={`question-item ${index === selectedQuestionIndex ? 'active' : ''}`}
              onClick={() => {
                setSelectedQuestionIndex(index)
                setHints([])
                setCurrentHintLevel(0)
              }}
            >
              <span className="q-number">{index + 1}</span>
              <span className="q-title">{q.title}</span>
              <span className={`q-difficulty ${q.difficulty}`}>
                {q.difficulty}
              </span>
            </div>
          ))}
        </div>
      </div>

      <div className="quiz-main">
        <div className="question-header">
          <h2>{currentQuestion.title}</h2>
          {currentQuestion.leetcode_id && (
            <span className="leetcode-link">
              LeetCode #{currentQuestion.leetcode_id}
            </span>
          )}
        </div>

        <div className="question-description">
          <pre>{currentQuestion.description}</pre>
        </div>

        <div className="hint-section">
          <h3>💡 Need Help?</h3>
          <p>Get hints to guide you through the problem</p>
          
          <div className="hint-buttons">
            <button
              className="btn-hint"
              onClick={() => requestHint(1)}
              disabled={currentHintLevel >= 1}
            >
              Strategy Hint
            </button>
            <button
              className="btn-hint"
              onClick={() => requestHint(2)}
              disabled={currentHintLevel >= 2}
            >
              Code Example
            </button>
            <button
              className="btn-hint"
              onClick={() => requestHint(3)}
              disabled={currentHintLevel >= 3}
            >
              Video Explanation
            </button>
          </div>

          {hints.length > 0 && (
            <div className="hints-display">
              {hints.map((hint, index) => (
                <div key={index} className={`hint-card hint-${hint.hint_type}`}>
                  <h4>
                    {hint.hint_type === 'strategy' && '📝 Strategy'}
                    {hint.hint_type === 'code' && '💻 Code Example'}
                    {hint.hint_type === 'video' && '🎥 Video'}
                  </h4>
                  <div className="hint-content">
                    {hint.hint_type === 'code' ? (
                      <pre>{hint.content}</pre>
                    ) : (
                      <p>{hint.content}</p>
                    )}
                    {hint.video_link && (
                      <a 
                        href={hint.video_link} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="video-link"
                      >
                        Watch on YouTube →
                      </a>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="action-buttons">
          <button className="btn-secondary" onClick={() => window.open('/code-check', '_blank')}>
            Test Your Code
          </button>
          <button className="btn-primary" onClick={markComplete}>
            Mark as Complete
          </button>
        </div>
      </div>
    </div>
  )
}

export default QuizPage

