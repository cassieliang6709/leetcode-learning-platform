import { useState } from 'react'
import { api } from '../services/api'
import './CodeCheckPage.css'

const CodeCheckPage = () => {
  const [code, setCode] = useState('')
  const [language, setLanguage] = useState('python')
  const [questionId, setQuestionId] = useState(1)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [notes, setNotes] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!code.trim()) {
      alert('Please enter your code first')
      return
    }

    setLoading(true)
    try {
      const response = await api.checkCode(1, {
        question_id: questionId,
        code: code,
        language: language,
        notes: notes
      })
      setResult(response.data)
    } catch (error) {
      console.error('Error checking code:', error)
      alert('Failed to check code. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const getResultClass = () => {
    if (!result) return ''
    return result.has_errors ? 'result-error' : 'result-success'
  }

  return (
    <div className="code-check-page">
      <div className="page-header">
        <h1>🤖 AI Code Review</h1>
        <p>Submit your code for instant feedback and suggestions</p>
      </div>

      <div className="code-check-container">
        <div className="code-input-section">
          <div className="input-header">
            <select 
              value={language} 
              onChange={(e) => setLanguage(e.target.value)}
              className="language-select"
            >
              <option value="python">Python</option>
              <option value="javascript">JavaScript</option>
              <option value="java">Java</option>
              <option value="cpp">C++</option>
            </select>
            <input
              type="number"
              value={questionId}
              onChange={(e) => setQuestionId(parseInt(e.target.value))}
              placeholder="Question ID"
              className="question-input"
            />
          </div>

          <textarea
            value={code}
            onChange={(e) => setCode(e.target.value)}
            placeholder="Paste your code here..."
            className="code-textarea"
            rows={20}
          />

          <textarea
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            placeholder="Add notes about your approach (optional)"
            className="notes-textarea"
            rows={3}
          />

          <button 
            onClick={handleSubmit} 
            disabled={loading}
            className="btn-submit"
          >
            {loading ? '🔄 Analyzing...' : '✨ Check Code'}
          </button>
        </div>

        <div className="code-result-section">
          <h3>📊 Analysis Results</h3>
          
          {loading && (
            <div className="loading-state">
              <p>AI is analyzing your code...</p>
            </div>
          )}

          {result && (
            <div className={`result-card ${getResultClass()}`}>
              <div className="result-header">
                {result.has_errors ? (
                  <h4>❌ Issues Found</h4>
                ) : (
                  <h4>✅ Code Looks Good!</h4>
                )}
              </div>

              {result.errors && result.errors.length > 0 && (
                <div className="result-section">
                  <h5>Errors:</h5>
                  <ul className="error-list">
                    {result.errors.map((error, index) => (
                      <li key={index}>{error}</li>
                    ))}
                  </ul>
                </div>
              )}

              {result.suggestions && result.suggestions.length > 0 && (
                <div className="result-section">
                  <h5>💡 Suggestions:</h5>
                  <ul className="suggestion-list">
                    {result.suggestions.map((suggestion, index) => (
                      <li key={index}>{suggestion}</li>
                    ))}
                  </ul>
                </div>
              )}

              {result.corrected_code && (
                <div className="result-section">
                  <h5>✨ Corrected Code:</h5>
                  <pre className="corrected-code">{result.corrected_code}</pre>
                </div>
              )}

              {result.complexity_analysis && (
                <div className="result-section">
                  <h5>⚡ Complexity:</h5>
                  <p>{result.complexity_analysis}</p>
                </div>
              )}
            </div>
          )}

          {!result && !loading && (
            <div className="empty-state">
              <p>Submit your code to see AI analysis results</p>
              <div className="tips">
                <h4>Tips:</h4>
                <ul>
                  <li>Write clean, readable code</li>
                  <li>Add comments to explain your logic</li>
                  <li>Consider edge cases</li>
                  <li>Think about time and space complexity</li>
                </ul>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default CodeCheckPage

