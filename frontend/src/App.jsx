import React, { useState, useRef, useEffect } from 'react'
import axios from 'axios'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import rehypeHighlight from 'rehype-highlight'
import { 
  Upload, 
  Send, 
  FileText, 
  MessageCircle, 
  RotateCcw, 
  Trash2, 
  BookOpen,
  ChevronDown,
  ChevronRight,
  Loader2
} from 'lucide-react'

const API_BASE_URL = 'http://localhost:8000'

function App() {
  const [pdfUploaded, setPdfUploaded] = useState(false)
  const [currentPdf, setCurrentPdf] = useState(null)
  const [messages, setMessages] = useState([])
  const [currentQuestion, setCurrentQuestion] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [sourceDocuments, setSourceDocuments] = useState([])
  const [expandedSources, setExpandedSources] = useState({})
  const [dragOver, setDragOver] = useState(false)
  
  const fileInputRef = useRef(null)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleFileUpload = async (file) => {
    if (!file || file.type !== 'application/pdf') {
      alert('Please select a PDF file')
      return
    }

    setIsLoading(true)
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await axios.post(`${API_BASE_URL}/upload-pdf`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })

      if (response.status === 200) {
        setPdfUploaded(true)
        setCurrentPdf(file.name)
        setMessages([])
        setSourceDocuments([])
        alert(`Successfully processed: ${file.name}`)
      }
    } catch (error) {
      console.error('Upload error:', error)
      alert(`Upload failed: ${error.response?.data?.detail || error.message}`)
    } finally {
      setIsLoading(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setDragOver(false)
    const files = e.dataTransfer.files
    if (files.length > 0) {
      handleFileUpload(files[0])
    }
  }

  const handleDragOver = (e) => {
    e.preventDefault()
    setDragOver(true)
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    setDragOver(false)
  }

  const sendMessage = async () => {
    if (!currentQuestion.trim() || isLoading) return

    const userMessage = { role: 'user', content: currentQuestion }
    setMessages(prev => [...prev, userMessage])
    setCurrentQuestion('')
    setIsLoading(true)

    try {
      const response = await axios.post(`${API_BASE_URL}/chat`, {
        question: currentQuestion,
        thread_id: 'react_user_1'
      }, { timeout: 60000 })

      if (response.status === 200) {
        const { answer, source_documents } = response.data
        const assistantMessage = { role: 'assistant', content: answer }
        setMessages(prev => [...prev, assistantMessage])
        setSourceDocuments(source_documents || [])
      }
    } catch (error) {
      console.error('Chat error:', error)
      const errorMessage = { 
        role: 'assistant', 
        content: `Sorry, I encountered an error: ${error.response?.data?.detail || error.message}` 
      }
      setMessages(prev => [...prev, errorMessage])
      setSourceDocuments([])
    } finally {
      setIsLoading(false)
    }
  }

  const startNewSession = async () => {
    try {
      await axios.post(`${API_BASE_URL}/new-session`)
      setMessages([])
      setSourceDocuments([])
      alert('Started new conversation!')
    } catch (error) {
      console.error('New session error:', error)
      alert('Failed to start new session')
    }
  }

  const clearAllData = async () => {
    if (!confirm('Are you sure you want to clear all data? This will remove the uploaded PDF and all conversations.')) {
      return
    }

    try {
      await axios.delete(`${API_BASE_URL}/clear-all`)
      setPdfUploaded(false)
      setCurrentPdf(null)
      setMessages([])
      setSourceDocuments([])
      alert('All data cleared!')
    } catch (error) {
      console.error('Clear all error:', error)
      alert('Failed to clear data')
    }
  }

  const toggleSourceExpansion = (index) => {
    setExpandedSources(prev => ({
      ...prev,
      [index]: !prev[index]
    }))
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  if (!pdfUploaded) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary-50 to-blue-50 flex items-center justify-center p-4">
        <div className="max-w-2xl w-full">
          <div className="text-center mb-8">
            <BookOpen className="w-16 h-16 text-primary-600 mx-auto mb-4" />
            <h1 className="text-4xl font-bold text-gray-900 mb-2">Research Paper Q&A</h1>
            <p className="text-lg text-gray-600">Upload a research paper and start asking questions</p>
          </div>

          <div 
            className={`upload-area ${dragOver ? 'dragover' : ''}`}
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onClick={() => fileInputRef.current?.click()}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf"
              onChange={(e) => e.target.files[0] && handleFileUpload(e.target.files[0])}
              className="hidden"
            />
            
            {isLoading ? (
              <div className="flex flex-col items-center">
                <Loader2 className="w-12 h-12 text-primary-600 animate-spin mb-4" />
                <p className="text-lg font-medium text-gray-700">Processing your research paper...</p>
                <p className="text-sm text-gray-500 mt-2">This may take a few moments</p>
              </div>
            ) : (
              <div className="flex flex-col items-center">
                <Upload className="w-12 h-12 text-gray-400 mb-4" />
                <p className="text-lg font-medium text-gray-700 mb-2">
                  Drop your PDF here or click to browse
                </p>
                <p className="text-sm text-gray-500">
                  Supports PDF files up to 50MB
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <BookOpen className="w-8 h-8 text-primary-600" />
              <div>
                <h1 className="text-xl font-semibold text-gray-900">Research Paper Q&A</h1>
                <p className="text-sm text-gray-600">
                  <FileText className="w-4 h-4 inline mr-1" />
                  {currentPdf}
                </p>
              </div>
            </div>
            
            <div className="flex items-center space-x-2">
              <button
                onClick={startNewSession}
                className="btn-secondary flex items-center space-x-2"
                disabled={isLoading}
              >
                <RotateCcw className="w-4 h-4" />
                <span>New Chat</span>
              </button>
              <button
                onClick={clearAllData}
                className="btn-secondary flex items-center space-x-2 text-red-600 hover:bg-red-50"
                disabled={isLoading}
              >
                <Trash2 className="w-4 h-4" />
                <span>Clear All</span>
              </button>
            </div>
          </div>
        </header>

        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto custom-scrollbar p-6">
          <div className="max-w-4xl mx-auto space-y-6">
            {messages.length === 0 ? (
              <div className="text-center py-12">
                <MessageCircle className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                <h3 className="text-xl font-medium text-gray-700 mb-2">Ready to answer your questions!</h3>
                <p className="text-gray-500 mb-6">Try asking about:</p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-2xl mx-auto text-sm">
                  <div className="bg-white p-3 rounded-lg border border-gray-200">
                    <span className="text-gray-700">Main findings or conclusions</span>
                  </div>
                  <div className="bg-white p-3 rounded-lg border border-gray-200">
                    <span className="text-gray-700">Methodology used</span>
                  </div>
                  <div className="bg-white p-3 rounded-lg border border-gray-200">
                    <span className="text-gray-700">Key concepts or definitions</span>
                  </div>
                  <div className="bg-white p-3 rounded-lg border border-gray-200">
                    <span className="text-gray-700">Specific sections or data</span>
                  </div>
                </div>
              </div>
            ) : (
              messages.map((message, index) => (
                <div key={index} className={`chat-message flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`message-bubble ${message.role === 'user' ? 'message-user' : 'message-assistant'}`}>
                    {message.role === 'user' ? (
                      <div className="whitespace-pre-wrap">{message.content}</div>
                    ) : (
                      <div className="markdown-content">
                        <ReactMarkdown
                          remarkPlugins={[remarkGfm]}
                          rehypePlugins={[rehypeHighlight]}
                        >
                          {message.content}
                        </ReactMarkdown>
                      </div>
                    )}
                  </div>
                </div>
              ))
            )}
            
            {isLoading && (
              <div className="flex justify-start">
                <div className="message-bubble message-assistant flex items-center space-x-2">
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Analyzing...</span>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Input Area */}
        <div className="border-t border-gray-200 bg-white p-6">
          <div className="max-w-4xl mx-auto">
            <div className="flex space-x-4">
              <div className="flex-1">
                <textarea
                  value={currentQuestion}
                  onChange={(e) => setCurrentQuestion(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Ask a question about the research paper..."
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
                  rows="2"
                  disabled={isLoading}
                />
              </div>
              <button
                onClick={sendMessage}
                disabled={!currentQuestion.trim() || isLoading}
                className="btn-primary flex items-center space-x-2 self-end disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Send className="w-4 h-4" />
                <span>Send</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Source Documents Sidebar */}
      <div className="w-80 bg-white border-l border-gray-200 flex flex-col">
        <div className="p-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900 flex items-center">
            <FileText className="w-5 h-5 mr-2" />
            Source Documents
          </h2>
        </div>
        
        <div className="flex-1 overflow-y-auto custom-scrollbar p-4">
          {sourceDocuments.length > 0 ? (
            <div className="space-y-3">
              <p className="text-sm text-gray-600 mb-4">
                <strong>{sourceDocuments.length}</strong> relevant chunks found
              </p>
              
              {sourceDocuments.map((doc, index) => (
                <div key={index} className="source-card">
                  <div 
                    className="flex items-center justify-between cursor-pointer"
                    onClick={() => toggleSourceExpansion(index)}
                  >
                    <h4 className="font-medium text-gray-900">
                      Source {doc.chunk_id || index + 1}
                    </h4>
                    {expandedSources[index] ? (
                      <ChevronDown className="w-4 h-4 text-gray-500" />
                    ) : (
                      <ChevronRight className="w-4 h-4 text-gray-500" />
                    )}
                  </div>
                  
                  {doc.metadata && (
                    <div className="mt-2 text-xs text-gray-500">
                      {doc.metadata['Header 1'] && (
                        <div><strong>Section:</strong> {doc.metadata['Header 1']}</div>
                      )}
                      {doc.metadata['Header 2'] && (
                        <div><strong>Subsection:</strong> {doc.metadata['Header 2']}</div>
                      )}
                    </div>
                  )}
                  
                  <div className="mt-3">
                    {expandedSources[index] ? (
                      <div className="markdown-content text-sm">
                        <ReactMarkdown
                          remarkPlugins={[remarkGfm]}
                          rehypePlugins={[rehypeHighlight]}
                        >
                          {doc.content}
                        </ReactMarkdown>
                      </div>
                    ) : (
                      <p className="text-sm text-gray-700">
                        {doc.content?.substring(0, 150)}
                        {doc.content?.length > 150 && '...'}
                      </p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <FileText className="w-12 h-12 text-gray-300 mx-auto mb-3" />
              <p className="text-gray-500 text-sm">
                Ask a question to see relevant document chunks here!
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
