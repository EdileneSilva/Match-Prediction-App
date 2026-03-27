import os
import requests
import time

teams = [
    ("psg.svg", "https://upload.wikimedia.org/wikipedia/en/a/a7/Paris_Saint-Germain_F.C..svg"),
    ("marseille.svg", "https://upload.wikimedia.org/wikipedia/commons/d/d8/Olympique_Marseille_logo.svg"),
    ("lyon.svg", "https://upload.wikimedia.org/wikipedia/en/c/c6/Olympique_Lyonnais.svg"),
    ("monaco.svg", "https://upload.wikimedia.org/wikipedia/en/b/ba/AS_Monaco_FC.svg"),
    ("lille.svg", "https://upload.wikimedia.org/wikipedia/en/3/3f/LOSC_Lille_logo.svg"),
    ("lens.svg", "https://upload.wikimedia.org/wikipedia/en/1/1c/RC_Lens_logo.svg"),
    ("rennes.svg", "https://upload.wikimedia.org/wikipedia/en/9/9e/Stade_Rennais_FC.svg"),
    ("nice.svg", "https://upload.wikimedia.org/wikipedia/en/2/2e/OGC_Nice_logo.svg"),
    ("reims.svg", "https://upload.wikimedia.org/wikipedia/en/0/0e/Stade_de_Reims_logo.svg"),
    ("montpellier.svg", "https://upload.wikimedia.org/wikipedia/en/3/3e/Montpellier_HSC_logo.svg"),
    ("toulouse.svg", "https://upload.wikimedia.org/wikipedia/en/0/0a/Toulouse_FC_logo.svg"),
    ("nantes.svg", "https://upload.wikimedia.org/wikipedia/en/5/54/FC_Nantes_logo.svg"),
    ("strasbourg.svg", "https://upload.wikimedia.org/wikipedia/en/8/80/Racing_Club_de_Strasbourg_logo.svg"),
    ("brest.svg", "https://upload.wikimedia.org/wikipedia/en/7/74/Stade_Brestois_29_logo.svg"),
    ("lorient.svg", "https://upload.wikimedia.org/wikipedia/en/c/c9/FC_Lorient_logo.svg"),
    ("clermont.svg", "https://upload.wikimedia.org/wikipedia/en/2/2e/Clermont_Foot_logo.svg"),
    ("lehavre.svg", "https://upload.wikimedia.org/wikipedia/en/6/6e/Le_Havre_AC_logo.svg"),
    ("metz.svg", "https://upload.wikimedia.org/wikipedia/en/4/4c/FC_Metz_logo.svg"),
]

# Storing in static/logos 
logo_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static", "logos")
os.makedirs(logo_dir, exist_ok=True)

print(f"Downloading logos to {logo_dir}...")

# Compliant User-Agent as per https://meta.wikimedia.org/wiki/User-Agent_policy
headers = {
    'User-Agent': 'MatchPredictionApp/1.0 (https://github.com/amaury/Match-Prediction-App; dev@example.com) python-requests/2.31.0'
}

for filename, url in teams:
    if os.path.exists(os.path.join(logo_dir, filename)):
        print(f"⏭️ {filename} already exists, skipping.")
        continue
        
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        with open(os.path.join(logo_dir, filename), "wb") as f:
            f.write(response.content)
        print(f"✅ {filename} downloaded.")
        time.sleep(2)  # Delay as per robot policy
    except Exception as e:
        print(f"❌ Failed to download {filename}: {e}")

print("✅ All logos finished!")
