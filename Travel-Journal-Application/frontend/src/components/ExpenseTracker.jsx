import React, { useState, useEffect } from 'react';
import api from '../api';
import { Wallet, PlusCircle, RotateCcw, FolderArchive, DollarSign, Tag, FileText, Trash2 } from 'lucide-react';

export default function ExpenseTracker() {
  const [expenses, setExpenses] = useState([]);
  const [archives, setArchives] = useState([]);
  const [category, setCategory] = useState('');
  const [amount, setAmount] = useState('');
  const [description, setDescription] = useState('');

  const fetchExpenses = async () => {
  try {
    const res = await api.get('/expenses/');
    // Ensure data is always an array
    setExpenses(Array.isArray(res.data) ? res.data : []);
    } catch (err) {
    console.error('Error fetching expenses:', err);
    setExpenses([]);
    }
  };

  const fetchArchives = async () => {
  try {
    const res = await api.get('/expenses/archives');
    // Ensure data is always an array
    setArchives(Array.isArray(res.data) ? res.data : []);
    } catch (err) {
    console.error('Error fetching archives:', err);
    setArchives([]);
    }
  };

  useEffect(() => {
    fetchExpenses();
    fetchArchives();
  }, []);

  const handleAdd = async (e) => {
    e.preventDefault();
    await api.post('/expenses/', { category, amount: parseFloat(amount), description });
    setCategory(''); setAmount(''); setDescription('');
    fetchExpenses();
  };

  const handleResetAndSave = async () => {
    if (expenses.length === 0) {
      alert("No active expenses to reset.");
      return;
    }
    if (!window.confirm("Are you sure you want to reset current expenses and save them as a Trip record?")) return;

    try {
      const res = await api.post('/expenses/reset');
      alert(`Saved as ${res.data.trip_name} and cleared current expenses!`);
      fetchExpenses();
      fetchArchives();
    } catch (err) {
      alert("Failed to reset expenses.");
    }
  };

  const handleDeleteArchive = async (archiveId) => {
    if (!window.confirm("Are you sure you want to delete this saved trip history?")) return;
    try {
      await api.delete(`/expenses/archives/${archiveId}`);
      fetchArchives();
    } catch (err) {
      alert("Failed to delete trip record.");
    }
  };

  const total = expenses.reduce((acc, curr) => acc + curr.amount, 0);

  return (
    <div className="space-y-8">
      <form onSubmit={handleAdd} className="bg-slate-800/80 backdrop-blur-md p-6 rounded-2xl border border-slate-700/60 shadow-xl space-y-4">
        <div className="flex items-center gap-2 text-teal-400 font-bold text-lg border-b border-slate-700/60 pb-3">
          <PlusCircle className="w-5 h-5" />
          <h3>Log Travel Expenditure</h3>
        </div>

        <div className="grid md:grid-cols-3 gap-4">
          <div>
            <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Category</label>
            <div className="relative">
              <Tag className="w-4 h-4 text-slate-400 absolute left-3 top-3.5" />
              <input 
                type="text" 
                placeholder="e.g. Food, Flight, Hotel" 
                value={category} 
                onChange={(e)=>setCategory(e.target.value)} 
                required 
                className="w-full bg-slate-900/80 pl-10 pr-3 py-2.5 rounded-xl border border-slate-700 text-white focus:outline-none focus:border-teal-400 transition text-sm" 
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Amount ($)</label>
            <div className="relative">
              <DollarSign className="w-4 h-4 text-slate-400 absolute left-3 top-3.5" />
              <input 
                type="number" 
                step="0.01" 
                placeholder="0.00" 
                value={amount} 
                onChange={(e)=>setAmount(e.target.value)} 
                required 
                className="w-full bg-slate-900/80 pl-10 pr-3 py-2.5 rounded-xl border border-slate-700 text-white focus:outline-none focus:border-teal-400 transition text-sm" 
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">Description</label>
            <div className="relative">
              <FileText className="w-4 h-4 text-slate-400 absolute left-3 top-3.5" />
              <input 
                type="text" 
                placeholder="Details of payment" 
                value={description} 
                onChange={(e)=>setDescription(e.target.value)} 
                required 
                className="w-full bg-slate-900/80 pl-10 pr-3 py-2.5 rounded-xl border border-slate-700 text-white focus:outline-none focus:border-teal-400 transition text-sm" 
              />
            </div>
          </div>
        </div>

        <button type="submit" className="bg-gradient-to-r from-teal-400 to-emerald-500 hover:from-teal-300 hover:to-emerald-400 text-slate-950 font-bold px-6 py-2.5 rounded-xl shadow-lg shadow-teal-500/20 transition text-sm">
          Add Expense Record
        </button>
      </form>

      <div className="bg-slate-800/80 backdrop-blur-md p-6 rounded-2xl border border-slate-700/60 shadow-xl space-y-4">
        <div className="flex flex-wrap justify-between items-center border-b border-slate-700/60 pb-4 gap-4">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-teal-500/10 rounded-xl text-teal-400 border border-teal-500/20">
              <Wallet className="w-6 h-6" />
            </div>
            <div>
              <h4 className="text-xl font-bold text-teal-300">Active Trip Total: ${total.toFixed(2)}</h4>
              <p className="text-xs text-slate-400">Current ongoing expenditures</p>
            </div>
          </div>

          {expenses.length > 0 && (
            <button 
              onClick={handleResetAndSave} 
              className="flex items-center gap-2 bg-gradient-to-r from-amber-400 to-orange-500 hover:from-amber-300 hover:to-orange-400 text-slate-950 font-bold px-4 py-2.5 rounded-xl text-xs shadow-md transition"
            >
              <RotateCcw className="w-4 h-4" />
              <span>Reset & Save Trip Expenses</span>
            </button>
          )}
        </div>

        {expenses.length === 0 ? (
          <p className="text-sm text-slate-400 italic py-2">No active expenses recorded. Add expenditures above or view saved trip records below.</p>
        ) : (
          <div className="divide-y divide-slate-700/60">
            {expenses.map((e) => (
              <div key={e._id} className="py-3 flex justify-between items-center text-sm">
                <div>
                  <span className="font-bold text-teal-300 mr-2">{e.category}:</span>
                  <span className="text-slate-300">{e.description}</span>
                </div>
                <span className="font-bold text-white text-base">${e.amount.toFixed(2)}</span>
              </div>
            ))}
          </div>
        )}
      </div>

      {archives.length > 0 && (
        <div className="bg-slate-800/80 backdrop-blur-md p-6 rounded-2xl border border-slate-700/60 shadow-xl space-y-4">
          <div className="flex items-center gap-2 text-amber-400 font-bold text-lg border-b border-slate-700/60 pb-3">
            <FolderArchive className="w-5 h-5" />
            <h4>Saved Trip Expense History</h4>
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            {archives.map((arc) => (
              <div key={arc._id} className="bg-slate-900/90 p-4 rounded-xl border border-slate-700/60 space-y-3 relative group">
                <div className="flex justify-between items-center pr-6">
                  <span className="font-bold text-teal-300 text-base">{arc.trip_name}</span>
                  <span className="bg-teal-500/20 text-teal-300 text-xs font-bold px-2.5 py-1 rounded-lg border border-teal-500/30">
                    Total: ${arc.total_amount.toFixed(2)}
                  </span>
                </div>

                <button 
                  onClick={() => handleDeleteArchive(arc._id)} 
                  title="Delete Trip Record" 
                  className="absolute top-3.5 right-3 text-slate-500 hover:text-rose-400 p-1 rounded-lg hover:bg-rose-500/10 transition"
                >
                  <Trash2 className="w-4 h-4" />
                </button>

                <p className="text-xs text-slate-400 font-mono">Archived: {new Date(arc.created_at).toLocaleDateString()}</p>
                <div className="text-xs text-slate-300 space-y-1.5 bg-slate-800/60 p-3 rounded-lg border border-slate-700/50">
                  {arc.expenses.map((item, idx) => (
                    <div key={idx} className="flex justify-between">
                      <span className="text-slate-300">• {item.category}: {item.description}</span>
                      <span className="font-medium text-teal-400">${item.amount.toFixed(2)}</span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
