<template>
  <div class="league-table-container">
    <div class="table-header">
      <div class="header-info">
        <h3>Classement Ligue 1</h3>
        <p class="subtitle">Saison 2025/2026</p>
      </div>
    </div>
    
    <div class="table-wrapper">
      <table class="ranking-table">
        <thead>
          <tr>
            <th class="text-center">Pos</th>
            <th>Équipe</th>
            <th class="text-center">MJ</th>
            <th class="text-center">Pts</th>
            <th class="text-center hide-mobile">G</th>
            <th class="text-center hide-mobile">N</th>
            <th class="text-center hide-mobile">P</th>
            <th class="text-center">DB</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="team in standings" :key="team.rank" :class="{ 'top-position': team.rank <= 3, 'low-position': team.rank >= 16 }">
            <td class="text-center">
              <span class="rank-badge">{{ team.rank }}</span>
            </td>
            <td>
              <div class="team-cell">
                <img :src="team.logo" :alt="team.team" class="team-logo-small" />
                <span class="team-name">{{ team.team }}</span>
              </div>
            </td>
            <td class="text-center">{{ team.played }}</td>
            <td class="text-center"><strong>{{ team.points }}</strong></td>
            <td class="text-center hide-mobile">{{ team.wins }}</td>
            <td class="text-center hide-mobile">{{ team.draws }}</td>
            <td class="text-center hide-mobile">{{ team.losses }}</td>
            <td class="text-center" :class="team.goals_diff >= 0 ? 'pos-diff' : 'neg-diff'">
              {{ team.goals_diff > 0 ? '+' : '' }}{{ team.goals_diff }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <div v-if="standings.length === 0" class="no-data">
       Initialisation du classement...
    </div>
  </div>
</template>

<script>
export default {
  name: 'LeagueTable',
  props: {
    standings: {
      type: Array,
      required: true
    }
  }
}
</script>

<style scoped>
.league-table-container {
  background: var(--glass-bg);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid var(--glass-border);
  border-radius: 24px;
  padding: 1.5rem;
  box-shadow: var(--glass-shadow);
  color: var(--text-primary);
  height: 100%;
}

.table-header {
  margin-bottom: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-info h3 {
  margin: 0;
  font-size: 1.4rem;
  font-weight: 800;
  background: linear-gradient(to right, #fff, #a0aec0);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.subtitle {
  margin: 0;
  font-size: 0.8rem;
  color: var(--text-secondary);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.table-wrapper {
  overflow-x: auto;
  /* Retrait de la limite de hauteur pour afficher tout le classement (18 équipes) */
}

.table-wrapper::-webkit-scrollbar {
  width: 6px;
}

.table-wrapper::-webkit-scrollbar-track {
  background: transparent;
}

.table-wrapper::-webkit-scrollbar-thumb {
  background: var(--glass-border);
  border-radius: 10px;
}

.ranking-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

.ranking-table th {
  text-align: left;
  padding: 1rem 0.5rem;
  color: var(--text-secondary);
  font-weight: 600;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  border-bottom: 1px solid var(--glass-border);
}

.ranking-table td {
  padding: 0.8rem 0.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.team-cell {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.team-logo-small {
  width: 28px;
  height: 28px;
  object-fit: contain;
}

.rank-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 6px;
  font-weight: 800;
  font-size: 0.8rem;
  background: rgba(255, 255, 255, 0.05);
}

.top-position .rank-badge {
  background: var(--accent-gradient);
  box-shadow: 0 0 10px rgba(224, 38, 255, 0.3);
}

.low-position .rank-badge {
  background: rgba(255, 59, 48, 0.2);
  color: #ff3b30;
}

.text-center {
  text-align: center;
}

.pos-diff {
  color: #4cd964;
  font-weight: 600;
}

.neg-diff {
  color: #ff3b30;
  font-weight: 600;
}

.team-name {
  font-weight: 500;
}

.no-data {
  text-align: center;
  padding: 2rem;
  color: var(--text-secondary);
}

@media (max-width: 1024px) {
  .hide-mobile {
    display: none;
  }
}
</style>
