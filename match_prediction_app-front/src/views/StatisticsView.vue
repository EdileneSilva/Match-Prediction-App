<template>
  <div class="dashboard">
    <!-- Main Content -->
    <main class="main-content">
      <div class="statistics-container">
        <h1 class="page-title">📊 Statistiques de l'IA</h1>

        <!-- Navigation par onglets -->
        <div class="tabs-container">
          <button 
            v-for="tab in tabs" 
            :key="tab.id"
            @click="activeTab = tab.id"
            :class="['tab-button', { active: activeTab === tab.id }]"
          >
            {{ tab.label }}
          </button>
        </div>

        <!-- Contenu des onglets -->
        <div class="tab-content">
          <!-- Onglet Classement -->
          <div v-if="activeTab === 'ranking'" class="tab-panel">
            <div class="ranking-section">
              <h2>🏆 Classement des Équipes</h2>
              
              <!-- Filtres -->
              <div class="filters-section">
                <select v-model="selectedLeague" class="filter-select">
                  <option value="all">Toutes les ligues</option>
                  <option value="ligue1">Ligue 1</option>
                </select>
                <select v-model="selectedSeason" class="filter-select">
                  <option value="2024">Saison 2024</option>
                  <option value="2023">Saison 2023</option>
                  <option value="2022">Saison 2022</option>
                </select>
              </div>

              <!-- Tableau de classement -->
              <div class="ranking-table-container">
                <table class="ranking-table">
                  <thead>
                    <tr>
                      <th>Pos</th>
                      <th>Équipe</th>
                      <th>MJ</th>
                      <th>V</th>
                      <th>N</th>
                      <th>D</th>
                      <th>BP</th>
                      <th>BC</th>
                      <th>Diff</th>
                      <th>Pts</th>
                      <th>Forme</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(team, index) in rankingData" :key="team.id" 
                        :class="getRankingRowClass(index)">
                      <td class="position">{{ team.position }}</td>
                      <td class="team-name">
                        <div class="team-info">
                              <img 
                                v-if="isUrl(team.logo)" 
                                :src="team.logo" 
                                :alt="team.name"
                                class="team-logo-img"
                                @error="$event.target.style.display='none'"
                              />
                              <span v-else class="team-logo">{{ team.logo || '⚽' }}</span>
                              {{ team.name }}
                        </div>
                      </td>
                      <td>{{ team.matchesPlayed }}</td>
                      <td>{{ team.wins }}</td>
                      <td>{{ team.draws }}</td>
                      <td>{{ team.losses }}</td>
                      <td class="goals">{{ team.goalsFor }}</td>
                      <td class="goals-conceded">{{ team.goalsAgainst }}</td>
                      <td :class="getGoalDiffClass(team.goalDifference)">
                        {{ team.goalDifference > 0 ? '+' : '' }}{{ team.goalDifference }}
                      </td>
                      <td class="points">{{ team.points }}</td>
                      <td>
                        <div class="form-indicators">
                          <span v-for="(result, i) in team.form" :key="i" 
                                :class="getFormClass(result)">
                            {{ result }}
                          </span>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <!-- Onglet Forme Récente -->
          <div v-if="activeTab === 'form'" class="tab-panel">
            <div class="form-section">
              <h2>📈 Forme Récente</h2>
              
              <!-- Sélection d'équipe -->
              <div class="team-selector">
                <select v-model="selectedTeam" class="team-select">
                  <option value="">Choisir une équipe</option>
                  <option v-for="team in teamsList" :key="team.id" :value="team.id">
                    {{ team.name }}
                  </option>
                </select>
              </div>

              <!-- Statistiques de forme -->
              <div v-if="selectedTeam" class="form-stats">
                <div class="form-cards">
                  <div class="form-card">
                    <div class="form-icon">🔥</div>
                    <div class="form-content">
                      <div class="form-value">{{ currentForm.winRate }}%</div>
                      <div class="form-label">Taux de victoire</div>
                    </div>
                  </div>
                  <div class="form-card">
                    <div class="form-icon">⚡</div>
                    <div class="form-content">
                      <div class="form-value">{{ currentForm.avgGoals }}</div>
                      <div class="form-label">Moyenne de buts</div>
                    </div>
                  </div>
                  <div class="form-card">
                    <div class="form-icon">🛡️</div>
                    <div class="form-content">
                      <div class="form-value">{{ currentForm.cleanSheets }}</div>
                      <div class="form-label">Matchs sans encaisser</div>
                    </div>
                  </div>
                </div>

                <!-- Graphique de forme -->
                <div class="form-chart">
                  <h3>📊 Derniers 10 matchs</h3>
                  <div class="matches-timeline">
                    <div v-for="(match, index) in recentMatches" :key="index" 
                         class="match-item" :class="getMatchResultClass(match.result)">
                      <div class="match-date">{{ match.date }}</div>
                      <div class="match-opponent">{{ match.opponent }}</div>
                      <div class="match-score">{{ match.score }}</div>
                      <div class="match-result">{{ match.result }}</div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Message si aucune équipe sélectionnée -->
              <div v-else class="no-selection">
                <p>👆 Veuillez sélectionner une équipe pour voir sa forme récente</p>
              </div>
            </div>
          </div>

          <!-- Onglet Buts Marqués -->
          <div v-if="activeTab === 'goals'" class="tab-panel">
            <div class="goals-section">
              <h2>⚽ Buts Marqués</h2>
              
              <!-- Statistiques générales -->
              <div class="goals-overview">
                <div class="goals-cards">
                  <div class="goals-card">
                    <div class="goals-icon">🎯</div>
                    <div class="goals-content">
                      <div class="goals-value">{{ totalGoals }}</div>
                      <div class="goals-label">Total de buts</div>
                    </div>
                  </div>
                  <div class="goals-card">
                    <div class="goals-icon">📊</div>
                    <div class="goals-content">
                      <div class="goals-value">{{ avgGoalsPerMatch }}</div>
                      <div class="goals-label">Moyenne par match</div>
                    </div>
                  </div>
                  <div class="goals-card">
                    <div class="goals-icon">🏆</div>
                    <div class="goals-content">
                      <div class="goals-value">{{ topScorer.name }}</div>
                      <div class="goals-label">Meilleur buteur</div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Classement des buteurs -->
              <div class="top-scorers">
                <h3>🥇 Meilleurs Buteurs</h3>
                <div class="scorers-list">
                  <div v-for="(scorer, index) in topScorers" :key="scorer.id" 
                       class="scorer-item" :class="getScorerClass(index)">
                    <div class="scorer-rank">{{ index + 1 }}</div>
                    <div class="scorer-info">
                      <div class="scorer-name">{{ scorer.name }}</div>
                      <div class="scorer-team">{{ scorer.team }}</div>
                    </div>
                    <div class="scorer-stats">
                      <div class="scorer-goals">{{ scorer.goals }} buts</div>
                      <div class="scorer-matches">{{ scorer.matches }} matchs</div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Buts par équipes -->
              <div class="goals-distribution">
                <h3>📈 Buts par équipes</h3>
                <div class="distribution-chart">
                  <div class="chart-item" v-for="(period, index) in goalsDistribution" :key="index">
                    <div class="period-label">{{ period.team }}</div>
                    <div class="period-bar">
                      <div class="bar-fill" :style="{width: period.percentage + '%'}"></div>
                    </div>
                    <div class="period-value">{{ period.goals }} buts</div>
                  </div>
                </div>
              </div>
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
  name: 'StatisticsView',
  data() {
    return {
      activeTab: 'ranking',
      selectedLeague: 'all',
      selectedSeason: '2024',
      selectedTeam: '',
      loading: false,
      error: null,
      
      tabs: [
        { id: 'ranking', label: 'Classement' },
        { id: 'form',    label: 'Forme Récente' },
        { id: 'goals',   label: 'Buts Marqués' }
      ],
      
      rankingData: [],
      teamsList: [],
      
      currentForm: { winRate: 0, avgGoals: 0, cleanSheets: 0 },
      recentMatches: [],
      
      totalGoals: 0,
      avgGoalsPerMatch: 0,
      topScorer: { name: 'N/A', goals: 0 },
      topScorers: [],
      
      // Données hardcodées en attendant l'endpoint goals-stats
      goalsDistribution: [
        { label: '0-15 min',  goals: 22, percentage: 14 },
        { label: '15-30 min', goals: 35, percentage: 22 },
        { label: '30-45 min', goals: 28, percentage: 18 },
        { label: '45-60 min', goals: 31, percentage: 20 },
        { label: '60-75 min', goals: 24, percentage: 15 },
        { label: '75-90 min', goals: 16, percentage: 11 }
      ]
    }
  },
  
  async mounted() {
    await this.loadStandings()
    await this.loadGoalsStats()
  },
  
  methods: {
    isUrl(value) {
      return typeof value === 'string' && (value.startsWith('http') || value.startsWith('/'))
    },

    // ─── Classement (appel indépendant) ────────────────────────────────────
    async loadStandings() {
      this.loading = true
      try {
        const response = await apiClient.get('/dashboard/standings')
        
        if (response.status === 'success' && Array.isArray(response.data)) {
          this.rankingData = response.data.map(item => ({
            id:             item.position  ?? item.rank,
            position:       item.position  ?? item.rank,
            name:           item.team      ?? '—',
            logo:           item.logo      || '⚽',
            matchesPlayed:  item.played    ?? 0,
            wins:           item.wins      ?? 0,
            draws:          item.draws     ?? 0,
            losses:         item.losses    ?? 0,
            goalsFor:       item.goals_for      ?? 0,   // ← champs LFP
            goalsAgainst:   item.goals_against  ?? 0,
            goalDifference: item.goals_diff     ?? 0,
            points:         item.points    ?? 0,
            form:           item.form      || []
          }))

          // Peupler la liste d'équipes pour l'onglet Forme
          this.teamsList = this.rankingData.map(t => ({ id: t.id, name: t.name }))
        }
      } catch (err) {
        this.error = "Erreur lors du chargement du classement"
        console.error('Standings error:', err)
      } finally {
        this.loading = false
      }
    },

    // ─── Stats de buts (appel indépendant — ne bloque pas le classement) ───
    async loadGoalsStats() {
      try {
        const response = await apiClient.get('/dashboard/goals-stats')
        
        if (response.status === 'success' && response.data) {
          const d = response.data
          this.totalGoals        = d.total_goals        ?? 0
          this.avgGoalsPerMatch  = d.avg_goals_per_match ?? 0
          this.topScorer         = {
            name:  d.top_scorer?.name  ?? 'N/A',
            goals: d.top_scorer?.goals ?? 0
          }
          this.topScorers = (d.top_scorers ?? []).map((s, i) => ({
            id:      s.id     ?? i + 1,
            name:    s.name,
            team:    s.team   ?? '—',
            goals:   s.goals  ?? 0,
            matches: s.matches ?? 0
          }))
          // Ici les items ont bien "label" pour le template
          this.goalsDistribution = (d.clubs_goals_distribution ?? []).map(item => ({
            label:      item.team       ?? item.label,
            goals:      item.goals      ?? 0,
            percentage: item.percentage ?? 0
          }))
        }
      } catch (err) {
        // Echec silencieux — l'onglet Buts garde les données hardcodées
        console.warn('Goals stats indisponible, données par défaut utilisées.')
      }
    },

    // ─── Méthodes utilitaires ───────────────────────────────────────────────
    getRankingRowClass(index) {
      if (index === 0) return 'rank-first'
      if (index === 1) return 'rank-second'
      if (index === 2) return 'rank-third'
      if (index < 6)   return 'rank-european'
      if (index >= this.rankingData.length - 3) return 'rank-relegation'
      return ''
    },
    
    getGoalDiffClass(diff) {
      if (diff > 0) return 'diff-positive'
      if (diff < 0) return 'diff-negative'
      return 'diff-neutral'
    },
    
    getFormClass(result) {
      switch (result) {
        case 'V': return 'form-win'
        case 'N': return 'form-draw'
        case 'D': return 'form-loss'
        default:  return ''
      }
    },
    
    getMatchResultClass(result) {
      switch (result) {
        case 'V': return 'match-win'
        case 'N': return 'match-draw'
        case 'D': return 'match-loss'
        default:  return ''
      }
    },
    
    getScorerClass(index) {
      if (index === 0) return 'scorer-first'
      if (index === 1) return 'scorer-second'
      if (index === 2) return 'scorer-third'
      return ''
    }
  }
}
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  padding-top: 80px;
}

