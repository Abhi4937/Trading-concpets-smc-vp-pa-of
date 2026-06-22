import { SearchIcon, FilterIcon, XIcon } from './Icons.jsx';

const SETUPS = [
  { key: 'breakout',    label: 'Breakout',    color: '#10b981' },
  { key: 'bounce',      label: 'Bounce',      color: '#14b8a6' },
  { key: 'reversal_up', label: 'Reversal ↑',  color: '#38bdf8' },
  { key: 'fakeout',     label: 'Fakeout',     color: '#f59e0b' },
  { key: 'breakdown',   label: 'Breakdown',   color: '#f43f5e' },
];

function Section({ title, children }) {
  return (
    <div style={{ marginBottom: '20px' }}>
      <div style={{ fontSize: '11px', fontWeight: 600, color: '#8b97ab', letterSpacing: '0.08em', textTransform: 'uppercase', marginBottom: '8px' }}>
        {title}
      </div>
      {children}
    </div>
  );
}

export function FilterRail({ filters, onFiltersChange, sectors, onReset }) {
  const { search, direction, setupFilter, sector, minRelVol, minRs, inPlayOnly } = filters;

  const set = (key, val) => onFiltersChange({ ...filters, [key]: val });

  const toggleSetup = (key) => {
    const next = setupFilter.includes(key)
      ? setupFilter.filter(s => s !== key)
      : [...setupFilter, key];
    set('setupFilter', next);
  };

  return (
    <aside
      style={{
        width: '256px',
        flexShrink: 0,
        background: '#121826',
        borderRight: '1px solid #243044',
        padding: '16px',
        overflowY: 'auto',
        height: '100%',
      }}
    >
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '7px', color: '#e6edf6', fontWeight: 600, fontSize: '14px' }}>
          <FilterIcon size={15} />
          Filters
        </div>
        <button
          onClick={onReset}
          aria-label="Reset all filters"
          style={{
            background: 'none',
            border: '1px solid #243044',
            borderRadius: '6px',
            color: '#8b97ab',
            fontSize: '11px',
            padding: '3px 8px',
            cursor: 'pointer',
            transition: 'color 0.15s, border-color 0.15s',
          }}
          onMouseEnter={e => { e.currentTarget.style.color = '#e6edf6'; e.currentTarget.style.borderColor = '#6366f1'; }}
          onMouseLeave={e => { e.currentTarget.style.color = '#8b97ab'; e.currentTarget.style.borderColor = '#243044'; }}
        >
          Reset
        </button>
      </div>

      {/* Search */}
      <Section title="Search">
        <div style={{ position: 'relative' }}>
          <SearchIcon size={14} className="" style={{ position: 'absolute', left: 9, top: '50%', transform: 'translateY(-50%)', color: '#8b97ab' }} />
          <div style={{ position: 'absolute', left: 9, top: '50%', transform: 'translateY(-50%)', color: '#8b97ab', pointerEvents: 'none', display: 'flex' }}>
            <SearchIcon size={14} />
          </div>
          <input
            type="text"
            value={search}
            onChange={e => set('search', e.target.value)}
            placeholder="Symbol or name…"
            aria-label="Search stocks by symbol or name"
            style={{
              width: '100%',
              background: '#1a2233',
              border: '1px solid #243044',
              borderRadius: '7px',
              padding: '7px 10px 7px 30px',
              color: '#e6edf6',
              fontSize: '13px',
              outline: 'none',
            }}
            onFocus={e => e.target.style.borderColor = '#6366f1'}
            onBlur={e => e.target.style.borderColor = '#243044'}
          />
          {search && (
            <button
              onClick={() => set('search', '')}
              aria-label="Clear search"
              style={{ position: 'absolute', right: 8, top: '50%', transform: 'translateY(-50%)', background: 'none', border: 'none', cursor: 'pointer', color: '#8b97ab', display: 'flex', padding: 0 }}
            >
              <XIcon size={13} />
            </button>
          )}
        </div>
      </Section>

      {/* Direction */}
      <Section title="Direction">
        <div style={{ display: 'flex', background: '#1a2233', borderRadius: '8px', padding: '3px', gap: '2px' }}>
          {['all', 'long', 'short'].map(d => (
            <button
              key={d}
              onClick={() => set('direction', d)}
              aria-label={`Filter ${d} direction`}
              aria-pressed={direction === d}
              style={{
                flex: 1,
                background: direction === d ? (d === 'long' ? '#22c55e22' : d === 'short' ? '#ef444422' : '#6366f122') : 'transparent',
                border: direction === d ? `1px solid ${d === 'long' ? '#22c55e55' : d === 'short' ? '#ef444455' : '#6366f155'}` : '1px solid transparent',
                borderRadius: '6px',
                color: direction === d ? (d === 'long' ? '#22c55e' : d === 'short' ? '#ef4444' : '#e6edf6') : '#8b97ab',
                fontSize: '12px',
                fontWeight: 600,
                padding: '5px 0',
                cursor: 'pointer',
                transition: 'all 0.15s',
                textTransform: 'capitalize',
              }}
            >
              {d === 'long' ? '▲ Long' : d === 'short' ? '▼ Short' : 'All'}
            </button>
          ))}
        </div>
      </Section>

      {/* Setup filter */}
      <Section title="Setup">
        <div style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
          {SETUPS.map(({ key, label, color }) => {
            const active = setupFilter.includes(key);
            return (
              <button
                key={key}
                onClick={() => toggleSetup(key)}
                aria-label={`Filter setup: ${label}`}
                aria-pressed={active}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  background: active ? `${color}18` : '#1a2233',
                  border: `1px solid ${active ? color + '55' : '#243044'}`,
                  borderRadius: '7px',
                  padding: '6px 10px',
                  cursor: 'pointer',
                  color: active ? color : '#8b97ab',
                  fontSize: '12px',
                  fontWeight: active ? 600 : 400,
                  transition: 'all 0.15s',
                  textAlign: 'left',
                }}
              >
                <span style={{
                  width: 8, height: 8, borderRadius: '50%',
                  background: active ? color : '#243044',
                  flexShrink: 0,
                  transition: 'background 0.15s',
                }} />
                {label}
                {active && (
                  <XIcon size={11} style={{ marginLeft: 'auto', opacity: 0.7 }} />
                )}
                {active && (
                  <span style={{ marginLeft: 'auto' }}>
                    <XIcon size={11} />
                  </span>
                )}
              </button>
            );
          })}
        </div>
      </Section>

      {/* Sector */}
      <Section title="Sector">
        <select
          value={sector}
          onChange={e => set('sector', e.target.value)}
          aria-label="Filter by sector"
          style={{
            width: '100%',
            background: '#1a2233',
            border: '1px solid #243044',
            borderRadius: '7px',
            padding: '7px 10px',
            color: '#e6edf6',
            fontSize: '13px',
            outline: 'none',
            cursor: 'pointer',
          }}
        >
          <option value="">All Sectors</option>
          {sectors.map(s => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>
      </Section>

      {/* RelVol slider */}
      <Section title={`Min RelVol: ${minRelVol.toFixed(1)}×`}>
        <input
          type="range"
          min={1.0}
          max={5.0}
          step={0.1}
          value={minRelVol}
          onChange={e => set('minRelVol', parseFloat(e.target.value))}
          aria-label={`Minimum relative volume: ${minRelVol}`}
          style={{ width: '100%' }}
        />
        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '10px', color: '#8b97ab', marginTop: '3px' }}>
          <span>1.0×</span>
          <span>5.0×</span>
        </div>
      </Section>

      {/* RS min slider */}
      <Section title={`Min RS Rank: ${minRs}`}>
        <input
          type="range"
          min={0}
          max={100}
          step={5}
          value={minRs}
          onChange={e => set('minRs', parseInt(e.target.value))}
          aria-label={`Minimum RS rank: ${minRs}`}
          style={{ width: '100%' }}
        />
        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '10px', color: '#8b97ab', marginTop: '3px' }}>
          <span>0</span>
          <span>100</span>
        </div>
      </Section>

      {/* In-play toggle */}
      <Section title="In-Play Only">
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <span style={{ fontSize: '13px', color: '#8b97ab' }}>RelVol ≥ 2×</span>
          <label className="toggle-switch" aria-label="Show only in-play stocks">
            <input
              type="checkbox"
              checked={inPlayOnly}
              onChange={e => set('inPlayOnly', e.target.checked)}
            />
            <span className="toggle-slider" />
          </label>
        </div>
      </Section>
    </aside>
  );
}
