export default function ProblemDrawer({
  problems,
  questionId,
  searchQuery,
  searchResults,
  searchLoading,
  onSearch,
  onSelect,
  onClose,
}) {
  return (
    <>
      <div className="drawer-overlay" onClick={onClose} />
      <div className="problems-drawer">
        <div className="drawer-header">
          <h3>📚 LeetCode Hot 100</h3>
          <button className="close-drawer-btn" onClick={onClose}>✕</button>
        </div>

        <div className="drawer-search">
          <input
            type="text"
            className="drawer-search-input"
            placeholder="Search problems (e.g. sliding window, two sum)..."
            value={searchQuery}
            onChange={(e) => onSearch(e.target.value)}
          />
          {searchLoading && <span className="search-loading">...</span>}
        </div>

        <div className="drawer-content">
          {searchQuery && searchResults !== null && (
            <>
              <div className="drawer-section-label">
                {searchResults.length > 0
                  ? `Semantic results for "${searchQuery}"`
                  : `No results for "${searchQuery}"`}
              </div>
              {searchResults.map(prob => (
                <ProblemItem
                  key={prob.id}
                  prob={prob}
                  active={questionId === prob.id}
                  onClick={() => onSelect(prob.id)}
                />
              ))}
              <div className="drawer-section-label" style={{ marginTop: 12 }}>All Problems</div>
            </>
          )}

          {(!searchQuery || searchResults === null) && problems.map(prob => (
            <ProblemItem
              key={prob.id}
              prob={prob}
              active={questionId === prob.id}
              onClick={() => onSelect(prob.id)}
            />
          ))}
        </div>
      </div>
    </>
  )
}

function ProblemItem({ prob, active, onClick }) {
  return (
    <div
      className={`drawer-problem-item ${active ? 'active' : ''}`}
      onClick={onClick}
    >
      <div className="drawer-problem-header">
        <span className="drawer-problem-number">#{prob.leetcode_id}</span>
        <span className={`difficulty-badge ${prob.difficulty}`}>{prob.difficulty}</span>
      </div>
      <div className="drawer-problem-title">{prob.title}</div>
    </div>
  )
}
