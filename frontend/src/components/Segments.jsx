import { CENTERS, POINTS } from "../data/mock.js";
import { segmentOf } from "../utils/model.js";

export default function Segments({ s }) {
  const W = 520, H = 320, x = (h) => 40 + (h / 24) * (W - 60), y = (q) => H - 36 - (q / 100) * (H - 56);
  const seg = segmentOf(s);
  return (
    <>
      <h2>Student segments (K-Means, K = 3)</h2>
      <p className="muted">Silhouette score 0.52. {s.name} belongs to <b>{seg.name}</b>.</p>
      <svg viewBox={`0 0 ${W} ${H}`} className="chart" role="img" aria-label="Scatter of study hours versus quiz average by segment">
        {[0, 25, 50, 75, 100].map((q) => <g key={q}><line x1="40" x2={W - 20} y1={y(q)} y2={y(q)} stroke="#dfe5e8" /><text x="34" y={y(q) + 4} textAnchor="end" fontSize="10" fill="#5d6b72">{q}</text></g>)}
        {[0, 6, 12, 18, 24].map((h) => <text key={h} x={x(h)} y={H - 18} textAnchor="middle" fontSize="10" fill="#5d6b72">{h}h</text>)}
        <text x={W / 2} y={H - 3} textAnchor="middle" fontSize="11" fill="#5d6b72">Study hours per week</text>
        <text x="10" y="14" fontSize="11" fill="#5d6b72">Quiz average</text>
        {POINTS.map((p, i) => <circle key={i} cx={x(p.h)} cy={y(p.q)} r="4" fill={CENTERS[p.ci].color} opacity=".55" />)}
        <circle cx={x(s.hours)} cy={y(s.quiz)} r="8" fill="none" stroke="#14213d" strokeWidth="3" />
        <text x={x(s.hours) + 12} y={y(s.quiz) - 8} fontSize="11" fontWeight="700" fill="#14213d">{s.name.split(" ")[0]}</text>
      </svg>
      <div className="grid">{CENTERS.map((c) => (
        <div key={c.name} className="row"><span><i className="dot" style={{ background: c.color }} />{c.name}</span><span className="muted">{c.note}</span></div>))}</div>
    </>
  );
}
