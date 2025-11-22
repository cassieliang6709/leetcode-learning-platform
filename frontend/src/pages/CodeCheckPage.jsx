import { useState, useEffect } from 'react'
import { api } from '../services/api'
import './CodeCheckPage.css'

const CodeCheckPage = () => {
  const [code, setCode] = useState('')
  const [language, setLanguage] = useState('python')
  const [questionId, setQuestionId] = useState(null)
  const [selectedProblem, setSelectedProblem] = useState(null)
  const [problems, setProblems] = useState([])
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [notes, setNotes] = useState('')
  const [hints, setHints] = useState({})
  const [hintsUsed, setHintsUsed] = useState(0)
  const [testResults, setTestResults] = useState(null)
  const [runOutput, setRunOutput] = useState(null)
  const [activeTab, setActiveTab] = useState('testcases') // 'testcases' or 'result'
  const [aiSuggestion, setAiSuggestion] = useState(null)
  const [loadingAiSuggestion, setLoadingAiSuggestion] = useState(false)
  const [showChatDialog, setShowChatDialog] = useState(false)
  const [chatHistory, setChatHistory] = useState([])
  const [chatMessage, setChatMessage] = useState('')
  const [loadingChat, setLoadingChat] = useState(false)

  useEffect(() => {
    loadProblems()
  }, [])

  const loadProblems = async () => {
    try {
      const response = await api.getProblems()
      setProblems(response.data.problems)
      if (response.data.problems.length > 0) {
        selectProblem(response.data.problems[0].id)
      }
    } catch (error) {
      console.error('Error loading problems:', error)
    }
  }

  const selectProblem = async (problemId) => {
    try {
      const response = await api.getProblemDetail(problemId)
      setSelectedProblem(response.data)
      setQuestionId(problemId)
      setHints({})
      setHintsUsed(0)
      setResult(null)
      setTestResults(null)
      setRunOutput(null)
      setAiSuggestion(null)
      setChatHistory([])
      
      // Load starter code for the selected language
      loadStarterCode(problemId, language)
    } catch (error) {
      console.error('Error loading problem details:', error)
    }
  }

  const loadStarterCode = async (problemId, lang) => {
    try {
      const response = await api.getStarterCode(problemId, lang)
      if (response.data.code) {
        setCode(response.data.code)
      } else {
        setCode('')
      }
    } catch (error) {
      console.error('Error loading starter code:', error)
      setCode('')
    }
  }

  const handleLanguageChange = (newLanguage) => {
    setLanguage(newLanguage)
    if (questionId) {
      loadStarterCode(questionId, newLanguage)
    }
  }

  const requestHint = async (level) => {
    if (!questionId) {
      alert('Please select a problem first')
      return
    }

    try {
      const response = await api.requestCodeHint(questionId, level)
      setHints(prev => ({
        ...prev,
        [level]: response.data
      }))
      setHintsUsed(Math.max(hintsUsed, level))
    } catch (error) {
      console.error('Error requesting hint:', error)
      alert('Failed to get hint. Please try again.')
    }
  }

  const handleRun = async () => {
    if (!code.trim()) {
      alert('Please enter your code first')
      return
    }

    setLoading(true)
    setActiveTab('result')
    setRunOutput(null)
    setTestResults(null)
    
    try {
      const response = await api.runCode(code, language)
      setRunOutput(response.data.result)
    } catch (error) {
      console.error('Error running code:', error)
      setRunOutput({
        success: false,
        error: error.response?.data?.detail || 'Failed to run code. Please try again.'
      })
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async () => {
    if (!code.trim()) {
      alert('Please enter your code first')
      return
    }

    if (!questionId) {
      alert('Please select a problem first')
      return
    }

    setLoading(true)
    setActiveTab('result')
    setTestResults(null)
    setRunOutput(null)
    setAiSuggestion(null)
    
    try {
      const response = await api.submitCode(questionId, code, language)
      setTestResults(response.data)
      
      // Check if any tests failed
      const hasFailed = response.data.summary?.failed > 0
      
      if (hasFailed) {
        // Automatically get AI suggestion for failed tests
        fetchAiSuggestion(response.data.test_results)
      }
      
      // Also save to code check history
      await api.checkCode(1, {
        question_id: questionId,
        code: code,
        language: language,
        notes: notes
      })
    } catch (error) {
      console.error('Error submitting code:', error)
      alert(error.response?.data?.detail || 'Failed to submit code. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const fetchAiSuggestion = async (testResults) => {
    if (!questionId || !code) return
    
    setLoadingAiSuggestion(true)
    try {
      const response = await api.getFailureSuggestion(
        questionId,
        code,
        language,
        testResults
      )
      setAiSuggestion(response.data)
    } catch (error) {
      console.error('Error getting AI suggestion:', error)
      setAiSuggestion({
        success: false,
        error: 'Failed to get AI suggestion. Please try the chat feature.'
      })
    } finally {
      setLoadingAiSuggestion(false)
    }
  }

  const handleSendChatMessage = async () => {
    if (!chatMessage.trim()) return
    
    const userMessage = chatMessage.trim()
    setChatMessage('')
    
    // Add user message to history
    const newHistory = [
      ...chatHistory,
      { role: 'user', content: userMessage }
    ]
    setChatHistory(newHistory)
    
    setLoadingChat(true)
    try {
      const response = await api.chatWithAI(
        questionId,
        code,
        language,
        userMessage,
        chatHistory.length > 0 ? chatHistory : null
      )
      
      // Add AI response to history
      setChatHistory([
        ...newHistory,
        { role: 'assistant', content: response.data.response }
      ])
    } catch (error) {
      console.error('Error chatting with AI:', error)
      setChatHistory([
        ...newHistory,
        { role: 'assistant', content: 'Sorry, I encountered an error. Please try again.' }
      ])
    } finally {
      setLoadingChat(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendChatMessage()
    }
  }

  const handleAICheck = async () => {
    if (!code.trim()) {
      alert('Please enter your code first')
      return
    }

    if (!questionId) {
      alert('Please select a problem first')
      return
    }

    setLoading(true)
    setActiveTab('result')
    
    try {
      const response = await api.checkCode(1, {
        question_id: questionId,
        code: code,
        language: language,
        notes: notes
      })
      setResult(response.data)
      setTestResults(null)
      setRunOutput(null)
    } catch (error) {
      console.error('Error checking code:', error)
      alert('Failed to check code. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'easy': return '#00b894'
      case 'medium': return '#fdcb6e'
      case 'hard': return '#d63031'
      default: return '#636e72'
    }
  }

  const getHintIcon = (level) => {
    switch (level) {
      case 1: return '💡'
      case 2: return '💻'
      case 3: return '🎥'
      default: return '❓'
    }
  }

  const getHintTitle = (level) => {
    switch (level) {
      case 1: return 'Strategy Hint'
      case 2: return 'Code Hint'
      case 3: return 'Video Tutorial'
      default: return 'Hint'
    }
  }

  const getResultClass = () => {
    if (!result) return ''
    return result.has_errors ? 'result-error' : 'result-success'
  }

  return (
    <div className="code-check-page">
      <div className="page-header">
        <h1>🤖 LeetCode Code Check</h1>
        <p>Select a problem, get hints, and check your solution</p>
      </div>

      <div className="code-check-layout">
        {/* Left: Problem Selection */}
        <div className="problems-sidebar">
          <h3>📚 LeetCode Hot 100</h3>
          <div className="problems-list">
            {problems.map(prob => (
              <div
                key={prob.id}
                className={`problem-item ${questionId === prob.id ? 'active' : ''}`}
                onClick={() => selectProblem(prob.id)}
              >
                <div className="problem-header">
                  <span className="problem-number">#{prob.leetcode_id}</span>
                  <span 
                    className="difficulty-badge"
                    style={{ backgroundColor: getDifficultyColor(prob.difficulty) }}
                  >
                    {prob.difficulty}
                  </span>
                </div>
                <div className="problem-title">{prob.title}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Middle: Problem Details & Code Editor */}
        <div className="code-input-section">
          {selectedProblem && (
            <>
              <div className="problem-details">
                <h2>
                  #{selectedProblem.leetcode_id}. {selectedProblem.title}
                  <span 
                    className="difficulty-badge"
                    style={{ backgroundColor: getDifficultyColor(selectedProblem.difficulty) }}
                  >
                    {selectedProblem.difficulty}
                  </span>
                </h2>
                <div className="problem-description">
                  {selectedProblem.description}
                </div>
              </div>

              {/* Hint System */}
              <div className="hints-section">
                <h4>💡 Need Help?</h4>
                <div className="hint-buttons">
                  {[1, 2, 3].map(level => (
                    <button
                      key={level}
                      onClick={() => requestHint(level)}
                      className={`hint-btn ${hints[level] ? 'active' : ''}`}
                      disabled={level > 1 && !hints[level - 1]}
                    >
                      {getHintIcon(level)} {getHintTitle(level)}
                    </button>
                  ))}
                </div>
                
                {/* Display Hints */}
                <div className="hints-display">
                  {Object.keys(hints).sort().map(level => {
                    const hint = hints[level]
                    return (
                      <div key={level} className={`hint-card hint-level-${level}`}>
                        <div className="hint-header">
                          <strong>{getHintIcon(parseInt(level))} {getHintTitle(parseInt(level))}</strong>
                        </div>
                        <div className="hint-content">
                          {hint.hint_type === 'code' ? (
                            <pre className="hint-code">{hint.content}</pre>
                          ) : hint.hint_type === 'video' ? (
                            <div>
                              <p>{hint.content}</p>
                              {hint.video_link && (
                                <a 
                                  href={hint.video_link} 
                                  target="_blank" 
                                  rel="noopener noreferrer"
                                  className="video-link"
                                >
                                  🎥 Watch Video Tutorial
                                </a>
                              )}
                            </div>
                          ) : (
                            <p>{hint.content}</p>
                          )}
                        </div>
                      </div>
                    )
                  })}
                </div>
              </div>

              {/* Code Editor */}
              <div className="code-editor-section">
                <div className="editor-header">
                  <select 
                    value={language} 
                    onChange={(e) => handleLanguageChange(e.target.value)}
                    className="language-select"
                  >
                    <option value="python">Python</option>
                    <option value="javascript">JavaScript</option>
                    <option value="java">Java</option>
                    <option value="cpp">C++</option>
                  </select>
                </div>

                <textarea
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                  placeholder="Write your solution here..."
                  className="code-textarea"
                  rows={15}
                  spellCheck={false}
                />

                <div className="action-buttons">
                  <button 
                    onClick={handleRun} 
                    disabled={loading}
                    className="btn-run"
                  >
                    {loading && !testResults ? '▶️ Running...' : '▶️ Run Code'}
                  </button>
                  <button 
                    onClick={handleSubmit} 
                    disabled={loading}
                    className="btn-submit"
                  >
                    {loading && activeTab === 'result' && !runOutput ? '🔄 Submitting...' : '✅ Submit'}
                  </button>
                  <button 
                    onClick={handleAICheck} 
                    disabled={loading}
                    className="btn-ai-check"
                  >
                    {loading && result ? '🤖 Analyzing...' : '🤖 AI Check'}
                  </button>
                </div>
              </div>
            </>
          )}
        </div>

        {/* Right: Test Cases & Results */}
        <div className="code-result-section">
          <div className="result-tabs">
            <button 
              className={`tab ${activeTab === 'testcases' ? 'active' : ''}`}
              onClick={() => setActiveTab('testcases')}
            >
              📋 Test Cases
            </button>
            <button 
              className={`tab ${activeTab === 'result' ? 'active' : ''}`}
              onClick={() => setActiveTab('result')}
            >
              📊 Results
            </button>
          </div>

          {activeTab === 'testcases' && selectedProblem && (
            <div className="testcases-panel">
              {selectedProblem.test_cases && selectedProblem.test_cases.length > 0 ? (
                <div className="test-cases-list">
                  {selectedProblem.test_cases.map((tc, index) => (
                    <div key={index} className="test-case-item">
                      <h4>Test Case {index + 1}</h4>
                      <div className="test-case-content">
                        <div className="test-input">
                          <strong>Input:</strong>
                          <pre>{tc.input}</pre>
                        </div>
                        <div className="test-expected">
                          <strong>Expected Output:</strong>
                          <pre>{tc.expected}</pre>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="empty-state">
                  <p>No test cases available for this problem</p>
                </div>
              )}
            </div>
          )}

          {activeTab === 'result' && (
            <div className="results-panel">
              {loading && (
                <div className="loading-state">
                  <p>⏳ Running your code...</p>
                </div>
              )}

              {/* Test Results from Submit */}
              {testResults && !loading && (
                <div className="test-results">
                  <div className={`result-summary ${testResults.summary?.passed === testResults.summary?.total ? 'success' : 'error'}`}>
                    <h3>
                      {testResults.summary?.passed === testResults.summary?.total ? '✅ Accepted' : '❌ Wrong Answer'}
                    </h3>
                    <p>
                      {testResults.summary?.passed} / {testResults.summary?.total} test cases passed 
                      ({testResults.summary?.pass_rate?.toFixed(1)}%)
                    </p>
                  </div>

                  {/* AI Suggestion for Failed Tests */}
                  {testResults.summary?.failed > 0 && (
                    <div className="ai-suggestion-section">
                      <div className="ai-suggestion-header">
                        <h4>🤖 AI Suggestion</h4>
                        {loadingAiSuggestion && <span className="loading-text">Analyzing...</span>}
                      </div>
                      
                      {aiSuggestion && aiSuggestion.success && (
                        <div className="ai-suggestion-content">
                          <div className="suggestion-text">
                            {aiSuggestion.suggestion.split('\n').map((line, idx) => (
                              <p key={idx}>{line}</p>
                            ))}
                          </div>
                        </div>
                      )}
                      
                      {aiSuggestion && !aiSuggestion.success && (
                        <div className="ai-suggestion-error">
                          <p>{aiSuggestion.error}</p>
                        </div>
                      )}
                      
                      {!aiSuggestion && !loadingAiSuggestion && (
                        <div className="ai-suggestion-placeholder">
                          <p>AI is analyzing your code to provide helpful suggestions...</p>
                        </div>
                      )}
                    </div>
                  )}

                  <div className="test-cases-results">
                    {testResults.test_results?.map((result, index) => (
                      <div key={index} className={`test-result-item ${result.passed ? 'passed' : 'failed'}`}>
                        <div className="test-result-header">
                          <h4>
                            {result.passed ? '✅' : '❌'} Test Case {result.test_case_id}
                          </h4>
                          {result.run_time > 0 && (
                            <span className="run-time">{result.run_time}ms</span>
                          )}
                        </div>
                        <div className="test-result-content">
                          <div className="test-detail">
                            <strong>Input:</strong>
                            <pre>{result.input}</pre>
                          </div>
                          <div className="test-detail">
                            <strong>Expected:</strong>
                            <pre>{result.expected}</pre>
                          </div>
                          <div className="test-detail">
                            <strong>Your Output:</strong>
                            <pre className={result.passed ? 'correct' : 'incorrect'}>
                              {result.actual || '(no output)'}
                            </pre>
                          </div>
                          {result.error && (
                            <div className="test-error">
                              <strong>Error:</strong>
                              <pre>{result.error}</pre>
                            </div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Run Output */}
              {runOutput && !loading && !testResults && (
                <div className="run-output">
                  <h3>💻 Output</h3>
                  {runOutput.success ? (
                    <div className="output-success">
                      <pre>{runOutput.output || '(no output)'}</pre>
                      {runOutput.run_time > 0 && (
                        <p className="run-time">Runtime: {runOutput.run_time}ms</p>
                      )}
                    </div>
                  ) : (
                    <div className="output-error">
                      <h4>❌ Runtime Error</h4>
                      <pre>{runOutput.error}</pre>
                      {runOutput.compile_output && (
                        <div className="compile-output">
                          <strong>Compile Output:</strong>
                          <pre>{runOutput.compile_output}</pre>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              )}

              {/* AI Analysis Result */}
              {result && !loading && !testResults && !runOutput && (
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

              {!result && !loading && !testResults && !runOutput && (
                <div className="empty-state">
                  <p>Run your code or submit to see results</p>
                  <div className="tips">
                    <h4>💪 Tips:</h4>
                    <ul>
                      <li>Use <strong>Run Code</strong> to test quickly</li>
                      <li>Use <strong>Submit</strong> to run all test cases</li>
                      <li>Use <strong>AI Check</strong> for code review</li>
                      <li>Check test cases tab to understand requirements</li>
                    </ul>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Floating Chat Button */}
      {questionId && (
        <button 
          className="floating-chat-btn"
          onClick={() => setShowChatDialog(!showChatDialog)}
          title="Chat with AI"
        >
          💬
        </button>
      )}

      {/* AI Chat Dialog */}
      {showChatDialog && (
        <div className="chat-dialog">
          <div className="chat-header">
            <h3>🤖 AI Assistant</h3>
            <button 
              className="close-chat-btn"
              onClick={() => setShowChatDialog(false)}
            >
              ✕
            </button>
          </div>

          <div className="chat-messages">
            {chatHistory.length === 0 ? (
              <div className="chat-welcome">
                <p>👋 Hi! I'm your AI coding assistant.</p>
                <p>Ask me anything about the problem, your code, or debugging!</p>
                <div className="chat-suggestions">
                  <button onClick={() => setChatMessage("Can you explain this problem?")}>
                    Explain the problem
                  </button>
                  <button onClick={() => setChatMessage("What's wrong with my code?")}>
                    Debug my code
                  </button>
                  <button onClick={() => setChatMessage("How can I optimize this?")}>
                    Optimization tips
                  </button>
                </div>
              </div>
            ) : (
              chatHistory.map((msg, idx) => (
                <div key={idx} className={`chat-message ${msg.role}`}>
                  <div className="message-avatar">
                    {msg.role === 'user' ? '👤' : '🤖'}
                  </div>
                  <div className="message-content">
                    {msg.content.split('\n').map((line, i) => (
                      <p key={i}>{line}</p>
                    ))}
                  </div>
                </div>
              ))
            )}
            {loadingChat && (
              <div className="chat-message assistant">
                <div className="message-avatar">🤖</div>
                <div className="message-content">
                  <p className="typing-indicator">Thinking...</p>
                </div>
              </div>
            )}
          </div>

          <div className="chat-input-area">
            <textarea
              value={chatMessage}
              onChange={(e) => setChatMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me anything about the code..."
              rows={2}
              disabled={loadingChat}
            />
            <button 
              onClick={handleSendChatMessage}
              disabled={!chatMessage.trim() || loadingChat}
              className="send-btn"
            >
              {loadingChat ? '⏳' : '📤'}
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

export default CodeCheckPage

