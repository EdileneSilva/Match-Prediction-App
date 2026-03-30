from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from pathlib import Path
from datetime import datetime
import pandas as pd
import joblib
import numpy as np

from ..database import get_db
from ..models.match import MatchData, TeamStatsReference, TrainLog
from ..core.config import settings

router = APIRouter(tags=["ML Training"])


# Import CSV -> MatchData

@router.post("/data/import", summary="Importer le CSV dans la base de données")
def import_csv(db: Session = Depends(get_db)):
    """
    Importe les données du CSV dans la table match_data (Raw Data Store).
    Les doublons sont ignorés via (date, home_team, away_team).
    À lancer une fois après avoir généré le CSV avec data_agregation.ipynb.
    """
    csv_path = Path(settings.DATASET_PATH)

    if not csv_path.exists():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"CSV introuvable : {csv_path}"
        )

    try:
        df = pd.read_csv(csv_path)
        df["Date"] = pd.to_datetime(df["Date"])
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lecture CSV : {e}"
        )

    inserted = 0
    for _, row in df.iterrows():
        # Éviter les doublons
        exists = db.query(MatchData).filter(
            MatchData.date      == row["Date"],
            MatchData.home_team == row["HomeTeam"],
            MatchData.away_team == row["AwayTeam"],
        ).first()

        if exists:
            continue

        def safe(col):
            return float(row[col]) if col in row.index and pd.notna(row[col]) else None

        match = MatchData(
            date      = row["Date"],
            season    = int(row["league.season"]),
            round_num = int(row["Round"]),
            home_team = row["HomeTeam"],
            away_team = row["AwayTeam"],
            referee   = row.get("Referee"),
            home_score = int(row["HomeScore"]) if pd.notna(row.get("HomeScore")) else None,
            away_score = int(row["AwayScore"]) if pd.notna(row.get("AwayScore")) else None,
            result     = row.get("Result"),
            home_goals_scored_home   = safe("home_goals_scored_home"),
            home_goals_conceded_home = safe("home_goals_conceded_home"),
            home_win_rate_home       = safe("home_win_rate_home"),
            away_goals_scored_away   = safe("away_goals_scored_away"),
            away_goals_conceded_away = safe("away_goals_conceded_away"),
            away_win_rate_away       = safe("away_win_rate_away"),
            home_season_rank         = safe("home_season_rank"),
            away_season_rank         = safe("away_season_rank"),
            home_rolling_scored      = safe("home_rolling_scored"),
            home_rolling_conceded    = safe("home_rolling_conceded"),
            home_rolling_win_rate    = safe("home_rolling_win_rate"),
            away_rolling_scored      = safe("away_rolling_scored"),
            away_rolling_conceded    = safe("away_rolling_conceded"),
            away_rolling_win_rate    = safe("away_rolling_win_rate"),
        )
        db.add(match)
        inserted += 1

    db.commit()

    total = db.query(func.count(MatchData.id)).scalar()
    return {
        "status":   "success",
        "inserted": inserted,
        "total":    total,
        "message":  f"{inserted} nouveaux matchs importés. Total en base : {total}."
    }


# Train → TeamStatsReference + TrainLog

@router.post("/train", summary="Entraîner le modèle et peupler la Feature Store")
def train_model(db: Session = Depends(get_db)):
    """
    Lance l'entraînement complet :
    1. Lit les données depuis match_data (Raw Data Store)
    2. Entraîne le modèle avec validation croisée
    3. Sauvegarde le modèle en fichier joblib
    4. Calcule et persiste les features dans team_stats_reference (Feature Store)
    5. Enregistre les métriques dans train_log (Model Registry)
    """
    from sklearn.model_selection import cross_val_score
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.calibration import CalibratedClassifierCV
    from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline
    from datetime import date

    # 1. Lire depuis la BD
    n_matches = db.query(func.count(MatchData.id)).filter(
        MatchData.result.isnot(None)
    ).scalar()

    if n_matches == 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Aucun match en base. Lancez d'abord POST /data/import."
        )

    matches = db.query(MatchData).filter(MatchData.result.isnot(None)).all()

    df = pd.DataFrame([{
        "HomeTeam":                  m.home_team,
        "AwayTeam":                  m.away_team,
        "Referee":                   m.referee or "Inconnu",
        "Result":                    m.result,
        "league.season":             m.season,
        "Round":                     m.round_num,
        "home_goals_scored_home":    m.home_goals_scored_home or 0.0,
        "home_goals_conceded_home":  m.home_goals_conceded_home or 0.0,
        "home_win_rate_home":        m.home_win_rate_home or 0.0,
        "away_goals_scored_away":    m.away_goals_scored_away or 0.0,
        "away_goals_conceded_away":  m.away_goals_conceded_away or 0.0,
        "away_win_rate_away":        m.away_win_rate_away or 0.0,
        "home_season_rank":          m.home_season_rank or 0.0,
        "away_season_rank":          m.away_season_rank or 0.0,
        "home_rolling_scored":       m.home_rolling_scored or 0.0,
        "home_rolling_conceded":     m.home_rolling_conceded or 0.0,
        "home_rolling_win_rate":     m.home_rolling_win_rate or 0.0,
        "away_rolling_scored":       m.away_rolling_scored or 0.0,
        "away_rolling_conceded":     m.away_rolling_conceded or 0.0,
        "away_rolling_win_rate":     m.away_rolling_win_rate or 0.0,
    } for m in matches])

    # 2. Entraînement
    cat_features = ["HomeTeam", "AwayTeam", "Referee"]
    num_features = [
        "home_goals_scored_home",  "home_goals_conceded_home",  "home_win_rate_home",
        "away_goals_scored_away",  "away_goals_conceded_away",  "away_win_rate_away",
        "home_season_rank",        "away_season_rank",
        "home_rolling_scored",     "home_rolling_conceded",     "home_rolling_win_rate",
        "away_rolling_scored",     "away_rolling_conceded",     "away_rolling_win_rate",
        "Round",                   "league.season",
    ]

    le = LabelEncoder()
    X  = df[num_features + cat_features]
    y  = le.fit_transform(df["Result"])

    preprocessor = ColumnTransformer([
        ("num", StandardScaler(),                       num_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_features),
    ])
    pipeline   = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier",   RandomForestClassifier(
            n_estimators=200, max_depth=10,
            class_weight="balanced_subsample", random_state=42
        ))
    ])
    calibrated = CalibratedClassifierCV(estimator=pipeline, method="sigmoid", cv=5)

    try:
        cv_acc = cross_val_score(calibrated, X, y, cv=5, scoring="accuracy")
        cv_ll  = cross_val_score(calibrated, X, y, cv=5, scoring="neg_log_loss")
        calibrated.fit(X, y)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur entraînement : {e}"
        )

    # 3. Sauvegarder le modèle
    version    = date.today().strftime("%Y%m%d")
    model_path = Path(settings.MODEL_PATH)
    model_path.parent.mkdir(exist_ok=True)
    joblib.dump(calibrated, model_path)

    # Recharger dans ml_service
    from ..services.ml_service import ml_service
    ml_service.model           = calibrated
    ml_service.is_model_loaded = True

    # 4. Peupler la Feature Store (TeamStatsReference)
    _populate_feature_store(db, df)

    # Recharger les stats dans ml_service depuis la BD
    ml_service.load_stats_from_db(db)

    # 5. Enregistrer dans TrainLog
    log = TrainLog(
        model_version = version,
        n_samples     = len(df),
        cv_accuracy   = round(float(cv_acc.mean()), 4),
        cv_log_loss   = round(float(-cv_ll.mean()), 4),
        status        = "success",
    )
    db.add(log)
    db.commit()

    return {
        "status":        "success",
        "model_version": version,
        "cv_accuracy":   round(float(cv_acc.mean()), 4),
        "cv_log_loss":   round(float(-cv_ll.mean()), 4),
        "n_samples":     len(df),
    }


