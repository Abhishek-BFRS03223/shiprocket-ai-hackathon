import React, { useState } from 'react'
import './App.css'

function App() {
  const [productName, setProductName] = useState('')
  const [isGenerating, setIsGenerating] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')

  const [showPreview, setShowPreview] = useState(false)

  // Generate website from product name
  const generateWebsite = async () => {
    if (!productName.trim()) {
      setError('Please enter a product name')
      return
    }

    console.log('🚀 Starting generation for:', productName)
    setIsGenerating(true)
    setError('')
    setResult(null)

    try {
      const response = await fetch('http://localhost:3000/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ product_name: productName.trim() })
      })

      const data = await response.json()
      console.log('📥 Received response:', data)
      
      if (data.success) {
        setResult(data)
        setProductName('') // Clear input
        console.log('✅ Success! Site content length:', data.site_content?.length || 0)
      } else {
        setError(data.message || 'Generation failed')
      }
    } catch (err) {
      console.error('❌ Generation error:', err)
      setError('Failed to connect to server. Make sure backend is running.')
    } finally {
      setIsGenerating(false)
    }
  }

  // Open website in new window
  const openSiteInNewWindow = () => {
    if (!result?.site_content) return
    
    try {
      const newWindow = window.open('', '_blank', 'width=1200,height=800,scrollbars=yes,resizable=yes')
      if (newWindow) {
        newWindow.document.write(result.site_content)
        newWindow.document.close()
        newWindow.focus()
      } else {
        // Fallback if popup was blocked
        downloadWebsite()
      }
    } catch (error) {
      console.error('Failed to open new window:', error)
      downloadWebsite()
    }
  }

  // Download website as HTML file
  const downloadWebsite = () => {
    if (!result?.site_content) return
    
    const blob = new Blob([result.site_content], { type: 'text/html' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${result.product_name.replace(/[^a-zA-Z0-9]/g, '_')}_website.html`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  // Copy website HTML to clipboard
  const copyWebsiteContent = async () => {
    if (!result?.site_content) return
    
    try {
      await navigator.clipboard.writeText(result.site_content)
      alert('✅ Website HTML copied to clipboard!')
    } catch (error) {
      console.error('Failed to copy:', error)
      alert('❌ Failed to copy to clipboard')
    }
  }



  // Generate demo sites
  const generateDemoSites = async () => {
    setIsGenerating(true)
    setError('')
    
    try {
      const response = await fetch('http://localhost:3000/api/demo/generate', {
        method: 'POST'
      })
      
      const data = await response.json()
      
      if (data.success) {
        setResult({ message: 'Demo sites generated successfully!', demo: true })
      } else {
        setError('Demo generation failed')
      }
    } catch (err) {
      setError('Failed to generate demo sites')
    } finally {
      setIsGenerating(false)
    }
  }



  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <h1>🚀 One-Click Site Generator</h1>
        <p>Enter any product name and get a professional website with images instantly</p>
      </header>

      {/* Main Generator */}
      <main className="main">
        <div className="generator-card">
          <h2>Generate Your Website</h2>
          
          <div className="input-section">
            <input
              type="text"
              value={productName}
              onChange={(e) => setProductName(e.target.value)}
              placeholder="Enter product name (e.g., Smart Coffee Maker, AI Drone, Yoga Mat)"
              className="product-input"
              onKeyPress={(e) => e.key === 'Enter' && generateWebsite()}
              disabled={isGenerating}
            />
            
            <div className="button-group">
              <button
                onClick={generateWebsite}
                disabled={isGenerating || !productName.trim()}
                className="generate-btn primary"
              >
                {isGenerating ? '🔄 Generating...' : '✨ Generate Website'}
              </button>
              
              <button
                onClick={generateDemoSites}
                disabled={isGenerating}
                className="demo-btn secondary"
              >
                🎯 Generate 5 Demo Sites
              </button>
            </div>
          </div>

          {/* Error Display */}
          {error && (
            <div className="error-message">
              ❌ {error}
            </div>
          )}

          {/* Enhanced Success Result */}
          {result && result.site_content && (
            <div className="success-message enhanced">
              <h3>✅ Website Generated Successfully!</h3>
              <p><strong>Product:</strong> {result.product_name}</p>
              <p><strong>Theme:</strong> Dynamic ({result.theme})</p>
              <p><strong>Content Length:</strong> {result.site_content.length.toLocaleString()} characters</p>
              
              <div className="website-actions">
                <button
                  onClick={openSiteInNewWindow}
                  className="action-btn primary"
                >
                  🚀 Open in New Window
                </button>
                
                <button
                  onClick={downloadWebsite}
                  className="action-btn secondary"
                >
                  💾 Download Website
                </button>
                
                <button
                  onClick={copyWebsiteContent}
                  className="action-btn secondary"
                >
                  📋 Copy HTML
                </button>
                
                <button
                  onClick={() => setShowPreview(!showPreview)}
                  className="action-btn secondary"
                >
                  👁️ {showPreview ? 'Hide' : 'Show'} Preview
                </button>
              </div>

              <div className="tip-message">
                💡 <strong>Tip:</strong> If "Open in New Window" doesn't work due to popup blockers, use "Download Website" or "Show Preview"
              </div>
              
              {showPreview && (
                <div className="preview-section">
                  <h4>📱 Website Preview</h4>
                  <iframe
                    srcDoc={result.site_content}
                    style={{
                      width: '100%',
                      height: '600px',
                      border: '2px solid #667eea',
                      borderRadius: '10px'
                    }}
                    title="Generated Website Preview"
                  />
                </div>
              )}
            </div>
          )}

          {/* Demo Success Result */}
          {result && result.demo && (
            <div className="success-message">
              ✅ {result.message}
            </div>
          )}
        </div>


      </main>

      {/* Footer */}
      <footer className="footer">
        <p>🏆 Shiprocket AI Hackathon - One-Click Site Generator</p>
        <p>✨ Professional websites with images in seconds</p>
      </footer>
    </div>
  )
}

export default App 