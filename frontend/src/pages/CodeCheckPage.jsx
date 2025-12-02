import { useState, useEffect, useRef } from 'react'
import { api } from '../services/api'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import rehypeHighlight from 'rehype-highlight'
import Editor from '@monaco-editor/react'
import 'highlight.js/styles/github-dark.css'
import './NeetCodeStyle.css'

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
  const [activeTab, setActiveTab] = useState('testcases') // 'testcases' or 'result'
  const [aiSuggestion, setAiSuggestion] = useState(null)
  const [loadingAiSuggestion, setLoadingAiSuggestion] = useState(false)
  const [showChatDialog, setShowChatDialog] = useState(false)
  const [chatHistory, setChatHistory] = useState([])
  const [chatMessage, setChatMessage] = useState('')
  const [loadingChat, setLoadingChat] = useState(false)
  const [isChatMaximized, setIsChatMaximized] = useState(false)
  
  // NeetCode 风格新增状态
  const [descWidth, setDescWidth] = useState('40%')
  const [isConsoleOpen, setIsConsoleOpen] = useState(true)
  const [hintsExpanded, setHintsExpanded] = useState(false)
  const [isResizing, setIsResizing] = useState(false)
  const [showProblemsDrawer, setShowProblemsDrawer] = useState(false)
  
  const resizerRef = useRef(null)
  const splitPaneRef = useRef(null)

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

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
    // You can add a toast notification here
  }

  // 拖拽调整大小
  const handleResizeMouseDown = (e) => {
    e.preventDefault()
    setIsResizing(true)
    
    const startX = e.clientX
    const startWidth = splitPaneRef.current?.querySelector('.description-pane')?.offsetWidth || 0
    
    const handleMouseMove = (e) => {
      if (!splitPaneRef.current) return
      
      const containerWidth = splitPaneRef.current.offsetWidth
      const newWidth = startWidth + (e.clientX - startX)
      const minWidth = 300
      const maxWidth = containerWidth * 0.6
      
      if (newWidth >= minWidth && newWidth <= maxWidth) {
        setDescWidth(`${newWidth}px`)
      }
    }
    
    const handleMouseUp = () => {
      setIsResizing(false)
      document.removeEventListener('mousemove', handleMouseMove)
      document.removeEventListener('mouseup', handleMouseUp)
    }
    
    document.addEventListener('mousemove', handleMouseMove)
    document.addEventListener('mouseup', handleMouseUp)
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
    <div className="neetcode-layout">
      {/* ==================== 题目列表侧边抽屉 ==================== */}
      {showProblemsDrawer && (
        <>
          <div className="drawer-overlay" onClick={() => setShowProblemsDrawer(false)}></div>
          <div className="problems-drawer">
            <div className="drawer-header">
              <h3>📚 LeetCode Hot 100</h3>
              <button 
                className="close-drawer-btn"
                onClick={() => setShowProblemsDrawer(false)}
              >
                ✕
              </button>
            </div>
            <div className="drawer-content">
              {problems.map(prob => (
                <div
                  key={prob.id}
                  className={`drawer-problem-item ${questionId === prob.id ? 'active' : ''}`}
                  onClick={() => {
                    selectProblem(prob.id)
                    setShowProblemsDrawer(false)
                  }}
                >
                  <div className="drawer-problem-header">
                    <span className="drawer-problem-number">#{prob.leetcode_id}</span>
                    <span 
                      className={`difficulty-badge ${prob.difficulty}`}
                    >
                      {prob.difficulty}
                    </span>
                  </div>
                  <div className="drawer-problem-title">{prob.title}</div>
                </div>
              ))}
            </div>
          </div>
        </>
      )}

      {/* ==================== 顶部工具栏 ==================== */}
      <div className="top-toolbar">
        <button 
          className="menu-btn" 
          title="题目列表"
          onClick={() => setShowProblemsDrawer(true)}
        >
          ☰
        </button>
        
        {selectedProblem && (
          <>
            <div className="problem-title">
              <span className="problem-number">#{selectedProblem.leetcode_id}.</span>
              <h3>{selectedProblem.title}</h3>
              <span className={`difficulty-badge ${selectedProblem.difficulty}`}>
                {selectedProblem.difficulty}
              </span>
            </div>
          </>
        )}
        
        <div className="toolbar-spacer"></div>
        
        {/* 快捷按钮 */}
        <button 
          className="icon-btn hint-btn"
          onClick={() => setHintsExpanded(!hintsExpanded)}
          title="查看提示"
        >
          💡 Hints ({Object.keys(hints).length}/3)
        </button>
        
        <button 
          className="icon-btn ai-btn"
          onClick={() => setShowChatDialog(true)}
          title="AI 助手"
        >
          🤖 AI
        </button>
        
        <div className="toolbar-divider"></div>
        
        <select 
          className="language-select"
          value={language}
          onChange={(e) => handleLanguageChange(e.target.value)}
        >
          <option value="python">Python</option>
          <option value="javascript">JavaScript</option>
          <option value="java">Java</option>
          <option value="cpp">C++</option>
        </select>
        
        <button 
          className="btn-submit" 
          onClick={handleSubmit}
          disabled={loading}
        >
          {loading ? '⏳ Submitting...' : '✓ Submit'}
        </button>
      </div>

      {/* ==================== 水平分屏区域 ==================== */}
      <div className="split-pane" ref={splitPaneRef}>
        {/* 左侧：题目描述 + Hints */}
        <div className="description-pane" style={{ width: descWidth }}>
          {selectedProblem && (
            <div className="description-content">
              {/* 题目描述 */}
              <div className="problem-description">
                <div className="description-text">
                  {selectedProblem.description}
                </div>
                
                {/* Examples */}
                {selectedProblem.test_cases && selectedProblem.test_cases.length > 0 && (
                  <div className="examples-section">
                    <h4>Examples</h4>
                    {selectedProblem.test_cases.slice(0, 2).map((tc, idx) => (
                      <div key={idx} className="example-item">
                        <strong>Example {idx + 1}:</strong>
                        <div className="example-code">
                          <div>Input: {tc.input}</div>
                          <div>Output: {tc.expected}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
              
              {/* ============ Hints 区域（可折叠）============ */}
              <div className="hints-section">
                <button 
                  className="hints-header"
                  onClick={() => setHintsExpanded(!hintsExpanded)}
                >
                  <span className="hints-title">
                    💡 Hints ({Object.keys(hints).length}/3)
                  </span>
                  <span className="expand-icon">
                    {hintsExpanded ? '▼' : '▶'}
                  </span>
                </button>
                
                {hintsExpanded && (
                  <div className="hints-list">
                    {[1, 2, 3].map(level => (
                      <div key={level} className="hint-item">
                        {hints[level] ? (
                          <div className="hint-content">
                            <div className="hint-label">
                              Level {level} - {getHintTitle(level)}
                            </div>
                            <div className="hint-text">
                              {hints[level].hint_type === 'code' ? (
                                <pre className="hint-code">{hints[level].content}</pre>
                              ) : hints[level].hint_type === 'video' ? (
                                <>
                                  <p>{hints[level].content}</p>
                                  {hints[level].video_link && (
                                    <a 
                                      href={hints[level].video_link} 
                                      target="_blank" 
                                      rel="noopener noreferrer"
                                      className="hint-video-link"
                                    >
                                      🎥 Watch Video Tutorial
                                    </a>
                                  )}
                                </>
                              ) : (
                                <p>{hints[level].content}</p>
                              )}
                            </div>
                          </div>
                        ) : (
                          <button
                            className="unlock-hint-btn"
                            onClick={() => requestHint(level)}
                            disabled={level > 1 && !hints[level - 1]}
                          >
                            <span>{getHintIcon(level)}</span>
                            <span>Unlock {getHintTitle(level)}</span>
                          </button>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        {/* 拖拽分隔条 */}
        <div 
          className={`resizer ${isResizing ? 'resizing' : ''}`}
          ref={resizerRef}
          onMouseDown={handleResizeMouseDown}
        ></div>

        {/* 右侧：Monaco Editor */}
        <div className="editor-pane">
          {selectedProblem && (
            <Editor
              height="100%"
              language={language}
              value={code}
              onChange={(value) => setCode(value || '')}
              theme="vs"
              options={{
                minimap: { enabled: false },
                fontSize: 14,
                lineNumbers: 'on',
                scrollBeyondLastLine: false,
                automaticLayout: true,
                tabSize: 4,
                wordWrap: 'on',
                folding: true,
                lineNumbersMinChars: 3,
                glyphMargin: false,
                renderLineHighlight: 'all',
                scrollbar: {
                  verticalScrollbarSize: 10,
                  horizontalScrollbarSize: 10,
                },
              }}
            />
          )}
        </div>
      </div>

      {/* ==================== 底部控制台 ==================== */}
      <div className={`console-panel ${isConsoleOpen ? 'open' : 'closed'}`}>
        <div className="console-tabs">
          <button 
            className={`console-tab ${activeTab === 'testcases' ? 'active' : ''}`}
            onClick={() => setActiveTab('testcases')}
          >
            📋 Test Cases
          </button>
          <button 
            className={`console-tab ${activeTab === 'result' ? 'active' : ''}`}
            onClick={() => setActiveTab('result')}
          >
            📊 Results
          </button>
          
          <div className="console-spacer"></div>
          
          <button 
            className="toggle-console-btn"
            onClick={() => setIsConsoleOpen(!isConsoleOpen)}
            title={isConsoleOpen ? "Collapse Console" : "Expand Console"}
          >
            {isConsoleOpen ? '▼' : '▲'}
          </button>
        </div>

        {isConsoleOpen && (
          <div className="console-content">
            {activeTab === 'testcases' && selectedProblem && (
              <div className="testcases-panel">
                {selectedProblem.test_cases && selectedProblem.test_cases.length > 0 ? (
                  <>
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
                  </>
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
                  <div className="empty-state">
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
                        <div className="ai-suggestion-content markdown-content">
                          <ReactMarkdown
                            remarkPlugins={[remarkGfm]}
                            rehypePlugins={[rehypeHighlight]}
                          >
                            {aiSuggestion.suggestion}
                          </ReactMarkdown>
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

              {/* AI Analysis Result */}
              {result && !loading && !testResults && (
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

                {!result && !loading && !testResults && (
                  <div className="empty-state">
                    <p>Submit your code to see test results</p>
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>

      {/* ==================== AI 助手浮动按钮 ==================== */}
      {questionId && (
        <button 
          className="floating-ai-btn"
          onClick={() => setShowChatDialog(!showChatDialog)}
          title="AI 助手"
        >
          🤖
        </button>
      )}

      {/* AI Chat Dialog */}
      {showChatDialog && (
        <div className={`ai-chat-dialog ${isChatMaximized ? 'maximized' : ''}`}>
          <div className="chat-header">
            <h3>🤖 AI Assistant</h3>
            <div className="chat-header-actions">
              <button 
                className="chat-header-btn"
                onClick={() => setIsChatMaximized(!isChatMaximized)}
                title={isChatMaximized ? "Restore" : "Maximize"}
              >
                {isChatMaximized ? '🗗' : '🗖'}
              </button>
              <button 
                className="chat-header-btn"
                onClick={() => setShowChatDialog(false)}
              >
                ✕
              </button>
            </div>
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
                  <div className="message-content markdown-content">
                    <ReactMarkdown
                      remarkPlugins={[remarkGfm]}
                      rehypePlugins={[rehypeHighlight]}
                      components={{
                        code: ({node, inline, className, children, ...props}) => {
                          const match = /language-(\w+)/.exec(className || '')
                          const codeContent = String(children).replace(/\n$/, '')
                          
                          return !inline && match ? (
                            <div className="code-block-container">
                              <div className="code-block-header">
                                <span className="code-language">{match[1]}</span>
                                <button 
                                  className="copy-code-btn"
                                  onClick={() => copyToClipboard(codeContent)}
                                  title="Copy code"
                                >
                                  📋 Copy
                                </button>
                              </div>
                              <code className={className} {...props}>
                                {children}
                              </code>
                            </div>
                          ) : (
                            <code className={className} {...props}>
                              {children}
                            </code>
                          )
                        }
                      }}
                    >
                      {msg.content}
                    </ReactMarkdown>
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

