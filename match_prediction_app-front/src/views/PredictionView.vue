<template>
  <div class="dashboard">
    <main class="main-content">
      <div v-if="error" class="error-message gsap-entrance">
        {{ error }}
      </div>

      <!-- Team Selection Container -->
      <div v-if="!isPredicting && !predictionResult" class="prediction-container gsap-entrance">
        <h1 class="page-title">Arena de Prédiction</h1>

        <div class="selection-section">
          <div class="team-selectors">
            <div class="form-group team-card" :class="{ 'has-selection': selectedTeam1 }">
              <label for="team1">Domicile</label>
              <div class="select-wrapper-hero">
                <div class="logo-placeholder">
                  <img v-if="selectedTeam1?.logo_url" :src="selectedTeam1.logo_url" class="team-logo-giant" alt="">
                  <div v-else class="empty-logo">?</div>
                </div>
                <select id="team1" v-model="selectedTeam1" class="glow-input team-select">
                  <option :value="null">Choisir l'équipe</option>
                  <option v-for="team in teams" :key="team.id" :value="team">{{ team.name }}</option>
                </select>
              </div>
            </div>

            <div class="vs-indicator-hero">
              <div class="vs-ring"></div>
              <span class="vs-text">VS</span>
            </div>

            <div class="form-group team-card" :class="{ 'has-selection': selectedTeam2 }">
              <label for="team2">Extérieur</label>
              <div class="select-wrapper-hero">
                <div class="logo-placeholder">
                  <img v-if="selectedTeam2?.logo_url" :src="selectedTeam2.logo_url" class="team-logo-giant" alt="">
                  <div v-else class="empty-logo">?</div>
                </div>
                <select id="team2" v-model="selectedTeam2" class="glow-input team-select">
                  <option :value="null">Choisir l'équipe</option>
                  <option v-for="team in teams" :key="team.id" :value="team">{{ team.name }}</option>
                </select>
              </div>
            </div>
          </div>

          <div v-if="selectedTeam1 && selectedTeam2 && selectedTeam1.id === selectedTeam2.id" style="color: #ef4444; font-weight: bold; margin-bottom: 2rem; text-align: center;">
            <i class="fas fa-exclamation-triangle"></i> Veuillez choisir deux équipes différentes (pas de match contre soi-même).
          </div>
          <button class="predict-btn-hero magnetic-btn" @click="launchPrediction"
            :disabled="!selectedTeam1 || !selectedTeam2 || selectedTeam1?.id === selectedTeam2?.id">
            <span class="btn-text">Lancer l'Analyse IA</span>
          </button>
        </div>
      </div>

      <!-- AI Scanning Arena -->
      <div v-if="isPredicting" class="scanning-arena">
        <div class="scanning-content">
          <div class="scanning-logos">
            <img :src="selectedTeam1?.logo_url" class="scan-logo logo-left" alt="">
            <div class="scanning-ray"></div>
            <img :src="selectedTeam2?.logo_url" class="scan-logo logo-right" alt="">
          </div>
          <h2 class="scanning-title">Analyse Neuronale en cours...</h2>
          <div class="scanning-bar-container">
            <div class="scanning-bar-fill"></div>
          </div>
          <p class="scanning-subtitle">Traitement des statistiques et probabilités historiques</p>
        </div>
      </div>

      <!-- Prediction Results (Dramatic Reveal) -->
      <div v-if="predictionResult && !isPredicting" class="results-container gsap-results">
        <div class="winner-reveal">
          <h2 class="reveal-badge">Vainqueur Probable</h2>
          <div class="winner-logo-container">
             <div class="winner-glow"></div>
             <img v-if="winnerTeam.logo_url" :src="winnerTeam.logo_url" class="winner-logo-reveal" alt="">
             <div v-else class="draw-icon">🤝</div>
          </div>
          <h3 class="winner-name">{{ winnerTeam.name }}</h3>
        </div>

        <div class="prediction-stats-grid">
          <div class="stat-card">
            <span class="stat-label">Victoire {{ selectedTeam1?.name }}</span>
            <div class="progress-bar-hero">
              <div class="progress-fill" ref="barT1" :style="{ backgroundColor: getColor('t1') }"></div>
            </div>
            <span class="stat-value-hero" ref="valT1" :style="{ color: getColor('t1') }">0%</span>
          </div>

          <div class="stat-card">
            <span class="stat-label">Match Nul</span>
            <div class="progress-bar-hero">
              <div class="progress-fill" ref="barDraw" :style="{ backgroundColor: getColor('draw') }"></div>
            </div>
            <span class="stat-value-hero" ref="valDraw" :style="{ color: getColor('draw') }">0%</span>
          </div>

          <div class="stat-card">
            <span class="stat-label">Victoire {{ selectedTeam2?.name }}</span>
            <div class="progress-bar-hero">
              <div class="progress-fill" ref="barT2" :style="{ backgroundColor: getColor('t2') }"></div>
            </div>
            <span class="stat-value-hero" ref="valT2" :style="{ color: getColor('t2') }">0%</span>
          </div>
        </div>

        <div class="actions-group">
          <button class="save-btn-hero magnetic-btn" @click="savePrediction">
            <span class="btn-text">Enregistrer la Prédiction</span>
          </button>
          <button class="reset-btn" @click="resetArena">
            Nouvelle Analyse
          </button>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { apiClient } from '@/api/client'
