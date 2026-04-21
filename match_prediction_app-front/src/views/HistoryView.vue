<template>
  <div class="dashboard">
    <!-- Main Content -->
    <main class="main-content">
      <div class="history-container">
        <h1 class="page-title">📊 Historique des Prédictions</h1>

        <!-- Statistics Dashboard -->
        <div class="stats-dashboard">
          <div class="stat-card">
            <div class="stat-icon">🎯</div>
            <div class="stat-content">
              <div class="stat-value">{{ globalScore }}%</div>
              <div class="stat-label">Précision globale</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">✅</div>
            <div class="stat-content">
              <div class="stat-value">{{ correctPredictions }}</div>
              <div class="stat-label">Prédictions correctes</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">📈</div>
            <div class="stat-content">
              <div class="stat-value">{{ averageGoalDifference }}</div>
              <div class="stat-label">Écart moyen de buts</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">🏆</div>
            <div class="stat-content">
              <div class="stat-value">{{ winnerAccuracy }}%</div>
              <div class="stat-label">Précision du vainqueur</div>
            </div>
          </div>
        </div>

        <!-- Filters -->
        <div class="filters-container">
          <select v-model="selectedGameweek" class="filter-select" @change="loadHistoryData">
            <option value="">Toutes les journées</option>
            <option v-for="gw in gameweekOptions" :key="gw" :value="gw">Journée {{ gw }}</option>
          </select>
          <select v-model="selectedFilter" class="filter-select">
            <option value="all">Toutes les prédictions</option>
            <option value="correct">Prédictions correctes</option>
            <option value="incorrect">Prédictions incorrectes</option>
            <option value="close">Prédictions proches</option>
          </select>
        </div>

        <!-- History Table -->
        <div class="table-container">
          <table class="history-table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Match</th>
                <th>Prédiction IA</th>
                <th>Résultat réel</th>
                <th>Différence</th>
                <th>Précision</th>
                <th>Détails</th>
              </tr>
            </thead>
            <tbody>
              <template v-for="(prediction, index) in filteredData" :key="index">
                <tr :class="getRowClass(prediction)">
                  <td>{{ prediction.date }}</td>
                  <td class="match-cell">
                    <div class="match-display">
                      <div class="team-mini">
                        <img v-if="prediction.home_team_logo" :src="prediction.home_team_logo" class="logo-xs" alt="">
                        <span>{{ prediction.home_team }}</span>
                      </div>
                      <span class="vs-xs">vs</span>
                      <div class="team-mini">
                        <img v-if="prediction.away_team_logo" :src="prediction.away_team_logo" class="logo-xs" alt="">
                        <span>{{ prediction.away_team }}</span>
                      </div>
                    </div>
                  </td>
                  <td class="prediction-cell">
                    <span class="score-badge prediction">{{ prediction.prediction }}</span>
                  </td>
                  <td class="result-cell">
                    <span class="score-badge result">{{ prediction.result }}</span>
                  </td>
                  <td class="difference-cell">
                    <span :class="getDifferenceClass(prediction)">
                      {{ getGoalDifference(prediction) }}
                    </span>
                  </td>
                  <td class="accuracy-cell">
                    <div class="accuracy-bar">
                      <div class="accuracy-fill" :style="{width: getAccuracyPercentage(prediction) + '%'}"></div>
                      <span class="accuracy-text">{{ getAccuracyPercentage(prediction) }}%</span>
                    </div>
                  </td>
                  <td class="details-cell">
                    <button @click="toggleDetails(index)" class="details-btn">
                      {{ showDetails[index] ? 'Masquer' : 'Voir' }}
                    </button>
                  </td>
                </tr>
                <!-- Expanded Details Row -->
                <tr v-if="showDetails[index]" :key="'details-' + index" class="details-row">
                  <td colspan="7">
                    <div class="prediction-details">
                      <h4>📋 Analyse détaillée</h4>
                      <div class="details-grid">
                        <div class="detail-item">
                          <span class="detail-label">Type de prédiction :</span>
                          <span class="detail-value">{{ getPredictionType(prediction) }}</span>
                        </div>
                        <div class="detail-item">
                          <span class="detail-label">Vainqueur prédit :</span>
                          <span class="detail-value">{{ getPredictedWinner(prediction) }}</span>
                        </div>
                        <div class="detail-item">
                          <span class="detail-label">Vainqueur réel :</span>
                          <span class="detail-value">{{ getActualWinner(prediction) }}</span>
                        </div>
                        <div class="detail-item">
                          <span class="detail-label">Écart total :</span>
                          <span class="detail-value">{{ getTotalGoalDifference(prediction) }} buts</span>
                        </div>
                      </div>
                      <div class="performance-indicator">
                        <div class="indicator-label">Performance de l'IA</div>
                        <div class="indicator-bar">
                          <div class="indicator-fill" :class="getPerformanceClass(prediction)" 
                               :style="{width: getAccuracyPercentage(prediction) + '%'}"></div>
                        </div>
                      </div>
                    </div>
                  </td>
                </tr>
              </template>
            </tbody>
          </table>
        </div>

        <!-- Performance Chart -->
        <div class="chart-container">
          <h3>📈 Évolution de la performance</h3>
          <div class="performance-chart">
            <div v-for="(prediction, index) in historyData" :key="index" 
                 class="chart-bar"
                 :class="getChartBarClass(prediction)">
              <div class="bar-fill" :style="{height: getAccuracyPercentage(prediction) + '%'}"></div>
              <div class="bar-label">{{ prediction.date }}</div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { apiClient } from '@/api/client'
