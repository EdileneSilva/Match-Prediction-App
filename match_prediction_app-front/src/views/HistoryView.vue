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
              <tr v-for="(prediction, index) in filteredData" :key="index" 
                  :class="getRowClass(prediction)">
                <td>{{ prediction.date }}</td>
                <td class="match-cell">{{ prediction.match }}</td>
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

export default {
  name: 'HistoryView',
  data() {
    return {
      historyData: [],
      error: null
    }
  },
  async mounted() {
    try {
      const data = await apiClient.get('/predictions/history')
      this.historyData = data.map(item => ({
        date: new Date(item.created_at).toLocaleDateString('fr-FR'),
        match: `${item.home_team} - ${item.away_team}`,
        prediction: this.formatResult(item.predicted_result),
        confidence: (item.confidence_score * 100).toFixed(1) + '%',
        isCorrect: true // On ne connaît pas encore le vrai résultat
      }))
    } catch (err) {
      this.error = "Erreur lors de la récupération de l'historique"
      console.error(err)
    }
  },
  methods: {
    formatResult(result) {
      const mapping = {
        'HOME_WIN': 'Victoire Domicile',
        'AWAY_WIN': 'Victoire Extérieur',
        'DRAW': 'Match Nul'
      }
      return mapping[result] || result
    }
  },
  computed: {
    globalScore() {
      if (this.historyData.length === 0) return 0
      const correctPredictions = this.historyData.filter(p => p.isCorrect).length
      const totalPredictions = this.historyData.length
      return Math.round((correctPredictions / totalPredictions) * 100)
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

.main-content {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.history-container {
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

/* Statistics Dashboard */
.stats-dashboard {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-icon {
  font-size: 2rem;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 50%;
}

.stat-value {
  font-size: 1.8rem;
  font-weight: bold;
  color: #333;
}

.stat-label {
  font-size: 0.9rem;
  color: #666;
  margin-top: 0.25rem;
}

/* Filters */
.filters-container {
  margin-bottom: 1.5rem;
}

.filter-select {
  padding: 0.75rem 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  background: white;
  cursor: pointer;
  transition: border-color 0.2s;
}

.filter-select:focus {
  outline: none;
  border-color: #667eea;
}

/* Table Styles */
.table-container {
  overflow-x: auto;
  margin-bottom: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.history-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
}

.history-table th {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.history-table td {
  padding: 1rem;
  border-bottom: 1px solid #e0e0e0;
  color: #333;
  font-size: 0.95rem;
}

/* Row Classes */
.row-correct {
  background: rgba(40, 167, 69, 0.05);
}

.row-close {
  background: rgba(255, 193, 7, 0.05);
}

.row-incorrect {
  background: rgba(220, 53, 69, 0.05);
}

/* Cell Styles */
.match-cell {
  font-weight: 600;
  color: #333;
}

.prediction-cell, .result-cell {
  text-align: center;
}

.score-badge {
  display: inline-block;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: bold;
  font-size: 0.9rem;
}

.score-badge.prediction {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  border: 2px solid #667eea;
}

.score-badge.result {
  background: rgba(40, 167, 69, 0.1);
  color: #28a745;
  border: 2px solid #28a745;
}

.difference-cell {
  text-align: center;
  font-weight: bold;
}

.diff-perfect { color: #28a745; }
.diff-good { color: #ffc107; }
.diff-average { color: #fd7e14; }
.diff-poor { color: #dc3545; }

/* Accuracy Bar */
.accuracy-cell {
  padding: 0.5rem;
}

.accuracy-bar {
  position: relative;
  height: 20px;
  background: #e0e0e0;
  border-radius: 10px;
  overflow: hidden;
}

.accuracy-fill {
  height: 100%;
  background: linear-gradient(90deg, #28a745, #20c997);
  transition: width 0.3s ease;
}

.accuracy-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 0.75rem;
  font-weight: bold;
  color: #333;
}

/* Details Button */
.details-btn {
  padding: 0.5rem 1rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.85rem;
  transition: background 0.2s;
}

.details-btn:hover {
  background: #5a6fd8;
}

/* Details Row */
.details-row {
  background: rgba(102, 126, 234, 0.02);
}

.prediction-details {
  padding: 1.5rem;
}

.prediction-details h4 {
  margin: 0 0 1rem 0;
  color: #333;
  font-size: 1.1rem;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem;
  background: white;
  border-radius: 6px;
  border: 1px solid #e0e0e0;
}

.detail-label {
  font-weight: 600;
  color: #666;
}

.detail-value {
  color: #333;
  font-weight: 500;
}

/* Performance Indicator */
.performance-indicator {
  margin-top: 1rem;
}

.indicator-label {
  font-weight: 600;
  color: #333;
  margin-bottom: 0.5rem;
}

.indicator-bar {
  height: 12px;
  background: #e0e0e0;
  border-radius: 6px;
  overflow: hidden;
}

.indicator-fill {
  height: 100%;
  transition: width 0.3s ease;
}

.performance-excellent { background: linear-gradient(90deg, #28a745, #20c997); }
.performance-good { background: linear-gradient(90deg, #ffc107, #fd7e14); }
.performance-average { background: linear-gradient(90deg, #fd7e14, #dc3545); }
.performance-poor { background: #dc3545; }

/* Performance Chart */
.chart-container {
  margin-top: 2rem;
  padding: 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.chart-container h3 {
  margin: 0 0 1.5rem 0;
  color: #333;
  text-align: center;
}

.performance-chart {
  display: flex;
  align-items: end;
  justify-content: space-around;
  height: 200px;
  gap: 1rem;
  padding: 1rem;
  background: rgba(102, 126, 234, 0.02);
  border-radius: 8px;
}

.chart-bar {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: end;
  max-width: 60px;
}

.bar-fill {
  width: 100%;
  background: linear-gradient(180deg, #667eea, #764ba2);
  border-radius: 4px 4px 0 0;
  transition: height 0.3s ease;
}

.bar-label {
  margin-top: 0.5rem;
  font-size: 0.75rem;
  color: #666;
  text-align: center;
}

/* Responsive Design */
@media (max-width: 768px) {
  .main-content {
    padding: 1rem;
  }

  .history-container {
    padding: 1.5rem;
  }

  .stats-dashboard {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }

  .history-table {
    font-size: 0.8rem;
  }

  .history-table th,
  .history-table td {
    padding: 0.5rem 0.25rem;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .details-grid {
    grid-template-columns: 1fr;
  }

  .performance-chart {
    height: 150px;
  }
}
</style>