"""
Unit tests — app/utils/team_mapper.py
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.utils.team_mapper import normalize_team, TEAM_NAME_MAPPING


class TestNormalizeTeam:

    def test_paris_sg(self):
        assert normalize_team("Paris Saint-Germain") == "Paris SG"

    def test_marseille(self):
        assert normalize_team("Olympique de Marseille") == "Marseille"

    def test_lyon(self):
        assert normalize_team("Olympique Lyonnais") == "Lyon"

    def test_monaco(self):
        assert normalize_team("AS Monaco") == "Monaco"

    def test_lens(self):
        assert normalize_team("RC Lens") == "Lens"

    def test_lille(self):
        assert normalize_team("LOSC Lille") == "Lille"

    def test_rennes(self):
        assert normalize_team("Stade Rennais FC") == "Rennes"

    def test_strasbourg(self):
        assert normalize_team("RC Strasbourg Alsace") == "Strasbourg"

    def test_nantes(self):
        assert normalize_team("FC Nantes") == "Nantes"

    def test_nice(self):
        assert normalize_team("OGC Nice") == "Nice"

    def test_lorient(self):
        assert normalize_team("FC Lorient") == "Lorient"

    def test_toulouse(self):
        assert normalize_team("Toulouse FC") == "Toulouse"

    def test_brest(self):
        assert normalize_team("Stade Brestois 29") == "Stade Brestois"

    def test_le_havre(self):
        assert normalize_team("Le Havre AC") == "Le Havre"

    def test_le_havre_variant(self):
        assert normalize_team("Havre AC") == "Le Havre"

    def test_unknown_name_returned_as_is(self):
        assert normalize_team("Clermont Foot") == "Clermont Foot"

    def test_strips_leading_trailing_spaces(self):
        assert normalize_team("  RC Lens  ") == "Lens"

    def test_empty_string_returned_as_is(self):
        assert normalize_team("") == ""

    def test_all_mapped_values_are_strings(self):
        for k, v in TEAM_NAME_MAPPING.items():
            assert isinstance(v, str)

    def test_mapping_is_not_empty(self):
        assert len(TEAM_NAME_MAPPING) > 10
