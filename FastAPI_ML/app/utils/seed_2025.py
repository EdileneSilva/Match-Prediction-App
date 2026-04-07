import sys
import os

# Add the project root to sys.path to allow absolute imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.database import SessionLocal, engine
from app.models.match import Team, Match, TeamMatchStats
from sqlalchemy import text

def seed_2025():
    db = SessionLocal()
    try:
        print("--- Début du seeding Ligue 1 2025/2026 ---")
        
        # 1. Nettoyage (Ordre important pour les FK)
        print("Nettoyage des anciennes données...")
        try:
            db.execute(text("DELETE FROM team_match_stats"))
            db.execute(text("DELETE FROM match"))
            db.execute(text("DELETE FROM team"))
            db.commit()
            print("Nettoyage réussi.")
        except Exception as clean_err:
            print(f"Erreur lors du nettoyage: {clean_err}")
            db.rollback()
            # On continue quand même ? Si c'est vide ça passe.

        # 2. Liste des équipes 2025/2026
        teams_data = [
            {"name": "Paris Saint Germain"},
            {"name": "Olympique de Marseille"},
            {"name": "AS Monaco"},
            {"name": "Lille OSC"},
            {"name": "OGC Nice"},
            {"name": "Olympique Lyonnais"},
            {"name": "RC Lens"},
            {"name": "Stade Rennais"},
            {"name": "Stade Brestois 29"},
            {"name": "Toulouse FC"},
            {"name": "RC Strasbourg Alsace"},
            {"name": "Stade de Reims"},
            {"name": "Montpellier HSC"},
            {"name": "AJ Auxerre"},
            {"name": "Angers SCO"},
            {"name": "FC Nantes"},
            {"name": "FC Lorient"},
            {"name": "Paris FC"},
        ]

        print(f"Insertion de {len(teams_data)} équipes...")
        for t in teams_data:
            new_team = Team(name=t["name"])
            db.add(new_team)
        
        db.commit()
        print("--- Seeding terminé avec succès ---")

    except Exception as e:
        print(f"Erreur lors du seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_2025()
