import React, { useState, useEffect } from 'react';
import api from '../api';
import { PlusCircle, MapPin, Calendar, Trash2, Image as ImageIcon, BookOpen } from 'lucide-react';

export default function JournalManager() {
  const [journals, setJournals] = useState([]);
  const [title, setTitle] = useState('');
  const [destination, setDestination] = useState('');
  const [content, setContent] = useState('');
  const [file, setFile] = useState(null);

  const fetchJournals = async () => {
    try {
      const res = await api.get('/journals/');
      setJournals(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchJournals();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    let imageUrl = '';
    if (file) {
      const formData = new FormData();
      formData.append('file', file);
      const uploadRes = await api.post('/journals/upload-image', formData);
      imageUrl = uploadRes.data.image_url;
    }

    await api.post('/journals/', { title, destination, content, image_url: imageUrl });
    setTitle(''); setDestination(''); setContent(''); setFile(null);
    fetchJournals();
  };

  const handleDelete = async (id) => {
    await api.delete(`/journals/${id}`);
    fetchJournals();
  };

  return (
    <div className="space-y-8">
      <form onSubmit={handleSubmit} className="bg-slate-800/80 backdrop-blur-md p-6 rounded-2xl border border-slate-700/60 shadow-xl space-y-4">
        <div className="flex items-center gap-2 text-teal-400 font-bold text-lg border-b border-slate-700/60 pb-3">
          <PlusCircle className="w-5 h-5" />
          <h3>Create New Journal Log</h3>
        </div>

        <div className="grid md:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Journal Title</label>
            <input 
              type="text" 
              placeholder="e.g. Sunset at Beach" 
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
          <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Experience & Reflections</label>
          <textarea 
            placeholder="Write your personal memories and thoughts..." 
            value={content} 
            onChange={(e)=>setContent(e.target.value)} 
            required 
            className="w-full bg-slate-900/80 p-3 rounded-xl border border-slate-700 text-white focus:outline-none focus:border-teal-400 transition text-sm h-28" 
          />
        </div>

        <div className="flex flex-wrap justify-between items-center gap-4 pt-2">
          <div className="flex items-center gap-2 bg-slate-900/60 px-3 py-2 rounded-xl border border-slate-700/60 text-xs text-slate-300">
            <ImageIcon className="w-4 h-4 text-teal-400" />
            <input type="file" onChange={(e)=>setFile(e.target.files[0])} className="text-xs text-slate-400 file:mr-2 file:py-1 file:px-2 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-teal-500/20 file:text-teal-300" />
          </div>

          <button type="submit" className="bg-gradient-to-r from-teal-400 to-emerald-500 hover:from-teal-300 hover:to-emerald-400 text-slate-950 font-bold px-6 py-2.5 rounded-xl shadow-lg shadow-teal-500/20 transition transform active:scale-95 text-sm">
            Save Journal Log
          </button>
        </div>
      </form>

      <div>
        <div className="flex items-center justify-between mb-4">
          <h4 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-teal-400" />
            <span>Your Travel Memory Log</span>
          </h4>
          <span className="bg-slate-800 text-teal-300 text-xs font-bold px-3 py-1 rounded-full border border-slate-700">
            {journals.length} Saved Entries
          </span>
        </div>

        {journals.length === 0 ? (
          <div className="bg-slate-800/40 p-8 rounded-2xl border border-slate-700/40 text-center text-slate-400 text-sm">
            No journal entries yet. Create your first travel log using the form above!
          </div>
        ) : (
          <div className="grid md:grid-cols-2 gap-6">
            {journals.map((j) => (
              <div key={j._id} className="bg-slate-800/80 backdrop-blur-md p-5 rounded-2xl border border-slate-700/60 shadow-xl flex flex-col justify-between hover:border-slate-600 transition group">
                <div>
                  <div className="flex justify-between items-start gap-2 mb-2">
                    <h5 className="text-lg font-bold text-teal-300 group-hover:text-teal-200 transition">{j.title}</h5>
                    <button onClick={()=>handleDelete(j._id)} className="text-slate-500 hover:text-rose-400 p-1.5 rounded-lg hover:bg-rose-500/10 transition">
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>

                  <div className="flex items-center gap-4 text-xs text-slate-400 mb-3">
                    <span className="flex items-center gap-1 text-teal-400/90 font-medium">
                      <MapPin className="w-3.5 h-3.5" />
                      {j.destination}
                    </span>
                    <span className="flex items-center gap-1 font-mono">
                      <Calendar className="w-3.5 h-3.5" />
                      {new Date(j.created_at).toLocaleDateString()}
                    </span>
                  </div>

                  <p className="text-sm text-slate-200 leading-relaxed mb-4">{j.content}</p>
                </div>

                {j.image_url && (
                  <img src={`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}${j.image_url}`} alt="Travel" className="w-full h-48 object-cover rounded-xl border border-slate-700/50 mt-2" />
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
