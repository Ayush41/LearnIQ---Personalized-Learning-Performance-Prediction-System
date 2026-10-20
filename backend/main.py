from __future__ import annotations

import pickle
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sklearn.cluster import KMeans
from sklearn.inspection import permutation_importance
from sklearn.metrics import silhouette_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "processed"
MODEL_DIR = PROJECT_ROOT / "models"
STUDENT_DATA_PATH = DATA_DIR / "student_performance_processed.csv"
TOPIC_DATA_PATH = DATA_DIR / "topic_attempts_processed.csv"
MODEL_CANDIDATES = [
    MODEL_DIR / "student_performance_ensemble.pkl",
    MODEL_DIR / "student_performance_model.pkl",
]
EXCLUDED_FEATURES = {
    "student_id",
    "performance_category",
    "risk_level",
    "final_marks",
    "passed",
}

app = FastAPI(
    title="LearnIQ API",
    description="Student performance prediction and learning analytics for the LearnIQ MVP.",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PredictionRequest(BaseModel):
    features: dict[str, Any] = Field(default_factory=dict)


class WhatIfRequest(BaseModel):
    current: dict[str, Any] = Field(default_factory=dict)
    scenario: dict[str, Any] = Field(default_factory=dict)


def _read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise HTTPException(status_code=503, detail=f"Required data file not found: {path.name}")
    return pd.read_csv(path)


def _student_data() -> pd.DataFrame:
    return _read_csv(STUDENT_DATA_PATH)


def _topic_data() -> pd.DataFrame:
    return _read_csv(TOPIC_DATA_PATH)


def _load_model() -> tuple[Any | None, str | None]:
    for path in MODEL_CANDIDATES:
        if path.exists():
            try:
                with path.open("rb") as model_file:
                    return pickle.load(model_file), path.name
            except Exception as error:
                raise RuntimeError(f"Could not load model artifact {path.name}: {error}") from error
    return None, None


model, model_filename = _load_model()


def _feature_columns(df: pd.DataFrame) -> list[str]:
    return [column for column in df.columns if column not in EXCLUDED_FEATURES]


def _feature_defaults(df: pd.DataFrame, columns: list[str]) -> dict[str, Any]:
    defaults: dict[str, Any] = {}
    for column in columns:
        series = df[column]
        if pd.api.types.is_numeric_dtype(series):
            median = series.median()
            defaults[column] = 0 if pd.isna(median) else float(median)
        else:
            mode = series.mode(dropna=True)
            defaults[column] = str(mode.iloc[0]) if not mode.empty else "unknown"
    return defaults


def _prediction(features: dict[str, Any]) -> dict[str, Any]:
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="No trained model found. Run a model notebook to create a model artifact first.",
        )

    df = _student_data()
    columns = _feature_columns(df)
    row = _feature_defaults(df, columns)
    for key, value in features.items():
        if key in row and value is not None:
            row[key] = value

    input_frame = pd.DataFrame([{column: row[column] for column in columns}], columns=columns)
    try:
        predicted_class = str(model.predict(input_frame)[0])
        probabilities: dict[str, float] = {}
        if hasattr(model, "predict_proba"):
            values = model.predict_proba(input_frame)[0]
            classes = model.classes_
            probabilities = {
                str(label): round(float(probability), 4)
                for label, probability in zip(classes, values)
            }
        confidence = probabilities.get(predicted_class)
    except Exception as error:
        raise HTTPException(status_code=422, detail=f"Could not score the supplied features: {error}") from error

    normalized_class = predicted_class.strip().lower()
    risk = "High" if normalized_class in {"poor", "needs improvement", "fail", "at risk"} else (
        "Medium" if normalized_class in {"average", "moderate"} else "Low"
    )
    return {
        "predicted_category": predicted_class,
        "confidence": confidence,
        "risk_level": risk,
        "class_probabilities": probabilities,
        "model": model_filename,
    }


