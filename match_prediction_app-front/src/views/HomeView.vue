<template>
  <div class="dashboard">
    <!-- Navigation Bar -->
    <nav class="navbar">
      <div class="nav-brand">LOGO</div>
      <div class="nav-menu">
        <router-link to="/" class="nav-item active">Dashboard</router-link>
        <router-link to="/predictions" class="nav-item">Prédictions</router-link>
        <router-link to="/history" class="nav-item">Historique</router-link>
        <router-link to="/profile" class="nav-item">Profil</router-link>
        <router-link to="/exit" class="nav-item exit">Exit</router-link>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="main-content">
      <!-- Info Cards -->
      <section class="info-cards">
        <div class="card">
          <div class="card-icon">📊</div>
          <div class="card-content">
            <h3>Score utilisateur</h3>
            <p class="score">85 pts</p>
          </div>
        </div>
        <div class="card">
          <div class="card-icon">⚽</div>
          <div class="card-content">
            <h3>Matchs</h3>
            <p>12 Matchs prédits</p>
          </div>
        </div>
        <div class="card">
          <div class="card-icon">📈</div>
          <div class="card-content">
            <h3>Statistiques</h3>
            <p>74% Réussite</p>
          </div>
        </div>
      </section>

      <!-- Today's Matches -->
      <section class="matches-section">
        <h2>Matchs du jour</h2>
        <div class="matches-list">
          <div class="match-item">
            <div class="match-teams">
              <span>PSG</span>
              <span>vs</span>
              <span>Marseille</span>
            </div>
            <div class="match-percentage">65%</div>
            <button class="view-btn">Voir</button>
          </div>
          <div class="match-item">
            <div class="match-teams">
              <span>Lyon</span>
              <span>vs</span>
              <span>Lille</span>
            </div>
            <div class="match-percentage">52%</div>
            <button class="view-btn">Voir</button>
          </div>
          <div class="match-item">
            <div class="match-teams">
              <span>Monaco</span>
              <span>vs</span>
              <span>Nice</span>
            </div>
            <div class="match-percentage">71%</div>
            <button class="view-btn">Voir</button>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
export default {
  name: 'HomeView'
}
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Navigation */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.nav-brand {
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
}

.nav-menu {
  display: flex;
  gap: 2rem;
}

.nav-item {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.nav-item:hover {
  color: white;
  background: rgba(255, 255, 255, 0.1);
}

.nav-item.active {
  color: white;
  background: rgba(255, 255, 255, 0.2);
}

.nav-item.exit {
  background: rgba(255, 67, 54, 0.3);
  color: #ff4336;
}

.nav-item.exit:hover {
  background: rgba(255, 67, 54, 0.5);
}

/* Main Content */
.main-content {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

/* Info Cards */
.info-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

.card-icon {
  font-size: 2.5rem;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 12px;
}

.card-content h3 {
  margin: 0 0 0.5rem 0;
  color: #333;
  font-size: 1rem;
  font-weight: 600;
}

.card-content p {
  margin: 0;
  color: #666;
  font-size: 1.1rem;
  font-weight: 500;
}

.score {
  color: #667eea !important;
  font-size: 1.5rem !important;
  font-weight: bold !important;
}

/* Matches Section */
.matches-section {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.matches-section h2 {
  margin: 0 0 1.5rem 0;
  color: #333;
  font-size: 1.5rem;
  font-weight: 600;
}

.matches-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.match-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 12px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.match-item:hover {
  background: rgba(255, 255, 255, 1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.match-teams {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  font-weight: 500;
  color: #333;
  flex: 1;
}

.match-teams span:first-child,
.match-teams span:last-child {
  font-weight: 600;
  color: #667eea;
}

.match-percentage {
  font-size: 1.2rem;
  font-weight: bold;
  color: #667eea;
  margin: 0 2rem;
}

.view-btn {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  padding: 0.5rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.view-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
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
  
  .info-cards {
    grid-template-columns: 1fr;
  }
  
  .match-item {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .match-percentage {
    margin: 0;
  }
}
</style>