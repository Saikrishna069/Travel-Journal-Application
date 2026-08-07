import React, { useState, useEffect } from 'react';
import api from './api';
import ChatAssistant from './components/ChatAssistant';
import JournalManager from './components/JournalManager';
import ExpenseTracker from './components/ExpenseTracker';
import DestinationPlanner from './components/DestinationPlanner';
import { BookOpen, Sparkles, Wallet, Compass, LogOut, Compass as AppLogo, User, Lock, Mail } from 'lucide-react';

export default function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [authMode, setAuthMode] = useState('login');
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [activeTab, setActiveTab] = useState('journals');

  useEffect(() => {
    const checkSession = async () => {
      if (token) {
        try {
          await api.get('/auth/me');
        } catch (err) {
          localStorage.removeItem('token');
          setToken(null);
        }
      }
    };
    checkSession();
  }, [token]);

  const handleAuth = async (e) => {
    e.preventDefault();
    try {
      if (authMode === 'register') {
        const res = await api.post('/auth/register', { username, email, password });
        if (res.data.access_token) {
          localStorage.setItem('token', res.data.access_token);
          setToken(res.data.access_token);
        } else {
          alert('Registered successfully! Logging in...');
          const loginRes = await api.post('/auth/login', { username, password });
          localStorage.setItem('token', loginRes.data.access_token);
          setToken(loginRes.data.access_token);
        }
      } else {
        const res = await api.post('/auth/login', { username, password });
        localStorage.setItem('token', res.data.access_token);
        setToken(res.data.access_token);
      }
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message || 'Authentication failed.';
      alert(`Authentication Error: ${errorMsg}`);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
  };

  if (!token) {
    return (
      <div className="min-h-screen bg-[url('https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=2000&q=80')] bg-cover bg-fixed bg-center text-white flex items-center justify-center p-4 relative">
        <div className="absolute inset-0 bg-slate-950/80 backdrop-blur-sm"></div>
        <div className="bg-slate-900/90 backdrop-blur-xl p-8 rounded-3xl shadow-2xl w-full max-w-md border border-slate-700/60 relative z-10 overflow-hidden">
          <div className="flex flex-col items-center mb-6">
            <div className="p-3.5 bg-gradient-to-tr from-teal-500 to-emerald-400 rounded-2xl shadow-lg text-slate-950 mb-3">
              <AppLogo className="w-9 h-9" />
            </div>
            <h2 className="text-2xl font-black tracking-tight text-white">
              Travel Journal Assistant
            </h2>
            <p className="text-xs text-teal-300/90 font-medium mt-1">Smart Agentic Workspace</p>
          </div>

          <form onSubmit={handleAuth} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">Username</label>
              <div className="relative">
                <User className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
                <input
                  type="text"
                  className="w-full bg-slate-800/90 pl-10 pr-3 py-3 rounded-xl border border-slate-700 text-white focus:outline-none focus:border-teal-400 transition text-sm"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="e.g. Saikrishna"
                  required
                />
              </div>
            </div>

            {authMode === 'register' && (
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">Email</label>
                <div className="relative">
                  <Mail className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
                  <input
                    type="email"
                    className="w-full bg-slate-800/90 pl-10 pr-3 py-3 rounded-xl border border-slate-700 text-white focus:outline-none focus:border-teal-400 transition text-sm"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="user@example.com"
                    required
                  />
                </div>
              </div>
            )}

            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">Password</label>
              <div className="relative">
                <Lock className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
                <input
                  type="password"
                  className="w-full bg-slate-800/90 pl-10 pr-3 py-3 rounded-xl border border-slate-700 text-white focus:outline-none focus:border-teal-400 transition text-sm"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  required
                />
              </div>
            </div>

            <button
              type="submit"
              className="w-full bg-gradient-to-r from-teal-400 to-emerald-500 hover:from-teal-300 hover:to-emerald-400 py-3 rounded-xl font-bold text-slate-950 shadow-lg shadow-teal-500/20 transition transform active:scale-98 text-sm"
            >
              {authMode === 'login' ? 'Sign In to Workspace' : 'Create Free Account & Start Session'}
            </button>
          </form>

          <div className="text-center mt-6 border-t border-slate-700/50 pt-4">
            <button
              onClick={() => setAuthMode(authMode === 'login' ? 'register' : 'login')}
              className="text-xs font-semibold text-teal-400 hover:text-teal-300 transition"
            >
              {authMode === 'login' ? 'New user? Register account' : 'Already registered? Sign In'}
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[url('https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=2000&q=80')] bg-cover bg-fixed bg-center text-slate-100 flex flex-col font-sans relative">
      <div className="absolute inset-0 bg-slate-950/85 backdrop-blur-sm"></div>

      <header className="sticky top-0 z-50 bg-slate-900/90 backdrop-blur-md border-b border-slate-800/80 shadow-md">
        <div className="max-w-7xl mx-auto px-4 py-3 flex flex-wrap justify-between items-center gap-4 relative z-10">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-gradient-to-tr from-teal-500 to-emerald-400 rounded-2xl text-slate-950 shadow-md">
              <AppLogo className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-lg font-black tracking-tight text-white">Travel Journal Assistant</h1>
              <span className="text-[10px] text-teal-400 font-mono tracking-widest uppercase">Smart Agentic Workspace</span>
            </div>
          </div>

          <nav className="flex items-center gap-1 bg-slate-800/90 p-1.5 rounded-2xl border border-slate-700/60 shadow-inner">
            <button
              onClick={() => setActiveTab('journals')}
              className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold transition-all ${
                activeTab === 'journals'
                  ? 'bg-gradient-to-r from-teal-400 to-emerald-500 text-slate-950 shadow-md shadow-teal-500/20'
                  : 'text-slate-400 hover:text-white hover:bg-slate-700/50'
              }`}
            >
              <BookOpen className="w-4 h-4" />
              <span>Journals</span>
            </button>

            <button
              onClick={() => setActiveTab('ai')}
              className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold transition-all ${
                activeTab === 'ai'
                  ? 'bg-gradient-to-r from-teal-400 to-emerald-500 text-slate-950 shadow-md shadow-teal-500/20'
                  : 'text-slate-400 hover:text-white hover:bg-slate-700/50'
              }`}
            >
              <Sparkles className="w-4 h-4" />
              <span>AI Chat</span>
            </button>

            <button
              onClick={() => setActiveTab('expenses')}
              className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold transition-all ${
                activeTab === 'expenses'
                  ? 'bg-gradient-to-r from-teal-400 to-emerald-500 text-slate-950 shadow-md shadow-teal-500/20'
                  : 'text-slate-400 hover:text-white hover:bg-slate-700/50'
              }`}
            >
              <Wallet className="w-4 h-4" />
              <span>Expenses</span>
            </button>

            <button
              onClick={() => setActiveTab('planner')}
              className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold transition-all ${
                activeTab === 'planner'
                  ? 'bg-gradient-to-r from-teal-400 to-emerald-500 text-slate-950 shadow-md shadow-teal-500/20'
                  : 'text-slate-400 hover:text-white hover:bg-slate-700/50'
              }`}
            >
              <Compass className="w-4 h-4" />
              <span>Planner</span>
            </button>
          </nav>

          <button
            onClick={handleLogout}
            className="flex items-center gap-1.5 bg-rose-500/10 hover:bg-rose-500/20 border border-rose-500/30 text-rose-400 px-3.5 py-2 rounded-xl text-xs font-semibold transition"
          >
            <LogOut className="w-3.5 h-3.5" />
            <span>Sign Out</span>
          </button>
        </div>
      </header>

      <main className="flex-1 max-w-7xl mx-auto w-full p-4 md:p-8 relative z-10">
        {activeTab === 'journals' && <JournalManager />}
        {activeTab === 'ai' && <ChatAssistant />}
        {activeTab === 'expenses' && <ExpenseTracker />}
        {activeTab === 'planner' && <DestinationPlanner />}
      </main>
    </div>
  );
}
