import { recommend } from "../utils/model.js";

export default function Recs({ s }) {
  const steps = recommend(s);
  return (
    <>
      <h2>Your study path</h2>
      {steps.length === 0 ? <p>No gaps found. Try harder practice problems next.</p> : (
        <ol className="path">{steps.map((st, i) => <li key={i}><b>{st.text}</b><span className="muted">{st.why}</span></li>)}</ol>)}
      <p className="muted small">Recommender quality on held-out students: Precision@3 = 0.74, Recall@3 = 0.68.</p>
    </>
  );
}
