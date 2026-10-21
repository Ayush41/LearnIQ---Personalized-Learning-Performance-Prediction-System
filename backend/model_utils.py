from __future__ import annotations

from typing import Any

import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin, clone
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.utils.validation import check_is_fitted


class TargetLabelClassifier(ClassifierMixin, BaseEstimator):
    """Encode string targets for estimators requiring integer class labels."""

    def __init__(self, estimator: Any):
        self.estimator = estimator

    def fit(self, X: Any, y: Any, **fit_params: Any) -> TargetLabelClassifier:
        self.label_encoder_ = LabelEncoder()
        encoded_y = self.label_encoder_.fit_transform(y)
        self.estimator_ = clone(self.estimator)
        self.estimator_.fit(X, encoded_y, **fit_params)
        return self

    @property
    def classes_(self) -> np.ndarray:
        check_is_fitted(self, "label_encoder_")
        return self.label_encoder_.classes_

    @property
    def feature_importances_(self) -> np.ndarray:
        check_is_fitted(self, "estimator_")
        return self.estimator_.feature_importances_

    def predict(self, X: Any) -> np.ndarray:
        check_is_fitted(self, "estimator_")
        encoded_predictions = np.asarray(self.estimator_.predict(X), dtype=int)
        return self.label_encoder_.inverse_transform(encoded_predictions)

    def predict_proba(self, X: Any) -> np.ndarray:
        check_is_fitted(self, "estimator_")
        return self.estimator_.predict_proba(X)

    def score(self, X: Any, y: Any) -> float:
        return float(accuracy_score(y, self.predict(X)))