import React, { useState } from 'react'
import './App.css'

function App() {
  const [productName, setProductName] = useState('')
  const [isGenerating, setIsGenerating] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [generatedSites, setGeneratedSites] = useState([])

  // Generate website from product name
  const generateWebsite = async () => {
    if (!productName.trim()) {
      setError('Please enter a product name')
      return
    }

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
      
      if (data.success) {
        setResult(data)
        loadGeneratedSites() // Refresh the sites list
        setProductName('') // Clear input
      } else {
        setError(data.message || 'Generation failed')
      }
    } catch (err) {
      setError('Failed to connect to server. Make sure backend is running.')
    } finally {
      setIsGenerating(false)
    }
  }

  // Load all generated sites
  const loadGeneratedSites = async () => {
    try {
      const response = await fetch('http://localhost:3000/api/sites')
      const data = await response.json()
      
      if (data.success) {
        setGeneratedSites(data.sites)
      }
    } catch (err) {
      console.error('Failed to load sites:', err)
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
        loadGeneratedSites()
      } else {
        setError('Demo generation failed')
      }
    } catch (err) {
      setError('Failed to generate demo sites')
    } finally {
      setIsGenerating(false)
    }
  }

  // Load sites on component mount
  React.useEffect(() => {
    loadGeneratedSites()
  }, [])

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

          {/* Success Result */}
          {result && (
            <div className="success-message">
              ✅ {result.demo ? result.message : `Website generated for "${result.product_name}"`}
              {result.site_path && (
                <div className="result-actions">
                  <a 
                    href={`http://localhost:3000/generated/${result.site_path.split('/').pop()}/index.html`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="view-site-btn"
                  >
                    🌐 View Website
                  </a>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Generated Sites Gallery */}
        {generatedSites.length > 0 && (
          <div className="sites-gallery">
            <h3>📂 Generated Websites ({generatedSites.length})</h3>
            <div className="sites-grid">
              {generatedSites.map((site, index) => (
                <div key={index} className="site-card">
                  <h4>{site.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}</h4>
                  <div className="site-actions">
                    <a
                      href={`http://localhost:3000/generated/${site}/index.html`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="view-btn"
                    >
                      👁️ View
                    </a>
                    <a
                      href={`http://localhost:3000/api/sites/${site}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="preview-btn"
                    >
                      🔗 Direct Link
                    </a>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
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