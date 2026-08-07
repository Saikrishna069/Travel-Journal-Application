import React, { useState, useEffect } from 'react';
import api from '../api';
import { PlusCircle, MapPin, Calendar, Trash2, Image as ImageIcon, BookOpen, Share2, Map, Check } from 'lucide-react';

export default function JournalManager() {
  const [journals, setJournals] = useState([]);
  const [title, setTitle] = useState('');
  const [destination, setDestination] = useState('');
  const [content, setContent] = useState('');
  const [file, setFile] = useState(null);
  const [copiedId, setCopiedId] = useState(null);

  const fetchJournals = async () => {
    try {
      const res = await api.get('/journals/');
      setJournals(Array.isArray(res.data) ? res.data : []);
    } catch (err) {
      console.error("Error fetching journals:", err);
      setJournals([]);
    }
  };

  useEffect(() => {
    fetchJournals();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    let imageUrl = '';
    try {
      if (file) {
        const formData = new FormData();
        formData.append('file', file);
        const uploadRes = await api.post('/journals/upload-image', formData);
        imageUrl = uploadRes.data.image_url || '';
      }

      await api.post('/journals/', { title, destination, content, image_url: imageUrl });
      setTitle(''); setDestination(''); setContent(''); setFile(null);
      fetchJournals();
    } catch (err) {
      alert("Failed to save journal entry. Please check backend connection.");
    }
  };

  const handleDelete = async (id) => {
    try {
      await api.delete(`/journals/${id}`);
      fetchJournals();
    } catch (err) {
      alert("Failed to delete journal entry.");
    }
  };

  const handleShare = (journal) => {
    const shareText = `🌍 Travel Journal: ${journal.title}\n📍 Location: ${journal.destination}\n📖 Reflection: ${journal.content}\n\nShared via AI Travel Journal Assistant`;
    navigator.clipboard.writeText(shareText);
    setCopiedId(journal._id);
    alert(`Copied "${journal.title}" travel story to clipboard! Ready to share with friends.`);
    setTimeout(() => setCopiedId(null), 3000);
  };

  const safeJournals = Array.isArray(journals) ? journals : [];

  return (
    <div className="space-y-8">
      {/* Log Trip Form */}
      <form onSubmit={handleSubmit} className="bg-slate-800/80 backdrop-blur-md p-6 rounded-2xl border border-slate-700/60 shadow-xl space-y-4">
        <div className="flex items-center gap-2 text-teal-400 font-bold text-lg border-b border-slate-700/60 pb-3">
          <PlusCircle className="w-5 h-5" />
          <h3>Log Trip & Memories</h3>
        </div>

        <div className="grid md:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Journal Title</label>
            <input 
              type="text" 
              placeholder="e.g. Exploring Historic Kyoto" 
              value={title} 
              onChange={(e)=>setTitle(e.target.value)} 
              required 
              className="w-full bg-slate-900/80 p-3 rounded-xl border border-slate-700 text-white focus:outline-none focus:border-teal-400 transition text-sm" 
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Destination Name</label>
            <input 
              type="text" 
              placeholder="e.g. Kyoto, Japan" 
              value={destination} 
              onChange={(e)=>setDestination(e.target.value)} 
              required 
              className="w-full bg-slate-900/80 p-3 rounded-xl border border-slate-700 text-white focus:outline-none focus:border-teal-400 transition text-sm" 
            />
          </div>
        </div>

        <div>
          <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Thoughts, Reflections & Highlights</label>
          <textarea 
            placeholder="Write your notes, memories, and stories..." 
            value={content} 
            onChange={(e)=>setContent(e.target.value)} 
            required 
            className="w-full bg-slate-900/80 p-3 rounded-xl border border-slate-700 text-white focus:outline-none focus:border-teal-400 transition text-sm h-28" 
          />
        </div>

        <div className="flex flex-wrap justify-between items-center gap-4 pt-2">
          <div className="flex items-center gap-2 bg-slate-900/60 px-3 py-2 rounded-xl border border-slate-700/60 text-xs text-slate-300">
            <ImageIcon className="w-4 h-4 text-teal-400" />
            <span className="text-xs text-slate-400 font-medium">Attach Photo:</span>
            <input type="file" onChange={(e)=>setFile(e.target.files[0])} className="text-xs text-slate-400 file:mr-2 file:py-1 file:px-2 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-teal-500/20 file:text-teal-300" />
          </div>

          <button type="submit" className="bg-gradient-to-r from-teal-400 to-emerald-500 hover:from-teal-300 hover:to-emerald-400 text-slate-950 font-bold px-6 py-2.5 rounded-xl shadow-lg shadow-teal-500/20 transition transform active:scale-95 text-sm">
            Save Trip Journal
          </button>
        </div>
      </form>

      {/* Memory Logs & Journey Map */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h4 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-teal-400" />
            <span>Your Journey Log & Memories</span>
          </h4>
          <span className="bg-slate-800 text-teal-300 text-xs font-bold px-3 py-1 rounded-full border border-slate-700">
            {safeJournals.length} Saved Entries
          </span>
        </div>

        {safeJournals.length === 0 ? (
          <div className="bg-slate-800/40 p-8 rounded-2xl border border-slate-700/40 text-center text-slate-400 text-sm">
            No journal entries recorded yet. Log your first trip using the form above!
          </div>
        ) : (
          <div className="grid md:grid-cols-2 gap-6">
            {safeJournals.map((j) => (
              <div key={j._id || Math.random()} className="bg-slate-800/80 backdrop-blur-md p-5 rounded-2xl border border-slate-700/60 shadow-xl flex flex-col justify-between hover:border-slate-600 transition group space-y-4">
                <div>
                  <div className="flex justify-between items-start gap-2 mb-2">
                    <h5 className="text-lg font-bold text-teal-300 group-hover:text-teal-200 transition">{j.title}</h5>
                    <div className="flex items-center gap-1">
                      <button 
                        onClick={() => handleShare(j)} 
                        title="Share Entry with Friends" 
                        className="text-slate-400 hover:text-teal-300 p-1.5 rounded-lg hover:bg-teal-500/10 transition"
                      >
                        {copiedId === j._id ? <Check className="w-4 h-4 text-emerald-400" /> : <Share2 className="w-4 h-4" />}
                      </button>
                      {j._id && (
                        <button 
                          onClick={()=>handleDelete(j._id)} 
                          title="Delete Entry" 
                          className="text-slate-500 hover:text-rose-400 p-1.5 rounded-lg hover:bg-rose-500/10 transition"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      )}
                    </div>
                  </div>

                  <div className="flex items-center gap-4 text-xs text-slate-400 mb-3">
                    <span className="flex items-center gap-1 text-teal-400/90 font-medium">
                      <MapPin className="w-3.5 h-3.5" />
                      {j.destination}
                    </span>
                    <span className="flex items-center gap-1 font-mono">
                      <Calendar className="w-3.5 h-3.5" />
                      {j.created_at ? new Date(j.created_at).toLocaleDateString() : 'Recent'}
                    </span>
                  </div>

                  <p className="text-sm text-slate-200 leading-relaxed mb-3">{j.content}</p>

                  {/* Attached Photo */}
                  {j.image_url && (
                    <img 
                      src={`${import.meta.env.VITE_API_URL || 'https://travel-journal-application-ysdk.onrender.com'}${j.image_url}`} 
                      alt="Travel Memory" 
                      className="w-full h-48 object-cover rounded-xl border border-slate-700/50 mb-3" 
                    />
                  )}

                  {/* OpenStreetMap Interactive Location Map */}
                  <div className="rounded-xl overflow-hidden border border-slate-700/60 bg-slate-900/90 p-2">
                    <div className="flex items-center gap-1.5 text-xs text-teal-400 mb-2 font-medium">
                      <Map className="w-3.5 h-3.5" />
                      <span>Interactive Journey Map ({j.destination}):</span>
                    </div>
                    <iframe
                      title={`Map for ${j.destination}`}
                      width="100%"
                      height="150"
                      className="rounded-lg border-0"
                      loading="lazy"
                      src={`https://maps.google.com/maps?q=${encodeURIComponent(j.destination)}&t=&z=11&ie=UTF8&iwloc=&output=embed`}
                    ></iframe>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
