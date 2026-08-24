import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import rehypeHighlight from 'rehype-highlight'

const fmt = (val) => {
  if (val === null || val === undefined) return ''
  if (typeof val === 'object') return JSON.stringify(val, null, 2)
  return String(val)
}

export default function ResultsView({
  testResults,
  result,
  runMode,
  loading,
  aiSuggestion,
  loadingAiSuggestion,
  optimizationSuggestion,
  loadingOptimization,
}) {
  if (loading) {
    return <div className="empty-state"><p>⏳ Running your code...</p></div>
  }

  if (!testResults && !result) {
    return <div className="empty-state"><p>Run or submit your code to see results</p></div>
  }

  return (
    <div className="results-panel">
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

          {testResults.summary?.failed > 0 && (
            <div className="ai-suggestion-section">
              <div className="ai-suggestion-header">
                <h4>🤖 AI Suggestion</h4>
                {loadingAiSuggestion && <span className="loading-text">Analyzing...</span>}
              </div>
              {aiSuggestion?.success && (
                <div className="ai-suggestion-content markdown-content">
                  <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeHighlight]}>
                    {aiSuggestion.suggestion}
                  </ReactMarkdown>
                </div>
              )}
              {aiSuggestion && !aiSuggestion.success && (
                <div className="ai-suggestion-error"><p>{aiSuggestion.error}</p></div>
              )}
              {!aiSuggestion && !loadingAiSuggestion && (
                <div className="ai-suggestion-placeholder">
                  <p>AI is analyzing your code to provide helpful suggestions...</p>
                </div>
              )}
            </div>
          )}

          {testResults.summary?.passed === testResults.summary?.total && (
            <div className="ai-suggestion-section optimization-section">
              <div className="ai-suggestion-header">
                <h4>🚀 Optimization Suggestions</h4>
                {loadingOptimization && <span className="loading-text">Analyzing...</span>}
              </div>
              {optimizationSuggestion?.success && (
                <div className="ai-suggestion-content markdown-content">
                  <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeHighlight]}>
                    {optimizationSuggestion.suggestion}
                  </ReactMarkdown>
                </div>
              )}
              {optimizationSuggestion && !optimizationSuggestion.success && (
                <div className="ai-suggestion-error"><p>{optimizationSuggestion.error}</p></div>
              )}
              {!optimizationSuggestion && !loadingOptimization && (
                <div className="ai-suggestion-placeholder">
                  <p>AI is analyzing your code to provide optimization tips...</p>
                </div>
              )}
            </div>
          )}

          <div className="test-cases-results">
            {testResults.test_results?.map((r, index) => (
              <div key={index} className={`test-result-item ${r.passed ? 'passed' : 'failed'}`}>
                <div className="test-result-header">
                  <h4>{r.passed ? '✅' : '❌'} Test Case {r.test_case_id}</h4>
                  {r.run_time > 0 && <span className="run-time">{r.run_time}ms</span>}
                </div>
                <div className="test-result-content">
                  <div className="test-detail"><strong>Input:</strong><pre>{fmt(r.input)}</pre></div>
                  <div className="test-detail"><strong>Expected:</strong><pre>{fmt(r.expected)}</pre></div>
                  <div className="test-detail">
                    <strong>Your Output:</strong>
                    <pre className={r.passed ? 'correct' : 'incorrect'}>{r.actual || '(no output)'}</pre>
                  </div>
                  {r.error && (
                    <div className="test-error"><strong>Error:</strong><pre>{r.error}</pre></div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {result && !testResults && (
        <div className={`result-card ${result.has_errors ? 'result-error' : 'result-success'}`}>
          <div className="result-header">
            {result.has_errors ? <h4>❌ Issues Found</h4> : <h4>✅ Code Looks Good!</h4>}
          </div>
          {result.errors?.length > 0 && (
            <div className="result-section">
              <h5>Errors:</h5>
              <ul className="error-list">{result.errors.map((e, i) => <li key={i}>{e}</li>)}</ul>
            </div>
          )}
          {result.suggestions?.length > 0 && (
            <div className="result-section">
              <h5>💡 Suggestions:</h5>
              <ul className="suggestion-list">{result.suggestions.map((s, i) => <li key={i}>{s}</li>)}</ul>
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
  )
}
