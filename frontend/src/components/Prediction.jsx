import { MODELS } from "../data/mock.js";
import { predict } from "../utils/model.js";
import { riskClass, Badge, Bar } from "./ui.jsx";

export default function Prediction({ s }) {
  const p = predict(s);
  return (
    <>
      <h2>Prediction for {s.name}</h2>
      <div className="grid">
        <div className="row"><span>Predicted marks</span><b>{p.marks.toFixed(1)} / 100</b><Bar value={p.marks} tone={riskClass(p.risk)} /></div>
        <div className="row"><span>Pass probability</span><b>{(p.pass * 100).toFixed(1)}%</b><Bar value={p.pass * 100} tone={riskClass(p.risk)} /></div>
        <div className="row"><span>Performance category</span><b>{p.category}</b></div>
        <div className="row"><span>Risk level</span><Badge risk={p.risk} /></div>
      </div>
      <h2>Model comparison</h2>
      <table><thead><tr><th>Model</th><th>Accuracy</th><th>Precision</th><th>Recall</th><th>F1</th><th>ROC-AUC</th></tr></thead>
        <tbody>{MODELS.map((m, i) => (
          <tr key={m.name} className={i === 3 ? "sel" : ""}><td>{m.name}{i === 3 && " (saved)"}</td><td>{m.acc}</td><td>{m.pre}</td><td>{m.rec}</td><td>{m.f1}</td><td>{m.auc}</td></tr>))}</tbody></table>
    </>
  );
}
