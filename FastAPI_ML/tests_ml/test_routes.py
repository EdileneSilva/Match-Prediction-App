"""
Integration tests — FastAPI routes (no real database).
All DB dependencies are replaced with MagicMock.
"""
import pytest
import io
import numpy as np
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture(scope="module")
def client():
    with patch("app.database.create_engine"), \
         patch("app.database.Base.metadata.create_all"), \
         patch("app.core.config.settings") as mock_settings:

        mock_settings.PROJECT_NAME    = "Test"
        mock_settings.PROJECT_VERSION = "0.0.1"
        mock_settings.DATABASE_URL    = "sqlite:///:memory:"
        mock_settings.MODEL_PATH      = "/tmp/no_model.joblib"
        mock_settings.DATA_DIR        = "/tmp/"
        mock_settings.DATASET_PATH    = "/tmp/"
        mock_settings.CORS_ORIGINS    = ["*"]

        from app.main import app
        from app.database import get_db

        app.dependency_overrides[get_db] = lambda: MagicMock()
        yield TestClient(app)
        app.dependency_overrides.clear()


def _seeded_db():
    """Returns a mock DB with two known teams."""
    home = MagicMock(); home.name = "Paris SG"
    away = MagicMock(); away.name = "Lyon"
    db   = MagicMock()
    db.query.return_value.filter.return_value.first.side_effect = [home, away]
    return db


def _mock_ml(loaded=True, has_stats=True):
    m = MagicMock()
    m.is_model_loaded = loaded
    m.home_stats      = MagicMock() if has_stats else None
    m.predict_match.return_value = {
        "match":      "Paris SG vs Lyon",
        "prediction": "HOME_WIN",
        "confidence": 0.72,
        "probabilities": {"HOME": 0.72, "DRAW": 0.18, "AWAY": 0.10},
    }
    return m


# ---------------------------------------------------------------------------
# GET /health
# ---------------------------------------------------------------------------

class TestHealth:

    def test_returns_200(self, client):
        assert client.get("/health").status_code == 200

    def test_returns_ok_status(self, client):
        assert client.get("/health").json()["status"] == "ok"

    def test_has_service_key(self, client):
        assert "service" in client.get("/health").json()


# ---------------------------------------------------------------------------
# GET /teams
# ---------------------------------------------------------------------------

class TestGetTeams:

    def test_returns_200(self, client):
        assert client.get("/teams").status_code == 200

    def test_returns_list(self, client):
        assert isinstance(client.get("/teams").json(), list)


# ---------------------------------------------------------------------------
# POST /predict
# ---------------------------------------------------------------------------

class TestPredict:

    def test_returns_200(self, client):
        from app.main import app
        from app.database import get_db
        app.dependency_overrides[get_db] = lambda: _seeded_db()
        with patch("app.routes.predict.ml_service", _mock_ml()):
            response = client.post("/predict", json={
                "home_team": "Paris SG", "away_team": "Lyon", "season": 2024})
        assert response.status_code == 200

    def test_response_has_prediction_key(self, client):
        from app.main import app
        from app.database import get_db
        app.dependency_overrides[get_db] = lambda: _seeded_db()
        with patch("app.routes.predict.ml_service", _mock_ml()):
            response = client.post("/predict", json={
                "home_team": "Paris SG", "away_team": "Lyon", "season": 2024})
        assert "prediction" in response.json()

    def test_response_has_probabilities_key(self, client):
        from app.main import app
        from app.database import get_db
        app.dependency_overrides[get_db] = lambda: _seeded_db()
        with patch("app.routes.predict.ml_service", _mock_ml()):
            response = client.post("/predict", json={
                "home_team": "Paris SG", "away_team": "Lyon", "season": 2024})
        assert "probabilities" in response.json()

    def test_returns_404_for_unknown_team(self, client):
        from app.main import app
        from app.database import get_db
        db = MagicMock()
        db.query.return_value.filter.return_value.first.return_value = None
        app.dependency_overrides[get_db] = lambda: db
        with patch("app.routes.predict.ml_service", _mock_ml()):
            response = client.post("/predict", json={
                "home_team": "Unknown FC", "away_team": "Lyon", "season": 2024})
        assert response.status_code == 404

    def test_returns_503_when_model_not_loaded(self, client):
        from app.main import app
        from app.database import get_db
        app.dependency_overrides[get_db] = lambda: _seeded_db()
        with patch("app.routes.predict.ml_service", _mock_ml(loaded=False)):
            response = client.post("/predict", json={
                "home_team": "Paris SG", "away_team": "Lyon", "season": 2024})
        assert response.status_code == 503

    def test_returns_503_when_stats_missing(self, client):
        from app.main import app
        from app.database import get_db
        app.dependency_overrides[get_db] = lambda: _seeded_db()
        with patch("app.routes.predict.ml_service", _mock_ml(has_stats=False)):
            response = client.post("/predict", json={
                "home_team": "Paris SG", "away_team": "Lyon", "season": 2024})
        assert response.status_code == 503

    def test_missing_body_returns_422(self, client):
        assert client.post("/predict", json={}).status_code == 422

    def test_response_echoes_team_names(self, client):
        from app.main import app
        from app.database import get_db
        app.dependency_overrides[get_db] = lambda: _seeded_db()
        with patch("app.routes.predict.ml_service", _mock_ml()):
            data = client.post("/predict", json={
                "home_team": "Paris SG", "away_team": "Lyon", "season": 2024}).json()
        assert data["home_team"] == "Paris SG"
        assert data["away_team"] == "Lyon"


