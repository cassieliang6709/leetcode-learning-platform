import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { api } from '../services/api'
import './LearningPage.css'

const LearningPage = () => {
  const { pointId } = useParams()
  const navigate = useNavigate()
  
  const [loading, setLoading] = useState(true)
  const [knowledgePoint, setKnowledgePoint] = useState(null)
  const [questions, setQuestions] = useState([])
  const [currentStep, setCurrentStep] = useState('article') // article, quiz, practice
  const [currentQuizIndex, setCurrentQuizIndex] = useState(0)
  const [selectedAnswer, setSelectedAnswer] = useState(null)
  const [showExplanation, setShowExplanation] = useState(false)
  const [quizResults, setQuizResults] = useState([])

  useEffect(() => {
    loadLearningContent()
  }, [pointId])

  const loadLearningContent = async () => {
    try {
      setLoading(true)
      const [detailRes, questionsRes] = await Promise.all([
        api.getKnowledgePointDetail(pointId),
        api.getKnowledgePointQuestions(pointId)
      ])
      
      setKnowledgePoint(detailRes.data)
      setQuestions(questionsRes.data)
    } catch (error) {
      console.error('Error loading learning content:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleContinueToQuiz = () => {
    if (!knowledgePoint?.reading_questions || knowledgePoint.reading_questions.length === 0) {
      setCurrentStep('practice')
    } else {
      setCurrentStep('quiz')
    }
  }

  const handleAnswerSelect = (index) => {
    if (showExplanation) return
    setSelectedAnswer(index)
  }

  const handleCheckAnswer = () => {
    const currentQuestion = knowledgePoint.reading_questions[currentQuizIndex]
    const isCorrect = selectedAnswer === currentQuestion.correct_answer
    
    setQuizResults([...quizResults, isCorrect])
    setShowExplanation(true)
  }

  const handleNextQuestion = () => {
    if (currentQuizIndex < knowledgePoint.reading_questions.length - 1) {
      setCurrentQuizIndex(currentQuizIndex + 1)
      setSelectedAnswer(null)
      setShowExplanation(false)
    } else {
      setCurrentStep('practice')
    }
  }

  const handleProblemClick = (questionId) => {
    navigate(`/code-check/${questionId}`)
  }

  const getDifficultyColor = (difficulty) => {
    const colors = {
      easy: '#10b981',
      medium: '#f59e0b',
      hard: '#ef4444'
    }
    return colors[difficulty?.toLowerCase()] || colors.medium
  }

  if (loading) {
    return (
      <div className="learning-container">
        <div className="learning-loading">
          <div className="spinner"></div>
          <p>Loading learning content...</p>
        </div>
      </div>
    )
  }

  if (!knowledgePoint) {
    return (
      <div className="learning-container">
        <div className="learning-error">
          <h2>Knowledge point not found</h2>
          <button onClick={() => navigate('/roadmap')} className="btn-back">
            Back to Roadmap
          </button>
        </div>
      </div>
    )
  }

  const progressPercentage = 
    currentStep === 'article' ? 33 : 
    currentStep === 'quiz' ? 66 : 
    100

  return (
    <div className="learning-container">
      {/* Progress Bar */}
      <div className="learning-progress-bar">
        <div className="progress-track">
          <div 
            className="progress-fill" 
            style={{ width: `${progressPercentage}%` }}
          />
        </div>
        <div className="progress-steps">
          <div className={`step ${currentStep === 'article' ? 'active' : 'completed'}`}>
            <div className="step-circle">📖</div>
            <span>Read</span>
          </div>
          <div className={`step ${currentStep === 'quiz' ? 'active' : currentStep === 'practice' ? 'completed' : ''}`}>
            <div className="step-circle">❓</div>
            <span>Quiz</span>
          </div>
          <div className={`step ${currentStep === 'practice' ? 'active' : ''}`}>
            <div className="step-circle">💻</div>
            <span>Practice</span>
          </div>
        </div>
      </div>

      {/* Article Step */}
      {currentStep === 'article' && (
        <div className="learning-content">
          <div className="learning-header">
            <button onClick={() => navigate('/roadmap')} className="btn-back-simple">
              ← Back
            </button>
            <h1>{knowledgePoint.name}</h1>
            <span 
              className="difficulty-badge"
              style={{ backgroundColor: getDifficultyColor(knowledgePoint.difficulty) }}
            >
              {knowledgePoint.difficulty}
            </span>
          </div>

          <div className="article-card">
            {knowledgePoint.article_content ? (
              <div className="article-content">
                {knowledgePoint.article_content.split('\n\n').map((paragraph, index) => (
                  <p key={index}>{paragraph}</p>
                ))}
              </div>
            ) : (
              <div className="article-placeholder">
                <h2>{knowledgePoint.name}</h2>
                <p>{knowledgePoint.description}</p>
                <div className="placeholder-message">
                  📝 Article content will be available soon.
                </div>
              </div>
            )}
          </div>

          <div className="learning-actions">
            <button onClick={handleContinueToQuiz} className="btn-continue">
              Continue →
            </button>
          </div>
        </div>
      )}

      {/* Quiz Step */}
      {currentStep === 'quiz' && knowledgePoint.reading_questions && (
        <div className="learning-content">
          <div className="quiz-header">
            <h2>Check Your Understanding</h2>
            <span className="quiz-counter">
              {currentQuizIndex + 1} / {knowledgePoint.reading_questions.length}
            </span>
          </div>

          <div className="quiz-card">
            <h3 className="quiz-question">
              {knowledgePoint.reading_questions[currentQuizIndex].question}
            </h3>

            <div className="quiz-options">
              {knowledgePoint.reading_questions[currentQuizIndex].options.map((option, index) => {
                const isSelected = selectedAnswer === index
                const isCorrect = index === knowledgePoint.reading_questions[currentQuizIndex].correct_answer
                const showResult = showExplanation
                
                let optionClass = 'quiz-option'
                if (showResult) {
                  if (isCorrect) optionClass += ' correct'
                  else if (isSelected) optionClass += ' incorrect'
                } else if (isSelected) {
                  optionClass += ' selected'
                }

                return (
                  <button
                    key={index}
                    className={optionClass}
                    onClick={() => handleAnswerSelect(index)}
                    disabled={showExplanation}
                  >
                    <span className="option-letter">{String.fromCharCode(65 + index)}</span>
                    <span className="option-text">{option}</span>
                    {showResult && isCorrect && <span className="check-icon">✓</span>}
                    {showResult && isSelected && !isCorrect && <span className="cross-icon">✗</span>}
                  </button>
                )
              })}
            </div>

            {showExplanation && (
              <div className={`explanation ${quizResults[quizResults.length - 1] ? 'correct' : 'incorrect'}`}>
                <div className="explanation-header">
                  {quizResults[quizResults.length - 1] ? (
                    <>
                      <span className="icon">🎉</span>
                      <strong>Correct!</strong>
                    </>
                  ) : (
                    <>
                      <span className="icon">💡</span>
                      <strong>Not quite</strong>
                    </>
                  )}
                </div>
                <p>{knowledgePoint.reading_questions[currentQuizIndex].explanation}</p>
              </div>
            )}
          </div>

          <div className="learning-actions">
            {!showExplanation ? (
              <button 
                onClick={handleCheckAnswer} 
                className="btn-check"
                disabled={selectedAnswer === null}
              >
                Check Answer
              </button>
            ) : (
              <button onClick={handleNextQuestion} className="btn-continue">
                {currentQuizIndex < knowledgePoint.reading_questions.length - 1 ? 'Next →' : 'Start Practice →'}
              </button>
            )}
          </div>
        </div>
      )}

      {/* Practice Step */}
      {currentStep === 'practice' && (
        <div className="learning-content">
          <div className="practice-header">
            <h2>Practice Problems</h2>
            <p>Apply what you learned with these LeetCode problems</p>
          </div>

          {questions.length > 0 ? (
            <div className="problems-grid">
              {questions.map((question, index) => (
                <div 
                  key={question.id} 
                  className="problem-card"
                  onClick={() => handleProblemClick(question.id)}
                >
                  <div className="problem-header">
                    <span className="problem-number">#{index + 1}</span>
                    {question.leetcode_id && (
                      <span className="leetcode-badge">LC {question.leetcode_id}</span>
                    )}
                  </div>
                  
                  <h3 className="problem-title">{question.title}</h3>
                  
                  <div className="problem-footer">
                    <span 
                      className="problem-difficulty"
                      style={{ color: getDifficultyColor(question.difficulty) }}
                    >
                      ● {question.difficulty}
                    </span>
                    <button className="btn-solve">
                      Solve →
                    </button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="empty-state">
              <p>No practice problems available yet.</p>
              <button onClick={() => navigate('/roadmap')} className="btn-back">
                Back to Roadmap
              </button>
            </div>
          )}

          <div className="learning-actions">
            <button onClick={() => navigate('/roadmap')} className="btn-finish">
              ✓ Complete & Return
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

export default LearningPage

