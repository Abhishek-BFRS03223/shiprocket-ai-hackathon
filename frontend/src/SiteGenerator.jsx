import { useState, useEffect } from 'react'
import axios from 'axios'

const SiteGenerator = () => {
  const [productName, setProductName] = useState('')
  const [isGenerating, setIsGenerating] = useState(false)
  const [generatedSite, setGeneratedSite] = useState(null)
  const [generatedSites, setGeneratedSites] = useState([])
  const [error, setError] = useState('')
  const [showPreview, setShowPreview] = useState(false)

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

    console.log('🚀 Starting website generation for:', productName)
    setIsGenerating(true)
    setError('')
    setGeneratedSite(null)

    try {
      console.log('📡 Sending request to:', `${API_BASE}/generate`)
      const response = await axios.post(`${API_BASE}/generate`, {
        product_name: productName,
      })

      console.log('📥 Received response:', response.data)
      
      if (response.data.success) {
        console.log('✅ Success! Setting generated site state')
        console.log('🎯 Site content length:', response.data.site_content?.length || 0)
        setGeneratedSite(response.data)
        setProductName('') // Clear input
        setError('')
        console.log('🎨 Generated site state set successfully')
      } else {
        console.log('❌ Generation failed:', response.data.message)
        setError(response.data.message || 'Generation failed')
      }
    } catch (err) {
      console.error('🔥 Generation error:', err)
      setError(err.response?.data?.message || 'Network error occurred')
    } finally {
      setIsGenerating(false)
      console.log('🏁 Generation process completed')
    }
  }

  const generateDemoSites = async () => {
    setIsGenerating(true)
    setError('')

    try {
      const response = await axios.get(`${API_BASE}/demo/generate`)
      
      if (response.data.success) {
        alert(`Demo completed! Generated ${response.data.total_generated} enhanced sites with dynamic themes`)
      } else {
        setError('Demo generation failed')
      }
    } catch (err) {
      setError('Demo generation failed')
      console.error('Demo error:', err)
    } finally {
      setIsGenerating(false)
    }
  }

  const openSiteInNewWindow = () => {
    if (!generatedSite?.site_content) return
    
    // Try opening in new window first
    try {
      const newWindow = window.open('', '_blank', 'width=1200,height=800,scrollbars=yes,resizable=yes')
      if (newWindow) {
        newWindow.document.write(generatedSite.site_content)
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

  const downloadWebsite = () => {
    if (!generatedSite?.site_content) return
    
    const blob = new Blob([generatedSite.site_content], { type: 'text/html' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${generatedSite.product_name.replace(/[^a-zA-Z0-9]/g, '_')}_website.html`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const copyWebsiteContent = async () => {
    if (!generatedSite?.site_content) return
    
    try {
      await navigator.clipboard.writeText(generatedSite.site_content)
      alert('✅ Website HTML copied to clipboard!')
    } catch (error) {
      console.error('Failed to copy:', error)
      alert('❌ Failed to copy to clipboard')
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      generateWebsite()
    }
  }

  return (
    <>
      <style>
        {`
          @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
          }
        `}
      </style>
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '20px', fontFamily: 'Inter, Arial, sans-serif' }}>
      {/* Enhanced Header */}
      <div style={{ textAlign: 'center', marginBottom: '40px' }}>
        <h1 style={{ 
          fontSize: '3.5rem', 
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text',
          marginBottom: '15px',
          fontWeight: '700'
        }}>
          🚀 Enhanced AI Site Generator
        </h1>
        <p style={{ fontSize: '1.3rem', color: '#666', marginBottom: '10px' }}>
          Generate stunning ecommerce websites with dynamic themes, AI-powered content, and product-specific images!
        </p>
        <p style={{ fontSize: '1rem', color: '#888', maxWidth: '600px', margin: '0 auto' }}>
          ✨ Dynamic Themes • 🖼️ AI Generated Images • 🛍️ Ecommerce Ready • ⚡ Instant Generation
        </p>
      </div>

      {/* Enhanced Generator */}
      <div style={{
        background: 'white',
        borderRadius: '20px',
        padding: '40px',
        boxShadow: '0 20px 60px rgba(0,0,0,0.1)',
        marginBottom: '40px',
        border: '1px solid rgba(0,0,0,0.05)'
      }}>
        <div style={{ display: 'flex', gap: '15px', marginBottom: '25px', alignItems: 'center' }}>
          <input
            type="text"
            value={productName}
            onChange={(e) => setProductName(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Enter product name (e.g., 'Smart Coffee Maker', 'Designer Handbag', 'Gaming Laptop')"
            disabled={isGenerating}
            style={{
              flex: 1,
              padding: '18px 25px',
              border: '2px solid #e0e0e0',
              borderRadius: '50px',
              fontSize: '1.1rem',
              outline: 'none',
              transition: 'all 0.3s ease',
              fontFamily: 'inherit'
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
              padding: '18px 35px',
              fontSize: '1.1rem',
              fontWeight: '600',
              cursor: isGenerating ? 'not-allowed' : 'pointer',
              transition: 'all 0.3s ease',
              minWidth: '180px',
              boxShadow: isGenerating ? 'none' : '0 8px 25px rgba(102, 126, 234, 0.3)'
            }}
            onMouseOver={(e) => !isGenerating && (e.target.style.transform = 'translateY(-2px)')}
            onMouseOut={(e) => e.target.style.transform = 'translateY(0)'}
          >
            {isGenerating ? '🔄 Generating...' : '🚀 Generate Site'}
          </button>
        </div>

        {/* Enhanced Demo Button */}
        <div style={{ textAlign: 'center' }}>
          <button
            onClick={generateDemoSites}
            disabled={isGenerating}
            style={{
              background: 'transparent',
              border: '2px solid #667eea',
              color: '#667eea',
              borderRadius: '25px',
              padding: '12px 30px',
              fontSize: '1rem',
              cursor: isGenerating ? 'not-allowed' : 'pointer',
              transition: 'all 0.3s ease',
              fontWeight: '500'
            }}
            onMouseOver={(e) => !isGenerating && (e.target.style.background = '#667eea', e.target.style.color = 'white')}
            onMouseOut={(e) => (e.target.style.background = 'transparent', e.target.style.color = '#667eea')}
          >
            🎭 Generate Demo Portfolio (7 Sites)
          </button>
        </div>

        {error && (
          <div style={{
            background: 'linear-gradient(135deg, #ff6b6b, #ee5a24)',
            color: 'white',
            border: 'none',
            borderRadius: '15px',
            padding: '20px',
            marginTop: '25px',
            boxShadow: '0 8px 25px rgba(255, 107, 107, 0.3)'
          }}>
            <strong>❌ Error:</strong> {error}
          </div>
        )}

        {/* Quick Success Indicator */}
        {generatedSite && !error && (
          <div style={{
            background: 'linear-gradient(135deg, #00b894, #00cec9)',
            color: 'white',
            border: 'none',
            borderRadius: '15px',
            padding: '20px',
            marginTop: '25px',
            boxShadow: '0 8px 25px rgba(0, 184, 148, 0.3)',
            textAlign: 'center',
            animation: 'fadeIn 0.5s ease-in'
          }}>
            <strong>🎉 Website Generated Successfully!</strong>
            <br />
            <small>Scroll down to see your website options ⬇️</small>
          </div>
        )}
      </div>

      {/* Debug Section */}
      {process.env.NODE_ENV === 'development' && (
        <div style={{
          background: '#f0f0f0',
          padding: '15px',
          borderRadius: '10px',
          marginBottom: '20px',
          fontSize: '0.9rem'
        }}>
          <strong>🔍 Debug Info:</strong>
          <br />
          • generatedSite exists: {generatedSite ? '✅ Yes' : '❌ No'}
          <br />
          • Site content length: {generatedSite?.site_content?.length || 0}
          <br />
          • Product name: {generatedSite?.product_name || 'None'}
          <br />
          • Success: {generatedSite?.success ? '✅' : '❌'}
        </div>
      )}

      {/* Enhanced Success Result */}
      {generatedSite && (
        <div style={{
          background: 'linear-gradient(135deg, #00b894, #00cec9)',
          color: 'white',
          borderRadius: '20px',
          padding: '35px',
          marginBottom: '40px',
          boxShadow: '0 20px 60px rgba(0, 184, 148, 0.3)'
        }}>
          <h3 style={{ marginBottom: '20px', fontSize: '1.8rem', fontWeight: '600' }}>
            ✅ Successfully Generated: {generatedSite.product_name}
          </h3>
          
          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', 
            gap: '20px', 
            marginBottom: '25px',
            background: 'rgba(255,255,255,0.1)',
            padding: '25px',
            borderRadius: '15px'
          }}>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '2rem', marginBottom: '8px' }}>🎨</div>
              <div style={{ fontWeight: '600', marginBottom: '5px' }}>Theme</div>
              <div style={{ opacity: 0.9 }}>Dynamic ({generatedSite.theme})</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '2rem', marginBottom: '8px' }}>🖼️</div>
              <div style={{ fontWeight: '600', marginBottom: '5px' }}>Images</div>
              <div style={{ opacity: 0.9 }}>AI Generated</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '2rem', marginBottom: '8px' }}>🛍️</div>
              <div style={{ fontWeight: '600', marginBottom: '5px' }}>Type</div>
              <div style={{ opacity: 0.9 }}>Ecommerce Ready</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '2rem', marginBottom: '8px' }}>⚡</div>
              <div style={{ fontWeight: '600', marginBottom: '5px' }}>Generated</div>
              <div style={{ opacity: 0.9 }}>{new Date(generatedSite.generated_at).toLocaleTimeString()}</div>
            </div>
          </div>

          <div style={{ display: 'flex', gap: '15px', justifyContent: 'center', flexWrap: 'wrap' }}>
            <button
              onClick={openSiteInNewWindow}
              style={{
                background: 'rgba(255,255,255,0.2)',
                backdropFilter: 'blur(10px)',
                color: 'white',
                border: '1px solid rgba(255,255,255,0.3)',
                borderRadius: '12px',
                padding: '15px 25px',
                fontSize: '1rem',
                fontWeight: '600',
                cursor: 'pointer',
                transition: 'all 0.3s ease'
              }}
              onMouseOver={(e) => e.target.style.background = 'rgba(255,255,255,0.3)'}
              onMouseOut={(e) => e.target.style.background = 'rgba(255,255,255,0.2)'}
            >
              🚀 Open in New Window
            </button>
            
            <button
              onClick={downloadWebsite}
              style={{
                background: 'rgba(255,255,255,0.2)',
                backdropFilter: 'blur(10px)',
                color: 'white',
                border: '1px solid rgba(255,255,255,0.3)',
                borderRadius: '12px',
                padding: '15px 25px',
                fontSize: '1rem',
                fontWeight: '600',
                cursor: 'pointer',
                transition: 'all 0.3s ease'
              }}
              onMouseOver={(e) => e.target.style.background = 'rgba(255,255,255,0.3)'}
              onMouseOut={(e) => e.target.style.background = 'rgba(255,255,255,0.2)'}
            >
              💾 Download Website
            </button>
            
            <button
              onClick={copyWebsiteContent}
              style={{
                background: 'rgba(255,255,255,0.2)',
                backdropFilter: 'blur(10px)',
                color: 'white',
                border: '1px solid rgba(255,255,255,0.3)',
                borderRadius: '12px',
                padding: '15px 25px',
                fontSize: '1rem',
                fontWeight: '600',
                cursor: 'pointer',
                transition: 'all 0.3s ease'
              }}
              onMouseOver={(e) => e.target.style.background = 'rgba(255,255,255,0.3)'}
              onMouseOut={(e) => e.target.style.background = 'rgba(255,255,255,0.2)'}
            >
              📋 Copy HTML
            </button>
            
            <button
              onClick={() => setShowPreview(!showPreview)}
              style={{
                background: 'rgba(255,255,255,0.2)',
                backdropFilter: 'blur(10px)',
                color: 'white',
                border: '1px solid rgba(255,255,255,0.3)',
                borderRadius: '12px',
                padding: '15px 25px',
                fontSize: '1rem',
                fontWeight: '600',
                cursor: 'pointer',
                transition: 'all 0.3s ease'
              }}
              onMouseOver={(e) => e.target.style.background = 'rgba(255,255,255,0.3)'}
              onMouseOut={(e) => e.target.style.background = 'rgba(255,255,255,0.2)'}
            >
              👁️ {showPreview ? 'Hide' : 'Show'} Preview
            </button>
          </div>

          <div style={{ 
            marginTop: '20px', 
            padding: '15px', 
            background: 'rgba(255,255,255,0.1)', 
            borderRadius: '10px',
            fontSize: '0.9rem',
            opacity: 0.9
          }}>
            <strong>💡 Features:</strong> {generatedSite.message}
          </div>

          <div style={{ 
            marginTop: '15px', 
            padding: '12px', 
            background: 'rgba(255,255,255,0.08)', 
            borderRadius: '8px',
            fontSize: '0.85rem',
            opacity: 0.8,
            textAlign: 'center'
          }}>
            🌟 <strong>Tip:</strong> If "Open in New Window" doesn't work due to popup blockers, use "Download Website" or "Show Preview" to view your site!
          </div>
        </div>
      )}

      {/* Enhanced Preview */}
      {generatedSite && showPreview && (
        <div style={{
          background: 'white',
          borderRadius: '20px',
          padding: '25px',
          boxShadow: '0 20px 60px rgba(0,0,0,0.1)',
          marginBottom: '40px'
        }}>
          <div style={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center', 
            marginBottom: '20px',
            paddingBottom: '15px',
            borderBottom: '2px solid #f0f0f0'
          }}>
            <h3 style={{ color: '#667eea', fontSize: '1.5rem', fontWeight: '600' }}>
              📱 Website Preview
            </h3>
            <button
              onClick={() => setShowPreview(false)}
              style={{
                background: '#ff6b6b',
                color: 'white',
                border: 'none',
                borderRadius: '20px',
                padding: '8px 15px',
                cursor: 'pointer',
                fontSize: '0.9rem'
              }}
            >
              ✕ Close
            </button>
          </div>
          
          <div style={{
            border: '3px solid #667eea',
            borderRadius: '15px',
            overflow: 'hidden',
            boxShadow: '0 10px 30px rgba(0,0,0,0.1)'
          }}>
            <iframe
              srcDoc={generatedSite.site_content}
              style={{
                width: '100%',
                height: '600px',
                border: 'none'
              }}
              title="Generated Website Preview"
            />
          </div>
          
          <div style={{ 
            textAlign: 'center', 
            marginTop: '15px',
            color: '#666',
            fontSize: '0.9rem'
          }}>
            🔄 This preview shows your generated website with dynamic theme and AI-generated content
          </div>
        </div>
      )}

      {/* Enhanced Info Section */}
      <div style={{
        background: 'linear-gradient(135deg, #f8f9fa, #e9ecef)',
        borderRadius: '20px',
        padding: '35px',
        textAlign: 'center'
      }}>
        <h3 style={{ 
          color: '#495057', 
          marginBottom: '20px', 
          fontSize: '1.5rem',
          fontWeight: '600'
        }}>
          🌟 Enhanced Features
        </h3>
        
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', 
          gap: '25px',
          marginTop: '25px'
        }}>
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '2.5rem', marginBottom: '10px' }}>🎨</div>
            <h4 style={{ color: '#495057', marginBottom: '8px', fontWeight: '600' }}>Dynamic Themes</h4>
            <p style={{ color: '#6c757d', fontSize: '0.9rem', lineHeight: '1.5' }}>
              6 unique themes randomly selected for each generation
            </p>
          </div>
          
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '2.5rem', marginBottom: '10px' }}>🤖</div>
            <h4 style={{ color: '#495057', marginBottom: '8px', fontWeight: '600' }}>AI-Powered Content</h4>
            <p style={{ color: '#6c757d', fontSize: '0.9rem', lineHeight: '1.5' }}>
              GPT-generated content specific to your product
            </p>
          </div>
          
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '2.5rem', marginBottom: '10px' }}>🖼️</div>
            <h4 style={{ color: '#495057', marginBottom: '8px', fontWeight: '600' }}>Smart Images</h4>
            <p style={{ color: '#6c757d', fontSize: '0.9rem', lineHeight: '1.5' }}>
              Hugging Face AI generates product-specific images
            </p>
          </div>
          
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '2.5rem', marginBottom: '10px' }}>🛍️</div>
            <h4 style={{ color: '#495057', marginBottom: '8px', fontWeight: '600' }}>Ecommerce Ready</h4>
            <p style={{ color: '#6c757d', fontSize: '0.9rem', lineHeight: '1.5' }}>
              Complete product catalogs and shopping features
            </p>
          </div>
          
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '2.5rem', marginBottom: '10px' }}>⚡</div>
            <h4 style={{ color: '#495057', marginBottom: '8px', fontWeight: '600' }}>Temporary Sites</h4>
            <p style={{ color: '#6c757d', fontSize: '0.9rem', lineHeight: '1.5' }}>
              Auto-cleanup for privacy and system efficiency
            </p>
          </div>
          
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '2.5rem', marginBottom: '10px' }}>🚀</div>
            <h4 style={{ color: '#495057', marginBottom: '8px', fontWeight: '600' }}>Instant Generation</h4>
            <p style={{ color: '#6c757d', fontSize: '0.9rem', lineHeight: '1.5' }}>
              Professional websites generated in seconds
            </p>
          </div>
        </div>
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
    </>
  )
}

export default SiteGenerator 