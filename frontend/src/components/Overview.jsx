import { FEATURES } from "../data/mock.js";
import { predict, segmentOf } from "../utils/model.js";
import { Badge, Bar } from "./ui.jsx";

export default function Overview({ s, all, pick }) {
  const p = predict(s);
  return (
    <>
      <section className="hero">
        <div><div className="big">{p.marks.toFixed(0)}</div><div className="muted">predicted final marks</div></div>
        <div><div className="big">{Math.round(p.pass * 100)}%</div><div className="muted">chance of passing</div></div>
        <div><Badge risk={p.risk} /><div className="muted" style={{ marginTop: 8 }}>{segmentOf(s).name}</div></div>
      </section>
      <h2>Current inputs</h2>
      <div className="grid">
        {FEATURES.map((f) => (
          <div key={f.k} className="row"><span>{f.label}</span><b>{s[f.k]}{f.unit}</b><Bar value={(s[f.k] / f.max) * 100} /></div>
        ))}
      </div>
      <h2>All students</h2>
      <table><thead><tr><th>Student</th><th>Predicted marks</th><th>Risk</th><th>Segment</th></tr></thead>
        <tbody>{all.map((x) => (
          <tr key={x.id} className={x.id === s.id ? "sel" : ""} onClick={() => pick(x.id)}>
            <td>{x.name}</td><td>{predict(x).marks.toFixed(0)}</td><td><Badge risk={predict(x).risk} /></td><td>{segmentOf(x).name}</td>
          </tr>))}</tbody></table>
    </>
  );
}
