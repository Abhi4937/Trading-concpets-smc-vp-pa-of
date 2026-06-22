/**
 * Sparkline.jsx — Inline SVG sparkline with gradient area fill.
 * No external chart library. Pure SVG.
 */

export function Sparkline({ data = [], width = 100, height = 30, id }) {
  if (!data || data.length < 2) {
    return <svg width={width} height={height} aria-hidden="true" />;
  }

  const min = Math.min(...data);
  const max = Math.max(...data);
  const range = max - min || 1;

  const pad = 2;
  const w = width - pad * 2;
  const h = height - pad * 2;

  const toX = (i) => pad + (i / (data.length - 1)) * w;
  const toY = (v) => pad + h - ((v - min) / range) * h;

  const points = data.map((v, i) => `${toX(i)},${toY(v)}`).join(' ');
  const isUp = data[data.length - 1] >= data[0];
  const color = isUp ? '#22c55e' : '#ef4444';
  const colorStop = isUp ? '#22c55e' : '#ef4444';

  // Area path: line + close polygon bottom
  const areaPath = [
    `M ${toX(0)},${toY(data[0])}`,
    ...data.slice(1).map((v, i) => `L ${toX(i + 1)},${toY(v)}`),
    `L ${toX(data.length - 1)},${pad + h}`,
    `L ${toX(0)},${pad + h}`,
    'Z',
  ].join(' ');

  const gradId = `spark-grad-${id || Math.random().toString(36).slice(2)}`;

  return (
    <svg
      width={width}
      height={height}
      viewBox={`0 0 ${width} ${height}`}
      aria-hidden="true"
      style={{ display: 'block', overflow: 'visible' }}
    >
      <defs>
        <linearGradient id={gradId} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor={colorStop} stopOpacity="0.25" />
          <stop offset="100%" stopColor={colorStop} stopOpacity="0.02" />
        </linearGradient>
      </defs>
      {/* Area fill */}
      <path d={areaPath} fill={`url(#${gradId})`} />
      {/* Line */}
      <polyline
        points={points}
        fill="none"
        stroke={color}
        strokeWidth={1.5}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      {/* End dot */}
      <circle
        cx={toX(data.length - 1)}
        cy={toY(data[data.length - 1])}
        r={2}
        fill={color}
      />
    </svg>
  );
}