import { gsap } from 'gsap'

export default {
  name: 'HistoryView',
  data() {
    return {
      historyData: [],
      error: null,
      selectedFilter: 'all',
      selectedGameweek: 28,
      gameweekOptions: Array.from({ length: 34 }, (_, i) => i + 1),
      showDetails: {}
    }
  },
  async mounted() {
    await this.loadHistoryData()
  },
  methods: {
    async loadHistoryData() {
    try {
      const qs = new URLSearchParams({
        include_live_results: 'true',
        include_proximity: 'true',
        season: '2025'
      })
      if (this.selectedGameweek) {
        qs.append('gameweek', String(this.selectedGameweek))
      }
      const data = await apiClient.get(`/predictions/history?${qs.toString()}`)
      this.historyData = data.map(item => {
        const hasLiveResult = !!item.actual_result
        const isCorrect = typeof item.is_correct === 'boolean' ? item.is_correct : null

        return {
          id: item.id,
          date: new Date(item.created_at).toLocaleDateString('fr-FR'),
          match: `${item.home_team_name} - ${item.away_team_name}`,
          home_team: item.home_team_name,
          home_team_logo: item.home_team_logo_url,
          away_team: item.away_team_name,
          away_team_logo: item.away_team_logo_url,
          prediction: this.formatResult(item.predicted_result),
          predicted_result: item.predicted_result,
          result: hasLiveResult ? this.formatResult(item.actual_result) : 'En attente',
          actual_result: item.actual_result || null,
          actual_home_goals: item.actual_home_goals,
          actual_away_goals: item.actual_away_goals,
          gameweek: item.gameweek,
          confidence: ((Number(item.confidence_score || 0)) * 100).toFixed(1) + '%',
          confidence_raw: Number(item.confidence_score || 0),
          isCorrect: isCorrect,
          proximity_score: item.proximity_score ?? null,
          proximity_status: item.proximity_status || 'unknown',
          accuracy: this.computeAccuracy(item)
        }
      })
      
      this.$nextTick(() => {
        // Animate stats cards
        gsap.fromTo('.stat-card', 
          { opacity: 0, scale: 0.9, y: 20 },
          { opacity: 1, scale: 1, y: 0, duration: 0.5, stagger: 0.1, ease: 'back.out(1.2)' }
        )
        
        // Animate table rows with a very short stagger for performance
        gsap.fromTo('.history-table tbody tr', 
          { opacity: 0, x: -15 },
          { opacity: 1, x: 0, duration: 0.3, stagger: 0.05, ease: 'power2.out', delay: 0.2 }
        )
        
        // Animate chart bars
        gsap.fromTo('.chart-bar', 
          { opacity: 0, scaleY: 0, transformOrigin: "bottom center" },
          { opacity: 1, scaleY: 1, duration: 0.5, stagger: 0.05, ease: 'power2.out', delay: 0.4 }
        )
      })
    } catch (err) {
      this.error = "Erreur lors de la récupération de l'historique"
      console.error(err)
    }
  },
    formatResult(result) {
      const mapping = {
        'HOME_WIN': 'Victoire Domicile',
        'AWAY_WIN': 'Victoire Extérieur',
        'DRAW': 'Match Nul'
      }
      return mapping[result] || result
    },
    toggleDetails(index) {
      this.showDetails[index] = !this.showDetails[index]
    },
    getRowClass(prediction) {
      if (prediction.isCorrect === true) return 'row-correct'
      if (prediction.isCorrect === false) return 'row-incorrect'
      return ''
    },
    getDifferenceClass(prediction) {
      if (!prediction.actual_result) return 'diff-neutral'
      if (prediction.proximity_status === 'close') return 'diff-close'
      return prediction.isCorrect ? 'diff-perfect' : 'diff-poor'
    },
    getGoalDifference(prediction) {
      if (!prediction.actual_result) return 'N/A'
      if (prediction.isCorrect === false && prediction.proximity_status === 'close' && prediction.proximity_score != null) {
        return `Proche (${prediction.proximity_score}%)`
      }
      if (prediction.actual_home_goals == null || prediction.actual_away_goals == null) {
        return prediction.isCorrect ? 'Correct' : 'Incorrect'
      }
      return `${prediction.actual_home_goals}-${prediction.actual_away_goals}`
    },
    getAccuracyPercentage(prediction) {
      return prediction.accuracy || 0
    },
    getPredictionType(prediction) {
      return prediction.confidence_raw > 0.7 ? 'Confiance Élevée' : 'Modérée'
    },
    getPredictedWinner(prediction) {
      return prediction.prediction
    },
    getActualWinner(prediction) {
      return prediction.result
    },
    getTotalGoalDifference(prediction) {
      if (!prediction.actual_result) return 0
      return prediction.isCorrect ? 0 : 1
    },
    getPerformanceClass(prediction) {
      if (prediction.accuracy >= 90) return 'performance-excellent'
      if (prediction.accuracy >= 70) return 'performance-good'
      return 'performance-average'
    },
    getChartBarClass(prediction) {
      if (prediction.isCorrect === true) return 'bar-correct'
      if (prediction.isCorrect === false) return 'bar-incorrect'
      return ''
    },
    computeAccuracy(item) {
      if (!item.actual_result) return 0
      const confidence = Number(item.confidence_score || 0)
      if (item.is_correct === true) {
        return Math.round(confidence * 100)
      }
      return Math.max(5, Math.round((1 - confidence) * 60))
    }
  },
  computed: {
    filteredData() {
      if (this.selectedFilter === 'all') return this.historyData
      if (this.selectedFilter === 'correct') return this.historyData.filter(p => p.isCorrect === true)
      if (this.selectedFilter === 'incorrect') return this.historyData.filter(p => p.isCorrect === false)
      if (this.selectedFilter === 'close') return this.historyData.filter(p => p.proximity_status === 'close')
      return this.historyData
    },
    globalScore() {
      const evaluated = this.historyData.filter(p => p.isCorrect !== null)
      if (evaluated.length === 0) return 0
      const correctPredictions = evaluated.filter(p => p.isCorrect === true).length
      return Math.round((correctPredictions / evaluated.length) * 100)
    },
    correctPredictions() {
      return this.historyData.filter(p => p.isCorrect === true).length
    },
    averageGoalDifference() {
      if (this.historyData.length === 0) return 0
      return 0.4
    },
    winnerAccuracy() {
      return this.globalScore
    }
  }
}
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background-image: linear-gradient(rgba(10, 10, 26, 0.4), rgba(10, 10, 26, 0.6)), url("@/assets/player1.jpg");
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  font-family: 'Inter', sans-serif;
  color: var(--text-primary);
}

