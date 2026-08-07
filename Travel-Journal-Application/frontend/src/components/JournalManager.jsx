import React, { useState, useEffect } from 'react';
import api from '../api';
import { PlusCircle, MapPin, Calendar, Trash2, Image as ImageIcon, BookOpen, Share2, Map, Check, FileText, Sparkles, Navigation } from 'lucide-react';

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
    const shareText = `🌍 Travel Journal: ${journal.title}\n📍 Destination: ${journal.destination}\n📖 Highlights & Notes: ${journal.content}\n\nShared via AI Travel Journal Assistant`;
    navigator.clipboard.writeText(shareText);
    setCopiedId(journal._id);
    alert(`Copied "${journal.title}" travel story to clipboard!`);
    setTimeout(() => setCopiedId(null), 3000);
  };

  const safeJournals = Array.isArray(journals) ? journals : [];

  return (
    <div className="space-y-8">
      {/* Feature 1, 2, 3: Log Trips, Add Photos, Write Notes */}
      <form onSubmit={handleSubmit} className="bg-slate-800/80 backdrop-blur-md p-6 rounded-3xl border border-slate-700/60 shadow-2xl space-y-6">
        <div className="flex justify-between items-center border-b border-slate-700/60 pb-4">
          <div className="flex items-center gap-2.5 text-teal-400 font-bold text-lg">
            <div className="p-2 bg-teal-500/10 rounded-xl">
              <PlusCircle className="w-6 h-6 text-teal-400" />
            </div>
            <div>
              <h3 className="text-white text-lg font-extrabold">Log New Travel Experience</h3>
              <p className="text-xs text-slate-400 font-normal">Capture destinations, photos, notes, and map coordinates</p>
            </div>
          </div>
          <span className="bg-teal-500/10 text-teal-300 text-xs font-semibold px-3 py-1 rounded-full border border-teal-500/20 hidden sm:inline">
            5 Core Features Integrated
          </span>
        </div>

        <div className="grid md:grid-cols-2 gap-4">
          {/* Feature 1: Log Trips - Titles & Destination */}
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5 flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5 text-teal-400" />
              <span>1. Trip Highlight Title</span>
            </label>
            <input 
              type="text" 
              placeholder="e.g. Sunset at Charminar & Bazaar Tour" 
              value={title} 
              onChange={(e)=>setTitle(e.target.value)} 
              required 
              className="w-full bg-slate-900/80 px-4 py-3 rounded-xl border border-slate-700 text-white focus:outline-none focus:border-teal-400 transition text-sm" 
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5 flex items-center gap-1.5">
              <MapPin className="w-3.5 h-3.5 text-teal-400" />
              <span>Destination Name & Location</span>
            </label>
            <input 
              type="text" 
              placeholder="e.g. Hyderabad, Telangana, India" 
              value={destination} 
              onChange={(e)=>setDestination(e.target.value)} 
              required 
              className="w-full bg-slate-900/80 px-4 py-3 rounded-xl border border-slate-700 text-white focus:outline-none focus:border-teal-400 transition text-sm" 
            />
          </div>
        </div>

        {/* Feature 3: Write Notes - Thoughts, Reflections & Stories */}
        <div>
          <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5 flex items-center gap-1.5">
            <FileText className="w-3.5 h-3.5 text-teal-400" />
            <span>3. Write Notes (Thoughts, Reflections & Stories)</span>
          </label>
          <textarea 
            placeholder="Capture your personal travel memories, cultural highlights, and stories..." 
            value={content} 
            onChange={(e)=>setContent(e.target.value)} 
            required 
            className="w-full bg-slate-900/80 px-4 py-3 rounded-xl border border-slate-700 text-white focus:outline-none focus:border-teal-400 transition text-sm h-32 leading-relaxed" 
          />
        </div>

        {/* Feature 2: Add Photos */}
        <div className="flex flex-wrap justify-between items-center gap-4 pt-2 border-t border-slate-700/50">
          <div className="flex items-center gap-2 bg-slate-900/80 px-4 py-2.5 rounded-xl border border-slate-700 text-xs text-slate-300">
            <ImageIcon className="w-4 h-4 text-teal-400 shrink-0" />
            <span className="font-semibold text-slate-300">2. Add Photos:</span>
            <input 
              type="file" 
              onChange={(e)=>setFile(e.target.files[0])} 
              className="text-xs text-slate-400 file:mr-2 file:py-1 file:px-2.5 file:rounded-lg file:border-0 file:text-xs file:font-bold file:bg-teal-500/20 file:text-teal-300" 
            />
          </div>

          <button type="submit" className="bg-gradient-to-r from-teal-400 to-emerald-500 hover:from-teal-300 hover:to-emerald-400 text-slate-950 font-extrabold px-7 py-3 rounded-xl shadow-lg shadow-teal-500/20 transition transform active:scale-95 text-sm flex items-center gap-2">
            <span>Save Travel Entry</span>
          </button>
        </div>
      </form>

      {/* Feature 4 & 5: Map Locations & Share Entries Display */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h4 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-teal-400" />
            <span>Recorded Trip Memories ({safeJournals.length})</span>
          </h4>
        </div>

        {safeJournals.length === 0 ? (
          <div className="bg-slate-800/40 p-10 rounded-3xl border border-slate-700/40 text-center text-slate-400 text-sm space-y-2">
            <Navigation className="w-8 h-8 text-teal-400/50 mx-auto animate-pulse" />
            <p className="font-semibold">No travel entries logged yet.</p>
            <p className="text-xs text-slate-500">Log your first trip using the form above to view your memories, attached photos, interactive location maps, and shareable stories!</p>
          </div>
        ) : (
          <div className="grid md:grid-cols-2 gap-6">
            {safeJournals.map((j) => (
              <div key={j._id || Math.random()} className="bg-slate-800/80 backdrop-blur-md p-6 rounded-3xl border border-slate-700/60 shadow-xl flex flex-col justify-between hover:border-slate-600 transition group space-y-4">
                <div>
                  <div className="flex justify-between items-start gap-2 mb-3">
                    <h5 className="text-lg font-bold text-teal-300 group-hover:text-teal-200 transition">{j.title}</h5>
                    <div className="flex items-center gap-1.5">
                      {/* Feature 5: Share Entries */}
                      <button 
                        onClick={() => handleShare(j)} 
                        title="5. Share Entry with Friends (1-Click Clipboard)" 
                        className="flex items-center gap-1 bg-teal-500/10 hover:bg-teal-500/20 border border-teal-500/30 text-teal-300 px-2.5 py-1.5 rounded-lg text-xs font-semibold transition"
                      >
                        {copiedId === j._id ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Share2 className="w-3.5 h-3.5" />}
                        <span className="hidden sm:inline">Share</span>
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

                  <div className="flex items-center gap-4 text-xs text-slate-400 mb-3 bg-slate-900/60 p-2.5 rounded-xl border border-slate-800">
                    <span className="flex items-center gap-1 text-teal-400 font-semibold">
                      <MapPin className="w-3.5 h-3.5" />
                      {j.destination}
                    </span>
                    <span className="flex items-center gap-1 font-mono text-slate-400">
                      <Calendar className="w-3.5 h-3.5" />
                      {j.created_at ? new Date(j.created_at).toLocaleDateString() : 'Recent'}
                    </span>
                  </div>

                  <p className="text-sm text-slate-200 leading-relaxed mb-4 whitespace-pre-line">{j.content}</p>

                  {/* Feature 2: Added Photos */}
                  {j.image_url && (
                    <div className="mb-4">
                      <span className="text-xs text-slate-400 font-semibold block mb-1">Attached Travel Photo:</span>
                      <img 
                        src={`${import.meta.env.VITE_API_URL || 'https://travel-journal-application-ysdk.onrender.com'}${j.image_url}`} 
                        alt="Travel Memory" 
                        className="w-full h-52 object-cover rounded-2xl border border-slate-700/50 shadow-md" 
                      />
                    </div>
                  )}

                  {/* Feature 4: Map Locations (Google Maps Embed) */}
                  <div className="rounded-2xl overflow-hidden border border-slate-700/60 bg-slate-900/90 p-2.5">
                    <div className="flex items-center gap-1.5 text-xs text-teal-400 mb-2 font-bold">
                      <Map className="w-3.5 h-3.5" />
                      <span>4. Map Locations ({j.destination}):</span>
                    </div>
                    <iframe
                      title={`Map for ${j.destination}`}
                      width="100%"
                      height="160"
                      className="rounded-xl border-0"
                      loading="lazy"
                      src={`https://maps.google.com/maps?q=${encodeURIComponent(j.destination)}&t=&z=12&ie=UTF8&iwloc=&output=embed`}
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
