import React, { useState } from 'react';
import api from '../api';
import { Compass, Search, MapPin, DollarSign, Calendar, Lightbulb, Landmark } from 'lucide-react';

export default function DestinationPlanner() {
  const [destination, setDestination] = useState('');
  const [plan, setPlan] = useState(null);

  const handlePlan = async (e) => {
    e.preventDefault();
    try {
      const res = await api.get(`/planner/recommend?destination=${encodeURIComponent(destination)}`);
      setPlan(res.data);
    } catch (err) {
      alert("Failed to load destination guide.");
    }
  };

  return (
    <div className="space-y-8">
      <form onSubmit={handlePlan} className="bg-slate-800/80 backdrop-blur-md p-6 rounded-2xl border border-slate-700/60 shadow-xl flex gap-3">
        <div className="relative flex-1">
          <Search className="w-5 h-5 text-slate-400 absolute left-3.5 top-3.5" />
          <input 
            type="text" 
            placeholder="Search City or Region (e.g. Kyoto, Paris, Tokyo, Hyderabad, Rome)" 
            value={destination} 
            onChange={(e)=>setDestination(e.target.value)} 
            required 
            className="w-full bg-slate-900/80 pl-11 pr-4 py-3 rounded-xl border border-slate-700 text-white focus:outline-none focus:border-teal-400 transition text-sm" 
          />
        </div>
        <button type="submit" className="bg-gradient-to-r from-teal-400 to-emerald-500 hover:from-teal-300 hover:to-emerald-400 text-slate-950 font-bold px-6 py-3 rounded-xl flex items-center gap-2 shadow-lg shadow-teal-500/20 transition text-sm">
          <Compass className="w-4 h-4" />
          <span>Plan Trip</span>
        </button>
      </form>

      {plan && (
        <div className="bg-slate-800/80 backdrop-blur-md p-6 rounded-2xl border border-slate-700/60 shadow-xl space-y-6">
          <div className="flex items-center gap-2 text-2xl font-black text-teal-300 border-b border-slate-700/60 pb-3">
            <MapPin className="w-6 h-6 text-teal-400" />
            <h3>Itinerary Guide for {plan.destination}</h3>
          </div>
          
          <div className="grid md:grid-cols-2 gap-4 text-sm">
            <div className="bg-slate-900/80 p-4 rounded-xl border border-slate-700/50 flex items-center gap-3">
              <div className="p-2.5 bg-teal-500/10 text-teal-400 rounded-xl">
                <DollarSign className="w-5 h-5" />
              </div>
              <div>
                <span className="text-xs text-slate-400 font-semibold uppercase">Daily Estimated Budget</span>
                <p className="text-teal-300 font-bold text-base">{plan.estimated_budget_per_day}</p>
              </div>
            </div>

            <div className="bg-slate-900/80 p-4 rounded-xl border border-slate-700/50 flex items-center gap-3">
              <div className="p-2.5 bg-amber-500/10 text-amber-400 rounded-xl">
                <Calendar className="w-5 h-5" />
              </div>
              <div>
                <span className="text-xs text-slate-400 font-semibold uppercase">Best Time to Visit</span>
                <p className="text-amber-300 font-bold text-base">{plan.best_time_to_visit}</p>
              </div>
            </div>
          </div>

          <div>
            <h4 className="font-bold text-slate-200 mb-3 text-base flex items-center gap-2">
              <Landmark className="w-5 h-5 text-teal-400" />
              <span>Special Places to Visit & Travel Costs:</span>
            </h4>
            <div className="space-y-2.5">
              {plan.must_visit.map((item, idx) => (
                <div key={idx} className="bg-slate-900/90 p-3.5 rounded-xl border border-slate-700/60 flex flex-wrap justify-between items-center gap-2 text-sm">
                  <span className="font-medium text-slate-200">{idx + 1}. {typeof item === 'object' ? item.place : item}</span>
                  {typeof item === 'object' && item.est_cost && (
                    <span className="bg-teal-500/20 text-teal-300 border border-teal-500/30 text-xs font-bold px-2.5 py-1 rounded-lg">
                      {item.est_cost}
                    </span>
                  )}
                </div>
              ))}
            </div>
          </div>

          <div className="bg-slate-900/90 p-4 rounded-xl border-l-4 border-teal-400 flex items-start gap-3">
            <Lightbulb className="w-5 h-5 text-teal-400 shrink-0 mt-0.5" />
            <div>
              <strong className="text-teal-300 block mb-1 text-sm">Essential Travel Tips:</strong>
              <p className="text-xs md:text-sm text-slate-300 leading-relaxed">{plan.local_tips}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