def _safe_records(frame: pd.DataFrame) -> list[dict[str, Any]]:
    return frame.astype(object).where(pd.notna(frame), None).to_dict(orient="records")


@app.get("/api/v1/health")
def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "student_data_loaded": STUDENT_DATA_PATH.exists(),
        "topic_data_loaded": TOPIC_DATA_PATH.exists(),
        "model_loaded": model is not None,
        "model": model_filename,
    }


@app.get("/api/v1/dashboard")
def dashboard() -> dict[str, Any]:
    students = _student_data()
    topics = _topic_data()
    category_counts = students["performance_category"].value_counts().to_dict()
    topic_summary = (
        topics.groupby("topic", as_index=False)
        .agg(avg_score=("topic_score", "mean"), attempts=("attempt_count", "sum"))
        .sort_values("avg_score")
    )
    return {
        "student_count": int(len(students)),
        "topic_attempt_count": int(len(topics)),
        "average_final_marks": round(float(students["final_marks"].mean()), 1),
        "pass_rate": round(float(students["passed"].mean() * 100), 1),
        "average_attendance": round(float(students["attendance_pct"].mean()), 1),
        "performance_categories": {str(key): int(value) for key, value in category_counts.items()},
        "topic_summary": _safe_records(topic_summary),
        "model": model_filename,
    }


@app.get("/api/v1/students")
def students(
    search: str = Query(default="", max_length=80),
    limit: int = Query(default=100, ge=1, le=500),
) -> dict[str, Any]:
    df = _student_data()
    if search:
        df = df[df["student_id"].astype(str).str.contains(search, case=False, na=False)]
    return {"items": _safe_records(df.head(limit)), "total": int(len(df))}


@app.get("/api/v1/students/{student_id}")
def student_detail(student_id: str) -> dict[str, Any]:
    df = _student_data()
    row = df[df["student_id"].astype(str) == student_id]
    if row.empty:
        raise HTTPException(status_code=404, detail="Student not found")
    topic_rows = _topic_data()
    topic_rows = topic_rows[topic_rows["student_id"].astype(str) == student_id]
    return {"student": _safe_records(row.head(1))[0], "topics": _safe_records(topic_rows)}


@app.get("/api/v1/students/{student_id}/knowledge-gaps")
def knowledge_gaps(student_id: str) -> dict[str, Any]:
    data = student_detail(student_id)["topics"]
    topics = pd.DataFrame(data)
    if topics.empty:
        return {"student_id": student_id, "topics": []}
    topics["status"] = np.select(
        [topics["topic_score"] >= 75, topics["topic_score"] >= 50],
        ["Strong", "Moderate"],
        default="Weak",
    )
    topics = topics.sort_values("topic_score")
    return {"student_id": student_id, "topics": _safe_records(topics)}


@app.get("/api/v1/students/{student_id}/recommendations")
def recommendations(student_id: str) -> dict[str, Any]:
    gaps = knowledge_gaps(student_id)["topics"]
    weak_topics = [topic for topic in gaps if topic["status"] != "Strong"]
    items = [
        {
            "topic": topic["topic"],
            "score": float(topic["topic_score"]),
            "priority": "High" if topic["status"] == "Weak" else "Medium",
            "action": f"Review {topic['topic']} and complete a short practice quiz.",
            "estimated_minutes": 30 if topic["status"] == "Weak" else 20,
        }
        for topic in weak_topics[:5]
    ]
    return {"student_id": student_id, "recommendations": items}


@app.post("/api/v1/predict")
def predict(request: PredictionRequest) -> dict[str, Any]:
    return _prediction(request.features)


@app.post("/api/v1/what-if")
def what_if(request: WhatIfRequest) -> dict[str, Any]:
    current = _prediction(request.current)
    scenario = _prediction(request.scenario)
    return {
        "current": current,
        "scenario": scenario,
        "category_changed": current["predicted_category"] != scenario["predicted_category"],
    }