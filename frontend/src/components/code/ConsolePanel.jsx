import ResultsView from './ResultsView'

const fmt = (val) => {
  if (val === null || val === undefined) return ''
  if (typeof val === 'object') return JSON.stringify(val, null, 2)
  return String(val)
}

export default function ConsolePanel({
  isConsoleOpen,
  activeTab,
  selectedProblem,
  testResults,
  result,
  runMode,
  loading,
  aiSuggestion,
  loadingAiSuggestion,
  optimizationSuggestion,
  loadingOptimization,
  submissions,
  loadingSubmissions,
  problems,
  isResultMaximized,
  onTabChange,
  onToggleConsole,
  onMaximizeResult,
  onSelectProblem,
}) {
  return (
    <div className={`console-panel ${isConsoleOpen ? 'open' : 'closed'}`}>
      <div className="console-tabs">
        <button
          className={`console-tab ${activeTab === 'testcases' ? 'active' : ''}`}
          onClick={() => onTabChange('testcases')}
        >
          📋 Test Cases
        </button>
        <button
          className={`console-tab ${activeTab === 'result' ? 'active' : ''}`}
          onClick={() => onTabChange('result')}
        >
          📊 Results
        </button>
        <button
          className={`console-tab ${activeTab === 'submissions' ? 'active' : ''}`}
          onClick={() => onTabChange('submissions')}
        >
          📜 My Submissions {submissions.length > 0 ? `(${submissions.length})` : ''}
        </button>

        <div className="console-spacer" />

        {activeTab === 'result' && (testResults || result) && (
          <button className="maximize-result-btn" onClick={onMaximizeResult} title="Maximize results">
            🔍
          </button>
        )}

        <button
          className="toggle-console-btn"
          onClick={onToggleConsole}
          title={isConsoleOpen ? 'Collapse Console' : 'Expand Console'}
        >
          {isConsoleOpen ? '▼' : '▲'}
        </button>
      </div>

      {isConsoleOpen && (
        <div className="console-content">
          {activeTab === 'testcases' && selectedProblem && (
            <div className="testcases-panel">
              {selectedProblem.test_cases?.length > 0 ? (
                selectedProblem.test_cases.map((tc, index) => (
                  <div key={index} className="test-case-item">
                    <h4>Test Case {index + 1}</h4>
                    <div className="test-case-content">
                      <div className="test-input"><strong>Input:</strong><pre>{fmt(tc.input)}</pre></div>
                      <div className="test-expected"><strong>Expected Output:</strong><pre>{fmt(tc.expected)}</pre></div>
                    </div>
                  </div>
                ))
              ) : (
                <div className="empty-state"><p>No test cases available for this problem</p></div>
              )}
            </div>
          )}

          {activeTab === 'result' && (
            <ResultsView
              testResults={testResults}
              result={result}
              runMode={runMode}
              loading={loading}
              aiSuggestion={aiSuggestion}
              loadingAiSuggestion={loadingAiSuggestion}
              optimizationSuggestion={optimizationSuggestion}
              loadingOptimization={loadingOptimization}
            />
          )}

          {activeTab === 'submissions' && (
            <div className="submissions-panel">
              {loadingSubmissions ? (
                <div className="empty-state"><p>Loading submissions...</p></div>
              ) : submissions.length === 0 ? (
                <div className="empty-state"><p>No submissions yet. Submit your code to track progress!</p></div>
              ) : (
                <div className="submissions-list">
                  {submissions.map((sub, idx) => {
                    const passed = sub.passed
                    const prob = problems.find(p => p.id === sub.question_id)
                    return (
                      <div
                        key={sub.id || idx}
                        className={`submission-item ${passed ? 'passed' : 'failed'}`}
                        onClick={() => sub.question_id && onSelectProblem(sub.question_id)}
                        style={{ cursor: 'pointer' }}
                      >
                        <div className="submission-header">
                          <span className={`submission-status ${passed ? 'accepted' : 'wrong'}`}>
                            {passed ? '✅ Accepted' : '❌ Wrong Answer'}
                          </span>
                          <span className="submission-lang">{sub.language}</span>
                          <span className="submission-time">
                            {sub.created_at ? new Date(sub.created_at).toLocaleDateString() : ''}
                          </span>
                        </div>
                        {prob && <div className="submission-problem">#{prob.leetcode_id} {prob.title}</div>}
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
  )
}
