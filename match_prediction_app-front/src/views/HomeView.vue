<template>
  <div class="dashboard">
    <!-- Main Content -->
    <main class="main-content">
      <!-- 2025/2026 Season Selection -->
      <section class="season-highlight gsap-list">
        <div class="season-badge">{{ pageTitle }}</div>
        <h1>Prédisez le <span class="text-highlight">Futur du Football</span></h1>
        <p class="subtitle">Analyse IA avancée pour la nouvelle saison. Plongez au cœur du championnat de Ligue 1.</p>
      </section>

      <div class="dashboard-grid">
        <!-- Matches Section -->
        <section class="matches-section gsap-list">
          <div class="section-header">
            <h2>{{ roundName }}</h2>
            <button @click="refreshData" class="refresh-btn magnetic-btn" :class="{ 'rotating': isRefreshing }" title="Actualiser les données">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 2v6h-6"></path><path d="M3 12a9 9 0 0 1 15-6.7L21 8"></path><path d="M3 22v-6h6"></path><path d="M21 12a9 9 0 0 1-15 6.7L3 16"></path></svg>
            </button>
          </div>
          
          <div class="matches-list" v-if="isLoading">
            <div class="skeleton-match match-item" v-for="i in 5" :key="'skel'+i">
              <div class="skeleton-text">Connexion à la LFP... Chargement IA en cours...</div>
            </div>
          </div>
          
          <div class="matches-list scrollable-list" v-else>
            <!-- Dynamic LIVE Matches -->
            <div 
              v-for="(match, index) in upcomingMatches" 
              :key="match.fixture_id || index"
              class="match-item" 
              :class="{ 'derby-highlight': match.is_derby || index === 0 }"
            >
              <div class="match-info">
                <span class="derby-tag" v-if="match.is_derby">LE CHOC</span>
                <span class="derby-tag" v-else-if="match.tag">{{ match.tag }}</span>
                <div class="match-teams">
                  <div class="team">
                    <img :src="match.home_team.logo" :alt="match.home_team.name" class="team-logo" />
                    <span class="team-name">{{ match.home_team.name.replace(/ Stade | Olympique | FC | ASC /g, ' ') }}</span>
                  </div>
                  <span class="vs-text">vs</span>
                  <div class="team">
                    <img :src="match.away_team.logo" :alt="match.away_team.name" class="team-logo" />
                    <span class="team-name">{{ match.away_team.name.replace(/ Stade | Olympique | FC | ASC /g, ' ') }}</span>
                  </div>
                </div>
              </div>
              <div class="match-meta">
                <button @click="analyze(match)" class="view-btn magnetic-btn">Analyser</button>
              </div>
            </div>
            
            <div v-if="upcomingMatches.length === 0" class="no-matches text-center">
              <p>Aucun match programmé pour le moment.</p>
            </div>
          </div>

          <div class="cta-container">
            <router-link to="/predictions" class="cta-btn secondary">Simulateur Manuel</router-link>
          </div>
        </section>

        <!-- Ranking Section -->
        <section class="ranking-section gsap-list">
          <LeagueTable :standings="standings" />
        </section>
      </div>
    </main>
  </div>
</template>

<script>
import gsap from 'gsap'
import { apiClient } from '@/api/client'
import LeagueTable from '@/components/dashboard/LeagueTable.vue'

