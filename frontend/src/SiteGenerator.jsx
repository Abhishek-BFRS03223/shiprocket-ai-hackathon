import { useState, useEffect } from 'react'
import axios from 'axios'

const SiteGenerator = () => {
  const [productName, setProductName] = useState('')
  const [isGenerating, setIsGenerating] = useState(false)
  const [generatedSite, setGeneratedSite] = useState(null)
  const [generatedSites, setGeneratedSites] = useState([])
  const [error, setError] = useState('')

  const API_BASE = 'http://localhost:3000/api'

  // Load existing sites on component mount
  useEffect(() => {
    loadGeneratedSites()
  }, [])

  const loadGeneratedSites = async () => {
    try {
      const response = await axios.get(`${API_BASE}/sites`)
      setGeneratedSites(response.data.sites || [])
    } catch (err) {
      console.error('Error loading sites:', err)
    }
  }

  const generateWebsite = async () => {
    if (!productName.trim()) {
      setError('Please enter a product name')
      return
    }

    setIsGenerating(true)
    setError('')
    setGeneratedSite(null)

    try {
      const response = await axios.post(`${API_BASE}/generate`, {
        product_name: productName,
        save_to_disk: true
      })

      if (response.data.success) {
        setGeneratedSite(response.data)
        await loadGeneratedSites() // Refresh the sites list
        setProductName('') // Clear input
      } else {
        setError(response.data.error || 'Generation failed')
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Network error occurred')
    } finally {
      setIsGenerating(false)
    }
  }

  const generateDemoSites = async () => {
    setIsGenerating(true)
    setError('')

    try {
      const response = await axios.get(`${API_BASE}/demo/generate`)
      
      if (response.data.demo_results) {
        await loadGeneratedSites() // Refresh the sites list
        alert(`Demo completed! Generated ${response.data.total_generated} sites`)
      }
    } catch (err) {
      setError('Demo generation failed')
    } finally {
      setIsGenerating(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      generateWebsite()
    }
  }

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      {/* Header */}
      <div style={{ textAlign: 'center', marginBottom: '40px' }}>
        <h1 style={{ 
          fontSize: '3rem', 
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          marginBottom: '10px'
        }}>
          🎯 One-Click Site Generator
        </h1>
        <p style={{ fontSize: '1.2rem', color: '#666', marginBottom: '30px' }}>
          Enter any product name and watch AI build a complete website instantly!
        </p>
      </div>

      {/* Main Generator */}
      <div style={{
        background: 'white',
        borderRadius: '20px',
        padding: '40px',
        boxShadow: '0 10px 30px rgba(0,0,0,0.1)',
        marginBottom: '40px'
      }}>
        <div style={{ display: 'flex', gap: '15px', marginBottom: '20px', alignItems: 'center' }}>
          <input
            type="text"
            value={productName}
            onChange={(e) => setProductName(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Enter product name (e.g., 'Smart Coffee Maker', 'Eco Backpack')"
            disabled={isGenerating}
            style={{
              flex: 1,
              padding: '15px 20px',
              border: '2px solid #e0e0e0',
              borderRadius: '50px',
              fontSize: '1.1rem',
              outline: 'none',
              transition: 'border-color 0.3s ease'
            }}
            onFocus={(e) => e.target.style.borderColor = '#667eea'}
            onBlur={(e) => e.target.style.borderColor = '#e0e0e0'}
          />
          
          <button
            onClick={generateWebsite}
            disabled={isGenerating || !productName.trim()}
            style={{
              background: isGenerating ? '#ccc' : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white',
              border: 'none',
              borderRadius: '50px',
              padding: '15px 30px',
              fontSize: '1.1rem',
              fontWeight: '600',
              cursor: isGenerating ? 'not-allowed' : 'pointer',
              transition: 'transform 0.3s ease',
              minWidth: '150px'
            }}
            onMouseOver={(e) => !isGenerating && (e.target.style.transform = 'translateY(-2px)')}
            onMouseOut={(e) => e.target.style.transform = 'translateY(0)'}
          >
            {isGenerating ? '🔄 Generating...' : '🚀 Generate Site'}
          </button>
        </div>

        {/* Demo Button */}
        <div style={{ textAlign: 'center' }}>
          <button
            onClick={generateDemoSites}
            disabled={isGenerating}
            style={{
              background: 'transparent',
              border: '2px solid #667eea',
              color: '#667eea',
              borderRadius: '25px',
              padding: '10px 25px',
              fontSize: '1rem',
              cursor: isGenerating ? 'not-allowed' : 'pointer',
              transition: 'all 0.3s ease'
            }}
            onMouseOver={(e) => !isGenerating && (e.target.style.background = '#667eea', e.target.style.color = 'white')}
            onMouseOut={(e) => (e.target.style.background = 'transparent', e.target.style.color = '#667eea')}
          >
            🎭 Generate 5 Demo Sites
          </button>
        </div>

        {error && (
          <div style={{
            background: '#ffe6e6',
            border: '1px solid #ff9999',
            borderRadius: '10px',
            padding: '15px',
            marginTop: '20px',
            color: '#cc0000'
          }}>
            ❌ {error}
          </div>
        )}
      </div>

      {/* Recent Generation Result */}
      {generatedSite && (
        <div style={{
          background: '#f0fff0',
          border: '2px solid #90EE90',
          borderRadius: '15px',
          padding: '30px',
          marginBottom: '40px'
        }}>
          <h3 style={{ color: '#228B22', marginBottom: '15px' }}>
            ✅ Successfully Generated: {generatedSite.product_name}
          </h3>
          
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '15px', marginBottom: '20px' }}>
            <div>
              <strong>Generation Method:</strong><br />
              {generatedSite.generation_method}
            </div>
            <div>
              <strong>Timestamp:</strong><br />
              {new Date(generatedSite.timestamp).toLocaleString()}
            </div>
            {generatedSite.saved_to && (
              <div>
                <strong>Saved To:</strong><br />
                {generatedSite.saved_to}
              </div>
            )}
          </div>

          {generatedSite.saved_to && (
            <div style={{ textAlign: 'center' }}>
              <a
                href={`http://localhost:3000/generated/${generatedSite.saved_to.split('/').pop()}/`}
                target="_blank"
                rel="noopener noreferrer"
                style={{
                  background: '#228B22',
                  color: 'white',
                  padding: '12px 25px',
                  borderRadius: '25px',
                  textDecoration: 'none',
                  fontWeight: '600',
                  display: 'inline-block',
                  transition: 'transform 0.3s ease'
                }}
                onMouseOver={(e) => e.target.style.transform = 'translateY(-2px)'}
                onMouseOut={(e) => e.target.style.transform = 'translateY(0)'}
              >
                🌐 View Generated Website
              </a>
            </div>
          )}
        </div>
      )}

      {/* Generated Sites Gallery */}
      {generatedSites.length > 0 && (
        <div>
          <h2 style={{ textAlign: 'center', marginBottom: '30px', color: '#333' }}>
            📁 Generated Websites ({generatedSites.length})
          </h2>
          
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
            gap: '20px'
          }}>
            {generatedSites.map((site, index) => (
              <div
                key={index}
                style={{
                  background: 'white',
                  borderRadius: '15px',
                  padding: '25px',
                  boxShadow: '0 5px 15px rgba(0,0,0,0.1)',
                  transition: 'transform 0.3s ease, box-shadow 0.3s ease'
                }}
                onMouseOver={(e) => {
                  e.currentTarget.style.transform = 'translateY(-5px)'
                  e.currentTarget.style.boxShadow = '0 10px 25px rgba(0,0,0,0.15)'
                }}
                onMouseOut={(e) => {
                  e.currentTarget.style.transform = 'translateY(0)'
                  e.currentTarget.style.boxShadow = '0 5px 15px rgba(0,0,0,0.1)'
                }}
              >
                <h3 style={{ color: '#667eea', marginBottom: '10px', fontSize: '1.2rem' }}>
                  {site.product_name || site.name}
                </h3>
                
                <div style={{ color: '#666', fontSize: '0.9rem', marginBottom: '15px' }}>
                  <div><strong>Created:</strong> {new Date(site.created).toLocaleDateString()}</div>
                  {site.generation_method && (
                    <div><strong>Method:</strong> {site.generation_method}</div>
                  )}
                </div>

                <a
                  href={`http://localhost:3000/generated/${site.name}/`}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{
                    background: '#667eea',
                    color: 'white',
                    padding: '10px 20px',
                    borderRadius: '20px',
                    textDecoration: 'none',
                    fontSize: '0.9rem',
                    fontWeight: '600',
                    display: 'inline-block',
                    transition: 'background 0.3s ease'
                  }}
                  onMouseOver={(e) => e.target.style.background = '#5a6fd8'}
                  onMouseOut={(e) => e.target.style.background = '#667eea'}
                >
                  🌐 View Site
                </a>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* No Sites Message */}
      {generatedSites.length === 0 && !isGenerating && (
        <div style={{
          textAlign: 'center',
          padding: '60px 20px',
          color: '#999',
          background: '#f9f9f9',
          borderRadius: '15px'
        }}>
          <h3>No websites generated yet</h3>
          <p>Enter a product name above to generate your first website!</p>
        </div>
      )}

      {/* Footer */}
      <div style={{
        textAlign: 'center',
        marginTop: '60px',
        padding: '30px',
        background: '#f8f9fa',
        borderRadius: '15px',
        color: '#666'
      }}>
        <h4>✨ How it works:</h4>
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
          gap: '20px',
          marginTop: '20px'
        }}>
          <div>
            <div style={{ fontSize: '2rem', marginBottom: '10px' }}>🤖</div>
            <strong>AI Analysis</strong><br />
            Product categorization & strategy
          </div>
          <div>
            <div style={{ fontSize: '2rem', marginBottom: '10px' }}>📝</div>
            <strong>Content Generation</strong><br />
            Headlines, copy & structure
          </div>
          <div>
            <div style={{ fontSize: '2rem', marginBottom: '10px' }}>🎨</div>
            <strong>Design & Layout</strong><br />
            Modern CSS & responsive design
          </div>
          <div>
            <div style={{ fontSize: '2rem', marginBottom: '10px' }}>🚀</div>
            <strong>Instant Deploy</strong><br />
            Ready-to-view website
          </div>
        </div>
      </div>
    </div>
  )
}

export default SiteGenerator 