# ---------------------------------------------------------------------------
# POST /train · GET /train/history
# ---------------------------------------------------------------------------

class TestTrain:

    def test_train_returns_200(self, client):
        with patch("app.routes.train.pipeline_service") as m:
            m.train.return_value = {
                "status": "success", "model_version": "20240101",
                "cv_accuracy": 0.65, "cv_log_loss": 0.88, "n_samples": 500}
            assert client.post("/train").status_code == 200

    def test_train_response_has_all_keys(self, client):
        with patch("app.routes.train.pipeline_service") as m:
            m.train.return_value = {
                "status": "success", "model_version": "20240101",
                "cv_accuracy": 0.65, "cv_log_loss": 0.88, "n_samples": 500}
            data = client.post("/train").json()
        for key in ["status", "model_version", "cv_accuracy", "cv_log_loss", "n_samples"]:
            assert key in data

    def test_train_returns_500_on_error(self, client):
        with patch("app.routes.train.pipeline_service") as m:
            m.train.side_effect = ValueError("Aucun match")
            assert client.post("/train").status_code == 500

    def test_history_returns_200(self, client):
        with patch("app.routes.train.pipeline_service") as m:
            m.get_history.return_value = []
            assert client.get("/train/history").status_code == 200

    def test_history_returns_list(self, client):
        with patch("app.routes.train.pipeline_service") as m:
            m.get_history.return_value = []
            assert isinstance(client.get("/train/history").json(), list)


# ---------------------------------------------------------------------------
# POST /ingest
# ---------------------------------------------------------------------------

class TestIngest:

    def test_without_file_calls_run_base(self, client):
        with patch("app.routes.ingestion.preparation_service") as m:
            m.run_base.return_value = {
                "status": "success", "inserted": 100, "total": 100, "message": "OK"}
            response = client.post("/ingest")
        assert response.status_code == 200
        m.run_base.assert_called_once()

    def test_with_csv_file_calls_run(self, client):
        csv = (
            "Date,HomeTeam,AwayTeam,FTHG,FTAG,FTR,HS,AS,HST,AST,"
            "HTHG,HTAG,HTR,HF,AF,HC,AC,HY,AY,HR,AR\n"
            "10/01/2024,Paris SG,Lyon,2,0,H,12,5,5,2,1,0,H,10,11,6,3,2,1,0,0\n"
        )
        with patch("app.routes.ingestion.preparation_service") as m:
            m.run.return_value = {
                "status": "success", "inserted": 1, "total": 1, "message": "OK"}
            response = client.post(
                "/ingest",
                files={"file": ("test.csv", io.BytesIO(csv.encode()), "text/csv")})
        assert response.status_code == 200
        m.run.assert_called_once()

    def test_returns_422_on_value_error(self, client):
        with patch("app.routes.ingestion.preparation_service") as m:
            m.run_base.side_effect = ValueError("Invalid data")
            assert client.post("/ingest").status_code == 422

    def test_returns_500_on_unexpected_error(self, client):
        with patch("app.routes.ingestion.preparation_service") as m:
            m.run_base.side_effect = RuntimeError("Unexpected error")
            assert client.post("/ingest").status_code == 500