def _populate_feature_store(db: Session, df: pd.DataFrame):
    """
    Calcule les features par équipe/saison et les persiste dans team_stats_reference.
    Supprime les entrées existantes pour la même saison avant de recalculer.
    """
    seasons = df["league.season"].unique()

    for season in seasons:
        # Supprimer les anciennes entrées pour cette saison
        db.query(TeamStatsReference).filter(
            TeamStatsReference.season == int(season)
        ).delete()

    # Stats domicile — groupby HomeTeam
    home_stats = df.groupby(["league.season", "HomeTeam"]).agg(
        goals_scored_home   = ("home_goals_scored_home",  "last"),
        goals_conceded_home = ("home_goals_conceded_home","last"),
        win_rate_home       = ("home_win_rate_home",      "last"),
        season_rank         = ("home_season_rank",        "last"),
        rolling_scored_home   = ("home_rolling_scored",   "last"),
        rolling_conceded_home = ("home_rolling_conceded", "last"),
        rolling_win_rate_home = ("home_rolling_win_rate", "last"),
    ).reset_index().rename(columns={"HomeTeam": "team", "league.season": "season"})

    # Stats extérieur — groupby AwayTeam
    away_stats = df.groupby(["league.season", "AwayTeam"]).agg(
        goals_scored_away   = ("away_goals_scored_away",  "last"),
        goals_conceded_away = ("away_goals_conceded_away","last"),
        win_rate_away       = ("away_win_rate_away",      "last"),
        rolling_scored_away   = ("away_rolling_scored",   "last"),
        rolling_conceded_away = ("away_rolling_conceded", "last"),
        rolling_win_rate_away = ("away_rolling_win_rate", "last"),
    ).reset_index().rename(columns={"AwayTeam": "team", "league.season": "season"})

    # Fusionner les deux
    merged = pd.merge(home_stats, away_stats, on=["season", "team"], how="outer")

    for _, row in merged.iterrows():
        stat = TeamStatsReference(
            team   = row["team"],
            season = int(row["season"]),
            goals_scored_home   = row.get("goals_scored_home"),
            goals_conceded_home = row.get("goals_conceded_home"),
            win_rate_home       = row.get("win_rate_home"),
            season_rank         = row.get("season_rank"),
            rolling_scored_home   = row.get("rolling_scored_home"),
            rolling_conceded_home = row.get("rolling_conceded_home"),
            rolling_win_rate_home = row.get("rolling_win_rate_home"),
            goals_scored_away   = row.get("goals_scored_away"),
            goals_conceded_away = row.get("goals_conceded_away"),
            win_rate_away       = row.get("win_rate_away"),
            rolling_scored_away   = row.get("rolling_scored_away"),
            rolling_conceded_away = row.get("rolling_conceded_away"),
            rolling_win_rate_away = row.get("rolling_win_rate_away"),
        )
        db.add(stat)

    db.commit()


# Historique des entraînements

@router.get("/train/history", summary="Historique des entraînements")
def get_train_history(limit: int = 20, db: Session = Depends(get_db)):
    """Retourne l'historique des entraînements avec leurs métriques."""
    logs = db.query(TrainLog).order_by(
        TrainLog.created_at.desc()
    ).limit(limit).all()

    return [{
        "id":            l.id,
        "created_at":    l.created_at,
        "model_version": l.model_version,
        "n_samples":     l.n_samples,
        "cv_accuracy":   l.cv_accuracy,
        "cv_log_loss":   l.cv_log_loss,
        "status":        l.status,
    } for l in logs]


def register_routes(app):
    app.include_router(router)