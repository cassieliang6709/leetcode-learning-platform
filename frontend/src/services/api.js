import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const api = {
  // Knowledge endpoints
  getKnowledgePoints: () => apiClient.get('/knowledge/points'),
  
  submitKnowledgeTest: (userId, testData) =>
    apiClient.post(`/knowledge/test/${userId}`, testData),
  
  getLearningPlan: (userId) =>
    apiClient.get(`/knowledge/plan/${userId}`),

  // Quiz endpoints
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
  checkCode: (userId, submissionData) =>
    apiClient.post(`/code/check/${userId}`, submissionData),
  
  requestCodeHint: (questionId, userId, code, hintLevel = 1) =>
    apiClient.post(`/code/hint/${questionId}/${userId}`, { code, hint_level: hintLevel }),
  
  getUserSubmissions: (userId, questionId = null) =>
    apiClient.get(`/code/submissions/${userId}`, {
      params: questionId ? { question_id: questionId } : {}
    }),
}

export default api


