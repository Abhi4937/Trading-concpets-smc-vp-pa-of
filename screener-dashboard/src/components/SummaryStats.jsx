import { TrendingUpIcon, TrendingDownIcon, ZapIcon, LayersIcon, ActivityIcon } from './Icons.jsx';

function StatCard({ icon, label, value, color, subLabel }) {
  return (
    <div
      style={{
        background: '#121826',
        border: '1px solid #243044',
        borderRadius: '10px',
        padding: '14px 18px',
        display: 'flex',
        alignItems: 'center',
        gap: '14px',
        flex: '1 1 0',
        minWidth: '140px',
      }}
    >
      <div
        style={{
          width: 38,
          height: 38,
          borderRadius: '9px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          background: `${color}18`,
          color,
          flexShrink: 0,
        }}
      >
        {icon}
      </div>
      <div>
        <div style={{ fontSize: '22px', fontWeight: 700, color: '#e6edf6', lineHeight: 1.1, fontFamily: 'ui-monospace, monospace' }}>
          {value}
        </div>
        <div style={{ fontSize: '12px', color: '#8b97ab', marginTop: '2px' }}>{label}</div>
        {subLabel && (
          <div style={{ fontSize: '11px', color, marginTop: '1px', fontWeight: 500 }}>{subLabel}</div>
        )}
      </div>
    </div>
  );
}

export function SummaryStats({ stocks }) {
  const inPlayCount = stocks.filter(s => s.inPlay).length;
  const longCount = stocks.filter(s => s.direction === 'long').length;
  const shortCount = stocks.filter(s => s.direction === 'short').length;
  const breakoutCount = stocks.filter(s => s.setup === 'breakout').length;

  // Strongest sector: most in-play stocks
  const sectorCounts = {};
  stocks.forEach(s => {
    if (s.inPlay) {
      sectorCounts[s.sector] = (sectorCounts[s.sector] || 0) + 1;
    }
  });
  const strongestSector = Object.entries(sectorCounts).sort((a, b) => b[1] - a[1])[0];

  return (
    <div
      style={{
        display: 'flex',
        gap: '12px',
        padding: '12px 20px',
        overflowX: 'auto',
        flexWrap: 'wrap',
      }}
    >
      <StatCard
        icon={<ZapIcon size={18} />}
        label="In-Play Stocks"
        value={inPlayCount}
        color="#6366f1"
        subLabel="RelVol ≥ 2×"
      />
      <StatCard
        icon={<TrendingUpIcon size={18} />}
        label="Long Setups"
        value={longCount}
        color="#22c55e"
        subLabel="Breakout / Bounce / Rev↑"
      />
      <StatCard
        icon={<TrendingDownIcon size={18} />}
        label="Short Setups"
        value={shortCount}
        color="#ef4444"
        subLabel="Breakdown / Fakeout"
      />
      <StatCard
        icon={<ActivityIcon size={18} />}
        label="Strongest Sector"
        value={strongestSector ? strongestSector[0] : '—'}
        color="#f59e0b"
        subLabel={strongestSector ? `${strongestSector[1]} in-play` : 'No data'}
      />
      <StatCard
        icon={<LayersIcon size={18} />}
        label="Breakouts Today"
        value={breakoutCount}
        color="#10b981"
        subLabel="Above ORH+PDH"
      />
    </div>
  );
}
