import { useState } from "react";
import { signIn } from "../utils/auth.js";

export default function Login({ onLogin }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [show, setShow] = useState(false);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    setError("");
    setBusy(true);
    try {
      onLogin(await signIn(email, password));
    } catch (err) {
      setError(err.message);
      setBusy(false);
    }
  };

  return (
    <div className="login">
      <div className="login-side">
        <div className="brand">
          <span className="mark">Lq</span>
          <div className="logo">LearnIQ</div>
        </div>

        <div className="pitch">
          <h1>Know who needs help before the exam does.</h1>
          <p>LearnIQ reads study hours, quiz scores, and topic-level attempts, then predicts marks, flags risk, and lines up what each student should study next.</p>
        </div>

        <svg className="ledger" viewBox="0 0 460 180" role="img" aria-label="Rising line chart of predicted marks over the term">
          <line x1="0" y1="30" x2="460" y2="30" className="rule" />
          <line x1="0" y1="75" x2="460" y2="75" className="rule" />
          <line x1="0" y1="120" x2="460" y2="120" className="rule" />
          <polyline points="10,140 90,118 170,126 250,88 330,64 410,34" className="trend" />
          <circle cx="410" cy="34" r="5" className="dot-hi" />
          <circle cx="250" cy="88" r="4" className="dot-mid" />
          <circle cx="90" cy="118" r="4" className="dot-lo" />
          <text x="10" y="160" className="axis-label">Week 1</text>
          <text x="410" y="160" textAnchor="end" className="axis-label">Exam</text>
        </svg>

        <div className="stats-row">
          <div><b>89%</b><span>XGBoost accuracy on held-out students</span></div>
          <div><b>3</b><span>learning segments discovered</span></div>
        </div>
      </div>

      <form className="login-form" onSubmit={submit} noValidate>
        <div className="form-head">
          <h2>Sign in</h2>
          <p className="muted">Use your mentor account to open the dashboard.</p>
        </div>

        <div className="field">
          <label htmlFor="email">Email</label>
          <input id="email" type="email" autoComplete="username" required value={email} onChange={(e) => setEmail(e.target.value)} />
        </div>
        <div className="field">
          <label htmlFor="password">Password</label>
          <div className="pw">
            <input id="password" type={show ? "text" : "password"} autoComplete="current-password" required value={password} onChange={(e) => setPassword(e.target.value)} />
            <button type="button" onClick={() => setShow(!show)} aria-pressed={show}>{show ? "Hide" : "Show"}</button>
          </div>
        </div>

        {error && <div className="err" role="alert">{error}</div>}

        <button className="primary" type="submit" disabled={busy || !email || !password}>
          {busy ? "Signing in…" : "Sign in"}
        </button>
      </form>
    </div>
  );
}
