/**
 * SetupBadge.jsx — Color-coded pill for trading setup + direction indicator.
 */

const SETUP_CONFIG = {
  breakout:    { label: 'Breakout',    color: '#10b981', bg: 'rgba(16,185,129,0.15)',  border: 'rgba(16,185,129,0.35)' },
  bounce:      { label: 'Bounce',      color: '#14b8a6', bg: 'rgba(20,184,166,0.15)',  border: 'rgba(20,184,166,0.35)' },
  reversal_up: { label: 'Reversal ↑',  color: '#38bdf8', bg: 'rgba(56,189,248,0.15)',  border: 'rgba(56,189,248,0.35)' },
  fakeout:     { label: 'Fakeout',     color: '#f59e0b', bg: 'rgba(245,158,11,0.15)',  border: 'rgba(245,158,11,0.35)' },
  breakdown:   { label: 'Breakdown',   color: '#f43f5e', bg: 'rgba(244,63,94,0.15)',   border: 'rgba(244,63,94,0.35)'  },
};

export function SetupBadge({ setup, direction, size = 'sm' }) {
  if (!setup) {
    return (
      <span
        style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '4px',
          padding: size === 'lg' ? '4px 10px' : '2px 7px',
          borderRadius: '999px',
          fontSize: size === 'lg' ? '12px' : '11px',
          fontWeight: 500,
          background: 'rgba(139,151,171,0.1)',
          border: '1px solid rgba(139,151,171,0.2)',
          color: '#8b97ab',
          whiteSpace: 'nowrap',
        }}
      >
        —
      </span>
    );
  }

  const cfg = SETUP_CONFIG[setup] || {};
  const dirSymbol = direction === 'long' ? '▲' : direction === 'short' ? '▼' : '';
  const dirColor = direction === 'long' ? '#22c55e' : direction === 'short' ? '#ef4444' : cfg.color;

  return (
    <span
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: '4px',
        padding: size === 'lg' ? '4px 10px' : '2px 7px',
        borderRadius: '999px',
        fontSize: size === 'lg' ? '12px' : '11px',
        fontWeight: 600,
        background: cfg.bg,
        border: `1px solid ${cfg.border}`,
        color: cfg.color,
        whiteSpace: 'nowrap',
        letterSpacing: '0.01em',
      }}
    >
      {dirSymbol && (
        <span style={{ color: dirColor, fontSize: size === 'lg' ? '10px' : '9px' }}>
          {dirSymbol}
        </span>
      )}
      {cfg.label}
    </span>
  );
}
