// Stand-ins for the trained models. Replace with POST /predict, /shap, /recommend.
import { TOPICS, PREREQ, FEATURES, CENTERS } from "../data/mock.js";

export const predict = (s) => {
  const marks = Math.max(0, Math.min(100, FEATURES.reduce((a, f) => a + f.w * s[f.k], 0)));
  const pass = 1 / (1 + Math.exp(-(marks - 50) / 7));
  const risk = marks < 50 ? "High" : marks < 65 ? "Medium" : "Low";
  const category = marks >= 80 ? "Excellent" : marks >= 65 ? "Good" : marks >= 50 ? "Average" : "Needs support";
  return { marks, pass, risk, category };
};
export const explain = (s) => FEATURES.map((f) => ({ label: f.label, v: f.w * (s[f.k] - f.mean) })).sort((a, b) => Math.abs(b.v) - Math.abs(a.v));
export const level = (x) => (x >= 75 ? "Strong" : x >= 50 ? "Moderate" : "Weak");
export const segmentOf = (s) => {
  const d = (c) => ((s.hours - c.hours) / 30) ** 2 + ((s.quiz - c.quiz) / 100) ** 2;
  return CENTERS.reduce((b, c) => (d(c) < d(b) ? c : b));
};
export const recommend = (s) => {
  const steps = [];
  TOPICS.forEach((t, i) => {
    const l = level(s.topics[i]);
    if (l === "Moderate") steps.push({ text: `Revise ${t}`, why: `Score ${s.topics[i]}% — close to strong.` });
    if (l === "Weak") {
      const blocked = PREREQ[t].filter((p) => level(s.topics[TOPICS.indexOf(p)]) === "Weak");
      steps.push({ text: `Study ${t}`, why: blocked.length ? `Score ${s.topics[i]}%. Fix ${blocked.join(", ")} first.` : `Score ${s.topics[i]}%. Prerequisites are covered.` });
    }
  });
  const firstWeak = TOPICS.find((t, i) => level(s.topics[i]) === "Weak");
  if (firstWeak) steps.push({ text: `Practice ${firstWeak} problems`, why: "Apply the concept before testing yourself." }, { text: `Attempt ${firstWeak} quiz`, why: "Confirms the gap is closed." });
  return steps;
};
