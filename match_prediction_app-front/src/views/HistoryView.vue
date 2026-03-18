<template>
  <div class="dashboard">
    <!-- Main Content -->
    <main class="main-content">
      <div class="history-container">
        <h1 class="page-title">Historique des Prédictions</h1>

        <!-- History Table -->
        <div class="table-container">
          <table class="history-table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Match</th>
                <th>Prédiction</th>
                <th>Résultat</th>
                <th>Statut</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(prediction, index) in historyData" :key="index">
                <td>{{ prediction.date }}</td>
                <td>{{ prediction.match }}</td>
                <td>{{ prediction.prediction }}</td>
                <td>{{ prediction.result }}</td>
                <td class="status-cell">
                  <span v-if="prediction.isCorrect" class="status-icon correct">✓</span>
                  <span v-else class="status-icon incorrect">✗</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Global Score -->
        <div class="global-score">
          <span class="score-label">Score global : </span>
          <span class="score-value">{{ globalScore }}%</span>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'HistoryView',
  data() {
    return {
      historyData: [
        {
          date: '12/03',
          match: 'PSG - OM',
          prediction: '2-1',
          result: '1-1',
          isCorrect: false
        },
        {
          date: '11/03',
          match: 'Lyon - Lille',
          prediction: '1-0',
          result: '1-0',
          isCorrect: true
        },
        {
          date: '10/03',
          match: 'Monaco - Nice',
          prediction: '3-1',
          result: '2-1',
          isCorrect: true
        }
      ]
    }
  },
  computed: {
    globalScore() {
      const correctPredictions = this.historyData.filter(p => p.isCorrect).length;
      const totalPredictions = this.historyData.length;
      return Math.round((correctPredictions / totalPredictions) * 100);
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
  max-width: 1000px;
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

/* Table Styles */
.table-container {
  overflow-x: auto;
  margin-bottom: 2rem;
}

.history-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.history-table th {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  font-size: 0.95rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.history-table td {
  padding: 1rem;
  border-bottom: 1px solid #e0e0e0;
  color: #333;
  font-size: 0.95rem;
}

.history-table tbody tr:hover {
  background: rgba(102, 126, 234, 0.05);
}

.history-table tbody tr:last-child td {
  border-bottom: none;
}

/* Status Icons */
.status-cell {
  text-align: center;
}

.status-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  font-weight: bold;
  font-size: 14px;
}

.status-icon.correct {
  background: #28a745;
  color: white;
}

.status-icon.incorrect {
  background: #dc3545;
  color: white;
}

/* Global Score */
.global-score {
  text-align: center;
  padding: 1.5rem;
  background: rgba(102, 126, 234, 0.1);
  border-radius: 8px;
  border: 2px solid rgba(102, 126, 234, 0.2);
}

.score-label {
  color: #555;
  font-size: 1.1rem;
  font-weight: 500;
}

.score-value {
  font-weight: bold;
  color: #667eea;
  font-size: 1.3rem;
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

  .history-container {
    padding: 1.5rem;
  }

  .history-table {
    font-size: 0.85rem;
  }

  .history-table th,
  .history-table td {
    padding: 0.75rem 0.5rem;
  }

  .page-title {
    font-size: 1.5rem;
  }

}
</style>