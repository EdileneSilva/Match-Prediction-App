<template>
  <div class="dashboard">
    <main class="main-content">
      <div v-if="error" class="error-message gsap-entrance">
        {{ error }}
      </div>

      <!-- Team Selection Container -->
      <div class="prediction-container gsap-entrance">
        <h1 class="page-title">Arena de Prédiction</h1>

        <div class="selection-section">
          <div class="team-selectors">
            <div class="form-group">
              <label for="team1">Équipe Domicile</label>
              <select id="team1" v-model="selectedTeam1" class="glow-input team-select">
                <option :value="null">Sélectionner équipe</option>
                <option v-for="team in teams" :key="team.id" :value="team">{{ team.name }}</option>
              </select>
            </div>

            <div class="vs-indicator">
              <span class="vs-text">VS</span>
            </div>

            <div class="form-group">
              <label for="team2">Équipe Extérieur</label>
              <select id="team2" v-model="selectedTeam2" class="glow-input team-select">
                <option :value="null">Sélectionner équipe</option>
                <option v-for="team in teams" :key="team.id" :value="team">{{ team.name }}</option>
              </select>
            </div>
          </div>

          <button class="predict-btn magnetic-btn" @click="launchPrediction"
            :disabled="!selectedTeam1 || !selectedTeam2 || isPredicting"
            :class="{ 'is-loading': isPredicting }">
            <span class="btn-text" v-if="!isPredicting">Lancer la prédiction IA</span>
            <div class="loader" v-else></div>
          </button>
        </div>
      </div>

      <!-- Prediction Results (Dynamic Reveal) -->
      <div v-if="predictionResult" class="results-container gsap-results">
        <h2 class="result-title">Résultats de l'analyse</h2>

        <div class="prediction-stats">
          <div class="stat-item">
            <span class="stat-label">Victoire {{ selectedTeam1?.name }}</span>
            <div class="progress-bar">
              <div class="progress" ref="barT1" :style="{ backgroundColor: getColor('t1') }"></div>
            </div>
            <span class="stat-value" ref="valT1" :style="{ color: getColor('t1') }">0%</span>
          </div>

          <div class="stat-item">
            <span class="stat-label">Match nul</span>
            <div class="progress-bar">
              <div class="progress" ref="barDraw" :style="{ backgroundColor: getColor('draw') }"></div>
            </div>
            <span class="stat-value" ref="valDraw" :style="{ color: getColor('draw') }">0%</span>
          </div>

          <div class="stat-item">
            <span class="stat-label">Victoire {{ selectedTeam2?.name }}</span>
            <div class="progress-bar">
              <div class="progress" ref="barT2" :style="{ backgroundColor: getColor('t2') }"></div>
            </div>
            <span class="stat-value" ref="valT2" :style="{ color: getColor('t2') }">0%</span>
          </div>
        </div>

        <div class="score-prediction">
          <span class="score-label">Score Probable :</span>
          <span class="score-value">{{ predictionResult.probableScore }}</span>
        </div>

        <button class="save-btn magnetic-btn" @click="savePrediction">
          <span class="btn-text">Enregistrer ce ticket</span>
        </button>
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
  async mounted() {
    try {
      this.teams = await apiClient.get('/predictions/teams')
    } catch (err) {
      this.error = "Impossible de charger les équipes"
    }

    this.ctx = gsap.context(() => {
      // Animation d'entrée du container de selection
      gsap.fromTo('.gsap-entrance',
        { y: 30, opacity: 0 },
        { y: 0, opacity: 1, duration: 1, ease: 'power3.out' }
      );
      this.initMagneticButtons();
    }, this.$el);
  },
  unmounted() {
    if (this.ctx) this.ctx.revert();
  },
  methods: {
    initMagneticButtons() {
      const btns = gsap.utils.toArray('.magnetic-btn');
      btns.forEach(btn => {
        const xTo = gsap.quickTo(btn, "x", {duration: 0.4, ease: "power3", duration: 0.4});
        const yTo = gsap.quickTo(btn, "y", {duration: 0.4, ease: "power3", duration: 0.4});
        
        btn.addEventListener('mousemove', (e) => {
          if (btn.disabled) return;
          const rect = btn.getBoundingClientRect();
          const x = (e.clientX - (rect.left + rect.width / 2)) * 0.3;
          const y = (e.clientY - (rect.top + rect.height / 2)) * 0.3;
          xTo(x); yTo(y);
        });
        
        btn.addEventListener('mouseleave', () => { xTo(0); yTo(0); });
      });
    },
    getColor(type) {
      const res = this.predictionResult;
      if (!res) return '#64748b';
      const max = Math.max(res.team1Win, res.draw, res.team2Win);

      if (type === 't1') {
        return (res.team1Win === max && max > 0) ? '#10b981' : '#ef4444'; // Green or Red
      }
      if (type === 't2') {
        return (res.team2Win === max && max > 0) ? '#10b981' : '#ef4444'; // Green or Red
      }
      if (type === 'draw') {
        return (res.draw === max && max > 0) ? '#f59e0b' : '#64748b'; // Yellow or Gray
      }
    },
    async launchPrediction() {
      if (!this.selectedTeam1 || !this.selectedTeam2) return;

      const btn = document.querySelector('.predict-btn');
      if (btn) gsap.to(btn, { scale: 0.95, duration: 0.1, yoyo: true, repeat: 1 });

      this.isPredicting = true;
      this.predictionResult = null;
      this.error = null;

      try {
        const response = await apiClient.post('/predictions/predict', {
          home_team_id: this.selectedTeam1.id,
          away_team_id: this.selectedTeam2.id,
          home_team_name: this.selectedTeam1.name,
          away_team_name: this.selectedTeam2.name
        });

        const cScore = response.confidence_score;
        this.predictionResult = {
          team1Win: response.predicted_result === 'HOME_WIN' ? cScore * 100 : (1 - cScore) * 50,
          draw: response.predicted_result === 'DRAW' ? cScore * 100 : (1 - cScore) * 20,
          team2Win: response.predicted_result === 'AWAY_WIN' ? cScore * 100 : (1 - cScore) * 30,
          probableScore: "N/A"
        };

        const total = this.predictionResult.team1Win + this.predictionResult.draw + this.predictionResult.team2Win;
        this.predictionResult.team1Win = Math.round((this.predictionResult.team1Win / total) * 100);
        this.predictionResult.draw = Math.round((this.predictionResult.draw / total) * 100);
        this.predictionResult.team2Win = 100 - this.predictionResult.team1Win - this.predictionResult.draw;

        await nextTick();
        this.initMagneticButtons(); // re-init since new buttons might exist
        this.animateResults();
      } catch (err) {
        this.error = err.message;
      } finally {
        this.isPredicting = false;
      }
    },
    animateResults() {
      // Extreme Wow Effect Reveal
      gsap.fromTo('.gsap-results', 
         { scale: 0.8, opacity: 0, y: 50 },
         { scale: 1, opacity: 1, y: 0, duration: 1.2, ease: 'elastic.out(1, 0.75)' }
      );

      const t1 = this.predictionResult.team1Win;
      const draw = this.predictionResult.draw;
      const t2 = this.predictionResult.team2Win;

      // Progress bar growing effect
      gsap.fromTo(this.$refs.barT1, { width: "0%" }, { width: `${t1}%`, duration: 2, ease: 'power4.out', delay: 0.3 });
      gsap.fromTo(this.$refs.barDraw, { width: "0%" }, { width: `${draw}%`, duration: 2, ease: 'power4.out', delay: 0.3 });
      gsap.fromTo(this.$refs.barT2, { width: "0%" }, { width: `${t2}%`, duration: 2, ease: 'power4.out', delay: 0.3 });

      // Count up numbers
      gsap.fromTo(this.$refs.valT1, { innerHTML: 0 }, { innerHTML: t1, roundProps: "innerHTML", duration: 2, ease: 'power3.out', delay: 0.3, onUpdate() { this.targets()[0].innerHTML += '%' } });
      gsap.fromTo(this.$refs.valDraw, { innerHTML: 0 }, { innerHTML: draw, roundProps: "innerHTML", duration: 2, ease: 'power3.out', delay: 0.3, onUpdate() { this.targets()[0].innerHTML += '%' } });
      gsap.fromTo(this.$refs.valT2, { innerHTML: 0 }, { innerHTML: t2, roundProps: "innerHTML", duration: 2, ease: 'power3.out', delay: 0.3, onUpdate() { this.targets()[0].innerHTML += '%' } });
      
      // Pulse background effect on the highest score
      const max = Math.max(t1, draw, t2);
      if (t1 === max) gsap.to(this.$refs.valT1, { scale: 1.2, duration: 0.5, yoyo: true, repeat: 1, delay: 2.2 });
      if (t2 === max) gsap.to(this.$refs.valT2, { scale: 1.2, duration: 0.5, yoyo: true, repeat: 1, delay: 2.2 });
      if (draw === max && draw > 0) gsap.to(this.$refs.valDraw, { scale: 1.2, duration: 0.5, yoyo: true, repeat: 1, delay: 2.2 });
    },
    savePrediction() {
      gsap.to('.save-btn', { scale: 0.95, duration: 0.1, yoyo: true, repeat: 1, onComplete: () => {
        this.$router.push('/history');
      }});
    }
  }
}
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  /* Premium Dark Glassmorphism */
  background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
  font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #f8fafc;
  padding-bottom: 3rem;
}

