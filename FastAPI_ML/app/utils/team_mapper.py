TEAM_NAME_MAPPING = {
    # LFP Scraper Name -> ML Model Name
    "Angers SCO": "Angers SCO",
    "AJ Auxerre": "AJ Auxerre",
    "Stade Brestois 29": "Stade Brestois 29",
    "Le Havre AC": "Le Havre AC",
    "Havre AC": "Le Havre AC",
    "RC Lens": "RC Lens",
    "LOSC Lille": "LOSC Lille",
    "FC Lorient": "FC Lorient",
    "Olympique Lyonnais": "Olympique Lyonnais",
    "Olympique de Marseille": "Olympique de Marseille",
    "FC Metz": "FC Metz",
    "AS Monaco": "AS Monaco",
    "FC Nantes": "FC Nantes",
    "OGC Nice": "OGC Nice",
    "Paris FC": "Paris FC",
    "Paris Saint-Germain": "Paris Saint-Germain",
    "Stade Rennais FC": "Stade Rennais FC",
    "RC Strasbourg Alsace": "RC Strasbourg Alsace",
    "Toulouse FC": "Toulouse FC"
}

def normalize_team(lfp_name: str) -> str:
    """
    Transforme un nom d'équipe complet (LFP) en nom reconnu par le modèle ML.
    """
    # On enlève d'éventuels espaces en trop
    clean_name = lfp_name.strip()
    return TEAM_NAME_MAPPING.get(clean_name, clean_name)
