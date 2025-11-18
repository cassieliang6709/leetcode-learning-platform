import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../services/api'
import './HomePage.css'

const HomePage = () => {
  const [testStarted, setTestStarted] = useState(false)
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [answers, setAnswers] = useState([])
  const [testResult, setTestResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  // Demo test questions
  const testQuestions = [
    {
      id: 1,
      question: "Which data structure provides O(1) lookup time?",
      topic: "Hash Table",
      options: ["Array", "Hash Table", "Linked List", "Tree"],
      correctAnswer: 1
    },
    {
      id: 2,
      question: "What is the time complexity of binary search?",
      topic: "Binary Search",
      options: ["O(n)", "O(log n)", "O(n²)", "O(1)"],
      correctAnswer: 1
    },
    {
      id: 3,
      question: "Which technique is best for subarray problems?",
      topic: "Sliding Window",
      options: ["Two Pointers", "Sliding Window", "Binary Search", "DFS"],
      correctAnswer: 1
    }
  ]

  const startTest = () => {
    setTestStarted(true)
    setCurrentQuestion(0)
    setAnswers([])
    setTestResult(null)
  }

  const handleAnswer = (answerIndex) => {
    const question = testQuestions[currentQuestion]
    const isCorrect = answerIndex === question.correctAnswer

    setAnswers([...answers, {
      question_id: question.id,
      topic: question.topic,
      is_correct: isCorrect
    }])

    if (currentQuestion < testQuestions.length - 1) {
      setCurrentQuestion(currentQuestion + 1)
    } else {
      submitTest([...answers, {
        question_id: question.id,
        topic: question.topic,
        is_correct: isCorrect
      }])
    }
  }

  const submitTest = async (finalAnswers) => {
    setLoading(true)
    try {
      const response = await api.submitKnowledgeTest(1, { answers: finalAnswers })
      setTestResult(response.data)
      setTestStarted(false)
    } catch (error) {
      console.error('Error submitting test:', error)
      alert('Failed to submit test. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="home-page">
      <div className="hero-section">
        <h1>Master LeetCode with AI-Powered Learning</h1>
        <p>Test your knowledge, get personalized learning plans, and practice with guided hints</p>
      </div>

      {!testStarted && !testResult && (
        <div className="test-intro">
          <h2>📝 Take the Knowledge Assessment</h2>
          <p>Answer a few questions to help us create your personalized learning plan</p>
          <button className="btn-primary" onClick={startTest}>
            Start Assessment
          </button>
        </div>
      )}

      {testStarted && (
        <div className="test-container">
          <div className="progress-bar">
            <div 
              className="progress-fill" 
              style={{ width: `${((currentQuestion + 1) / testQuestions.length) * 100}%` }}
            />
          </div>
          <p className="question-counter">
            Question {currentQuestion + 1} of {testQuestions.length}
          </p>

          <div className="question-card">
            <h3>{testQuestions[currentQuestion].question}</h3>
            <div className="options">
              {testQuestions[currentQuestion].options.map((option, index) => (
                <button
                  key={index}
                  className="option-btn"
                  onClick={() => handleAnswer(index)}
                >
                  {option}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

      {loading && (
        <div className="loading">
          <p>🤖 AI is analyzing your results and creating your learning plan...</p>
        </div>
      )}

      {testResult && (
        <div className="test-result">
          <h2>✅ Assessment Complete!</h2>
          <div className="score-card">
            <h3>Your Score: {testResult.score}/100</h3>
            <p>Based on your results, we've created a personalized learning plan for you.</p>
          </div>

          <div className="recommendations">
            <h3>📚 Recommended Learning Path</h3>
            <ul>
              {testResult.ai_plan.next_steps?.map((step, index) => (
                <li key={index}>{step}</li>
              ))}
            </ul>
            <p className="estimate">Estimated time: {testResult.ai_plan.study_time_estimate}</p>
          </div>

          <button 
            className="btn-primary" 
            onClick={() => navigate('/roadmap')}
          >
            View Your Roadmap
          </button>
        </div>
      )}

      <div className="features">
        <div className="feature-card">
          <h3>🗺️ Personalized Roadmap</h3>
          <p>Get a customized learning path based on your current knowledge</p>
        </div>
        <div className="feature-card">
          <h3>💡 Multi-Level Hints</h3>
          <p>Stuck? Get strategy hints, code examples, or video explanations</p>
        </div>
        <div className="feature-card">
          <h3>🤖 AI Code Review</h3>
          <p>Submit your code for instant AI feedback and improvements</p>
        </div>
      </div>
    </div>
  )
}

export default HomePage

