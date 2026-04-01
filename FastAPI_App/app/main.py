from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes.base import register_routes


from .core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API Application (utilisateurs, historique, favoris, prédictions) pour la Match Prediction App.",
    version=settings.PROJECT_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8080",
        "http://localhost:5173",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from .database import engine, Base, SessionLocal
from .models.user import User
from .models.team import Team

# Création des tables (pour le mode dev/démo sans PostgreSQL)
# Base.metadata.create_all(bind=engine)

# Initialisation d'un utilisateur par défaut pour l'historique
db = SessionLocal()
try:
    if not db.query(User).filter(User.id == 1).first():
        default_user = User(
            id=1,
            username="dev_user",
            email="dev@example.com",
            hashed_password="fake_hashed_password"
        )
        db.add(default_user)
        db.commit()
finally:
    db.close()
 
# Insertion des équipes avec leurs logos
teams_to_add = [
    {"name": "Angers", "logo_url": "https://brandlogos.net/wp-content/uploads/2022/07/angers_sco-logo_brandlogos.net_1yevi-512x512.png"},
    {"name": "Auxerre", "logo_url": "https://brandlogos.net/wp-content/uploads/2018/12/aj_auxerre-logo_brandlogos.net_fwi5k-512x512.png"},
    {"name": "Le Havre", "logo_url": "https://brandlogos.net/wp-content/uploads/2018/12/le_havre_ac-logo_brandlogos.net_yx6ic-512x622.png"},
    {"name": "Lens", "logo_url": "https://brandlogos.net/wp-content/uploads/2018/12/rc-lens-logo-512x512.png"},
    {"name": "Lille", "logo_url": "https://brandlogos.net/wp-content/uploads/2021/01/lille-osc-logo-512x512.png"},
    {"name": "Lorient", "logo_url": "https://brandlogos.net/wp-content/uploads/2018/11/fc_lorient-logo_brandlogos.net_flntm-512x512.png"},
    {"name": "Lyon", "logo_url": "https://brandlogos.net/wp-content/uploads/2015/03/Olympique-Lyonnais-logo-512x594.png"},
    {"name": "Marseille", "logo_url": "https://brandlogos.net/wp-content/uploads/2014/12/olympique_de_marseille-logo_brandlogos.net_fnliw-512x657.png"},
    {"name": "Metz", "logo_url": "https://brandlogos.net/wp-content/uploads/2025/08/fc_metz-logo_brandlogos.net_umt95-512x737.png"},
    {"name": "Monaco", "logo_url": "https://brandlogos.net/wp-content/uploads/2018/11/AS-Monaco-FC-512x885.png"},
    {"name": "Nantes", "logo_url": "https://brandlogos.net/wp-content/uploads/2022/07/fc_nantes-logo_brandlogos.net_cawqm-512x512.png"},
    {"name": "Nice", "logo_url": "https://brandlogos.net/wp-content/uploads/2022/07/ogc_nice-logo_brandlogos.net_1nwir-512x512.png"},
    {"name": "Paris FC", "logo_url": "https://brandlogos.net/wp-content/uploads/2013/10/paris-fc-1969-vector-logo.png"},
    {"name": "Paris SG", "logo_url": "https://brandlogos.net/wp-content/uploads/2014/12/paris-saint-germain-logo-512x512.png"},
    {"name": "Rennes", "logo_url": "https://brandlogos.net/wp-content/uploads/2018/12/stade_rennais_fc-logo_brandlogos.net_eiekb-512x512.png"},
    {"name": "Stade Brestois", "logo_url": "https://brandlogos.net/wp-content/uploads/2022/07/stade_brestois_29-logo_brandlogos.net_llie5-512x512.png"},
    {"name": "Strasbourg", "logo_url": "https://brandlogos.net/wp-content/uploads/2019/01/rc_strasbourg_alsace-logo_brandlogos.net_sutxm-512x512.png"},
    {"name": "Toulouse", "logo_url": "https://brandlogos.net/wp-content/uploads/2022/07/toulouse_fc-logo_brandlogos.net_mpshb-512x512.png"}
]
 
for team_data in teams_to_add:
    existing = db.query(Team).filter(Team.name == team_data["name"]).first()
    if not existing:
        team = Team(name=team_data["name"], logo_url=team_data["logo_url"])
        db.add(team)
        print(f"✅ Ajouté: {team_data['name']}")
 
db.commit()
print("🎉 Équipes insérées avec succès !")

register_routes(app)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "app-api"}

