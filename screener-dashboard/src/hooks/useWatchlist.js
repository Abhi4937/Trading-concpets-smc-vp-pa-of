import { useState, useEffect } from 'react';

export function useWatchlist() {
  const [watchlist, setWatchlist] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem('nse_watchlist') || '[]');
    } catch {
      return [];
    }
  });

  useEffect(() => {
    localStorage.setItem('nse_watchlist', JSON.stringify(watchlist));
  }, [watchlist]);

  const addToWatchlist = (symbol) =>
    setWatchlist(prev => (prev.includes(symbol) ? prev : [...prev, symbol]));

  const removeFromWatchlist = (symbol) =>
    setWatchlist(prev => prev.filter(s => s !== symbol));

  const toggleWatchlist = (symbol) =>
    watchlist.includes(symbol) ? removeFromWatchlist(symbol) : addToWatchlist(symbol);

  const isWatched = (symbol) => watchlist.includes(symbol);

  return { watchlist, addToWatchlist, removeFromWatchlist, toggleWatchlist, isWatched };
}
