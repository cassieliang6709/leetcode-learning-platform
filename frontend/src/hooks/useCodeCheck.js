import { useReducer, useRef, useCallback, useEffect } from 'react'
import { api } from '../services/api'

const initialState = {
  code: '',
  language: 'python',
  questionId: null,
  selectedProblem: null,
  problems: [],
  result: null,
  loading: false,
  notes: '',
  hints: {},
  hintsUsed: 0,
  testResults: null,
  activeTab: 'testcases',
  aiSuggestion: null,
  loadingAiSuggestion: false,
  showChatDialog: false,
  chatHistory: [],
  chatMessage: '',
  loadingChat: false,
  isChatMaximized: false,
  isResultMaximized: false,
  optimizationSuggestion: null,
  loadingOptimization: false,
  submissions: [],
  loadingSubmissions: false,
  searchQuery: '',
  searchResults: null,
  searchLoading: false,
  descWidth: '40%',
  isConsoleOpen: true,
  runMode: 'run',
  hintsExpanded: false,
  isResizing: false,
  showProblemsDrawer: false,
}

function reducer(state, action) {
  if (action.type === 'PATCH') return { ...state, ...action.payload }
  return state
}

export function useCodeCheck() {
  const [state, dispatch] = useReducer(reducer, initialState)
  const patch = useCallback((payload) => dispatch({ type: 'PATCH', payload }), [])

  const searchTimeoutRef = useRef(null)
  const splitPaneRef = useRef(null)
  const resizerRef = useRef(null)

  useEffect(() => {
    loadProblems()
  }, [])

  const loadProblems = async () => {
    try {
      const response = await api.getProblems()
      patch({ problems: response.data.problems })
      if (response.data.problems.length > 0) {
        selectProblem(response.data.problems[0].id)
      }
    } catch (error) {
      console.error('Error loading problems:', error)
    }
  }

  const loadRecentSubmissions = async () => {
    patch({ loadingSubmissions: true })
    try {
      const response = await api.getRecentSubmissions(15)
      patch({ submissions: response.data.submissions || [] })
    } catch {
      // Not authenticated or no submissions
    } finally {
      patch({ loadingSubmissions: false })
    }
  }

  const handleProblemSearch = useCallback((query) => {
    patch({ searchQuery: query })
    if (searchTimeoutRef.current) clearTimeout(searchTimeoutRef.current)
    if (!query.trim()) {
      patch({ searchResults: null })
      return
    }
    searchTimeoutRef.current = setTimeout(async () => {
      patch({ searchLoading: true })
      try {
        const response = await api.semanticSearchProblems(query, 8)
        patch({ searchResults: response.data.results })
      } catch {
        patch({ searchResults: null })
      } finally {
        patch({ searchLoading: false })
      }
    }, 400)
  }, [])

  const selectProblem = async (problemId) => {
    try {
      const response = await api.getProblemDetail(problemId)
      patch({
        selectedProblem: response.data,
        questionId: problemId,
        hints: {},
        hintsUsed: 0,
        result: null,
        testResults: null,
        aiSuggestion: null,
        chatHistory: [],
      })
      loadStarterCode(problemId, state.language)
    } catch (error) {
      console.error('Error loading problem details:', error)
    }
  }

  const loadStarterCode = async (problemId, lang) => {
    try {
      const response = await api.getStarterCode(problemId, lang)
      patch({ code: response.data.code || '' })
    } catch {
      patch({ code: '' })
    }
  }

  const handleLanguageChange = (newLanguage) => {
    patch({ language: newLanguage })
    if (state.questionId) {
      loadStarterCode(state.questionId, newLanguage)
    }
  }

  const requestAIHint = async (level) => {
    if (!state.questionId) { alert('Please select a problem first'); return }
    if (!state.code.trim()) { alert('Write some code first — the AI hint is tailored to your current attempt!'); return }

    patch({ hints: { ...state.hints, [level]: { loading: true } } })
    try {
      const currentTestResults = state.testResults?.test_results || null
      const response = await api.getAIHint(state.questionId, state.code, state.language, level, currentTestResults)
      patch({
        hints: {
          ...state.hints,
          [level]: { loading: false, hint: response.data.hint, ragSources: response.data.rag_sources || [] },
        },
        hintsUsed: Math.max(state.hintsUsed, level),
      })
    } catch {
      patch({ hints: { ...state.hints, [level]: { loading: false, error: 'Failed to get hint. Please try again.' } } })
    }
  }

  const fetchAiSuggestion = async (testResultsData) => {
    if (!state.questionId || !state.code) return
    patch({ loadingAiSuggestion: true })
    try {
      const response = await api.getFailureSuggestion(state.questionId, state.code, state.language, testResultsData)
      patch({ aiSuggestion: response.data })
    } catch {
      patch({ aiSuggestion: { success: false, error: 'Failed to get AI suggestion. Please try the chat feature.' } })
    } finally {
      patch({ loadingAiSuggestion: false })
    }
  }

  const fetchOptimizationSuggestion = async () => {
    if (!state.questionId || !state.code) return
    patch({ loadingOptimization: true })
    try {
      const response = await api.getOptimizationSuggestion(state.questionId, state.code, state.language)
      patch({ optimizationSuggestion: response.data })
    } catch {
      patch({ optimizationSuggestion: { success: false, error: 'Failed to get optimization suggestion.' } })
    } finally {
      patch({ loadingOptimization: false })
    }
  }

  const executeCode = async (mode) => {
    if (!state.code.trim()) { alert('Please enter your code first'); return }
    if (!state.questionId) { alert('Please select a problem first'); return }

    patch({ runMode: mode, loading: true, activeTab: 'result', testResults: null, aiSuggestion: null, optimizationSuggestion: null })
    try {
      const response = await api.submitCode(state.questionId, state.code, state.language)
      patch({ testResults: response.data })
      if (mode === 'submit') {
        if (response.data.summary?.failed > 0) {
          fetchAiSuggestion(response.data.test_results)
        } else {
          fetchOptimizationSuggestion()
        }
      }
    } catch (error) {
      alert(error.response?.data?.detail || 'Failed to run code. Please try again.')
    } finally {
      patch({ loading: false })
    }
  }

  const handleSendChatMessage = async () => {
    if (!state.chatMessage.trim()) return
    const userMessage = state.chatMessage.trim()
    const newHistory = [...state.chatHistory, { role: 'user', content: userMessage }]
    patch({ chatMessage: '', chatHistory: newHistory, loadingChat: true })
    try {
      const response = await api.chatWithAI(
        state.questionId,
        state.code,
        state.language,
        userMessage,
        state.chatHistory.length > 0 ? state.chatHistory : null,
      )
      patch({
        chatHistory: [
          ...newHistory,
          { role: 'assistant', content: response.data.response, ragSources: response.data.rag_sources || [] },
        ],
      })
    } catch {
      patch({
        chatHistory: [...newHistory, { role: 'assistant', content: 'Sorry, I encountered an error. Please try again.' }],
      })
    } finally {
      patch({ loadingChat: false })
    }
  }

  const handleResizeMouseDown = (e) => {
    e.preventDefault()
    patch({ isResizing: true })
    const startX = e.clientX
    const startWidth = splitPaneRef.current?.querySelector('.description-pane')?.offsetWidth || 0

    const handleMouseMove = (e) => {
      if (!splitPaneRef.current) return
      const containerWidth = splitPaneRef.current.offsetWidth
      const newWidth = startWidth + (e.clientX - startX)
      const minWidth = 300
      const maxWidth = containerWidth * 0.6
      if (newWidth >= minWidth && newWidth <= maxWidth) {
        patch({ descWidth: `${newWidth}px` })
      }
    }
    const handleMouseUp = () => {
      patch({ isResizing: false })
      document.removeEventListener('mousemove', handleMouseMove)
      document.removeEventListener('mouseup', handleMouseUp)
    }
    document.addEventListener('mousemove', handleMouseMove)
    document.addEventListener('mouseup', handleMouseUp)
  }

  return {
    state,
    patch,
    splitPaneRef,
    resizerRef,
    loadProblems,
    loadRecentSubmissions,
    handleProblemSearch,
    selectProblem,
    handleLanguageChange,
    requestAIHint,
    executeCode,
    handleSendChatMessage,
    handleResizeMouseDown,
  }
}
