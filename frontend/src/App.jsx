import { useMemo, useState } from "react";
import { STUDENTS } from "./data/mock.js";
import Overview from "./components/Overview.jsx";
import Prediction from "./components/Prediction.jsx";
import Segments from "./components/Segments.jsx";
import Gaps from "./components/Gaps.jsx";
import Recs from "./components/Recs.jsx";
import WhatIf from "./components/WhatIf.jsx";
import Shap from "./components/Shap.jsx";
import Login from "./components/Login.jsx";
import { loadUser, signOut } from "./utils/auth.js";
import "./styles.css";

const TABS = [
  ["Overview", Overview], ["Prediction", Prediction], ["Segments", Segments],
  ["Knowledge gaps", Gaps], ["Study path", Recs], ["What-if", WhatIf], ["Explanation", Shap],
];

export default function App() {
  const [tab, setTab] = useState(0);
  const [id, setId] = useState(1);
  const [user, setUser] = useState(loadUser);
  const s = useMemo(() => STUDENTS.find((x) => x.id === id), [id]);
  const View = TABS[tab][1];

  if (!user) return <Login onLogin={setUser} />;

  const logout = () => { signOut(); setUser(null); setTab(0); };

  return (
    <div className="app">
      <aside>
        <div className="brand">
          <span className="mark">Lq</span>
          <div>
            <div className="logo">LearnIQ</div>
            <div className="tagline">Performance predictor</div>
          </div>
        </div>
        <nav>
          {TABS.map(([n], i) => (
            <button key={n} className={i === tab ? "on" : ""} onClick={() => setTab(i)}>{n}</button>
          ))}
        </nav>
        <div className="side-foot">
          <span className="who">{user.name}</span>
          <button className="linkbtn" onClick={logout}>Sign out</button>
        </div>
      </aside>
      <main>
        <header>
          <label className="picker">
            Student
            <select value={id} onChange={(e) => setId(+e.target.value)}>
              {STUDENTS.map((x) => <option key={x.id} value={x.id}>{x.name}</option>)}
            </select>
          </label>
          <span className="section-name">{TABS[tab][0]}</span>
        </header>
        <View key={tab + "-" + id} s={s} all={STUDENTS} pick={setId} />
      </main>
    </div>
  );
}