.main-content {
  padding: 2rem;
  max-width: 850px;
  margin: 0 auto;
}

/* Base Glassmorphism Container */
.prediction-container, .results-container {
  background: rgba(30, 41, 59, 0.5);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-radius: 20px;
  padding: 2.5rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.05);
  margin-bottom: 2rem;
  position: relative;
  overflow: hidden;
}

/* Ambient glow */
.results-container::before {
  content: '';
  position: absolute;
  top: -50%; left: -50%; width: 200%; height: 200%;
  background: radial-gradient(circle, rgba(99, 102, 241, 0.1) 0%, transparent 70%);
  z-index: -1;
  pointer-events: none;
}

.page-title {
  margin: 0 0 2rem 0;
  color: #f8fafc;
  font-size: 2.2rem;
  font-weight: 700;
  text-align: center;
  background: linear-gradient(135deg, #fff, #94a3b8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.result-title {
  margin: 0 0 2.5rem 0;
  color: #f8fafc;
  font-size: 1.8rem;
  font-weight: 700;
  text-align: center;
}

.error-message {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #fca5a5;
  padding: 1rem;
  border-radius: 12px;
  margin-bottom: 1.5rem;
  font-size: 1rem;
  text-align: center;
}

.selection-section {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.team-selectors {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
}

.form-group {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.form-group label {
  font-weight: 500;
  color: #cbd5e1;
  font-size: 1rem;
}

.glow-input {
  padding: 1rem 1.2rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.03);
  color: #f8fafc;
  cursor: pointer;
  appearance: none; /* Hide default dropdown arrow for custom styling */
}

.glow-input:focus {
  outline: none;
  border-color: #818cf8;
  background: rgba(255, 255, 255, 0.08);
  box-shadow: 0 0 20px rgba(99, 102, 241, 0.4);
}

.glow-input option {
  background: #1e293b;
  color: white;
}

.vs-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 1.5rem;
  width: 50px;
  height: 50px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 0 15px rgba(0,0,0,0.2);
}

.vs-text {
  font-weight: 800;
  color: #818cf8;
  font-size: 1.1rem;
}

/* Magnetic Buttons */
.magnetic-btn {
  position: relative;
  border: none;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  z-index: 1;
  overflow: hidden;
  transition: box-shadow 0.3s ease, opacity 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.magnetic-btn::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.2), transparent);
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: -1;
  border-radius: 12px;
}

