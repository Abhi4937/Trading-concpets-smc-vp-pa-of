import { ArrowUpIcon, ArrowDownIcon } from './Icons.jsx';
import { StockRow } from './StockRow.jsx';

const COLUMNS = [
  { key: null,        label: '★',         sortable: false, align: 'left',   width: 32 },
  { key: 'symbol',    label: 'Symbol',    sortable: true,  align: 'left',   width: 150 },
  { key: 'sector',    label: 'Sector',    sortable: false, align: 'left',   width: 100 },
  { key: 'ltp',       label: 'LTP',       sortable: true,  align: 'right',  width: 90 },
  { key: 'changePct', label: '%Chg',      sortable: true,  align: 'right',  width: 75 },
  { key: 'relVol',    label: 'RelVol',    sortable: true,  align: 'left',   width: 75 },
  { key: 'vwap',      label: 'VWAP',      sortable: false, align: 'left',   width: 100 },
  { key: 'rsRank',    label: 'RS',        sortable: true,  align: 'left',   width: 85 },
  { key: 'setup',     label: 'Setup',     sortable: false, align: 'left',   width: 120 },
  { key: null,        label: 'Trig / Stop / Target', sortable: false, align: 'left', width: 170 },
  { key: 'strength',  label: 'Str',       sortable: true,  align: 'left',   width: 70 },
  { key: null,        label: 'Spark',     sortable: false, align: 'left',   width: 100 },
];

function SortIcon({ direction }) {
  if (!direction) return <span style={{ width: 12, display: 'inline-block' }} />;
  return direction === 'asc'
    ? <ArrowUpIcon size={11} />
    : <ArrowDownIcon size={11} />;
}

export function StockTable({ stocks, sortConfig, onSort, selectedStock, onSelect, watchlist, onToggleWatchlist }) {
  if (stocks.length === 0) {
    return (
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '64px 32px',
        color: '#8b97ab',
      }}>
        <div style={{ fontSize: '32px', marginBottom: '12px' }}>🔍</div>
        <div style={{ fontSize: '16px', fontWeight: 600, color: '#e6edf6', marginBottom: '6px' }}>No stocks match your filters</div>
        <div style={{ fontSize: '13px' }}>Try adjusting the filter criteria in the left rail.</div>
      </div>
    );
  }

  return (
    <div style={{ overflowX: 'auto', width: '100%' }}>
      <table
        style={{
          width: '100%',
          borderCollapse: 'collapse',
          fontSize: '13px',
          tableLayout: 'auto',
        }}
        role="grid"
        aria-label="Stock screener results"
      >
        <thead>
          <tr style={{ background: '#0f1520', borderBottom: '2px solid #243044' }}>
            {COLUMNS.map((col, i) => (
              <th
                key={i}
                onClick={col.sortable && col.key ? () => onSort(col.key) : undefined}
                style={{
                  padding: '9px 10px',
                  textAlign: col.align,
                  fontSize: '11px',
                  fontWeight: 600,
                  color: sortConfig.key === col.key ? '#6366f1' : '#8b97ab',
                  letterSpacing: '0.06em',
                  textTransform: 'uppercase',
                  cursor: col.sortable && col.key ? 'pointer' : 'default',
                  userSelect: 'none',
                  whiteSpace: 'nowrap',
                  width: col.width,
                }}
                aria-sort={
                  sortConfig.key === col.key
                    ? sortConfig.dir === 'asc' ? 'ascending' : 'descending'
                    : 'none'
                }
              >
                <span style={{ display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
                  {col.label}
                  {col.sortable && col.key && (
                    <SortIcon direction={sortConfig.key === col.key ? sortConfig.dir : null} />
                  )}
                </span>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {stocks.map((stock, i) => (
            <StockRow
              key={stock.symbol}
              stock={stock}
              index={i}
              isSelected={selectedStock?.symbol === stock.symbol}
              isWatched={watchlist.includes(stock.symbol)}
              onSelect={onSelect}
              onToggleWatchlist={onToggleWatchlist}
            />
          ))}
        </tbody>
      </table>
    </div>
  );
}
