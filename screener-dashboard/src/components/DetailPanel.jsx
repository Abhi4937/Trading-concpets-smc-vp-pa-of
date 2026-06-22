import { XIcon, StarIcon } from './Icons.jsx';
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

function LevelRow({ label, value, accent }) {
  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '6px 0', borderBottom: '1px solid #1a2233' }}>
      <span style={{ fontSize: '12px', color: '#8b97ab' }}>{label}</span>
      <span className="mono" style={{ fontSize: '12px', fontWeight: 600, color: accent || '#e6edf6' }}>{fmt(value)}</span>
    </div>
  );
}

function RRBadge({ trigger, stop, target, dir }) {
  if (trigger == null || stop == null || target == null) return null;
  const risk = Math.abs(trigger - stop);
  const reward = Math.abs(target - trigger);
  if (risk === 0) return null;
  const rr = reward / risk;
  const color = rr >= 1.5 ? '#10b981' : rr >= 1 ? '#f59e0b' : '#ef4444';
  return (
    <span style={{
      display: 'inline-flex',
      alignItems: 'center',
      padding: '3px 9px',
      borderRadius: '6px',
      fontSize: '12px',
      fontWeight: 700,
      background: `${color}18`,
      border: `1px solid ${color}44`,
      color,
      fontFamily: 'ui-monospace, monospace',
    }}>
      R:R {rr.toFixed(2)}
    </span>
  );
}