export default {
  name: 'HomeView',
  components: {
    LeagueTable
  },
  data() {
    return {
      ctx: null,
      magneticElements: [],
      upcomingMatches: [],
      standings: [],
      isLoading: true,
      isRefreshing: false,
      roundName: "Prochaines Rencontres",
      pageTitle: "Ligue 1 McDonald's",
    }
  },
  async mounted() {
    await this.fetchData();
  },
  unmounted() {
    if (this.ctx) {
      this.ctx.revert();
    }
    // Nettoyer les event listeners
    this.magneticElements.forEach(item => {
      item.el.removeEventListener('mousemove', item.move);
      item.el.removeEventListener('mouseleave', item.leave);
    });
  },
  methods: {
    async fetchData() {
      this.isLoading = true;
      try {
        const [matchesData, standingsData] = await Promise.all([
          apiClient.get('/dashboard/upcoming'),
          apiClient.get('/dashboard/standings')
        ]);
        
        this.upcomingMatches = matchesData.matches || [];
        this.roundName = matchesData.round_name || "Prochaines Rencontres";
        this.pageTitle = matchesData.dates || "Ligue 1";
        this.standings = standingsData.data || [];
      } catch (err) {
        console.error("Impossible de récupérer les datas Dashboard API: ", err);
      } finally {
        this.isLoading = false;
        this.$nextTick(() => {
          this.setupAnimations();
        });
      }
    },
    async refreshData() {
      if (this.isRefreshing) return;
      this.isRefreshing = true;
      
      // Petit feedback visuel immédiat
      gsap.to('.refresh-btn svg', { rotate: "+=360", duration: 0.8, ease: "power2.inOut" });
      
      await this.fetchData();
      
      setTimeout(() => {
        this.isRefreshing = false;
        // Animation de succès
        gsap.fromTo('.dashboard-grid', 
          { filter: 'brightness(1.5)' }, 
          { filter: 'brightness(1)', duration: 0.5 }
        );
      }, 500);
    },
    analyze(match) {
      this.$router.push({
        path: '/predictions',
        query: {
          home: match.home_team.name,
          away: match.away_team.name
        }
      });
    },
    setupAnimations() {
       if (this.ctx) this.ctx.revert();
       
       this.ctx = gsap.context(() => {
         // Entrée de la page principale dynamique
         gsap.fromTo('.main-content',
           { y: -20, opacity: 0 },
           { y: 0, opacity: 1, duration: 0.8, ease: "power3.out" }
         );

         // Animation plus douce pour les sections
         gsap.fromTo('.gsap-list',
           { y: 30, opacity: 0 },
           { y: 0, opacity: 1, duration: 0.8, ease: "power2.out", stagger: 0.15 }
         );

         // Simple setup des boutons magnétiques
         this.magneticElements = [];
         const btns = gsap.utils.toArray('.magnetic-btn');
         btns.forEach(btn => {
           const xTo = gsap.quickTo(btn, "x", {duration: 0.4, ease: "power3"});
           const yTo = gsap.quickTo(btn, "y", {duration: 0.4, ease: "power3"});
           
           const mouseMove = (e) => {
             const rect = btn.getBoundingClientRect();
             const x = (e.clientX - (rect.left + rect.width / 2)) * 0.3;
             const y = (e.clientY - (rect.top + rect.height / 2)) * 0.3;
             xTo(x);
             yTo(y);
           };
           
           const mouseLeave = () => {
             xTo(0);
             yTo(0);
           };

           btn.addEventListener('mousemove', mouseMove);
           btn.addEventListener('mouseleave', mouseLeave);

           this.magneticElements.push({ el: btn, move: mouseMove, leave: mouseLeave });
         });
       }, this.$el);
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding-bottom: 2rem;
  background-image: linear-gradient(rgba(10, 10, 26, 0.4), rgba(10, 10, 26, 0.6)), url("@/assets/stadium2.jpg");
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
}

/* Header & Refresh */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.refresh-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--glass-border);
  color: var(--text-secondary);
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.refresh-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: var(--accent-secondary);
  border-color: var(--accent-secondary);
}

.refresh-btn.rotating svg {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Dashboard Grid */
.dashboard-grid {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 2rem;
  align-items: start;
}

/* Matches Section */
.matches-section {
  background: var(--glass-bg);
  border-radius: 24px;
  padding: 2.2rem;
  box-shadow: var(--glass-shadow);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid var(--glass-border);
}

.matches-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.scrollable-list {
  padding-right: 0.5rem;
}

.scrollable-list::-webkit-scrollbar {
  width: 5px;
}

.scrollable-list::-webkit-scrollbar-track {
  background: transparent;
}

.scrollable-list::-webkit-scrollbar-thumb {
  background: rgba(224, 38, 255, 0.2);
  border-radius: 10px;
}

.match-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 16px;
  border: 1px solid var(--glass-border);
  transition: all 0.3s ease;
}

.match-item:hover {
  background: var(--glass-hover);
  border-color: var(--accent-secondary);
  transform: scale(1.005) translateX(3px);
  box-shadow: 0 4px 15px rgba(0, 212, 255, 0.1);
}

.match-teams {
  display: flex;
  gap: 1.2rem;
  align-items: center;
  font-weight: 500;
  color: var(--text-primary);
  font-size: 1.1rem;
}

.team-logo {
  width: 32px;
  height: 32px;
  object-fit: contain;
}

.team-name {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 140px;
}

/* Analyser button */
.view-btn {
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
  color: #fff;
  border: none;
  padding: 0.7rem 1.6rem;
  border-radius: 10px;
  font-weight: 700;
  font-size: 0.9rem;
  letter-spacing: 0.03em;
  cursor: pointer;
  position: relative;
  z-index: 1;
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  box-shadow: 0 4px 15px rgba(224, 38, 255, 0.25), inset 0 1px 0 rgba(255,255,255,0.15);
  transition: all 0.3s ease;
}

.view-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 212, 255, 0.4), inset 0 1px 0 rgba(255,255,255,0.2);
  filter: brightness(1.1);
}

/* Responsive Design */
@media (max-width: 1100px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .main-content {
    padding: 100px 1rem 2rem;
  }

  .match-item {
    padding: 1.2rem;
  }
  
  .match-teams {
    font-size: 1rem;
    gap: 0.8rem;
  }

  .team-name {
    max-width: 100px;
  }
  
  .match-meta {
    gap: 1rem;
  }
  
  .view-btn {
    padding: 0.6rem 1.2rem;
    font-size: 0.8rem;
  }
}
</style>
