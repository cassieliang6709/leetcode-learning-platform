import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Send httpOnly auth cookie with every request
})

// Track whether a token refresh is already in-flight to avoid parallel refresh storms
let _refreshPromise = null

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    const url = originalRequest?.url || ''
    const isAuthEndpoint = url.includes('/auth/')

    // On 401 for non-auth endpoints: attempt one silent token refresh
    if (error.response?.status === 401 && !isAuthEndpoint && !originalRequest._retried) {
      originalRequest._retried = true

      try {
        if (!_refreshPromise) {
          _refreshPromise = apiClient.post('/auth/refresh').finally(() => {
            _refreshPromise = null
          })
        }
        await _refreshPromise
        // Retry the original request — the new access_token cookie is now set
        return apiClient(originalRequest)
      } catch {
        // Refresh itself failed (expired / revoked) — clear user and dispatch event
        // so AuthContext can update state without a hard page reload
        localStorage.removeItem('user')
        window.dispatchEvent(new CustomEvent('auth:expired'))
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

  submitKnowledgeTest: (testData) =>
    apiClient.post('/knowledge/test', testData),

  getLearningPlan: () =>
    apiClient.get('/knowledge/plan'),

  // Quiz endpoints
  getDailyQuiz: () =>
    apiClient.get('/quiz/daily'),

  submitAnswer: (questionId, selectedOption) =>
    apiClient.post('/quiz/answer', {
      question_id: questionId,
      selected_option: selectedOption,
    }),

  getDailyProgress: () =>
    apiClient.get('/quiz/progress'),

  getQuizzesByKnowledge: (knowledgePointId) =>
    apiClient.get(`/quiz/by-knowledge/${knowledgePointId}`),

  getQuizDetail: (questionId) =>
    apiClient.get(`/quiz/${questionId}`),

  submitQuizAttempt: (questionId, isCorrect, hintsUsed = 0) =>
    apiClient.post(`/quiz/${questionId}/attempt`, null, {
      params: { is_correct: isCorrect, hints_used: hintsUsed },
    }),

  getHint: (questionId, level) =>
    apiClient.get(`/quiz/${questionId}/hint/${level}`),

  // Code check endpoints
  checkCode: (submissionData) =>
    apiClient.post('/code/check', submissionData),

  getProblems: (category = null, difficulty = null) =>
    apiClient.get('/code/problems', {
      params: { category, difficulty },
    }),

  getProblemDetail: (questionId) =>
    apiClient.get(`/code/problem/${questionId}`),

  requestCodeHint: (questionId, hintLevel) =>
    apiClient.get(`/code/hint/${questionId}/${hintLevel}`),

  getUserSubmissions: (questionId = null) =>
    apiClient.get('/code/submissions/me', {
      params: questionId ? { question_id: questionId } : {},
    }),

  // Code execution endpoints
  submitCode: (questionId, code, language) =>
    apiClient.post(`/execution/submit/${questionId}`, {
      code,
      language,
    }),

  getStarterCode: (questionId, language = 'python') =>
    apiClient.get(`/execution/question/${questionId}/starter-code`, {
      params: { language },
    }),

  getSupportedLanguages: () =>
    apiClient.get('/execution/supported-languages'),

  // AI Assistant endpoints
  getFailureSuggestion: (questionId, code, language, testResults) =>
    apiClient.post('/ai/suggestion/failure', {
      question_id: questionId,
      code,
      language,
      test_results: testResults,
    }),

  chatWithAI: (questionId, code, language, message, chatHistory = null) =>
    apiClient.post('/ai/chat', {
      question_id: questionId,
      code,
      language,
      message,
      chat_history: chatHistory,
    }),

  getAIHint: (questionId, code, language, hintLevel, testResults = null) =>
    apiClient.post('/ai/hint', {
      question_id: questionId,
      code,
      language,
      hint_level: hintLevel,
      test_results: testResults,
    }),

  getOptimizationSuggestion: (questionId, code, language) =>
    apiClient.post('/ai/suggestion/optimization', {
      question_id: questionId,
      code,
      language,
    }),

  // Submission history
  getRecentSubmissions: (limit = 10) =>
    apiClient.get('/execution/submissions/me/recent', { params: { limit } }),

  // Semantic problem search (RAG)
  semanticSearchProblems: (q, topK = 8) =>
    apiClient.get('/rag/problems/search', { params: { q, top_k: topK } }),

  // Auth endpoints
  login: (username, password) =>
    apiClient.post('/auth/login', { username, password }),

  register: (username, email, password) =>
    apiClient.post('/auth/register', { username, email, password }),

  refresh: () =>
    apiClient.post('/auth/refresh'),

  logout: () =>
    apiClient.post('/auth/logout'),

  getCurrentUser: () =>
    apiClient.get('/auth/me'),
}

export default api
