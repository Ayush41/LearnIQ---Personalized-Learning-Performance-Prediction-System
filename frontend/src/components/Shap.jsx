import { predict, explain } from "../utils/model.js";
import { Badge } from "./ui.jsx";

export default function Shap({ s }) {
  const ex = explain(s), max = Math.max(...ex.map((e) => Math.abs(e.v)), 1), p = predict(s);
  return (
    <>
      <h2>Why this prediction?</h2>
      <p className="muted">Risk: <Badge risk={p.risk} />. Bars show how much each input moved the predicted marks away from the class average.</p>
      <div className="shap">{ex.map((e) => (
        <div key={e.label} className="srow">
          <span>{e.label}</span>
          <div className="axis"><div className={`sbar ${e.v >= 0 ? "pos" : "neg"}`} style={{ width: `${(Math.abs(e.v) / max) * 50}%`, [e.v >= 0 ? "left" : "right"]: "50%" }} /></div>
          <b>{e.v >= 0 ? "+" : ""}{e.v.toFixed(1)}</b>
        </div>))}</div>
    </>
  );
}
