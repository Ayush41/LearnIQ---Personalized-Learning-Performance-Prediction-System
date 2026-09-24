// LearnIQ dashboard — single-file React frontend (only dependency: react).
// All data below is mock. Replace each MOCK section with a fetch() to your Python API
// (FastAPI/Flask), e.g. GET /students, POST /predict, POST /shap, GET /recommendations/:id.

export const TOPICS = ["Arrays", "Linked List", "Stack", "Trees", "Graphs"];
export const PREREQ = { Arrays: [], "Linked List": ["Arrays"], Stack: ["Arrays"], Trees: ["Linked List", "Stack"], Graphs: ["Trees"] };
export const STUDENTS = [
  { id: 1, name: "Aarav Sharma", prev: 72, quiz: 78, assign: 80, att: 91, hours: 14, freq: 5, topics: [92, 85, 66, 41, 30] },
  { id: 2, name: "Meera Nair", prev: 58, quiz: 55, assign: 62, att: 74, hours: 8, freq: 3, topics: [80, 58, 48, 35, 22] },
  { id: 3, name: "Rohan Verma", prev: 41, quiz: 38, assign: 45, att: 60, hours: 4, freq: 2, topics: [55, 40, 30, 18, 10] },
  { id: 4, name: "Sana Iqbal", prev: 88, quiz: 90, assign: 92, att: 96, hours: 18, freq: 6, topics: [96, 94, 90, 82, 70] },
];
export const FEATURES = [
  { k: "prev", label: "Previous marks", w: 0.36, mean: 62, max: 100, unit: "%" },
  { k: "quiz", label: "Quiz average", w: 0.22, mean: 62, max: 100, unit: "%" },
  { k: "assign", label: "Assignment average", w: 0.14, mean: 66, max: 100, unit: "%" },
  { k: "att", label: "Attendance", w: 0.12, mean: 78, max: 100, unit: "%" },
  { k: "hours", label: "Study hours / week", w: 0.6, mean: 10, max: 30, unit: "h" },
  { k: "freq", label: "Study days / week", w: 0.8, mean: 4, max: 7, unit: "d" },
];
export const MODELS = [
  { name: "Logistic Regression", acc: 0.81, pre: 0.8, rec: 0.79, f1: 0.79, auc: 0.87 },
  { name: "Random Forest", acc: 0.87, pre: 0.86, rec: 0.85, f1: 0.85, auc: 0.93 },
  { name: "SVM", acc: 0.84, pre: 0.83, rec: 0.82, f1: 0.82, auc: 0.9 },
  { name: "XGBoost", acc: 0.89, pre: 0.88, rec: 0.87, f1: 0.87, auc: 0.95 },
];
export const CENTERS = [
  { name: "Consistent achievers", hours: 16, quiz: 82, color: "#2F8F6F", note: "High quiz scores, regular study routine." },
  { name: "Steady, inconsistent", hours: 9, quiz: 60, color: "#C98A2E", note: "Decent results, but study days are uneven." },
  { name: "Low engagement", hours: 4, quiz: 38, color: "#C1432E", note: "Few study hours and weak quiz results." },
];

const rng = (seed) => () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
export const POINTS = (() => {
  const r = rng(42);
  return CENTERS.flatMap((c, ci) => Array.from({ length: 24 }, () => ({ h: Math.max(0.5, c.hours + (r() - 0.5) * 8), q: Math.max(5, Math.min(98, c.quiz + (r() - 0.5) * 26)), ci })));
})();