import { nextTick } from 'vue'
import gsap from 'gsap'

export default {
  name: 'PredictionView',
  data() {
    return {
      selectedTeam1: null,
      selectedTeam2: null,
      isPredicting: false,
      predictionResult: null,
      teams: [],
      error: null,
      ctx: null
    }
  },
  computed: {
    winnerTeam() {
      if (!this.predictionResult) return null;
      const { team1Win, draw, team2Win } = this.predictionResult;
      const max = Math.max(team1Win, draw, team2Win);
      
      if (draw === max && draw > team1Win && draw > team2Win) {
         return { name: 'Match Nul', logo_url: null };
      }
      if (team1Win >= team2Win && team1Win >= draw) return this.selectedTeam1;
      return this.selectedTeam2;
    }
  },
  async mounted() {
    try {
      this.teams = await apiClient.get('/teams')
    } catch (err) {
      this.error = "Impossible de charger les équipes"
    }

    this.ctx = gsap.context(() => {
      this.animateEntrance();
      this.initMagneticButtons();
    }, this.$el);

    // Auto-fill and auto-predict from Dashboard queries
    const qHome = this.$route.query.home;
    const qAway = this.$route.query.away;
    if (qHome && qAway && this.teams.length > 0) {
      // Fuzzy matching to link LFP names with local DB names
      const findTeam = (name) => {
        const lowerName = name.toLowerCase().replace(/ fc| olympique| stade| asc| as /g, '');
        return this.teams.find(t => t.name.toLowerCase().includes(lowerName) || lowerName.includes(t.name.toLowerCase()));
      };
      
      this.selectedTeam1 = findTeam(qHome) || this.teams[0];
      this.selectedTeam2 = findTeam(qAway) || this.teams[1];
      
      // Lancer directement l'analyse !
      this.$nextTick(() => {
         this.launchPrediction();
      });
    }
  },
  unmounted() {
    if (this.ctx) this.ctx.revert();
  },
  methods: {
    animateEntrance() {
      gsap.fromTo('.gsap-entrance',
        { y: 60, opacity: 0, scale: 0.9 },
        { y: 0, opacity: 1, scale: 1, duration: 1.2, ease: 'expo.out' }
      );
    },
    initMagneticButtons() {
      const btns = gsap.utils.toArray('.magnetic-btn');
      btns.forEach(btn => {
        const xTo = gsap.quickTo(btn, "x", {duration: 0.4, ease: "power3"});
        const yTo = gsap.quickTo(btn, "y", {duration: 0.4, ease: "power3"});
        
        btn.addEventListener('mousemove', (e) => {
          if (btn.disabled) return;
          const rect = btn.getBoundingClientRect();
          const x = (e.clientX - (rect.left + rect.width / 2)) * 0.35;
          const y = (e.clientY - (rect.top + rect.height / 2)) * 0.35;
          xTo(x); yTo(y);
        });
        
        btn.addEventListener('mouseleave', () => { xTo(0); yTo(0); });
      });
    },
    getColor(type) {
      const res = this.predictionResult;
      if (!res) return '#64748b';
      const max = Math.max(res.team1Win, res.draw, res.team2Win);

      if (type === 't1') return (res.team1Win === max) ? 'var(--accent-primary)' : '#475569';
      if (type === 't2') return (res.team2Win === max) ? 'var(--accent-secondary)' : '#475569';
      if (type === 'draw') return (res.draw === max) ? '#f59e0b' : '#334155';
    },
    async launchPrediction() {
      if (!this.selectedTeam1 || !this.selectedTeam2) return;

      this.isPredicting = true;
      this.predictionResult = null;
      this.error = null;

      // Start scanning animation
      await nextTick();
      this.animateScanning();

      try {
        const response = await apiClient.post('/predict', {
          home_team: this.selectedTeam1.name,
          away_team: this.selectedTeam2.name,
          season: 2025
        });

        // Synthetic delay for "Analysis" feel
        await new Promise(resolve => setTimeout(resolve, 3000));

        const cScore = response.confidence_score;
        this.predictionResult = {
          team1Win: response.predicted_result === 'HOME_WIN' ? cScore * 100 : (1 - cScore) * 50,
          draw: response.predicted_result === 'DRAW' ? cScore * 100 : (1 - cScore) * 20,
          team2Win: response.predicted_result === 'AWAY_WIN' ? cScore * 100 : (1 - cScore) * 30
        };

        const total = this.predictionResult.team1Win + this.predictionResult.draw + this.predictionResult.team2Win;
        this.predictionResult.team1Win = Math.round((this.predictionResult.team1Win / total) * 100);
        this.predictionResult.draw = Math.round((this.predictionResult.draw / total) * 100);
        this.predictionResult.team2Win = 100 - this.predictionResult.team1Win - this.predictionResult.draw;

        this.isPredicting = false;
        await nextTick();
        this.animateResults();
      } catch (err) {
        this.error = err.message;
        this.isPredicting = false;
      }
    },
    animateScanning() {
      gsap.fromTo('.scanning-logos', { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.8 });
      gsap.to('.scanning-ray', { left: '100%', duration: 1.5, repeat: -1, yoyo: true, ease: 'sine.inOut' });
      gsap.to('.scan-logo', { filter: 'brightness(1.5)', duration: 0.5, repeat: -1, yoyo: true });
    },
    animateResults() {
      const tl = gsap.timeline();
      
      tl.fromTo('.winner-reveal', 
        { scale: 0, opacity: 0, rotate: -10 },
        { scale: 1, opacity: 1, rotate: 0, duration: 1, ease: 'back.out(1.7)' }
      );

      tl.fromTo('.winner-glow', 
        { opacity: 0, scale: 0.5 },
        { opacity: 1, scale: 1, duration: 1, repeat: -1, yoyo: true },
        "-=0.5"
      );

      tl.fromTo('.stat-card', 
        { x: -30, opacity: 0 },
        { x: 0, opacity: 1, duration: 0.6, stagger: 0.2, ease: 'power2.out' },
        "-=0.4"
      );

      // Progress bars
      const t1 = this.predictionResult.team1Win;
      const draw = this.predictionResult.draw;
      const t2 = this.predictionResult.team2Win;

      tl.fromTo(this.$refs.barT1, { width: "0%" }, { width: `${t1}%`, duration: 1.5, ease: 'power4.out' }, "-=0.5");
      tl.fromTo(this.$refs.barDraw, { width: "0%" }, { width: `${draw}%`, duration: 1.5, ease: 'power4.out' }, "-=1.3");
      tl.fromTo(this.$refs.barT2, { width: "0%" }, { width: `${t2}%`, duration: 1.5, ease: 'power4.out' }, "-=1.3");

      // Numbers
      tl.fromTo(this.$refs.valT1, { innerHTML: 0 }, { innerHTML: t1, roundProps: "innerHTML", duration: 1.5, onUpdate() { this.targets()[0].innerHTML += '%' } }, "-=1.5");
      tl.fromTo(this.$refs.valDraw, { innerHTML: 0 }, { innerHTML: draw, roundProps: "innerHTML", duration: 1.5, onUpdate() { this.targets()[0].innerHTML += '%' } }, "-=1.5");
      tl.fromTo(this.$refs.valT2, { innerHTML: 0 }, { innerHTML: t2, roundProps: "innerHTML", duration: 1.5, onUpdate() { this.targets()[0].innerHTML += '%' } }, "-=1.5");
    },
    resetArena() {
      this.predictionResult = null;
      this.selectedTeam1 = null;
      this.selectedTeam2 = null;
      nextTick(() => this.animateEntrance());
    },
    savePrediction() {
      this.$router.push('/history');
    }
  }
}
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background-image: linear-gradient(rgba(10, 10, 26, 0.7), rgba(10, 10, 26, 0.9)), url("@/assets/ballon3.jpg");
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  display: flex;
  align-items: center;
  justify-content: center;
}

