import { useState, useEffect, useMemo, useCallback } from 'react';
import { fetchScreenerData } from './services/dataSource.js';
import { useWatchlist } from './hooks/useWatchlist.js';
import { Header } from './components/Header.jsx';
import { SummaryStats } from './components/SummaryStats.jsx';
import { FilterRail } from './components/FilterRail.jsx';
import { StockTable } from './components/StockTable.jsx';
import { DetailPanel } from './components/DetailPanel.jsx';
import { WatchlistDrawer } from './components/WatchlistDrawer.jsx';

const DEFAULT_FILTERS = {
  search: '',
  direction: 'all',
  setupFilter: [],
  sector: '',
  minRelVol: 1.0,
  minRs: 0,
  inPlayOnly: false,
};

function applyFilters(stocks, filters) {
  const { search, direction, setupFilter, sector, minRelVol, minRs, inPlayOnly } = filters;
  const q = search.trim().toLowerCase();

  return stocks.filter(s => {
    if (q && !s.symbol.toLowerCase().includes(q) && !s.name.toLowerCase().includes(q)) return false;
    if (direction !== 'all' && s.direction !== direction) return false;
    if (setupFilter.length > 0 && !setupFilter.includes(s.setup)) return false;
    if (sector && s.sector !== sector) return false;
    if (s.relVol < minRelVol) return false;
    if (s.rsRank < minRs) return false;
    if (inPlayOnly && !s.inPlay) return false;
    return true;
  });
}

function applySorting(stocks, sortConfig) {
  if (!sortConfig.key) return stocks;
  return [...stocks].sort((a, b) => {
    let av = a[sortConfig.key];
    let bv = b[sortConfig.key];
    if (typeof av === 'string') av = av.toLowerCase();
    if (typeof bv === 'string') bv = bv.toLowerCase();
    if (av == null) av = sortConfig.dir === 'asc' ? Infinity : -Infinity;
    if (bv == null) bv = sortConfig.dir === 'asc' ? Infinity : -Infinity;
    return sortConfig.dir === 'asc' ? (av > bv ? 1 : -1) : (av < bv ? 1 : -1);
  });
}