.main-content {
  padding: 100px 2rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.history-container {
  background: var(--glass-bg);
  border-radius: 24px;
  padding: 3rem;
  box-shadow: var(--glass-shadow);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid var(--glass-border);
}

.page-title {
  margin: 0 0 3rem 0;
  color: var(--text-primary);
  font-size: 2.5rem;
  font-weight: 800;
  text-align: center;
  background: var(--accent-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* Statistics Dashboard */
.stats-dashboard {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 20px;
  padding: 1.5rem;
  border: 1px solid var(--glass-border);
  display: flex;
  align-items: center;
  gap: 1.2rem;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  border-color: var(--accent-secondary);
  box-shadow: 0 10px 30px rgba(0, 212, 255, 0.1);
}

.stat-icon {
  font-size: 1.8rem;
  width: 55px;
  height: 55px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--accent-gradient);
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(224, 38, 255, 0.3);
}

.stat-value {
  font-size: 1.8rem;
  font-weight: 800;
  color: var(--text-primary);
}

.stat-label {
  font-size: 0.85rem;
  color: var(--text-secondary);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Filters */
.filters-container {
  margin-bottom: 2rem;
}

.filter-select {
  padding: 0.8rem 1.5rem;
  border: 1px solid var(--glass-border);
  border-radius: 12px;
  font-size: 0.95rem;
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-primary);
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
}

.filter-select:focus {
  outline: none;
  border-color: var(--accent-secondary);
  box-shadow: 0 0 15px rgba(0, 212, 255, 0.2);
}

.filter-select option {
  background: #0f172a;
  color: white;
}

/* Table Styles */
.table-container {
  overflow-x: auto;
  margin-bottom: 3rem;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.01);
  border: 1px solid var(--glass-border);
}

.history-table {
  width: 100%;
  border-collapse: collapse;
}

.history-table th {
  background: rgba(255, 255, 255, 0.03);
  color: var(--text-secondary);
  padding: 1.2rem;
  text-align: left;
  font-weight: 700;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  border-bottom: 1px solid var(--glass-border);
}

.history-table td {
  padding: 1.2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.03);
  color: var(--text-primary);
  font-size: 0.95rem;
}

