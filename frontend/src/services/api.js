import axios from 'axios'

// Use environment variable for production, fallback to localhost for development
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add token to all requests
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle auth errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      const url = error.config?.url || ''
      // Don't redirect on auth endpoints — let the form show the error message
      const isAuthEndpoint = url.includes('/auth/login') || url.includes('/auth/register')
      // Don't redirect for optional-auth endpoints — just let the caller handle 401
      const isOptionalAuth = url.includes('/submissions/me/recent')
      if (!isAuthEndpoint && !isOptionalAuth) {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

export const api = {
  // Knowledge endpoints
  getKnowledgePoints: () => apiClient.get('/knowledge/points'),
  
  getKnowledgePointDetail: (pointId) =>
    apiClient.get(`/knowledge/points/${pointId}`),
  
  getKnowledgePointQuestions: (pointId) =>
    apiClient.get(`/knowledge/points/${pointId}/questions`),
  
  submitKnowledgeTest: (userId, testData) =>
    apiClient.post(`/knowledge/test/${userId}`, testData),
  
  getLearningPlan: (userId) =>
    apiClient.get(`/knowledge/plan/${userId}`),

  // Quiz endpoints
  getDailyQuiz: (userId) =>
    apiClient.get(`/quiz/daily/${userId}`),
  
  submitAnswer: (userId, questionId, selectedOption) =>
    apiClient.post(`/quiz/answer/${userId}`, {
      question_id: questionId,
      selected_option: selectedOption
    }),
  
  getDailyProgress: (userId) =>
    apiClient.get(`/quiz/progress/${userId}`),
  
  getQuizzesByKnowledge: (knowledgePointId) =>
    apiClient.get(`/quiz/by-knowledge/${knowledgePointId}`),
  
  getQuizDetail: (questionId) =>
    apiClient.get(`/quiz/${questionId}`),
  
  submitQuizAttempt: (questionId, userId, isCorrect, hintsUsed = 0) =>
    apiClient.post(`/quiz/${questionId}/attempt/${userId}`, null, {
      params: { is_correct: isCorrect, hints_used: hintsUsed }
    }),
  
  getHint: (questionId, level) =>
    apiClient.get(`/quiz/${questionId}/hint/${level}`),

  // Code check endpoints
  checkCode: (submissionData) =>
    apiClient.post('/code/check', submissionData),
  
  getProblems: (category = null, difficulty = null) =>
    apiClient.get('/code/problems', {
      params: { category, difficulty }
    }),
  
  getProblemDetail: (questionId) =>
    apiClient.get(`/code/problem/${questionId}`),
  
  requestCodeHint: (questionId, hintLevel) =>
    apiClient.get(`/code/hint/${questionId}/${hintLevel}`),
  
  getUserSubmissions: (userId, questionId = null) =>
    apiClient.get(`/code/submissions/${userId}`, {
      params: questionId ? { question_id: questionId } : {}
    }),

  // Code execution endpoints
  submitCode: (questionId, code, language) =>
    apiClient.post(`/execution/submit/${questionId}`, {
      code,
      language
    }),
  
  getStarterCode: (questionId, language = 'python') =>
    apiClient.get(`/execution/question/${questionId}/starter-code`, {
      params: { language }
    }),
  
  getSupportedLanguages: () =>
    apiClient.get('/execution/supported-languages'),

  // AI Assistant endpoints
  getFailureSuggestion: (questionId, code, language, testResults) =>
    apiClient.post('/ai/suggestion/failure', {
      question_id: questionId,
      code,
      language,
      test_results: testResults
    }),
  
  chatWithAI: (questionId, code, language, message, chatHistory = null) =>
    apiClient.post('/ai/chat', {
      question_id: questionId,
      code,
      language,
      message,
      chat_history: chatHistory
    }),
  
  getAIHint: (questionId, code, language, hintLevel, testResults = null) =>
    apiClient.post('/ai/hint', {
      question_id: questionId,
      code,
      language,
      hint_level: hintLevel,
      test_results: testResults
    }),

  getOptimizationSuggestion: (questionId, code, language) =>
    apiClient.post('/ai/suggestion/optimization', {
      question_id: questionId,
      code,
      language
    }),

  // Submission history
  getRecentSubmissions: (limit = 10) =>
    apiClient.get('/execution/submissions/me/recent', { params: { limit } }),

  // Semantic problem search (RAG C)
  semanticSearchProblems: (q, topK = 8) =>
    apiClient.get('/rag/problems/search', { params: { q, top_k: topK } }),

  // Auth endpoints
  login: (username, password) =>
    apiClient.post('/auth/login', { username, password }),
  
  register: (username, email, password) =>
    apiClient.post('/auth/register', { username, email, password }),
  
  getCurrentUser: () =>
    apiClient.get('/auth/me'),
}

export default api