.magnetic-btn:hover::before { opacity: 1; }

.predict-btn {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
  padding: 1.2rem;
  width: 100%;
  box-shadow: 0 8px 25px rgba(99, 102, 241, 0.3);
}

.predict-btn:hover:not(:disabled) {
  box-shadow: 0 12px 35px rgba(99, 102, 241, 0.5);
}

.predict-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: #475569;
  box-shadow: none;
}

.predict-btn.is-loading {
  cursor: wait;
}

.save-btn {
  width: 100%;
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  padding: 1.2rem;
  box-shadow: 0 8px 25px rgba(16, 185, 129, 0.3);
}

.save-btn:hover {
  box-shadow: 0 12px 35px rgba(16, 185, 129, 0.5);
}

.btn-text {
  display: inline-block;
  pointer-events: none;
}

/* Loader Animation */
.loader {
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top: 3px solid white;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Results Prediction Stats */
.prediction-stats {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  margin-bottom: 3rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.stat-label {
  flex: 0 0 180px;
  font-weight: 500;
  color: #e2e8f0;
  font-size: 1.1rem;
}

.stat-value {
  flex: 0 0 70px;
  font-weight: 800;
  font-size: 1.5rem;
  text-align: right;
  text-shadow: 0 0 10px currentColor; /* glow matches color */
}

.progress-bar {
  flex: 1;
  height: 12px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  overflow: hidden;
  box-shadow: inset 0 2px 4px rgba(0,0,0,0.3);
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.progress {
  height: 100%;
  border-radius: 10px;
  background-color: #64748b; /* overwritten dynamically */
  box-shadow: inset 0 -2px 4px rgba(0,0,0,0.2), 0 0 10px currentColor;
}

.score-prediction {
  text-align: center;
  margin-bottom: 3rem;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  display: flex;
  justify-content: center;
  align-items: baseline;
  gap: 1rem;
}

.score-label {
  color: #cbd5e1;
  font-size: 1.2rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.score-value {
  font-weight: 900;
  color: #f8fafc;
  font-size: 2rem;
  text-shadow: 0 0 15px rgba(255,255,255,0.4);
}

/* Responsive Design */
@media (max-width: 768px) {
  .team-selectors {
    flex-direction: column;
    gap: 1.5rem;
  }
  
  .vs-indicator {
    margin: 0;
  }
  
  .stat-item {
    flex-wrap: wrap;
    justify-content: space-between;
  }
  
  .stat-label {
    flex: 1 0 50%;
  }

  .stat-value {
    flex: 1 0 30%;
  }
  
  .progress-bar {
    flex: 0 0 100%;
    order: 3;
    margin-top: 0.5rem;
  }
}
</style>