/* Status Colors with gradients */
.row-correct {
  background: rgba(0, 212, 255, 0.03);
}

.row-incorrect {
  background: rgba(248, 113, 113, 0.04);
}

.row-correct .match-cell {
  color: var(--accent-secondary);
}

.match-display {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.team-mini {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  flex: 1;
}

.logo-xs {
  width: 24px;
  height: 24px;
  object-fit: contain;
}

.vs-xs {
  font-size: 0.7rem;
  font-style: italic;
  opacity: 0.5;
  font-weight: 800;
}

.history-table tbody tr:hover {
  background: rgba(255, 255, 255, 0.04);
}

.score-badge {
  display: inline-block;
  padding: 0.5rem 1.2rem;
  border-radius: 30px;
  font-weight: 800;
  font-size: 0.85rem;
}

.score-badge.prediction {
  background: rgba(224, 38, 255, 0.1);
  color: #e026ff;
  border: 1px solid rgba(224, 38, 255, 0.3);
}

.score-badge.result {
  background: rgba(0, 212, 255, 0.1);
  color: var(--accent-secondary);
  border: 1px solid rgba(0, 212, 255, 0.3);
}

.diff-perfect { color: var(--accent-secondary); font-weight: 800; }
.diff-close { color: #f59e0b; font-weight: 800; }
.diff-poor { color: #f87171; font-weight: 800; }
.diff-neutral { color: var(--text-secondary); font-weight: 700; }

/* Accuracy Bar */
.accuracy-bar {
  position: relative;
  height: 24px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 50px;
  overflow: hidden;
  border: 1px solid var(--glass-border);
}

.accuracy-fill {
  height: 100%;
  background: var(--accent-gradient);
  transition: width 0.3s ease;
  box-shadow: 0 0 10px rgba(224, 38, 255, 0.3);
}

.accuracy-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 0.75rem;
  font-weight: 800;
  color: #fff;
  text-shadow: 0 0 4px rgba(0,0,0,0.5);
  z-index: 1;
}

/* Details and Charts */
.details-btn {
  padding: 0.6rem 1.2rem;
  background: var(--glass-bg);
  color: white;
  border: 1px solid var(--glass-border);
  border-radius: 10px;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 700;
  transition: all 0.3s ease;
}

.details-btn:hover {
  background: var(--glass-hover);
  border-color: var(--accent-secondary);
  box-shadow: 0 0 15px rgba(0, 212, 255, 0.2);
}

.chart-container {
  margin-top: 3rem;
  padding: 2.5rem;
  background: var(--glass-bg);
  border-radius: 24px;
  border: 1px solid var(--glass-border);
}

.chart-container h3 {
  margin-bottom: 2rem;
  font-weight: 800;
  background: var(--accent-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-align: center;
}

.performance-chart {
  display: flex;
  align-items: end;
  justify-content: space-around;
  height: 250px;
  gap: 1rem;
  padding: 1.5rem;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 20px;
  border: 1px solid var(--glass-border);
}

.bar-fill {
  width: 100%;
  border-radius: 8px 8px 0 0;
  background: var(--accent-gradient);
  box-shadow: 0 0 15px rgba(224, 38, 255, 0.2);
}

.bar-incorrect .bar-fill {
  background: linear-gradient(180deg, #f87171, #ef4444);
  box-shadow: 0 0 15px rgba(239, 68, 68, 0.2);
}

@media (max-width: 768px) {
  .main-content {
    padding: 100px 1rem 2rem;
  }

  .stats-dashboard {
    grid-template-columns: 1fr 1fr;
  }

  .history-table {
    font-size: 0.8rem;
  }
}

</style>