export function DetailPanel({ stock, isWatched, onToggleWatchlist, onClose }) {
  if (!stock) {
    return (
      <div style={{
        width: '320px',
        flexShrink: 0,
        background: '#121826',
        borderLeft: '1px solid #243044',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '32px',
        color: '#8b97ab',
        fontSize: '13px',
        textAlign: 'center',
      }}>
        <div>
          <div style={{ fontSize: '28px', marginBottom: '10px', opacity: 0.4 }}>📊</div>
          Click a row to see setup details
        </div>
      </div>
    );
  }

  const chgColor = stock.changePct >= 0 ? '#22c55e' : '#ef4444';

  return (
    <div
      className="slide-in-right"
      style={{
        width: '320px',
        flexShrink: 0,
        background: '#121826',
        borderLeft: '1px solid #243044',
        overflowY: 'auto',
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      {/* Header */}
      <div style={{ padding: '16px', borderBottom: '1px solid #243044', display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between' }}>
        <div style={{ flex: 1, minWidth: 0 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
            <span style={{ fontSize: '18px', fontWeight: 800, color: '#e6edf6', letterSpacing: '0.02em' }}>{stock.symbol}</span>
            <SetupBadge setup={stock.setup} direction={stock.direction} size="sm" />
          </div>
          <div style={{ fontSize: '12px', color: '#8b97ab', marginTop: '2px' }}>{stock.name}</div>
          <div style={{ fontSize: '11px', color: '#6366f1', marginTop: '1px' }}>{stock.sector}</div>
        </div>
        <button
          onClick={onClose}
          aria-label="Close detail panel"
          style={{ background: 'none', border: '1px solid #243044', borderRadius: '6px', color: '#8b97ab', cursor: 'pointer', padding: '5px', display: 'flex', flexShrink: 0 }}
        >
          <XIcon size={14} />
        </button>
      </div>

      <div style={{ padding: '16px', flex: 1 }}>

        {/* Price */}
        <div style={{ display: 'flex', alignItems: 'baseline', gap: '10px', marginBottom: '6px' }}>
          <span className="mono" style={{ fontSize: '28px', fontWeight: 800, color: '#e6edf6' }}>
            {fmt(stock.ltp)}
          </span>
          <span className="mono" style={{ fontSize: '15px', fontWeight: 700, color: chgColor }}>
            {fmtPct(stock.changePct)}
          </span>
        </div>

        {/* Watchlist + RR */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '14px', flexWrap: 'wrap' }}>
          <button
            onClick={() => onToggleWatchlist(stock.symbol)}
            aria-label={isWatched ? 'Remove from watchlist' : 'Add to watchlist'}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '6px',
              padding: '5px 12px',
              borderRadius: '7px',
              background: isWatched ? 'rgba(245,158,11,0.15)' : '#1a2233',
              border: `1px solid ${isWatched ? 'rgba(245,158,11,0.4)' : '#243044'}`,
              color: isWatched ? '#f59e0b' : '#8b97ab',
              fontSize: '12px',
              fontWeight: 600,
              cursor: 'pointer',
              transition: 'all 0.15s',
            }}
          >
            <StarIcon filled={isWatched} size={13} />
            {isWatched ? 'Watching' : 'Watch'}
          </button>
          <RRBadge trigger={stock.trigger} stop={stock.stop} target={stock.target} dir={stock.direction} />
        </div>

        {/* Rationale */}
        {stock.rationale && (
          <div style={{
            background: '#1a2233',
            border: '1px solid #243044',
            borderRadius: '8px',
            padding: '10px 12px',
            fontSize: '12px',
            color: '#c5d0de',
            lineHeight: '1.6',
            marginBottom: '14px',
          }}>
            {stock.rationale}
          </div>
        )}

        {/* Trigger / Stop / Target */}
        {stock.setup && (
          <div style={{ marginBottom: '14px' }}>
            <div style={{ fontSize: '11px', fontWeight: 600, color: '#8b97ab', textTransform: 'uppercase', letterSpacing: '0.07em', marginBottom: '8px' }}>
              Trade Levels
            </div>
            <div style={{
              display: 'grid',
              gridTemplateColumns: '1fr 1fr 1fr',
              gap: '8px',
            }}>
              {[
                { label: 'Trigger', val: stock.trigger, color: '#38bdf8' },
                { label: 'Stop',    val: stock.stop,    color: '#ef4444' },
                { label: 'Target',  val: stock.target,  color: '#10b981' },
              ].map(({ label, val, color }) => (
                <div key={label} style={{
                  background: '#0f1520',
                  border: `1px solid ${color}33`,
                  borderRadius: '7px',
                  padding: '8px',
                  textAlign: 'center',
                }}>
                  <div style={{ fontSize: '10px', color, fontWeight: 600, marginBottom: '3px' }}>{label}</div>
                  <div className="mono" style={{ fontSize: '12px', fontWeight: 700, color: '#e6edf6' }}>{fmt(val)}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Sparkline larger */}
        <div style={{ marginBottom: '14px' }}>
          <div style={{ fontSize: '11px', fontWeight: 600, color: '#8b97ab', textTransform: 'uppercase', letterSpacing: '0.07em', marginBottom: '6px' }}>
            Intraday
          </div>
          <div style={{ background: '#0f1520', borderRadius: '8px', padding: '8px', border: '1px solid #243044' }}>
            <Sparkline data={stock.spark} width={272} height={56} id={`detail-${stock.symbol}`} />
          </div>
        </div>

        {/* Key levels */}
        <div style={{ marginBottom: '14px' }}>
          <div style={{ fontSize: '11px', fontWeight: 600, color: '#8b97ab', textTransform: 'uppercase', letterSpacing: '0.07em', marginBottom: '4px' }}>
            Key Levels
          </div>
          <LevelRow label="VWAP"       value={stock.vwap}    accent={stock.ltp >= stock.vwap ? '#22c55e' : '#ef4444'} />
          <LevelRow label="OR High"    value={stock.orHigh}  />
          <LevelRow label="OR Low"     value={stock.orLow}   />
          <LevelRow label="Prev Day H" value={stock.pdh}     accent="#f59e0b" />
          <LevelRow label="Prev Day L" value={stock.pdl}     accent="#f59e0b" />
          <LevelRow label="Day High"   value={stock.dayHigh} accent="#22c55e" />
          <LevelRow label="Day Low"    value={stock.dayLow}  accent="#ef4444" />
          <LevelRow label="Prev Close" value={stock.prevClose} />
          <LevelRow label="Open"       value={stock.open}    />
        </div>

        {/* RS + RelVol + OI */}
        <div style={{ marginBottom: '14px' }}>
          <div style={{ fontSize: '11px', fontWeight: 600, color: '#8b97ab', textTransform: 'uppercase', letterSpacing: '0.07em', marginBottom: '8px' }}>
            Market Context
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {/* RS */}
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <span style={{ fontSize: '12px', color: '#8b97ab' }}>RS Rank vs Nifty</span>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                <div style={{ width: 60, height: 5, background: '#243044', borderRadius: '3px', overflow: 'hidden' }}>
                  <div style={{
                    width: `${stock.rsRank}%`,
                    height: '100%',
                    background: stock.rsRank >= 70 ? '#10b981' : stock.rsRank >= 40 ? '#f59e0b' : '#ef4444',
                    borderRadius: '3px',
                  }} />
                </div>
                <span className="mono" style={{ fontSize: '12px', fontWeight: 700, color: '#e6edf6' }}>{stock.rsRank}</span>
              </div>
            </div>
            {/* RelVol */}
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <span style={{ fontSize: '12px', color: '#8b97ab' }}>Rel Volume</span>
              <span className="mono" style={{
                fontSize: '12px',
                fontWeight: 700,
                color: stock.relVol >= 2 ? '#a5b4fc' : '#8b97ab',
                background: stock.relVol >= 2 ? 'rgba(99,102,241,0.15)' : '#1a2233',
                border: '1px solid',
                borderColor: stock.relVol >= 2 ? 'rgba(99,102,241,0.35)' : '#243044',
                borderRadius: '5px',
                padding: '2px 7px',
              }}>
                {stock.relVol.toFixed(1)}×
              </span>
            </div>
            {/* OI Change */}
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <span style={{ fontSize: '12px', color: '#8b97ab' }}>OI Change</span>
              <span className="mono" style={{ fontSize: '12px', fontWeight: 700, color: stock.oiChangePct >= 0 ? '#22c55e' : '#ef4444' }}>
                {stock.oiChangePct >= 0 ? '+' : ''}{stock.oiChangePct?.toFixed(1)}%
              </span>
            </div>
          </div>
        </div>

        {/* Honesty banner */}
        <div style={{
          background: 'rgba(245,158,11,0.08)',
          border: '1px solid rgba(245,158,11,0.25)',
          borderRadius: '8px',
          padding: '10px 12px',
          fontSize: '11px',
          color: '#d4a14a',
          lineHeight: '1.5',
        }}>
          ⚠️ Screener narrows — confirm with volume profile / order flow / price action before entry. This is a decision-support tool, not a signal service.
        </div>

      </div>
    </div>
  );
}
