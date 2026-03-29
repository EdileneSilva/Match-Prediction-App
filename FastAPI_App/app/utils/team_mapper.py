TEAM_NAME_MAPPING = {
    # LFP Scraper Name -> ML Model Name
    "Angers SCO": "Angers",
    "AJ Auxerre": "Auxerre",
    "AS Monaco": "Monaco",
    "AS Saint-Étienne": "St Etienne",
    "Havre AC": "Le Havre",
    "LOSC Lille": "Lille",
    "Montpellier Hérault SC": "Montpellier",
    "FC Nantes": "Nantes",
    "OGC Nice": "Nice",
    "Olympique Lyonnais": "Lyon",
    "Olympique de Marseille": "Marseille",
    "Paris Saint-Germain": "Paris SG",
    "RC Lens": "Lens",
    "RC Strasbourg Alsace": "Strasbourg",
    "Stade Brestois 29": "Stade Brestois",
    "Stade de Reims": "Reims",
    "Stade Rennais FC": "Rennes",
    "Toulouse FC": "Toulouse",
    "FC Lorient": "Lorient",
    "Clermont Foot 63": "Clermont Foot",
    "ESTAC Troyes": "Estac Troyes",
    "FC Metz": "Metz",
    "AC Ajaccio": "Ajaccio"
}

def normalize_team(lfp_name: str) -> str:
    """
    Transforme un nom d'équipe complet (LFP) en nom reconnu par le modèle ML.
    """
    # On enlève d'éventuels espaces en trop
    clean_name = lfp_name.strip()
    return TEAM_NAME_MAPPING.get(clean_name, clean_name)
