import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    console.error("Error Boundary Caught:", error);
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("React Error Boundary Details:");
    console.error("Error:", error);
    console.error("Error Info:", errorInfo);
    console.error("Stack:", error?.stack);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-slate-950 text-white flex items-center justify-center p-6 text-center">
          <div className="bg-slate-900 p-8 rounded-2xl border border-slate-800 max-w-md">
            <h2 className="text-xl font-bold text-teal-400 mb-2">✈️ Travel Journal Assistant</h2>
            <p className="text-sm text-slate-300 mb-4">
              Error loading application. 
              <br />
              <span className="text-xs text-red-400 block mt-2 font-mono break-words">
                {this.state.error?.message || "Unknown error"}
              </span>
            </p>
            <div className="space-y-2">
              <button 
                onClick={() => { 
                  localStorage.clear(); 
                  window.location.reload(); 
                }} 
                className="w-full bg-teal-500 hover:bg-teal-600 text-slate-950 font-bold px-4 py-2 rounded-xl text-xs transition"
              >
                Reset Session & Reload
              </button>
              <button 
                onClick={() => { 
                  window.location.href = 'https://github.com/Saikrishna069/Travel-Journal-Application';
                }} 
                className="w-full bg-slate-700 hover:bg-slate-600 text-white font-bold px-4 py-2 rounded-xl text-xs transition"
              >
                Check GitHub
              </button>
            </div>
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
