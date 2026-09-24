export const riskClass = (r) => (r === "High" ? "bad" : r === "Medium" ? "mid" : "good");
export const Badge = ({ risk }) => <span className={`badge ${riskClass(risk)}`}>{risk} risk</span>;
export const Bar = ({ value, tone = "good" }) => (
  <div className="track"><div className={`fill ${tone}`} style={{ width: `${Math.max(2, Math.min(100, value))}%` }} /></div>
);

