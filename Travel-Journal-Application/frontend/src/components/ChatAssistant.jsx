import React, { useState } from 'react';
import api from '../api';
import { Bot, Send, User, Sparkles } from 'lucide-react';

export default function ChatAssistant() {
  const [messages, setMessages] = useState([
    { sender: 'agent', text: 'Hello! I am your AI Travel Assistant. Ask me for custom travel itineraries, historical attraction details, local food spots, or packing checklists!' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMsg = { sender: 'user', text: input };
    setMessages((prev) => [...prev, userMsg]);
    const currentInput = input;
    setInput('');
    setLoading(true);

    try {
      const res = await api.post('/ai/chat', { message: currentInput });
      setMessages((prev) => [...prev, { sender: 'agent', text: res.data.reply }]);
    } catch (err) {
      setMessages((prev) => [...prev, { sender: 'agent', text: 'Error contacting AI Travel Agent. Please verify server connection.' }]);
    } finally {
      setLoading(false);
    }
  };

  const safeMessages = Array.isArray(messages) ? messages : [];

  return (
    <div className="bg-slate-800/80 backdrop-blur-md border border-slate-700/60 rounded-2xl shadow-2xl p-5 flex flex-col h-[580px]">
      <div className="flex items-center justify-between border-b border-slate-700/60 pb-3 mb-4">
        <div className="flex items-center gap-2">
          <div className="p-2 bg-teal-500/20 text-teal-300 rounded-xl">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <h3 className="font-bold text-white text-base">AI Agentic Travel Assistant</h3>
            <span className="text-[10px] text-teal-400 font-mono">Powered by FastAPI & Natural Language LLM</span>
          </div>
        </div>
        <div className="flex items-center gap-1.5 text-xs text-teal-300 bg-teal-500/10 border border-teal-500/20 px-3 py-1 rounded-full">
          <Sparkles className="w-3.5 h-3.5 animate-pulse" />
          <span>Active Agent</span>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto space-y-3 p-3 bg-slate-900/90 rounded-xl border border-slate-800/80">
        {safeMessages.map((m, idx) => (
          <div key={idx} className={`flex items-start gap-2.5 max-w-xl ${m.sender === 'user' ? 'ml-auto flex-row-reverse' : ''}`}>
            <div className={`p-2 rounded-xl text-xs ${m.sender === 'user' ? 'bg-teal-500 text-slate-950' : 'bg-slate-800 text-teal-300 border border-slate-700'}`}>
              {m.sender === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
            </div>
            <div className={`p-3.5 rounded-2xl text-xs md:text-sm leading-relaxed ${
              m.sender === 'user' 
                ? 'bg-gradient-to-r from-teal-400 to-emerald-500 text-slate-950 font-medium shadow-md' 
                : 'bg-slate-800/90 text-slate-200 border border-slate-700/60 shadow-md'
            }`}>
              {m.text}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex items-center gap-2 text-xs text-slate-400 p-2">
            <Bot className="w-4 h-4 animate-bounce text-teal-400" />
            <span>AI Agent is generating travel suggestions...</span>
          </div>
        )}
      </div>

      <form onSubmit={sendMessage} className="flex gap-2 mt-4">
        <input 
          type="text" 
          value={input} 
          onChange={(e)=>setInput(e.target.value)} 
          placeholder="Ask for travel ideas, local dishes, or hotel tips..." 
          className="flex-1 bg-slate-900/80 px-4 py-3 rounded-xl border border-slate-700 text-white focus:outline-none focus:border-teal-400 transition text-sm" 
        />
        <button type="submit" className="bg-gradient-to-r from-teal-400 to-emerald-500 hover:from-teal-300 hover:to-emerald-400 text-slate-950 font-bold px-5 py-3 rounded-xl flex items-center gap-1.5 transition">
          <Send className="w-4 h-4" />
          <span className="hidden sm:inline">Send</span>
        </button>
      </form>
    </div>
  );
}
