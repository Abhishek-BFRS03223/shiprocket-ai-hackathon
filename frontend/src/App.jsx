import { useState } from 'react'
import axios from 'axios'
import SiteGenerator from './SiteGenerator'

function App() {
  const [message, setMessage] = useState('')
  const [currentView, setCurrentView] = useState('generator') // 'generator' or 'test'

  const testConnection = async () => {
    try {
      const response = await axios.get('http://localhost:3000/api/health')
      setMessage(response.data.message)
    } catch (error) {
      setMessage('Connection failed: ' + error.message)
    }
  }

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f5f7fa' }}>
      {/* Navigation */}
      <nav style={{
        background: 'white',
        padding: '15px 0',
        boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
        marginBottom: '20px'
      }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h2 style={{ margin: 0, color: '#333' }}>🚀 Shiprocket AI Hackathon</h2>
          <div style={{ display: 'flex', gap: '15px' }}>
            <button
              onClick={() => setCurrentView('generator')}
              style={{
                background: currentView === 'generator' ? '#667eea' : 'transparent',
                color: currentView === 'generator' ? 'white' : '#667eea',
                border: '2px solid #667eea',
                borderRadius: '20px',
                padding: '8px 20px',
                cursor: 'pointer',
                fontWeight: '600'
              }}
            >
              🎯 Site Generator
            </button>
            <button
              onClick={() => setCurrentView('test')}
              style={{
                background: currentView === 'test' ? '#667eea' : 'transparent',
                color: currentView === 'test' ? 'white' : '#667eea',
                border: '2px solid #667eea',
                borderRadius: '20px',
                padding: '8px 20px',
                cursor: 'pointer',
                fontWeight: '600'
              }}
            >
              🔧 System Test
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      {currentView === 'generator' ? (
        <SiteGenerator />
      ) : (
        <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif', maxWidth: '800px', margin: '0 auto' }}>
          <div style={{
            background: 'white',
            borderRadius: '15px',
            padding: '40px',
            boxShadow: '0 5px 15px rgba(0,0,0,0.1)'
          }}>
            <h2>🔧 System Connection Test</h2>
            <p>Test the connection between frontend and backend services.</p>
            
            <button 
              onClick={testConnection}
              style={{
                padding: '12px 25px',
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                color: 'white',
                border: 'none',
                borderRadius: '25px',
                cursor: 'pointer',
                fontSize: '1rem',
                fontWeight: '600',
                transition: 'transform 0.3s ease'
              }}
              onMouseOver={(e) => e.target.style.transform = 'translateY(-2px)'}
              onMouseOut={(e) => e.target.style.transform = 'translateY(0)'}
            >
              🔗 Test Backend Connection
            </button>
            
            {message && (
              <div style={{
                marginTop: '20px',
                padding: '15px',
                backgroundColor: message.includes('failed') ? '#ffebee' : '#e8f5e8',
                border: `2px solid ${message.includes('failed') ? '#f44336' : '#4caf50'}`,
                borderRadius: '10px',
                fontWeight: '600'
              }}>
                {message.includes('failed') ? '❌' : '✅'} {message}
              </div>
            )}

            <div style={{ marginTop: '30px', padding: '20px', background: '#f8f9fa', borderRadius: '10px' }}>
              <h4>🎯 Ready for Hackathon!</h4>
              <ul style={{ textAlign: 'left', lineHeight: '1.8' }}>
                <li>✅ <strong>Go Backend</strong> - API server with MongoDB/MySQL</li>
                <li>✅ <strong>React Frontend</strong> - Modern UI with Vite</li>
                <li>✅ <strong>AI Agent System</strong> - LangChain + OpenAI tools</li>
                <li>✅ <strong>Site Generator</strong> - One-click website creation</li>
                <li>✅ <strong>Free APIs</strong> - Groq, HuggingFace alternatives</li>
                <li>✅ <strong>Database Support</strong> - MongoDB, MySQL, PostgreSQL</li>
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default App; 