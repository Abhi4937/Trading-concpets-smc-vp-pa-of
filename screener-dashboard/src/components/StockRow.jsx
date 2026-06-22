import { StarIcon } from './Icons.jsx';
import { SetupBadge } from './SetupBadge.jsx';
import { Sparkline } from './Sparkline.jsx';

function fmt(n, decimals = 2) {
  if (n == null) return '—';
  return n.toLocaleString('en-IN', { minimumFractionDigits: decimals, maximumFractionDigits: decimals });
}

function fmtPct(n) {
  if (n == null) return '—';
  return (n >= 0 ? '+' : '') + n.toFixed(2) + '%';
}

function RelVolBadge({ val }) {
  const hot = val >= 2;
  return (
    <span
      style={{
        display: 'inline-block',
        padding: '2px 6px',
        borderRadius: '5px',
        fontSize: '11px',
        fontWeight: 600,
        background: hot ? 'rgba(99,102,241,0.18)' : 'rgba(139,151,171,0.1)',
        border: `1px solid ${hot ? 'rgba(99,102,241,0.4)' : 'rgba(139,151,171,0.2)'}`,
        color: hot ? '#a5b4fc' : '#8b97ab',
        fontFamily: 'ui-monospace, monospace',
      }}
    >
      {val.toFixed(1)}×
    </span>
  );
}

function VwapPill({ ltp, vwap }) {
  const above = ltp >= vwap;
  return (
    <span
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: '3px',
        padding: '2px 6px',
        borderRadius: '5px',
        fontSize: '11px',
        fontWeight: 600,
        background: above ? 'rgba(34,197,94,0.12)' : 'rgba(239,68,68,0.12)',
        color: above ? '#22c55e' : '#ef4444',
      }}
    >
      {above ? '▲' : '▼'} {fmt(vwap)}
    </span>
  );
}

function RsBar({ rank }) {
  const color = rank >= 70 ? '#10b981' : rank >= 40 ? '#f59e0b' : '#ef4444';
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
      <div style={{ width: 44, height: 5, background: '#243044', borderRadius: '3px', overflow: 'hidden' }}>
        <div style={{ width: `${rank}%`, height: '100%', background: color, borderRadius: '3px', transition: 'width 0.3s' }} />
      </div>
      <span style={{ fontSize: '11px', fontFamily: 'ui-monospace, monospace', color: '#8b97ab', minWidth: '22px' }}>{rank}</span>
    </div>
  );
}

function StrengthDots({ score }) {
  const filled = Math.round((score / 100) * 5);
  const color = score >= 70 ? '#10b981' : score >= 40 ? '#f59e0b' : '#8b97ab';
  return (
    <div style={{ display: 'flex', gap: '3px', alignItems: 'center' }} title={`Signal strength: ${score}/100`}>
      {[0, 1, 2, 3, 4].map(i => (
        <div
          key={i}
          style={{
            width: 6,
            height: 6,
            borderRadius: '50%',
            background: i < filled ? color : '#243044',
          }}
        />
      ))}
    </div>
  );
}

