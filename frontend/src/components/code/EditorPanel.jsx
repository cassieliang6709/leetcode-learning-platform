import { Suspense, lazy } from 'react'

const Editor = lazy(() => import('@monaco-editor/react'))

const EDITOR_OPTIONS = {
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
  scrollbar: { verticalScrollbarSize: 10, horizontalScrollbarSize: 10 },
}

export default function EditorPanel({ code, language, selectedProblem, onCodeChange }) {
  if (!selectedProblem) return null

  return (
    <div className="editor-pane">
      <Suspense fallback={<div className="empty-state" style={{ padding: '3rem 1.5rem' }}><p>Loading editor...</p></div>}>
        <Editor
          height="100%"
          language={language}
          value={code}
          onChange={(value) => onCodeChange(value || '')}
          theme="light"
          options={EDITOR_OPTIONS}
        />
      </Suspense>
    </div>
  )
}
