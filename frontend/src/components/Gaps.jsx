import { TOPICS, PREREQ } from "../data/mock.js";
import { level } from "../utils/model.js";
import { Bar } from "./ui.jsx";

export default function Gaps({ s }) {
  return (
    <>
      <h2>Knowledge gaps</h2>
      <div className="grid">{TOPICS.map((t, i) => {
        const l = level(s.topics[i]);
        return (
          <div key={t} className="row">
            <span>{t}</span><b>{s.topics[i]}% · {l}</b>
            <Bar value={s.topics[i]} tone={l === "Strong" ? "good" : l === "Moderate" ? "mid" : "bad"} />
            <span className="muted small">{PREREQ[t].length ? `Needs: ${PREREQ[t].join(", ")}` : "No prerequisites"}</span>
          </div>);
      })}</div>
    </>
  );
}
