import { XIcon, StarIcon } from './Icons.jsx';
import { SetupBadge } from './SetupBadge.jsx';

function fmt(n, decimals = 2) {
  if (n == null) return '—';
  return n.toLocaleString('en-IN', { minimumFractionDigits: decimals, maximumFractionDigits: decimals });
}

function fmtPct(n) {
  if (n == null) return '—';
  return (n >= 0 ? '+' : '') + n.toFixed(2) + '%';
}

export function WatchlistDrawer({ isOpen, onClose, watchedStocks, onRemove, onSelectStock }) {
  if (!isOpen) return null;

  return (
    <>
      {/* Backdrop */}
      <div
        onClick={onClose}
        style={{
          position: 'fixed',
          inset: 0,
          background: 'rgba(0,0,0,0.55)',
          zIndex: 40,
        }}
        aria-hidden="true"
      />

      {/* Drawer */}
      <div
        className="slide-in-right"
        style={{
          position: 'fixed',
          top: 0,
          right: 0,
          bottom: 0,
          width: '360px',
          background: '#121826',
          borderLeft: '1px solid #243044',
          zIndex: 50,
          display: 'flex',
          flexDirection: 'column',
          boxShadow: '-8px 0 32px rgba(0,0,0,0.5)',
        }}
        role="dialog"
        aria-modal="true"
        aria-label="Watchlist"
      >
        {/* Header */}
        <div style={{ padding: '18px 20px', borderBottom: '1px solid #243044', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <StarIcon filled size={16} style={{ color: '#f59e0b' }} />
            <span style={{ fontSize: '16px', fontWeight: 700, color: '#e6edf6' }}>Watchlist</span>
            <span style={{
              background: '#6366f118',
              border: '1px solid #6366f133',
              borderRadius: '99px',
              fontSize: '12px',
              fontWeight: 700,
              color: '#a5b4fc',
              padding: '1px 8px',
            }}>{watchedStocks.length}</span>
          </div>
          <button
            onClick={onClose}
            aria-label="Close watchlist"
            style={{ background: 'none', border: '1px solid #243044', borderRadius: '7px', color: '#8b97ab', cursor: 'pointer', padding: '6px', display: 'flex' }}
          >
            <XIcon size={15} />
          </button>
        </div>

        {/* List */}
        <div style={{ flex: 1, overflowY: 'auto', padding: '12px 16px' }}>
          {watchedStocks.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '48px 24px', color: '#8b97ab' }}>
              <div style={{ fontSize: '32px', marginBottom: '12px', opacity: 0.4 }}>★</div>
              <div style={{ fontSize: '14px', color: '#e6edf6', fontWeight: 600, marginBottom: '6px' }}>Watchlist is empty</div>
              <div style={{ fontSize: '12px' }}>Click the ★ on any stock row to add it here.</div>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {watchedStocks.map(stock => {
                const chgColor = (stock.changePct || 0) >= 0 ? '#22c55e' : '#ef4444';
                return (
                  <div
                    key={stock.symbol}
                    style={{
                      background: '#1a2233',
                      border: '1px solid #243044',
                      borderRadius: '10px',
                      padding: '12px 14px',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '12px',
                      cursor: 'pointer',
                      transition: 'border-color 0.15s, background 0.15s',
                    }}
                    onClick={() => { onSelectStock(stock); onClose(); }}
                    onMouseEnter={e => { e.currentTarget.style.borderColor = '#6366f155'; e.currentTarget.style.background = '#1e2a3f'; }}
                    onMouseLeave={e => { e.currentTarget.style.borderColor = '#243044'; e.currentTarget.style.background = '#1a2233'; }}
                    role="button"
                    tabIndex={0}
                    aria-label={`View ${stock.symbol} detail`}
                    onKeyDown={e => { if (e.key === 'Enter') { onSelectStock(stock); onClose(); } }}
                  >
                    {/* Symbol col */}
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <div style={{ fontWeight: 700, fontSize: '14px', color: '#e6edf6' }}>{stock.symbol}</div>
                      <div style={{ fontSize: '11px', color: '#8b97ab', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{stock.name}</div>
                    </div>

                    {/* Price + change */}
                    <div style={{ textAlign: 'right' }}>
                      <div className="mono" style={{ fontSize: '13px', fontWeight: 700, color: '#e6edf6' }}>{fmt(stock.ltp)}</div>
                      <div className="mono" style={{ fontSize: '12px', fontWeight: 600, color: chgColor }}>{fmtPct(stock.changePct)}</div>
                    </div>

                    {/* Setup badge */}
                    <div style={{ flexShrink: 0 }}>
                      <SetupBadge setup={stock.setup} direction={stock.direction} />
                    </div>

                    {/* Remove button */}
                    <button
                      onClick={e => { e.stopPropagation(); onRemove(stock.symbol); }}
                      aria-label={`Remove ${stock.symbol} from watchlist`}
                      style={{
                        background: 'none',
                        border: '1px solid #243044',
                        borderRadius: '6px',
                        color: '#8b97ab',
                        cursor: 'pointer',
                        padding: '5px',
                        display: 'flex',
                        flexShrink: 0,
                        transition: 'color 0.15s, border-color 0.15s',
                      }}
                      onMouseEnter={e => { e.currentTarget.style.color = '#ef4444'; e.currentTarget.style.borderColor = '#ef444455'; }}
                      onMouseLeave={e => { e.currentTarget.style.color = '#8b97ab'; e.currentTarget.style.borderColor = '#243044'; }}
                    >
                      <XIcon size={13} />
                    </button>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Footer */}
        <div style={{ padding: '12px 16px', borderTop: '1px solid #243044', fontSize: '11px', color: '#8b97ab', textAlign: 'center' }}>
          Stored in browser localStorage · Clears on data reset
        </div>
      </div>
    </>
  );
}
