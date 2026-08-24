import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import rehypeHighlight from 'rehype-highlight'

function copyToClipboard(text) {
  navigator.clipboard.writeText(text)
}

function CodeBlock({ node, inline, className, children, ...props }) {
  const match = /language-(\w+)/.exec(className || '')
  const codeContent = String(children).replace(/\n$/, '')
  if (!inline && match) {
    return (
      <div className="code-block-container">
        <div className="code-block-header">
          <span className="code-language">{match[1]}</span>
          <button className="copy-code-btn" onClick={() => copyToClipboard(codeContent)} title="Copy code">
            📋 Copy
          </button>
        </div>
        <code className={className} {...props}>{children}</code>
      </div>
    )
  }
  return <code className={className} {...props}>{children}</code>
}

export default function AIChatDialog({
  chatHistory,
  chatMessage,
  loadingChat,
  isChatMaximized,
  onSendMessage,
  onMessageChange,
  onToggleMaximize,
  onClose,
}) {
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      onSendMessage()
    }
  }

  return (
    <div className={`ai-chat-dialog ${isChatMaximized ? 'maximized' : ''}`}>
      <div className="chat-header">
        <h3>🤖 AI Assistant</h3>
        <div className="chat-header-actions">
          <button className="chat-header-btn" onClick={onToggleMaximize} title={isChatMaximized ? 'Restore' : 'Maximize'}>
            {isChatMaximized ? '🗗' : '🗖'}
          </button>
          <button className="chat-header-btn" onClick={onClose}>✕</button>
        </div>
      </div>

      <div className="chat-messages">
        {chatHistory.length === 0 ? (
          <div className="chat-welcome">
            <p>👋 Hi! I'm your AI coding assistant.</p>
            <p>Ask me anything about the problem, your code, or debugging!</p>
            <div className="chat-suggestions">
              <button onClick={() => onMessageChange('Can you explain this problem?')}>Explain the problem</button>
              <button onClick={() => onMessageChange("What's wrong with my code?")}>Debug my code</button>
              <button onClick={() => onMessageChange('How can I optimize this?')}>Optimization tips</button>
            </div>
          </div>
        ) : (
          chatHistory.map((msg, idx) => (
            <div key={idx} className={`chat-message ${msg.role}`}>
              <div className="message-avatar">{msg.role === 'user' ? '👤' : '🤖'}</div>
              <div className="message-content markdown-content">
                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  rehypePlugins={[rehypeHighlight]}
                  components={{ code: CodeBlock }}
                >
                  {msg.content}
                </ReactMarkdown>
                {msg.role === 'assistant' && msg.ragSources?.length > 0 && (
                  <div className="rag-sources">
                    <span className="rag-sources-label">Referenced:</span>
                    {msg.ragSources.map((src, i) => (
                      <span key={i} className="rag-source-badge">📚 {src.name}</span>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))
        )}
        {loadingChat && (
          <div className="chat-message assistant">
            <div className="message-avatar">🤖</div>
            <div className="message-content"><p className="typing-indicator">Thinking...</p></div>
          </div>
        )}
      </div>

      <div className="chat-input-area">
        <textarea
          value={chatMessage}
          onChange={(e) => onMessageChange(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask me anything about the code..."
          rows={2}
          disabled={loadingChat}
        />
        <button
          onClick={onSendMessage}
          disabled={!chatMessage.trim() || loadingChat}
          className="send-btn"
        >
          {loadingChat ? '⏳' : '📤'}
        </button>
      </div>
    </div>
  )
}
