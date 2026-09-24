import { useState } from "react";
import { FEATURES } from "../data/mock.js";
import { predict } from "../utils/model.js";

export default function WhatIf({ s }) {
  const [v, setV] = useState({ hours: s.hours, quiz: s.quiz, att: s.att, assign: s.assign });
  const base = predict(s), now = predict({ ...s, ...v }), d = now.marks - base.marks;
  const set = (k) => (e) => setV({ ...v, [k]: +e.target.value });
  return (
    <>
      <h2>What if {s.name.split(" ")[0]} changed?</h2>
      <div className="grid">{["hours", "quiz", "att", "assign"].map((k) => {
        const f = FEATURES.find((x) => x.k === k);
        return (
          <label key={k} className="row"><span>{f.label}</span><b>{v[k]}{f.unit}</b>
            <input type="range" min="0" max={f.max} value={v[k]} onChange={set(k)} /></label>);
      })}</div>
      <section className="hero">
        <div><div className="big">{base.marks.toFixed(0)}</div><div className="muted">current prediction</div></div>
        <div><div className="big">{now.marks.toFixed(0)}</div><div className="muted">with changes</div></div>
        <div><div className={`big ${d >= 0 ? "up" : "down"}`}>{d >= 0 ? "+" : ""}{d.toFixed(1)}</div><div className="muted">marks · {Math.round(now.pass * 100)}% pass chance</div></div>
      </section>
      <button className="ghost" onClick={() => setV({ hours: s.hours, quiz: s.quiz, att: s.att, assign: s.assign })}>Reset to current values</button>
    </>
  );
}
