import React, { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

class GlobalErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("CodeRescue UI Error Caught:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{
          minHeight: '100vh',
          backgroundColor: '#090d16',
          color: '#f8fafc',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '24px',
          fontFamily: 'system-ui, -apple-system, sans-serif'
        }}>
          <div style={{
            background: '#0f172a',
            border: '1px solid #ef4444',
            borderRadius: '12px',
            padding: '32px',
            maxWidth: '600px',
            textAlign: 'center',
            boxShadow: '0 8px 32px rgba(239, 68, 68, 0.2)'
          }}>
            <h1 style={{ fontSize: '24px', color: '#ef4444', margin: '0 0 12px' }}>
              🛡️ CodeRescue AI Interface Recovery
            </h1>
            <p style={{ color: '#cbd5e1', fontSize: '14px', margin: '0 0 16px' }}>
              An unexpected render error occurred. Click below to refresh your workspace.
            </p>
            <pre style={{
              background: '#060a12',
              color: '#fca5a5',
              padding: '12px',
              borderRadius: '6px',
              fontSize: '12px',
              textAlign: 'left',
              overflowX: 'auto',
              marginBottom: '20px'
            }}>
              {this.state.error?.message || "Unknown error"}
            </pre>
            <div style={{ display: 'flex', gap: '12px', justifyContent: 'center' }}>
              <button
                onClick={() => window.location.reload()}
                style={{
                  background: '#0284c7',
                  color: '#fff',
                  border: 'none',
                  padding: '10px 20px',
                  borderRadius: '6px',
                  fontWeight: '600',
                  cursor: 'pointer'
                }}
              >
                🔄 Refresh Application
              </button>
              <button
                onClick={() => {
                  localStorage.removeItem('coderescue_user');
                  window.location.reload();
                }}
                style={{
                  background: '#1e293b',
                  color: '#94a3b8',
                  border: '1px solid #334155',
                  padding: '10px 20px',
                  borderRadius: '6px',
                  fontWeight: '600',
                  cursor: 'pointer'
                }}
              >
                Reset Session & Login
              </button>
            </div>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <GlobalErrorBoundary>
      <App />
    </GlobalErrorBoundary>
  </StrictMode>,
)
