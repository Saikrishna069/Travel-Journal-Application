import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("React Error Boundary Caught Error:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-slate-950 text-white flex items-center justify-center p-6 text-center">
          <div className="bg-slate-900 p-8 rounded-2xl border border-slate-800 max-w-md">
            <h2 className="text-xl font-bold text-teal-400 mb-2">✈️ Travel Journal Assistant</h2>
            <p className="text-sm text-slate-300 mb-4">Workspace is initializing. Reloading application state...</p>
            <button 
              onClick={() => { localStorage.clear(); window.location.reload(); }} 
              className="bg-teal-500 text-slate-950 font-bold px-4 py-2 rounded-xl text-xs"
            >
              Reset Session & Reload
            </button>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  </React.StrictMode>
);