.main-content {
  width: 100%;
  max-width: 1100px;
  padding: 140px 2rem 60px;
  margin: 0 auto;
}

/* Prediction Container */
.prediction-container, .results-container, .scanning-arena {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(25px);
  -webkit-backdrop-filter: blur(25px);
  border-radius: 32px;
  padding: 4rem;
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 40px 100px rgba(0, 0, 0, 0.5), inset 0 0 80px rgba(255, 255, 255, 0.02);
}

.page-title {
  font-size: 3.5rem;
  font-weight: 900;
  text-align: center;
  margin-bottom: 4rem;
  background: linear-gradient(to right, #fff, var(--accent-secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -2px;
}

.team-selectors {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 3rem;
  margin-bottom: 4rem;
}

.team-card {
  flex: 1;
  background: rgba(255, 255, 255, 0.02);
  padding: 2.5rem;
  border-radius: 24px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.team-card.has-selection {
  background: rgba(255, 255, 255, 0.05);
  border-color: var(--accent-secondary);
  box-shadow: 0 20px 40px rgba(0, 212, 255, 0.1);
}

.team-card label {
  display: block;
  text-align: center;
  margin-bottom: 2rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 3px;
  color: var(--text-secondary);
  font-size: 0.8rem;
}

.select-wrapper-hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
}

.logo-placeholder {
  width: 140px;
  height: 140px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px dashed rgba(255, 255, 255, 0.1);
  position: relative;
}

.team-logo-giant {
  width: 90px;
  height: 90px;
  object-fit: contain;
  filter: drop-shadow(0 0 20px rgba(0, 212, 255, 0.4));
}

.empty-logo {
  font-size: 3rem;
  font-weight: 900;
  color: rgba(255, 255, 255, 0.1);
}

.glow-input {
  width: 100%;
  padding: 1.2rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: white;
  font-weight: 700;
  text-align: center;
}

/* VS Indicator */
.vs-indicator-hero {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100px;
  height: 100px;
}

.vs-ring {
  position: absolute;
  width: 80px;
  height: 80px;
  border: 2px solid var(--accent-secondary);
  border-radius: 50%;
  animation: pulseVS 2s infinite;
}

@keyframes pulseVS {
  0% { transform: scale(1); opacity: 0.8; }
  100% { transform: scale(1.5); opacity: 0; }
}

.vs-text {
  font-size: 2rem;
  font-weight: 950;
  color: var(--accent-secondary);
  font-style: italic;
  z-index: 2;
  text-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
}

.predict-btn-hero {
  width: 100%;
  padding: 2rem;
  background: var(--accent-gradient);
  border: none;
  border-radius: 20px;
  color: white;
  font-size: 1.5rem;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 2px;
  cursor: pointer;
  box-shadow: 0 20px 50px rgba(224, 38, 255, 0.3);
}

.predict-btn-hero:disabled {
  opacity: 0.3;
  cursor: not-allowed;
  filter: grayscale(1);
}

/* Scanning Arena */
.scanning-arena {
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

.scanning-logos {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4rem;
  position: relative;
  height: 200px;
}

.scan-logo {
  width: 120px;
  height: 120px;
  object-fit: contain;
}

.scanning-ray {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  width: 4px;
  background: var(--accent-secondary);
  box-shadow: 0 0 30px var(--accent-secondary), 0 0 60px var(--accent-secondary);
  height: 100%;
}

.scanning-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: white;
}

.scanning-bar-container {
  width: 100%;
  height: 8px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
  overflow: hidden;
}

.scanning-bar-fill {
  width: 40%;
  height: 100%;
  background: var(--accent-gradient);
  animation: moveScanBar 2s infinite ease-in-out;
}

@keyframes moveScanBar {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(300%); }
}