.main-content {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.statistics-container {
  background: var(--glass-bg);
  border-radius: 20px;
  padding: 2.5rem;
  box-shadow: var(--glass-shadow);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid var(--glass-border);
}

.page-title {
  margin: 0 0 2rem 0;
  color: var(--text-primary);
  font-size: 2rem;
  font-weight: 700;
  text-align: center;
  background: var(--accent-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Onglets */
.tabs-container {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid var(--glass-border);
  padding-bottom: 0;
}

.tab-button {
  padding: 1rem 2rem;
  background: none;
  border: none;
  border-bottom: 3px solid transparent;
  color: var(--text-secondary);
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: -2px;
}

.tab-button:hover {
  color: var(--accent-secondary);
  background: rgba(0, 212, 255, 0.05);
}

.tab-button.active {
  color: var(--accent-secondary);
  border-bottom-color: var(--accent-secondary);
  font-weight: 600;
}

.tab-content {
  min-height: 500px;
}

.tab-panel h2 {
  color: var(--text-primary);
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  border-bottom: 2px solid var(--accent-secondary);
  padding-bottom: 0.5rem;
}

/* Filtres */
.filters-section {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.filter-select, .team-select {
  padding: 0.75rem 1rem;
  border: 1px solid var(--glass-border);
  border-radius: 12px;
  font-size: 1rem;
  background: var(--glass-bg);
  color: var(--text-primary);
  cursor: pointer;
  transition: border-color 0.3s;
}

.filter-select:focus, .team-select:focus {
  outline: none;
  border-color: var(--accent-secondary);
  box-shadow: 0 0 0 3px rgba(0, 212, 255, 0.15);
}

/* Tableau de classement */
.ranking-table-container {
  overflow-x: auto;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.ranking-table {
  width: 100%;
  border-collapse: collapse;
  background: transparent;
}

.ranking-table th {
  background: var(--accent-gradient);
  color: white;
  padding: 1rem;
  text-align: center;
  font-weight: 600;
  font-size: 0.9rem;
}

.ranking-table td {
  padding: 0.75rem;
  text-align: center;
  border-bottom: 1px solid var(--glass-border);
  color: var(--text-primary);
}

.position {
  font-weight: bold;
  font-size: 1.1rem;
}

.team-name {
  text-align: left;
}

.team-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.team-logo {
  font-size: 1.2rem;
}

.goals, .goals-conceded {
  font-weight: 500;
}

.points {
  font-weight: bold;
  font-size: 1.1rem;
  color: var(--accent-secondary);
}

/* Classes de rang */
.rank-first { background: rgba(255, 215, 0, 0.1); }
.rank-second { background: rgba(192, 192, 192, 0.1); }
.rank-third { background: rgba(205, 127, 50, 0.1); }
.rank-european { background: rgba(102, 126, 234, 0.05); }
.rank-relegation { background: rgba(220, 53, 69, 0.05); }

/* Différence de buts */
.diff-positive { color: #28a745; font-weight: bold; }
.diff-negative { color: #dc3545; font-weight: bold; }
.diff-neutral { color: #666; }

/* Indicateurs de forme */
.form-indicators {
  display: flex;
  gap: 0.25rem;
  justify-content: center;
}

.form-indicators span {
  width: 20px;
  height: 20px;
  border-radius: 3px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
  font-weight: bold;
  color: white;
}

.form-win { background: #28a745; }
.form-draw { background: #ffc107; }
.form-loss { background: #dc3545; }

/* Cartes de statistiques */
.form-cards, .goals-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.form-card, .goals-card {
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: var(--glass-shadow);
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.form-card:hover, .goals-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 212, 255, 0.2);
}

.form-icon, .goals-icon {
  font-size: 2rem;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--accent-gradient);
  border-radius: 50%;
}

.form-value, .goals-value {
  font-size: 1.8rem;
  font-weight: bold;
  color: var(--text-primary);
}

.form-label, .goals-label {
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin-top: 0.25rem;
}

/* Timeline des matchs */
.matches-timeline {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.match-item {
  display: grid;
  grid-template-columns: 80px 1fr 80px 60px;
  align-items: center;
  padding: 1rem;
  border-radius: 12px;
  border: 1px solid var(--glass-border);
  background: var(--glass-bg);
}

.match-win { background: rgba(40, 167, 69, 0.08); border-color: rgba(40, 167, 69, 0.4); }
.match-draw { background: rgba(255, 193, 7, 0.08); border-color: rgba(255, 193, 7, 0.4); }
.match-loss { background: rgba(220, 53, 69, 0.08); border-color: rgba(220, 53, 69, 0.4); }

.match-date { font-weight: 600; color: var(--text-secondary); }
.match-opponent { font-weight: 500; color: var(--text-primary); }
.match-score { font-weight: bold; color: var(--text-primary); }
.match-result { font-weight: bold; color: var(--text-primary); }

/* Buteurs */
.scorers-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.scorer-item {
  display: flex;
  align-items: center;
  padding: 1rem;
  border-radius: 12px;
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.scorer-item:hover {
  transform: translateX(5px);
  box-shadow: 0 4px 20px rgba(0, 212, 255, 0.15);
}

.scorer-rank {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  margin-right: 1rem;
}

.scorer-first .scorer-rank { background: gold; color: #1a1a2e; }
.scorer-second .scorer-rank { background: silver; color: #1a1a2e; }
.scorer-third .scorer-rank { background: #cd7f32; color: white; }

.scorer-info {
  flex: 1;
}

.scorer-name {
  font-weight: 600;
  color: var(--text-primary);
}

.scorer-team {
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.scorer-stats {
  text-align: right;
}

.scorer-goals {
  font-weight: bold;
  font-size: 1.1rem;
  color: var(--accent-secondary);
}

.scorer-matches {
  font-size: 0.9rem;
  color: var(--text-secondary);
}

/* Distribution des buts */
.distribution-chart {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.chart-item {
  display: grid;
  grid-template-columns: 100px 1fr 80px;
  align-items: center;
  gap: 1rem;
}

.period-label {
  font-weight: 500;
  color: var(--text-secondary);
}

.period-bar {
  height: 20px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  background: var(--accent-gradient);
  transition: width 0.5s ease;
}

.period-value {
  font-weight: bold;
  color: var(--text-primary);
  text-align: right;
}

/* Message pas de sélection */
.no-selection {
  text-align: center;
  padding: 3rem;
  color: var(--text-secondary);
  font-size: 1.1rem;
}
.team-logo-img {
  width: 28px;
  height: 28px;
  object-fit: contain;
  border-radius: 4px;
}

/* Responsive */
@media (max-width: 768px) {
  .main-content {
    padding: 1rem;
  }

  .statistics-container {
    padding: 1.5rem;
  }

  .tabs-container {
    flex-direction: column;
    gap: 0;
  }

  .tab-button {
    border-bottom: 1px solid var(--glass-border);
    border-right: none;
    margin-bottom: 0;
  }

  .tab-button.active {
    border-bottom-color: var(--accent-secondary);
    border-right: none;
  }

  .filters-section {
    flex-direction: column;
  }

  .form-cards, .goals-cards {
    grid-template-columns: 1fr;
  }

  .match-item {
    grid-template-columns: 60px 1fr 60px 50px;
    font-size: 0.9rem;
  }

  .scorer-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .chart-item {
    grid-template-columns: 80px 1fr 60px;
    font-size: 0.9rem;
  }
}
</style>