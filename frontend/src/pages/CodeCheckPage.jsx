import { useState, useEffect, useRef, useCallback } from 'react'
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
  const [hints, setHints] = useState({})      // { level: { hint, ragSources, loading } }
  const [hintsUsed, setHintsUsed] = useState(0)
  const [testResults, setTestResults] = useState(null)
  const [activeTab, setActiveTab] = useState('testcases') // 'testcases' | 'result' | 'submissions'
  const [aiSuggestion, setAiSuggestion] = useState(null)
  const [loadingAiSuggestion, setLoadingAiSuggestion] = useState(false)
  const [showChatDialog, setShowChatDialog] = useState(false)
  const [chatHistory, setChatHistory] = useState([])
  const [chatMessage, setChatMessage] = useState('')
  const [loadingChat, setLoadingChat] = useState(false)
  const [isChatMaximized, setIsChatMaximized] = useState(false)
  const [isResultMaximized, setIsResultMaximized] = useState(false)
  const [optimizationSuggestion, setOptimizationSuggestion] = useState(null)
  const [loadingOptimization, setLoadingOptimization] = useState(false)

  // Submission history
  const [submissions, setSubmissions] = useState([])
  const [loadingSubmissions, setLoadingSubmissions] = useState(false)

  // Problem search (RAG C)
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState(null)
  const [searchLoading, setSearchLoading] = useState(false)

  // NeetCode style additional states
  const [descWidth, setDescWidth] = useState('40%')
  const [isConsoleOpen, setIsConsoleOpen] = useState(true)
  const [runMode, setRunMode] = useState('run') // 'run' | 'submit'
  const [hintsExpanded, setHintsExpanded] = useState(false)
  const [isResizing, setIsResizing] = useState(false)
  const [showProblemsDrawer, setShowProblemsDrawer] = useState(false)

  const resizerRef = useRef(null)
  const splitPaneRef = useRef(null)
  const searchTimeoutRef = useRef(null)

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

  const loadRecentSubmissions = async () => {
    try {
      const token = localStorage.getItem('token')
      if (!token) return
      setLoadingSubmissions(true)
      const response = await api.getRecentSubmissions(15)
      setSubmissions(response.data.submissions || [])
    } catch (error) {
      // Not authenticated or no submissions — silently ignore
    } finally {
      setLoadingSubmissions(false)
    }
  }

  const handleProblemSearch = useCallback((query) => {
    setSearchQuery(query)
    if (searchTimeoutRef.current) clearTimeout(searchTimeoutRef.current)
    if (!query.trim()) {
      setSearchResults(null)
      return
    }
    searchTimeoutRef.current = setTimeout(async () => {
      setSearchLoading(true)
      try {
        const response = await api.semanticSearchProblems(query, 8)
        setSearchResults(response.data.results)
      } catch {
        setSearchResults(null)
      } finally {
        setSearchLoading(false)
      }
    }, 400)
  }, [])

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

  const requestAIHint = async (level) => {
    if (!questionId) {
      alert('Please select a problem first')
      return
    }
    if (!code.trim()) {
      alert('Write some code first — the AI hint is tailored to your current attempt!')
      return
    }

    // Mark this level as loading
    setHints(prev => ({ ...prev, [level]: { loading: true } }))

    try {
      const currentTestResults = testResults?.test_results || null
      const response = await api.getAIHint(questionId, code, language, level, currentTestResults)
      setHints(prev => ({
        ...prev,
        [level]: {
          loading: false,
          hint: response.data.hint,
          ragSources: response.data.rag_sources || []
        }
      }))
      setHintsUsed(Math.max(hintsUsed, level))
    } catch (error) {
      console.error('Error requesting AI hint:', error)
      setHints(prev => ({ ...prev, [level]: { loading: false, error: 'Failed to get hint. Please try again.' } }))
    }
  }

  const executeCode = async (mode) => {
    if (!code.trim()) {
      alert('Please enter your code first')
      return
    }
    if (!questionId) {
      alert('Please select a problem first')
      return
    }

    setRunMode(mode)
    setLoading(true)
    setActiveTab('result')
    setTestResults(null)
    setAiSuggestion(null)
    setOptimizationSuggestion(null)

    try {
      const response = await api.submitCode(questionId, code, language)
      setTestResults(response.data)

      // Only fetch AI suggestions on Submit mode
      if (mode === 'submit') {
        const hasFailed = response.data.summary?.failed > 0
        if (hasFailed) {
          fetchAiSuggestion(response.data.test_results)
        } else {
          fetchOptimizationSuggestion()
        }
      }
    } catch (error) {
      console.error('Error running code:', error)
      alert(error.response?.data?.detail || 'Failed to run code. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleRunCode = () => executeCode('run')
  const handleSubmit  = () => executeCode('submit')

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

  const fetchOptimizationSuggestion = async () => {
    if (!questionId || !code) return
    
    setLoadingOptimization(true)
    try {
      const response = await api.getOptimizationSuggestion(
        questionId,
        code,
        language
      )
      setOptimizationSuggestion(response.data)
    } catch (error) {
      console.error('Error getting optimization suggestion:', error)
      setOptimizationSuggestion({
        success: false,
        error: 'Failed to get optimization suggestion.'
      })
    } finally {
      setLoadingOptimization(false)
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

      // Add AI response with RAG sources (RAG D)
      setChatHistory([
        ...newHistory,
        {
          role: 'assistant',
          content: response.data.response,
          ragSources: response.data.rag_sources || []
        }
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

  // Drag to resize
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
      const response = await api.checkCode({
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
      case 1: return '🤔'
      case 2: return '🧭'
      case 3: return '📝'
      default: return '❓'
    }
  }

  const getHintTitle = (level) => {
    switch (level) {
      case 1: return 'Socratic Question'
      case 2: return 'Direction Hint'
      case 3: return 'Pseudocode'
      default: return 'Hint'
    }
  }

  const getHintDesc = (level) => {
    switch (level) {
      case 1: return 'A guiding question — no spoilers'
      case 2: return 'Algorithm pattern + approach'
      case 3: return 'Pseudocode with TODO stubs'
      default: return ''
    }
  }

  const getResultClass = () => {
    if (!result) return ''
    return result.has_errors ? 'result-error' : 'result-success'
  }

  return (
    <div className="neetcode-layout">
      {/* ==================== Problem List Side Drawer ==================== */}
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
            {/* Search bar (RAG C) */}
            <div className="drawer-search">
              <input
                type="text"
                className="drawer-search-input"
                placeholder="Search problems (e.g. sliding window, two sum)..."
                value={searchQuery}
                onChange={(e) => handleProblemSearch(e.target.value)}
              />
              {searchLoading && <span className="search-loading">...</span>}
            </div>

            <div className="drawer-content">
              {/* Semantic search results */}
              {searchQuery && searchResults !== null && (
                <>
                  <div className="drawer-section-label">
                    {searchResults.length > 0
                      ? `Semantic results for "${searchQuery}"`
                      : `No results for "${searchQuery}"`}
                  </div>
                  {searchResults.map(prob => (
                    <div
                      key={prob.id}
                      className={`drawer-problem-item ${questionId === prob.id ? 'active' : ''}`}
                      onClick={() => {
                        selectProblem(prob.id)
                        setShowProblemsDrawer(false)
                        setSearchQuery('')
                        setSearchResults(null)
                      }}
                    >
                      <div className="drawer-problem-header">
                        <span className="drawer-problem-number">#{prob.leetcode_id}</span>
                        <span className={`difficulty-badge ${prob.difficulty}`}>
                          {prob.difficulty}
                        </span>
                      </div>
                      <div className="drawer-problem-title">{prob.title}</div>
                    </div>
                  ))}
                  <div className="drawer-section-label" style={{ marginTop: 12 }}>All Problems</div>
                </>
              )}

              {/* All problems list */}
              {(!searchQuery || searchResults === null) && problems.map(prob => (
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
                    <span className={`difficulty-badge ${prob.difficulty}`}>
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

      {/* ==================== Top Toolbar ==================== */}
      <div className="top-toolbar">
        <button 
          className="menu-btn" 
          title="Problem List"
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
        
        {/* Quick action buttons */}
        <button 
          className="icon-btn hint-btn"
          onClick={() => setHintsExpanded(!hintsExpanded)}
          title="View Hints"
        >
          💡 Hints ({Object.keys(hints).filter(k => hints[k]?.hint).length}/3)
        </button>
        
        <button 
          className="icon-btn ai-btn"
          onClick={() => setShowChatDialog(true)}
          title="AI Assistant"
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
          className="btn-run"
          onClick={handleRunCode}
          disabled={loading}
        >
          {loading && runMode === 'run' ? '⏳ Running...' : '▶ Run Code'}
        </button>

        <button
          className="btn-submit"
          onClick={handleSubmit}
          disabled={loading}
        >
          {loading && runMode === 'submit' ? '⏳ Submitting...' : '✓ Submit'}
        </button>
      </div>

      {/* ==================== Horizontal Split Pane ==================== */}
      <div className="split-pane" ref={splitPaneRef}>
        {/* Left: Problem Description + Hints */}
        <div className="description-pane" style={{ width: descWidth }}>
          {selectedProblem && (
            <div className="description-content">
              {/* Problem Description */}
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
              
              {/* ============ AI Hints Section (Collapsible) ============ */}
              <div className="hints-section">
                <button
                  className="hints-header"
                  onClick={() => setHintsExpanded(!hintsExpanded)}
                >
                  <span className="hints-title">
                    💡 AI Hints ({Object.keys(hints).filter(k => hints[k]?.hint).length}/3)
                  </span>
                  <span className="expand-icon">
                    {hintsExpanded ? '▼' : '▶'}
                  </span>
                </button>

                {hintsExpanded && (
                  <div className="hints-list">
                    {[1, 2, 3].map(level => {
                      const h = hints[level]
                      const prevUnlocked = level === 1 || hints[level - 1]?.hint
                      return (
                        <div key={level} className="hint-item">
                          {h?.hint ? (
                            <div className="hint-content">
                              <div className="hint-label">
                                {getHintIcon(level)} Level {level} — {getHintTitle(level)}
                              </div>
                              <div className="hint-text markdown-content">
                                <ReactMarkdown
                                  remarkPlugins={[remarkGfm]}
                                  rehypePlugins={[rehypeHighlight]}
                                >
                                  {h.hint}
                                </ReactMarkdown>
                              </div>
                              {h.ragSources && h.ragSources.length > 0 && (
                                <div className="rag-sources">
                                  <span className="rag-sources-label">Referenced:</span>
                                  {h.ragSources.map((src, i) => (
                                    <span key={i} className="rag-source-badge">📚 {src.name}</span>
                                  ))}
                                </div>
                              )}
                            </div>
                          ) : h?.loading ? (
                            <div className="hint-loading">
                              <span>🤖 AI is thinking...</span>
                            </div>
                          ) : h?.error ? (
                            <div className="hint-error">
                              <span>{h.error}</span>
                              <button className="unlock-hint-btn" onClick={() => requestAIHint(level)}>
                                Retry
                              </button>
                            </div>
                          ) : (
                            <button
                              className="unlock-hint-btn"
                              onClick={() => requestAIHint(level)}
                              disabled={!prevUnlocked}
                              title={!prevUnlocked ? 'Unlock previous hint first' : ''}
                            >
                              <span>{getHintIcon(level)}</span>
                              <span>{getHintTitle(level)}</span>
                              <span className="hint-desc">{getHintDesc(level)}</span>
                            </button>
                          )}
                        </div>
                      )
                    })}
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Drag Resizer */}
        <div 
          className={`resizer ${isResizing ? 'resizing' : ''}`}
          ref={resizerRef}
          onMouseDown={handleResizeMouseDown}
        ></div>

        {/* Right: Monaco Editor */}
        <div className="editor-pane">
          {selectedProblem && (
            <Editor
              height="100%"
              language={language}
              value={code}
              onChange={(value) => setCode(value || '')}
              theme="light"
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

      {/* ==================== Bottom Console ==================== */}
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
          <button
            className={`console-tab ${activeTab === 'submissions' ? 'active' : ''}`}
            onClick={() => { setActiveTab('submissions'); loadRecentSubmissions() }}
          >
            📜 My Submissions {submissions.length > 0 ? `(${submissions.length})` : ''}
          </button>

          <div className="console-spacer"></div>
          
          {activeTab === 'result' && (testResults || result) && (
            <button 
              className="maximize-result-btn"
              onClick={() => setIsResultMaximized(true)}
              title="Maximize results"
            >
              🔍
            </button>
          )}
          
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

                {/* Test Results from Run/Submit */}
                {testResults && !loading && (
                  <div className="test-results">
                    {runMode === 'run' ? (
                      <div className="result-badge-run">
                        <h3>▶ Code Run</h3>
                        <p>
                          {testResults.summary?.passed} / {testResults.summary?.total} test cases passed
                          ({testResults.summary?.pass_rate?.toFixed(1)}%)
                        </p>
                      </div>
                    ) : (
                      <div className={`result-summary ${testResults.summary?.passed === testResults.summary?.total ? 'success' : 'error'}`}>
                        <h3>
                          {testResults.summary?.passed === testResults.summary?.total ? '✅ Accepted' : '❌ Wrong Answer'}
                        </h3>
                        <p>
                          {testResults.summary?.passed} / {testResults.summary?.total} test cases passed
                          ({testResults.summary?.pass_rate?.toFixed(1)}%)
                        </p>
                      </div>
                    )}

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

                  {/* Optimization Suggestions for Passed Tests */}
                  {testResults.summary?.passed === testResults.summary?.total && (
                    <div className="ai-suggestion-section optimization-section">
                      <div className="ai-suggestion-header">
                        <h4>🚀 Optimization Suggestions</h4>
                        {loadingOptimization && <span className="loading-text">Analyzing...</span>}
                      </div>
                      
                      {optimizationSuggestion && optimizationSuggestion.success && (
                        <div className="ai-suggestion-content markdown-content">
                          <ReactMarkdown
                            remarkPlugins={[remarkGfm]}
                            rehypePlugins={[rehypeHighlight]}
                          >
                            {optimizationSuggestion.suggestion}
                          </ReactMarkdown>
                        </div>
                      )}
                      
                      {optimizationSuggestion && !optimizationSuggestion.success && (
                        <div className="ai-suggestion-error">
                          <p>{optimizationSuggestion.error}</p>
                        </div>
                      )}
                      
                      {!optimizationSuggestion && !loadingOptimization && (
                        <div className="ai-suggestion-placeholder">
                          <p>AI is analyzing your code to provide optimization tips...</p>
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
                    <p>Run or submit your code to see results</p>
                  </div>
                )}
              </div>
            )}

            {/* ==================== Submissions Tab ==================== */}
            {activeTab === 'submissions' && (
              <div className="submissions-panel">
                {loadingSubmissions ? (
                  <div className="empty-state"><p>Loading submissions...</p></div>
                ) : submissions.length === 0 ? (
                  <div className="empty-state">
                    <p>No submissions yet. Submit your code to track progress!</p>
                  </div>
                ) : (
                  <div className="submissions-list">
                    {submissions.map((sub, idx) => {
                      const passed = sub.passed
                      const prob = problems.find(p => p.id === sub.question_id)
                      return (
                        <div
                          key={sub.id || idx}
                          className={`submission-item ${passed ? 'passed' : 'failed'}`}
                          onClick={() => sub.question_id && selectProblem(sub.question_id)}
                          style={{ cursor: 'pointer' }}
                        >
                          <div className="submission-header">
                            <span className={`submission-status ${passed ? 'accepted' : 'wrong'}`}>
                              {passed ? '✅ Accepted' : '❌ Wrong Answer'}
                            </span>
                            <span className="submission-lang">{sub.language}</span>
                            <span className="submission-time">
                              {sub.created_at
                                ? new Date(sub.created_at).toLocaleDateString()
                                : ''}
                            </span>
                          </div>
                          {prob && (
                            <div className="submission-problem">
                              #{prob.leetcode_id} {prob.title}
                            </div>
                          )}
                        </div>
                      )
                    })}
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>

      {/* ==================== AI Assistant Floating Button ==================== */}
      {questionId && (
        <button 
          className="floating-ai-btn"
          onClick={() => setShowChatDialog(!showChatDialog)}
          title="AI Assistant"
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
                    {/* RAG D: show source badges */}
                    {msg.role === 'assistant' && msg.ragSources && msg.ragSources.length > 0 && (
                      <div className="rag-sources">
                        <span className="rag-sources-label">Referenced:</span>
                        {msg.ragSources.map((src, i) => (
                          <span key={i} className="rag-source-badge">
                            📚 {src.name}
                          </span>
                        ))}
                      </div>
                    )}
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

      {/* ==================== Maximized Result Window ==================== */}
      {isResultMaximized && (
        <div className="result-maximized-overlay" onClick={() => setIsResultMaximized(false)}>
          <div className="result-maximized-dialog" onClick={(e) => e.stopPropagation()}>
            <div className="result-maximized-header">
              <h3>📊 Test Results</h3>
              <button 
                className="close-maximized-btn"
                onClick={() => setIsResultMaximized(false)}
                title="Close"
              >
                ✕
              </button>
            </div>
            
            <div className="result-maximized-content">
              {/* Test Results from Run/Submit */}
              {testResults && (
                <div className="test-results">
                  {runMode === 'run' ? (
                    <div className="result-badge-run">
                      <h3>▶ Code Run</h3>
                      <p>
                        {testResults.summary?.passed} / {testResults.summary?.total} test cases passed
                        ({testResults.summary?.pass_rate?.toFixed(1)}%)
                      </p>
                    </div>
                  ) : (
                    <div className={`result-summary ${testResults.summary?.passed === testResults.summary?.total ? 'success' : 'error'}`}>
                      <h3>
                        {testResults.summary?.passed === testResults.summary?.total ? '✅ Accepted' : '❌ Wrong Answer'}
                      </h3>
                      <p>
                        {testResults.summary?.passed} / {testResults.summary?.total} test cases passed
                        ({testResults.summary?.pass_rate?.toFixed(1)}%)
                      </p>
                    </div>
                  )}

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

                  {/* Optimization Suggestions for Passed Tests */}
                  {testResults.summary?.passed === testResults.summary?.total && (
                    <div className="ai-suggestion-section optimization-section">
                      <div className="ai-suggestion-header">
                        <h4>🚀 Optimization Suggestions</h4>
                        {loadingOptimization && <span className="loading-text">Analyzing...</span>}
                      </div>
                      
                      {optimizationSuggestion && optimizationSuggestion.success && (
                        <div className="ai-suggestion-content markdown-content">
                          <ReactMarkdown
                            remarkPlugins={[remarkGfm]}
                            rehypePlugins={[rehypeHighlight]}
                          >
                            {optimizationSuggestion.suggestion}
                          </ReactMarkdown>
                        </div>
                      )}
                      
                      {optimizationSuggestion && !optimizationSuggestion.success && (
                        <div className="ai-suggestion-error">
                          <p>{optimizationSuggestion.error}</p>
                        </div>
                      )}
                      
                      {!optimizationSuggestion && !loadingOptimization && (
                        <div className="ai-suggestion-placeholder">
                          <p>AI is analyzing your code to provide optimization tips...</p>
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
              {result && !testResults && (
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
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default CodeCheckPage