/* Results Reveal */
.winner-reveal {
  text-align: center;
  margin-bottom: 4rem;
}

.reveal-badge {
  display: inline-block;
  padding: 0.5rem 2rem;
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
  border: 1px solid #10b981;
  border-radius: 50px;
  font-weight: 800;
  text-transform: uppercase;
  margin-bottom: 2rem;
}

.winner-logo-container {
  position: relative;
  display: flex;
  justify-content: center;
  margin-bottom: 2rem;
}

.winner-logo-reveal {
  width: 180px;
  height: 180px;
  object-fit: contain;
  filter: drop-shadow(0 0 40px rgba(16, 185, 129, 0.5));
  z-index: 2;
}

.draw-icon {
  font-size: 8rem;
  z-index: 2;
}

.winner-glow {
  position: absolute;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(16, 185, 129, 0.2) 0%, transparent 70%);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.winner-name {
  font-size: 3rem;
  font-weight: 900;
  color: white;
}

.prediction-stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  margin-bottom: 4rem;
}

.stat-card {
  background: rgba(255, 255, 255, 0.03);
  padding: 2rem;
  border-radius: 20px;
  text-align: center;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.stat-label {
  display: block;
  font-weight: 700;
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin-bottom: 1.5rem;
}

.stat-value-hero {
  display: block;
  font-size: 2.5rem;
  font-weight: 900;
  margin-top: 1rem;
}

.progress-bar-hero {
  height: 10px;
  background: rgba(0,0,0,0.3);
  border-radius: 5px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
}

.actions-group {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.save-btn-hero {
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  color: white;
  font-weight: 800;
  cursor: pointer;
}

.reset-btn {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: var(--text-secondary);
  border-radius: 16px;
  font-weight: 700;
  cursor: pointer;
}

@media (max-width: 768px) {
  .team-selectors {
    flex-direction: column;
    align-items: center;
  }
  .prediction-stats-grid {
    grid-template-columns: 1fr;
  }
  .actions-group {
    grid-template-columns: 1fr;
  }
  .page-title {
    font-size: 2.5rem;
  }
  .winner-logo-reveal {
    width: 120px;
    height: 120px;
  }
}

</style>