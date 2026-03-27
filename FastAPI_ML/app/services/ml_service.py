import os
from typing import Dict
import pandas as pd
import joblib
import numpy as np
from pathlib import Path

class MLService:
    def __init__(self):

        current_dir = Path(__file__).resolve()

        base_dir = current_dir.parent.parent.parent

        stats_path = f'{base_dir}/model/football_stats_reference.csv'
        model_path = f'{base_dir}/model/match_model_v1.joblib'

        try:
            self.model = joblib.load(model_path)
            self.is_model_loaded = True
        except Exception as e:
            print(f"Erreur chargement modèle : {e}")
            self.model = None
            self.is_model_loaded = False

        try:
            stats_df = pd.read_csv(stats_path)

            #  5 tables de references comme dans le notebook
            self.home_stats = stats_df.groupby(['league.season','HomeTeam'])[[
                'home_goals_scored_home','home_goals_conceded_home','home_win_rate_home'
            ]].first().reset_index().rename(columns={
                'HomeTeam':'Team',
                'home_goals_scored_home':'goals_scored_home',
                'home_goals_conceded_home':'goals_conceded_home',
                'home_win_rate_home':'win_rate_home',
            })
            
            self.away_stats = stats_df.groupby(['league.season','AwayTeam'])[[
                'away_goals_scored_away','away_goals_conceded_away','away_win_rate_away'
            ]].first().reset_index().rename(columns={
                'AwayTeam':'Team',
                'away_goals_scored_away':'goals_scored_away',
                'away_goals_conceded_away':'goals_conceded_away',
                'away_win_rate_away':'win_rate_away',})

            self.standings = stats_df.groupby(['league.season','HomeTeam'])[
                'home_season_rank'
            ].first().reset_index().rename(columns={'HomeTeam':'Team','home_season_rank':'season_rank'})

            self.rolling_home = stats_df.groupby(['league.season','HomeTeam'])[[
                'home_rolling_scored','home_rolling_conceded','home_rolling_win_rate'
            ]].last().reset_index().rename(columns={
                'HomeTeam':'Team',
                'home_rolling_scored':'rolling_scored',
                'home_rolling_conceded':'rolling_conceded',
                'home_rolling_win_rate':'rolling_win_rate',
            })

            self.rolling_away = stats_df.groupby(['league.season','AwayTeam'])[[
                'away_rolling_scored','away_rolling_conceded','away_rolling_win_rate'
            ]].last().reset_index().rename(columns={
                'AwayTeam':'Team',
                'away_rolling_scored':'rolling_scored',
                'away_rolling_conceded':'rolling_conceded',
                'away_rolling_win_rate':'rolling_win_rate',
            })

        except Exception as e:
            print(f"Erreur chargement stats : {e}")
            self.stats_df = pd.DataFrame()
        
            self.is_model_loaded = False

    def get_stat(self, team, season, col, source):
        try:
            return source.set_index(['league.season','Team']).loc[(season, team), col]
        except: return 0.0

    def predict_match(self, home_team: str, away_team: str, referee: str, season: int, round_num: int) -> Dict:
        
        input_data = {
            # Stats Saison (Lieu)
            'home_goals_scored_home': self.get_stat(home_team, season, 'goals_scored_home', self.home_stats),
            'home_goals_conceded_home': self.get_stat(home_team, season, 'goals_conceded_home', self.home_stats),
            'home_win_rate_home': self.get_stat(home_team, season, 'win_rate_home', self.home_stats),
            'away_goals_scored_away': self.get_stat(away_team, season, 'goals_scored_away', self.away_stats),
            'away_goals_conceded_away': self.get_stat(away_team, season, 'goals_conceded_away', self.away_stats),
            'away_win_rate_away': self.get_stat(away_team, season, 'win_rate_away', self.away_stats),
            'home_season_rank': self.get_stat(home_team, season, 'season_rank', self.standings),
            'away_season_rank': self.get_stat(away_team, season, 'season_rank', self.standings),
            
            # Rolling Averages (Forme sur 5 matchs)
            'home_rolling_scored': self.get_stat(home_team, season, 'rolling_scored', self.rolling_home),
            'home_rolling_conceded': self.get_stat(home_team, season, 'rolling_conceded', self.rolling_home),
            'home_rolling_win_rate': self.get_stat(home_team, season, 'rolling_win_rate', self.rolling_home),
            'away_rolling_scored': self.get_stat(away_team, season, 'rolling_scored', self.rolling_away),
            'away_rolling_conceded': self.get_stat(away_team, season, 'rolling_conceded', self.rolling_away),
            'away_rolling_win_rate': self.get_stat(away_team, season, 'rolling_win_rate', self.rolling_away),
            
            # Variables saisies par l'utilisateur
            'Round': round_num,
            'league.season': season,
            'HomeTeam': home_team,
            'AwayTeam': away_team,
            'Referee': referee
        }

        df_input = pd.DataFrame([input_data])

        probs = self.model.predict_proba(df_input)[0]
        pred = self.model.predict(df_input)[0]

        labels = {0:'Exterieur (A)', 1:'Nul (D)', 2:'Domicile (H)'}

        print('=' * 52)
        print(f'  {home_team}  vs  {away_team}')
        print(f'  Journee {round_num} - Saison {season}/{season+1} | Arbitre : {referee}')
        print('=' * 52)
        print(f'  {"Resultat":<20} {"Prob":>8} {"Cote juste":>12}')
        print('-' * 52)
        for idx, prob in enumerate(probs):
            marker   = ' <--' if idx == pred else ''
            odd      = f'{1/prob:.2f}' if prob > 0 else 'inf'
            print(f'  {labels[idx]:<20} {prob:>7.1%} {odd:>12}{marker}')
        print('=' * 52)
        print('  Les cotes justes ne incluent pas la marge bookmaker.')

        labels = {0: 'AWAY_WIN', 1: 'DRAW', 2: 'HOME_WIN'}
        pred_idx = np.argmax(probs)

        return {
            "match": f"{home_team} vs {away_team}",
            "prediction": labels[pred_idx],
            "confidence": round(float(probs[pred_idx]), 4),
            "probabilities": {
                "HOME": round(float(probs[2]), 4),
                "DRAW": round(float(probs[1]), 4),
                "AWAY": round(float(probs[0]), 4)
            },
            "fair_odds": {
                "H": round(1/probs[2], 2) if probs[2] > 0 else "inf",
                "D": round(1/probs[1], 2) if probs[1] > 0 else "inf",
                "A": round(1/probs[0], 2) if probs[0] > 0 else "inf"
            }
        }

ml_service = MLService()
