import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import rehypeHighlight from 'rehype-highlight'

const fmt = (val) => {
  if (val === null || val === undefined) return ''
  if (typeof val === 'object') return JSON.stringify(val, null, 2)
  return String(val)
}

const HINT_META = {
  1: { icon: '🤔', title: 'Socratic Question', desc: 'A guiding question — no spoilers' },
  2: { icon: '🧭', title: 'Direction Hint',    desc: 'Algorithm pattern + approach' },
  3: { icon: '📝', title: 'Pseudocode',         desc: 'Pseudocode with TODO stubs' },
}

export default function ProblemPanel({ selectedProblem, hints, hintsExpanded, onToggleHints, onRequestHint, style }) {
  if (!selectedProblem) return null

  return (
    <div className="description-pane" style={style}>
      <div className="description-content">
        <div className="problem-description">
          <div className="description-text">{selectedProblem.description}</div>

          {selectedProblem.test_cases?.length > 0 && (
            <div className="examples-section">
              <h4>Examples</h4>
              {selectedProblem.test_cases.slice(0, 2).map((tc, idx) => (
                <div key={idx} className="example-item">
                  <strong>Example {idx + 1}:</strong>
                  <div className="example-code">
                    <div>Input: {fmt(tc.input)}</div>
                    <div>Output: {fmt(tc.expected)}</div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="hints-section">
          <button className="hints-header" onClick={onToggleHints}>
            <span className="hints-title">
              💡 AI Hints ({Object.keys(hints).filter(k => hints[k]?.hint).length}/3)
            </span>
            <span className="expand-icon">{hintsExpanded ? '▼' : '▶'}</span>
          </button>

          {hintsExpanded && (
            <div className="hints-list">
              {[1, 2, 3].map(level => {
                const h = hints[level]
                const meta = HINT_META[level]
                const prevUnlocked = level === 1 || hints[level - 1]?.hint
                return (
                  <div key={level} className="hint-item">
                    {h?.hint ? (
                      <div className="hint-content">
                        <div className="hint-label">{meta.icon} Level {level} — {meta.title}</div>
                        <div className="hint-text markdown-content">
                          <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeHighlight]}>
                            {h.hint}
                          </ReactMarkdown>
                        </div>
                        {h.ragSources?.length > 0 && (
                          <div className="rag-sources">
                            <span className="rag-sources-label">Referenced:</span>
                            {h.ragSources.map((src, i) => (
                              <span key={i} className="rag-source-badge">📚 {src.name}</span>
                            ))}
                          </div>
                        )}
                      </div>
                    ) : h?.loading ? (
                      <div className="hint-loading"><span>🤖 AI is thinking...</span></div>
                    ) : h?.error ? (
                      <div className="hint-error">
                        <span>{h.error}</span>
                        <button className="unlock-hint-btn" onClick={() => onRequestHint(level)}>Retry</button>
                      </div>
                    ) : (
                      <button
                        className="unlock-hint-btn"
                        onClick={() => onRequestHint(level)}
                        disabled={!prevUnlocked}
                        title={!prevUnlocked ? 'Unlock previous hint first' : ''}
                      >
                        <span>{meta.icon}</span>
                        <span>{meta.title}</span>
                        <span className="hint-desc">{meta.desc}</span>
                      </button>
                    )}
                  </div>
                )
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