export function StockRow({ stock, isSelected, isWatched, onSelect, onToggleWatchlist, index }) {
  const chgColor = stock.changePct >= 0 ? '#22c55e' : '#ef4444';

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      onSelect(stock);
    }
  };

  return (
    <tr
      className={`stock-row${isSelected ? ' selected' : ''}`}
      onClick={() => onSelect(stock)}
      onKeyDown={handleKeyDown}
      tabIndex={0}
      role="row"
      aria-selected={isSelected}
      style={{ cursor: 'pointer', borderBottom: '1px solid #1a2233', transition: 'background 0.1s' }}
    >
      {/* Star */}
      <td style={{ padding: '10px 6px 10px 14px', width: 32 }}>
        <button
          onClick={e => { e.stopPropagation(); onToggleWatchlist(stock.symbol); }}
          aria-label={isWatched ? `Remove ${stock.symbol} from watchlist` : `Add ${stock.symbol} to watchlist`}
          style={{
            background: 'none',
            border: 'none',
            cursor: 'pointer',
            padding: '2px',
            color: isWatched ? '#f59e0b' : '#243044',
            display: 'flex',
            transition: 'color 0.15s',
          }}
          onMouseEnter={e => { if (!isWatched) e.currentTarget.style.color = '#8b97ab'; }}
          onMouseLeave={e => { if (!isWatched) e.currentTarget.style.color = '#243044'; }}
        >
          <StarIcon filled={isWatched} size={14} />
        </button>
      </td>

      {/* Symbol + name */}
      <td style={{ padding: '10px 10px' }}>
        <div style={{ fontWeight: 700, fontSize: '13px', color: '#e6edf6', letterSpacing: '0.02em' }}>
          {stock.symbol}
        </div>
        <div style={{ fontSize: '11px', color: '#8b97ab', marginTop: '1px', whiteSpace: 'nowrap', maxWidth: '140px', overflow: 'hidden', textOverflow: 'ellipsis' }}>
          {stock.name}
        </div>
      </td>

      {/* Sector */}
      <td style={{ padding: '10px 10px' }}>
        <span style={{ fontSize: '11px', color: '#8b97ab', background: '#1a2233', border: '1px solid #243044', borderRadius: '4px', padding: '2px 6px', whiteSpace: 'nowrap' }}>
          {stock.sector}
        </span>
      </td>

      {/* LTP */}
      <td style={{ padding: '10px 10px', textAlign: 'right' }}>
        <span className="mono" style={{ fontSize: '13px', fontWeight: 600, color: '#e6edf6' }}>
          {fmt(stock.ltp)}
        </span>
      </td>

      {/* %Chg */}
      <td style={{ padding: '10px 10px', textAlign: 'right' }}>
        <span className="mono" style={{ fontSize: '12px', fontWeight: 600, color: chgColor }}>
          {fmtPct(stock.changePct)}
        </span>
      </td>

      {/* RelVol */}
      <td style={{ padding: '10px 10px' }}>
        <RelVolBadge val={stock.relVol} />
      </td>

      {/* VWAP */}
      <td style={{ padding: '10px 10px' }}>
        <VwapPill ltp={stock.ltp} vwap={stock.vwap} />
      </td>

      {/* RS */}
      <td style={{ padding: '10px 10px' }}>
        <RsBar rank={stock.rsRank} />
      </td>

      {/* Setup */}
      <td style={{ padding: '10px 10px' }}>
        <SetupBadge setup={stock.setup} direction={stock.direction} />
      </td>

      {/* Trigger / Stop / Target */}
      <td style={{ padding: '10px 10px' }}>
        <div className="mono" style={{ fontSize: '11px', lineHeight: '1.5', color: '#8b97ab', minWidth: '130px' }}>
          <span style={{ color: '#38bdf8' }}>T</span>{' '}
          <span style={{ color: '#e6edf6' }}>{stock.trigger != null ? fmt(stock.trigger) : '—'}</span>
          {'  '}
          <span style={{ color: '#ef4444' }}>S</span>{' '}
          <span style={{ color: '#e6edf6' }}>{stock.stop != null ? fmt(stock.stop) : '—'}</span>
          {'  '}
          <span style={{ color: '#10b981' }}>TP</span>{' '}
          <span style={{ color: '#e6edf6' }}>{stock.target != null ? fmt(stock.target) : '—'}</span>
        </div>
      </td>

      {/* Strength */}
      <td style={{ padding: '10px 10px' }}>
        <StrengthDots score={stock.strength} />
      </td>

      {/* Sparkline */}
      <td style={{ padding: '10px 14px 10px 6px' }}>
        <Sparkline data={stock.spark} width={88} height={28} id={`row-${stock.symbol}`} />
      </td>
    </tr>
  );
}
