import { RefreshIcon, BookmarkIcon } from './Icons.jsx';

function IndexChip({ name, value, change }) {
  const up = change >= 0;
  const color = up ? '#22c55e' : '#ef4444';
  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
      background: '#1a2233',
      border: '1px solid #243044',
      borderRadius: '8px',
      padding: '5px 12px',
    }}>
      <span style={{ fontSize: '12px', color: '#8b97ab', fontWeight: 500 }}>{name}</span>
      <span className="mono" style={{ fontSize: '13px', fontWeight: 700, color: '#e6edf6' }}>
        {typeof value === 'number'
          ? value.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
          : value}
      </span>
      <span className="mono" style={{ fontSize: '12px', fontWeight: 600, color }}>
        {up ? '+' : ''}{change.toFixed(2)}%
      </span>
    </div>
  );
}

export function Header({ onRefresh, isRefreshing, lastUpdated, watchlistCount, onWatchlistOpen }) {
  const timeStr = lastUpdated
    ? lastUpdated.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
    : '—';

  return (
    <header style={{
      background: '#121826',
      borderBottom: '1px solid #243044',
      padding: '0 20px',
      display: 'flex',
      alignItems: 'center',
      gap: '16px',
      height: '58px',
      flexWrap: 'wrap',
      flexShrink: 0,
    }}>
      {/* Brand */}
      <div style={{ display: 'flex', flexDirection: 'column', marginRight: '4px' }}>
        <span style={{ fontSize: '15px', fontWeight: 800, color: '#e6edf6', letterSpacing: '0.01em', lineHeight: 1.1 }}>
          NSE Intraday Screener
        </span>
        <span style={{ fontSize: '10px', color: '#8b97ab', letterSpacing: '0.04em' }}>
          Intraday F&amp;O Universe · India
        </span>
      </div>

      {/* Divider */}
      <div style={{ width: 1, height: 32, background: '#243044', flexShrink: 0 }} />

      {/* Market regime chips */}
      <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
        <IndexChip name="NIFTY 50"   value={23847.65} change={0.42} />
        <IndexChip name="BANK NIFTY" value={51234.10} change={-0.18} />
        <IndexChip name="INDIA VIX"  value={13.45}    change={-2.10} />
      </div>

      {/* Sample badge */}
      <span style={{
        display: 'inline-flex',
        alignItems: 'center',
        padding: '3px 9px',
        background: 'rgba(245,158,11,0.15)',
        border: '1px solid rgba(245,158,11,0.35)',
        borderRadius: '6px',
        fontSize: '10px',
        fontWeight: 700,
        color: '#f59e0b',
        letterSpacing: '0.06em',
        textTransform: 'uppercase',
        flexShrink: 0,
      }}>
        Sample Data
      </span>

      {/* Spacer */}
      <div style={{ flex: 1 }} />

      {/* Last updated */}
      <span style={{ fontSize: '11px', color: '#8b97ab', flexShrink: 0 }}>
        Updated {timeStr}
      </span>

      {/* Refresh button */}
      <button
        onClick={onRefresh}
        disabled={isRefreshing}
        aria-label="Refresh screener data"
        style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '6px',
          background: '#1a2233',
          border: '1px solid #243044',
          borderRadius: '8px',
          color: '#8b97ab',
          fontSize: '12px',
          fontWeight: 600,
          padding: '6px 12px',
          cursor: isRefreshing ? 'wait' : 'pointer',
          transition: 'color 0.15s, border-color 0.15s',
          flexShrink: 0,
        }}
        onMouseEnter={e => { if (!isRefreshing) { e.currentTarget.style.color = '#e6edf6'; e.currentTarget.style.borderColor = '#6366f1'; } }}
        onMouseLeave={e => { e.currentTarget.style.color = '#8b97ab'; e.currentTarget.style.borderColor = '#243044'; }}
      >
        <RefreshIcon size={14} className={isRefreshing ? 'spinning' : ''} />
        {isRefreshing ? 'Refreshing…' : 'Refresh'}
      </button>

      {/* Watchlist button */}
      <button
        onClick={onWatchlistOpen}
        aria-label={`Open watchlist (${watchlistCount} items)`}
        style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '6px',
          background: watchlistCount > 0 ? 'rgba(245,158,11,0.12)' : '#1a2233',
          border: `1px solid ${watchlistCount > 0 ? 'rgba(245,158,11,0.35)' : '#243044'}`,
          borderRadius: '8px',
          color: watchlistCount > 0 ? '#f59e0b' : '#8b97ab',
          fontSize: '12px',
          fontWeight: 600,
          padding: '6px 12px',
          cursor: 'pointer',
          transition: 'all 0.15s',
          flexShrink: 0,
        }}
      >
        <BookmarkIcon size={14} />
        Watchlist
        {watchlistCount > 0 && (
          <span style={{
            background: '#f59e0b',
            color: '#000',
            borderRadius: '99px',
            fontSize: '10px',
            fontWeight: 800,
            padding: '1px 6px',
          }}>
            {watchlistCount}
          </span>
        )}
      </button>
    </header>
  );
}