export default function App() {
  const [allStocks, setAllStocks] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [dataSource, setDataSource] = useState('sample'); // 'live' | 'sample'
  const [asOf, setAsOf] = useState(null);                 // ISO string from backend

  const [filters, setFilters] = useState(DEFAULT_FILTERS);
  const [sortConfig, setSortConfig] = useState({ key: 'strength', dir: 'desc' });
  const [selectedStock, setSelectedStock] = useState(null);
  const [watchlistOpen, setWatchlistOpen] = useState(false);

  const { watchlist, toggleWatchlist, removeFromWatchlist, isWatched } = useWatchlist();

  const load = useCallback(async () => {
    try {
      // fetchScreenerData now returns { stocks, source, asOf } — never throws
      const data = await fetchScreenerData();
      setAllStocks(data.stocks ?? []);
      setDataSource(data.source ?? 'sample');
      setAsOf(data.asOf ?? null);
      setLastUpdated(new Date());
    } catch (err) {
      // Defensive: fetchScreenerData shouldn't throw, but guard anyway
      console.error('Screener fetch failed:', err);
    }
  }, []);

  // Initial load
  useEffect(() => {
    setIsLoading(true);
    load().finally(() => setIsLoading(false));
  }, [load]);

  // Refresh handler
  const handleRefresh = useCallback(async () => {
    setIsRefreshing(true);
    await load();
    setIsRefreshing(false);
  }, [load]);

  // Derive unique sectors
  const sectors = useMemo(
    () => [...new Set(allStocks.map(s => s.sector))].sort(),
    [allStocks]
  );

  // Filter + sort
  const filtered = useMemo(() => {
    const f = applyFilters(allStocks, filters);
    return applySorting(f, sortConfig);
  }, [allStocks, filters, sortConfig]);

  const handleSort = (key) => {
    setSortConfig(prev =>
      prev.key === key
        ? { key, dir: prev.dir === 'asc' ? 'desc' : 'asc' }
        : { key, dir: 'desc' }
    );
  };

  // Keep selectedStock in sync (if stock data refreshes)
  useEffect(() => {
    if (selectedStock) {
      const updated = allStocks.find(s => s.symbol === selectedStock.symbol);
      if (updated) setSelectedStock(updated);
    }
  }, [allStocks]);

  // Watchlist stocks (enriched)
  const watchedStocks = useMemo(
    () => watchlist.map(sym => allStocks.find(s => s.symbol === sym)).filter(Boolean),
    [watchlist, allStocks]
  );

  const hasDetailPanel = !!selectedStock;

  if (isLoading) {
    return (
      <div style={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        gap: '16px',
        background: '#0a0e17',
      }}>
        <div style={{
          width: 40,
          height: 40,
          border: '3px solid #243044',
          borderTopColor: '#6366f1',
          borderRadius: '50%',
          animation: 'spin 0.7s linear infinite',
        }} />
        <div style={{ color: '#8b97ab', fontSize: '14px' }}>Loading screener…</div>
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', overflow: 'hidden' }}>
      {/* Header */}
      <Header
        onRefresh={handleRefresh}
        isRefreshing={isRefreshing}
        lastUpdated={lastUpdated}
        watchlistCount={watchlist.length}
        onWatchlistOpen={() => setWatchlistOpen(true)}
        dataSource={dataSource}
        asOf={asOf}
      />

      {/* Summary row */}
      <SummaryStats stocks={allStocks} />

      {/* Main content */}
      <div style={{ display: 'flex', flex: 1, overflow: 'hidden' }}>
        {/* Filter rail */}
        <FilterRail
          filters={filters}
          onFiltersChange={setFilters}
          sectors={sectors}
          onReset={() => setFilters(DEFAULT_FILTERS)}
        />

        {/* Table + detail panel */}
        <div style={{ flex: 1, display: 'flex', overflow: 'hidden', minWidth: 0 }}>
          {/* Table area */}
          <div style={{ flex: 1, overflow: 'auto', minWidth: 0 }}>
            {/* Result count bar */}
            <div style={{
              padding: '8px 16px',
              borderBottom: '1px solid #1a2233',
              fontSize: '12px',
              color: '#8b97ab',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              background: '#0f1520',
              flexShrink: 0,
            }}>
              <span style={{ color: '#e6edf6', fontWeight: 600 }}>{filtered.length}</span>
              {' '}of{' '}
              <span>{allStocks.length}</span>
              {' '}stocks
              {filters.setupFilter.length > 0 && (
                <span style={{ color: '#6366f1' }}>· {filters.setupFilter.join(', ')}</span>
              )}
              {filters.inPlayOnly && <span style={{ color: '#6366f1' }}>· In-play only</span>}
              {filters.direction !== 'all' && (
                <span style={{ color: filters.direction === 'long' ? '#22c55e' : '#ef4444' }}>
                  · {filters.direction === 'long' ? '▲ Long' : '▼ Short'} only
                </span>
              )}
            </div>

            <StockTable
              stocks={filtered}
              sortConfig={sortConfig}
              onSort={handleSort}
              selectedStock={selectedStock}
              onSelect={setSelectedStock}
              watchlist={watchlist}
              onToggleWatchlist={toggleWatchlist}
            />

            {/* Footer honesty banner */}
            <div style={{
              padding: '16px 20px',
              borderTop: '1px solid #1a2233',
              fontSize: '11px',
              color: '#4a5568',
              lineHeight: '1.6',
            }}>
              ⚠️ <strong style={{ color: '#6b7280' }}>Risk disclaimer:</strong> This screener is for educational and decision-support purposes only. It is not financial advice. Always confirm setups with volume profile, order flow, and price action before entering a trade. Past scan results are not indicative of future performance.
              &nbsp;·&nbsp; Vault references: "07 — Index & Stock Universe" · "06 — Liquidity & Tradability Filters" · "03 — Long Scans" · "05 — Reversal Scans"
            </div>
          </div>

          {/* Detail panel — mounts only when a stock is selected, so the table uses full width by default */}
          {selectedStock && (
            <DetailPanel
              stock={selectedStock}
              isWatched={isWatched(selectedStock.symbol)}
              onToggleWatchlist={toggleWatchlist}
              onClose={() => setSelectedStock(null)}
            />
          )}
        </div>
      </div>

      {/* Watchlist drawer */}
      <WatchlistDrawer
        isOpen={watchlistOpen}
        onClose={() => setWatchlistOpen(false)}
        watchedStocks={watchedStocks}
        onRemove={removeFromWatchlist}
        onSelectStock={(stock) => { setSelectedStock(stock); }}
      />
    </div>
  );
}
