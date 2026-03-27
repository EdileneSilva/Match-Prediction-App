<template>
  <div class="dashboard">
<!-- Main Content -->
    <main class="main-content">
        <div v-if="error" class="error-message" style="margin-bottom: 1rem; color: #ff4d4f; text-align: center;">
          {{ error }}
        </div>

        <!-- Team Selection -->
        <div class="selection-section">
          <div class="team-selectors">
            <div class="form-group">
              <label for="team1">Équipe 1</label>
              <select id="team1" v-model="selectedTeam1" class="team-select">
                <option :value="null">Sélectionner équipe</option>
                <option v-for="team in teams" :key="team.id" :value="team">{{ team.name }}</option>
              </select>
            </div>

            <div class="vs-indicator">VS</div>

            <div class="form-group">
              <label for="team2">Équipe 2</label>
              <select id="team2" v-model="selectedTeam2" class="team-select">
                <option :value="null">Sélectionner équipe</option>
                <option v-for="team in teams" :key="team.id" :value="team">{{ team.name }}</option>
              </select>
            </div>
          </div>

          <button class="predict-btn" @click="launchPrediction"
            :disabled="!selectedTeam1 || !selectedTeam2 || isPredicting">
            {{ isPredicting ? 'Prédiction en cours...' : 'Lancer la prédiction IA' }}
          </button>
        </div>

        <!-- Prediction Results -->
        <div v-if="predictionResult" class="results-section">
          <h2>Résultat Prédiction</h2>

          <div class="prediction-stats">
            <div class="stat-item">
              <span class="stat-label">Victoire Équipe 1</span>
              <span class="stat-value">{{ predictionResult.team1Win }}%</span>
              <div class="progress-bar">
                <div class="progress" :style="{ width: predictionResult.team1Win + '%' }"></div>
              </div>
            </div>

            <div class="stat-item">
              <span class="stat-label">Match nul</span>
              <span class="stat-value">{{ predictionResult.draw }}%</span>
              <div class="progress-bar">
                <div class="progress" :style="{ width: predictionResult.draw + '%' }"></div>
              </div>
            </div>

            <div class="stat-item">
              <span class="stat-label">Victoire Équipe 2</span>
              <span class="stat-value">{{ predictionResult.team2Win }}%</span>
              <div class="progress-bar">
                <div class="progress" :style="{ width: predictionResult.team2Win + '%' }"></div>
              </div>
            </div>
          </div>

          <div class="score-prediction">
            <span class="score-label">Score probable : </span>
            <span class="score-value">{{ predictionResult.probableScore }}</span>
          </div>

          <button class="save-btn" @click="savePrediction">
            Enregistrer prédiction
          </button>
        </div>
    </main>
  </div>
</template>

<script>
import { apiClient } from '@/api/client'

