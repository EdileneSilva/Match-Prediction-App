import sys
import os

# Add parent directory to sys.path to allow importing from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base
from app.models.team import Team
from app.models.user import User, PredictionHistory, UserFavoriteTeam

# Ensure tables are created
Base.metadata.create_all(bind=engine)

teams_data = [
    {"name": "Paris Saint-Germain", "short_name": "PSG", "logo_url": "/static/logos/psg.svg"},
    {"name": "Olympique de Marseille", "short_name": "OM", "logo_url": "/static/logos/marseille.svg"},
    {"name": "Olympique Lyonnais", "short_name": "OL", "logo_url": "/static/logos/lyon.svg"},
    {"name": "AS Monaco", "short_name": "ASM", "logo_url": "/static/logos/monaco.svg"},
    {"name": "LOSC Lille", "short_name": "LOSC", "logo_url": "/static/logos/lille.svg"},
    {"name": "RC Lens", "short_name": "RCL", "logo_url": "/static/logos/lens.svg"},
    {"name": "Stade Rennais", "short_name": "Rennes", "logo_url": "/static/logos/rennes.svg"},
    {"name": "OGC Nice", "short_name": "Nice", "logo_url": "/static/logos/nice.svg"},
    {"name": "Stade de Reims", "short_name": "Reims", "logo_url": "/static/logos/reims.svg"},
    {"name": "Montpellier HSC", "short_name": "MHSC", "logo_url": "/static/logos/montpellier.svg"},
    {"name": "Toulouse FC", "short_name": "TFC", "logo_url": "/static/logos/toulouse.svg"},
    {"name": "FC Nantes", "short_name": "Nantes", "logo_url": "/static/logos/nantes.svg"},
    {"name": "RC Strasbourg", "short_name": "RCSA", "logo_url": "/static/logos/strasbourg.svg"},
    {"name": "Stade Brestois", "short_name": "Brest", "logo_url": "/static/logos/brest.svg"},
    {"name": "FC Lorient", "short_name": "Lorient", "logo_url": "/static/logos/lorient.svg"},
    {"name": "Clermont Foot", "short_name": "Clermont", "logo_url": "/static/logos/clermont.svg"},
    {"name": "Le Havre AC", "short_name": "HAC", "logo_url": "/static/logos/lehavre.svg"},
    {"name": "FC Metz", "short_name": "Metz", "logo_url": "/static/logos/metz.svg"},
]

def seed():
    db = SessionLocal()
    try:
        # Clear existing teams to avoid duplicates on re-run
        db.query(Team).delete()
        
        for team_info in teams_data:
            existing = db.query(Team).filter(Team.name == team_info["name"]).first()
            if not existing:
                team = Team(**team_info)
                db.add(team)
        
        db.commit()
        print(f"✅ Successfully seeded {len(teams_data)} teams.")
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding teams: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
