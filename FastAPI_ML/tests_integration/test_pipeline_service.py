"""
Unit tests — app/services/pipeline.py
"""
import pytest
import pandas as pd
import numpy as np
from unittest.mock import MagicMock, patch
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.pipeline import PipelineService


@pytest.fixture
def svc():
    return PipelineService()


# ---------------------------------------------------------------------------
# _build_pipeline
# ---------------------------------------------------------------------------

class TestBuildPipeline:

    def test_returns_calibrated_classifier(self, svc):
        from sklearn.calibration import CalibratedClassifierCV
        assert isinstance(svc._build_pipeline(), CalibratedClassifierCV)

    def test_inner_estimator_is_random_forest(self, svc):
        from sklearn.ensemble import RandomForestClassifier
        rf = svc._build_pipeline().estimator.named_steps["classifier"]
        assert isinstance(rf, RandomForestClassifier)

    def test_draw_class_has_highest_weight(self, svc):
        rf = svc._build_pipeline().estimator.named_steps["classifier"]
        assert rf.class_weight[1] > rf.class_weight[0]
        assert rf.class_weight[1] > rf.class_weight[2]

    def test_pipeline_fits_without_error(self, svc, training_df):
        from sklearn.preprocessing import LabelEncoder
        X = training_df[svc._NUM_FEATURES + svc._CAT_FEATURES]
        y = LabelEncoder().fit_transform(training_df["Result"])
        pipeline = svc._build_pipeline()
        pipeline.cv = 2  # reduce cv to match small test dataset
        pipeline.fit(X, y)


# ---------------------------------------------------------------------------
# train
# ---------------------------------------------------------------------------

class TestTrain:

    def test_raises_when_no_data(self, svc):
        db = MagicMock()
        with patch.object(svc, "_load_from_db", return_value=pd.DataFrame()):
            with pytest.raises(ValueError, match="Aucun match"):
                svc.train(db)

    def test_returns_success_status(self, svc, training_df):
        db = MagicMock()
        with patch.object(svc, "_load_from_db",          return_value=training_df), \
             patch.object(svc, "_build_pipeline",         return_value=MagicMock()), \
             patch.object(svc, "_save_model"), \
             patch.object(svc, "_populate_feature_store"), \
             patch.object(svc, "_save_train_log"), \
             patch("app.services.pipeline.cross_val_score",
                   return_value=np.array([0.65] * 5)), \
             patch("app.services.ml_service.ml_service"):
            result = svc.train(db)
        assert result["status"] == "success"

    def test_returns_correct_n_samples(self, svc, training_df):
        db = MagicMock()
        with patch.object(svc, "_load_from_db",          return_value=training_df), \
             patch.object(svc, "_build_pipeline",         return_value=MagicMock()), \
             patch.object(svc, "_save_model"), \
             patch.object(svc, "_populate_feature_store"), \
             patch.object(svc, "_save_train_log"), \
             patch("app.services.pipeline.cross_val_score",
                   return_value=np.array([0.65] * 5)), \
             patch("app.services.ml_service.ml_service"):
            result = svc.train(db)
        assert result["n_samples"] == len(training_df)

    def test_model_version_is_8_digit_date(self, svc, training_df):
        db = MagicMock()
        with patch.object(svc, "_load_from_db",          return_value=training_df), \
             patch.object(svc, "_build_pipeline",         return_value=MagicMock()), \
             patch.object(svc, "_save_model"), \
             patch.object(svc, "_populate_feature_store"), \
             patch.object(svc, "_save_train_log"), \
             patch("app.services.pipeline.cross_val_score",
                   return_value=np.array([0.65] * 5)), \
             patch("app.services.ml_service.ml_service"):
            result = svc.train(db)
        assert len(result["model_version"]) == 8
        assert result["model_version"].isdigit()

    def test_returns_cv_metrics(self, svc, training_df):
        db = MagicMock()
        with patch.object(svc, "_load_from_db",          return_value=training_df), \
             patch.object(svc, "_build_pipeline",         return_value=MagicMock()), \
             patch.object(svc, "_save_model"), \
             patch.object(svc, "_populate_feature_store"), \
             patch.object(svc, "_save_train_log"), \
             patch("app.services.pipeline.cross_val_score",
                   return_value=np.array([0.65] * 5)), \
             patch("app.services.ml_service.ml_service"):
            result = svc.train(db)
        assert "cv_accuracy" in result
        assert "cv_log_loss" in result


# ---------------------------------------------------------------------------
# get_history
# ---------------------------------------------------------------------------

class TestGetHistory:

    def test_returns_a_list(self, svc):
        db = MagicMock()
        db.query.return_value.order_by.return_value.limit.return_value.all.return_value = []
        assert isinstance(svc.get_history(db, limit=10), list)

    def test_respects_limit_parameter(self, svc):
        from app.models.match import TrainLog
        from datetime import datetime, timezone
        logs = [
            MagicMock(spec=TrainLog, id=i, created_at=datetime.now(timezone.utc),
                      model_version="20240101", n_samples=100,
                      cv_accuracy=0.6, cv_log_loss=0.9, status="success")
            for i in range(5)
        ]
        db = MagicMock()
        db.query.return_value.order_by.return_value.limit.return_value.all.return_value = logs[:2]
        assert len(svc.get_history(db, limit=2)) <= 2

    def test_record_has_all_expected_keys(self, svc):
        from app.models.match import TrainLog
        from datetime import datetime, timezone
        log = MagicMock(spec=TrainLog, id=1, created_at=datetime.now(timezone.utc),
                        model_version="20240101", n_samples=200,
                        cv_accuracy=0.67, cv_log_loss=0.85, status="success")
        db = MagicMock()
        db.query.return_value.order_by.return_value.limit.return_value.all.return_value = [log]
        record = svc.get_history(db, limit=1)[0]
        for key in ["id", "created_at", "model_version", "n_samples",
                    "cv_accuracy", "cv_log_loss", "status"]:
            assert key in record, f"Missing key: {key}"