export default {
  name: 'PredictionView',
  data() {
    return {
      selectedTeam1: null,
      selectedTeam2: null,
      isPredicting: false,
      predictionResult: null,
      teams: [],
      error: null
    }
  },
  async mounted() {
    try {
      this.teams = await apiClient.get('/predictions/teams')
    } catch (err) {
      this.error = "Impossible de charger les équipes"
      console.error(err)
    }
  },
  methods: {
    async launchPrediction() {
      if (!this.selectedTeam1 || !this.selectedTeam2) {
        return
      }

      this.isPredicting = true
      this.predictionResult = null
      this.error = null

      try {
        const response = await apiClient.post('/predictions/predict', {
          home_team_id: this.selectedTeam1.id,
          away_team_id: this.selectedTeam2.id,
          home_team_name: this.selectedTeam1.name,
          away_team_name: this.selectedTeam2.name
        })

        // On adapte le format de l'API App (predicted_result, confidence_score)
        // vers le format attendu par la vue (qui est plus détaillé avec des % par issue)
        // Pour l'instant, on simule la répartition si l'API ML ne donne qu'un seul gagnant
        // ou on adapte si possible.
        
        this.predictionResult = {
          team1Win: response.prediction === 'HOME_WIN' ? response.confidence * 100 : (1 - response.confidence) * 50,
          draw: response.prediction === 'DRAW' ? response.confidence * 100 : (1 - response.confidence) * 20,
          team2Win: response.prediction === 'AWAY_WIN' ? response.confidence * 100 : (1 - response.confidence) * 30,
          probableScore: "N/A"
        }

        // Normalisation à 100%
        const total = this.predictionResult.team1Win + this.predictionResult.draw + this.predictionResult.team2Win
        this.predictionResult.team1Win = Math.round((this.predictionResult.team1Win / total) * 100)
        this.predictionResult.draw = Math.round((this.predictionResult.draw / total) * 100)
        this.predictionResult.team2Win = 100 - this.predictionResult.team1Win - this.predictionResult.draw

      } catch (err) {
        this.error = err.message
      } finally {
        this.isPredicting = false
      }
    },

    savePrediction() {
      // Dans notre nouveau flux, la prédiction est déjà enregistrée en BD par le backend
      // lors de l'appel à /predict. On peut donc juste afficher un message ou rediriger.
      alert('Prédiction enregistrée dans votre historique !')
      this.$router.push('/history')
    }
  }
}
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Main Content */
.main-content {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.prediction-container {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 2.5rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.page-title {
  margin: 0 0 2rem 0;
  color: #333;
  font-size: 2rem;
  font-weight: 600;
  text-align: center;
}

/* Team Selection */
.selection-section {
  margin-bottom: 2rem;
}

.team-selectors {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
  margin-bottom: 2rem;
}

.form-group {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 500;
  color: #555;
  font-size: 0.95rem;
}

.team-select {
  padding: 0.875rem 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: #fafafa;
  cursor: pointer;
}

.team-select:focus {
  outline: none;
  border-color: #667eea;
  background: white;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.vs-indicator {
  font-weight: bold;
  color: #667eea;
  font-size: 1.2rem;
  padding: 0 1rem;
}

.predict-btn {
  width: 100%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  padding: 1rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.predict-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.predict-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Results Section */
.results-section {
  border-top: 1px solid #e0e0e0;
  padding-top: 2rem;
}

.results-section h2 {
  margin: 0 0 1.5rem 0;
  color: #333;
  font-size: 1.5rem;
  font-weight: 600;
}

.prediction-stats {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stat-label {
  flex: 0 0 150px;
  font-weight: 500;
  color: #555;
}

.stat-value {
  flex: 0 0 60px;
  font-weight: bold;
  color: #667eea;
  text-align: right;
}

.progress-bar {
  flex: 1;
  height: 8px;
  background: #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
}

.progress {
  height: 100%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  transition: width 0.5s ease;
}

.score-prediction {
  text-align: center;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: rgba(102, 126, 234, 0.1);
  border-radius: 8px;
}

.score-label {
  color: #555;
  font-size: 1.1rem;
}

.score-value {
  font-weight: bold;
  color: #667eea;
  font-size: 1.3rem;
}

.save-btn {
  width: 100%;
  background: linear-gradient(135deg, #28a745, #20c997);
  color: white;
  border: none;
  padding: 1rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.save-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(40, 167, 69, 0.4);
}

.logo-img {
  height: 1.5rem;
  width: auto;
}

/* Responsive Design */
@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
  }

  .nav-menu {
    flex-wrap: wrap;
    justify-content: center;
    gap: 1rem;
  }

  .main-content {
    padding: 1rem;
  }

  .prediction-container {
    padding: 1.5rem;
  }

  .team-selectors {
    flex-direction: column;
    gap: 1rem;
  }

  .vs-indicator {
    padding: 0.5rem 0;
  }

  .stat-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .stat-label {
    flex: none;
  }

  .stat-value {
    flex: none;
  }

  .progress-bar {
    width: 100%;
  }
}
</style>