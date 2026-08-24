import 'highlight.js/styles/github-dark.css'
import './NeetCodeStyle.css'

import { useCodeCheck } from '../hooks/useCodeCheck'
import ProblemDrawer from '../components/code/ProblemDrawer'
import ProblemPanel from '../components/code/ProblemPanel'
import EditorPanel from '../components/code/EditorPanel'
import ConsolePanel from '../components/code/ConsolePanel'
import AIChatDialog from '../components/code/AIChatDialog'
import ResultsView from '../components/code/ResultsView'

const CodeCheckPage = () => {
  const {
    state,
    patch,
    splitPaneRef,
    resizerRef,
    loadRecentSubmissions,
    handleProblemSearch,
    selectProblem,
    handleLanguageChange,
    requestAIHint,
    executeCode,
    handleSendChatMessage,
    handleResizeMouseDown,
  } = useCodeCheck()

  const {
    code, language, questionId, selectedProblem, problems,
    result, loading, hints, hintsUsed, testResults, activeTab,
    aiSuggestion, loadingAiSuggestion, showChatDialog, chatHistory,
    chatMessage, loadingChat, isChatMaximized, isResultMaximized,
    optimizationSuggestion, loadingOptimization, submissions,
    loadingSubmissions, searchQuery, searchResults, searchLoading,
    descWidth, isConsoleOpen, runMode, hintsExpanded, isResizing,
    showProblemsDrawer,
  } = state

  const handleTabChange = (tab) => {
    patch({ activeTab: tab })
    if (tab === 'submissions') loadRecentSubmissions()
  }

  const handleDrawerSelect = (id) => {
    selectProblem(id)
    patch({ showProblemsDrawer: false, searchQuery: '', searchResults: null })
  }

  return (
    <div className="neetcode-layout">
      {showProblemsDrawer && (
        <ProblemDrawer
          problems={problems}
          questionId={questionId}
          searchQuery={searchQuery}
          searchResults={searchResults}
          searchLoading={searchLoading}
          onSearch={handleProblemSearch}
          onSelect={handleDrawerSelect}
          onClose={() => patch({ showProblemsDrawer: false })}
        />
      )}

      {/* Top Toolbar */}
      <div className="top-toolbar">
        <button className="menu-btn" title="Problem List" onClick={() => patch({ showProblemsDrawer: true })}>
          ☰
        </button>

        {selectedProblem && (
          <div className="problem-title">
            <span className="problem-number">#{selectedProblem.leetcode_id}.</span>
            <h3>{selectedProblem.title}</h3>
            <span className={`difficulty-badge ${selectedProblem.difficulty}`}>{selectedProblem.difficulty}</span>
          </div>
        )}

        <div className="toolbar-spacer" />

        <button
          className="icon-btn hint-btn"
          onClick={() => patch({ hintsExpanded: !hintsExpanded })}
          title="View Hints"
        >
          💡 Hints ({Object.keys(hints).filter(k => hints[k]?.hint).length}/3)
        </button>

        <button className="icon-btn ai-btn" onClick={() => patch({ showChatDialog: true })} title="AI Assistant">
          🤖 AI
        </button>

        <div className="toolbar-divider" />

        <select className="language-select" value={language} onChange={(e) => handleLanguageChange(e.target.value)}>
          <option value="python">Python</option>
          <option value="javascript">JavaScript</option>
          <option value="java">Java</option>
          <option value="cpp">C++</option>
        </select>

        <button className="btn-run" onClick={() => executeCode('run')} disabled={loading}>
          {loading && runMode === 'run' ? '⏳ Running...' : '▶ Run Code'}
        </button>

        <button className="btn-submit" onClick={() => executeCode('submit')} disabled={loading}>
          {loading && runMode === 'submit' ? '⏳ Submitting...' : '✓ Submit'}
        </button>
      </div>

      {/* Split Pane */}
      <div className="split-pane" ref={splitPaneRef}>
        <ProblemPanel
          selectedProblem={selectedProblem}
          hints={hints}
          hintsExpanded={hintsExpanded}
          onToggleHints={() => patch({ hintsExpanded: !hintsExpanded })}
          onRequestHint={requestAIHint}
          style={{ width: descWidth }}
        />

        <div
          className={`resizer ${isResizing ? 'resizing' : ''}`}
          ref={resizerRef}
          onMouseDown={handleResizeMouseDown}
        />

        <EditorPanel
          code={code}
          language={language}
          selectedProblem={selectedProblem}
          onCodeChange={(value) => patch({ code: value })}
        />
      </div>

      <ConsolePanel
        isConsoleOpen={isConsoleOpen}
        activeTab={activeTab}
        selectedProblem={selectedProblem}
        testResults={testResults}
        result={result}
        runMode={runMode}
        loading={loading}
        aiSuggestion={aiSuggestion}
        loadingAiSuggestion={loadingAiSuggestion}
        optimizationSuggestion={optimizationSuggestion}
        loadingOptimization={loadingOptimization}
        submissions={submissions}
        loadingSubmissions={loadingSubmissions}
        problems={problems}
        isResultMaximized={isResultMaximized}
        onTabChange={handleTabChange}
        onToggleConsole={() => patch({ isConsoleOpen: !isConsoleOpen })}
        onMaximizeResult={() => patch({ isResultMaximized: true })}
        onSelectProblem={selectProblem}
      />

      {questionId && (
        <button
          className="floating-ai-btn"
          onClick={() => patch({ showChatDialog: !showChatDialog })}
          title="AI Assistant"
        >
          🤖
        </button>
      )}

      {showChatDialog && (
        <AIChatDialog
          chatHistory={chatHistory}
          chatMessage={chatMessage}
          loadingChat={loadingChat}
          isChatMaximized={isChatMaximized}
          onSendMessage={handleSendChatMessage}
          onMessageChange={(value) => patch({ chatMessage: value })}
          onToggleMaximize={() => patch({ isChatMaximized: !isChatMaximized })}
          onClose={() => patch({ showChatDialog: false })}
        />
      )}

      {isResultMaximized && (
        <div className="result-maximized-overlay" onClick={() => patch({ isResultMaximized: false })}>
          <div className="result-maximized-dialog" onClick={(e) => e.stopPropagation()}>
            <div className="result-maximized-header">
              <h3>📊 Test Results</h3>
              <button
                className="close-maximized-btn"
                onClick={() => patch({ isResultMaximized: false })}
                title="Close"
              >
                ✕
              </button>
            </div>
            <div className="result-maximized-content">
              <ResultsView
                testResults={testResults}
                result={result}
                runMode={runMode}
                loading={false}
                aiSuggestion={aiSuggestion}
                loadingAiSuggestion={loadingAiSuggestion}
                optimizationSuggestion={optimizationSuggestion}
                loadingOptimization={loadingOptimization}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default CodeCheckPage
