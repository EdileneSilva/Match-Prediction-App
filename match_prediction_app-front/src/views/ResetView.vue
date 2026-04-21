<template>
  <div class="auth-container">
    <div class="auth-box">
      <h1 class="auth-title gsap-reveal">Nouveau mot de passe</h1>
      <p class="auth-subtitle gsap-reveal">Saisissez votre nouveau mot de passe.</p>
      
      <form @submit.prevent="handleReset" class="auth-form gsap-reveal">
        <div class="form-group">
          <label for="password">Nouveau mot de passe</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            placeholder="••••••••" 
            required
            class="glow-input"
          >
        </div>
        
        <div class="form-group">
          <label for="confirmPassword">Confirmer le mot de passe</label>
          <input 
            type="password" 
            id="confirmPassword" 
            v-model="confirmPassword" 
            placeholder="••••••••" 
            required
            class="glow-input"
          >
        </div>
        
        <div v-if="message" class="success-message">{{ message }}</div>
        <div v-if="error" class="error-message">{{ error }}</div>
        
        <button type="submit" class="auth-btn" :disabled="isLoading">
          {{ isLoading ? 'Réinitialisation...' : 'Changer le mot de passe' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import { apiClient } from '@/api/client'
import { gsap } from 'gsap'

export default {
  name: 'ResetView',
  data() {
    return {
      password: '',
      confirmPassword: '',
      token: '',
      message: '',
      error: '',
      isLoading: false
    }
  },
  mounted() {
    this.token = this.$route.query.token
    if (!this.token) {
      this.error = "Token manquant dans l'URL"
    }
    
    gsap.fromTo('.auth-box',
      { opacity: 0, scale: 0.95, y: 20 },
      { opacity: 1, scale: 1, y: 0, duration: 0.6, ease: 'power3.out' }
    )
    gsap.fromTo('.gsap-reveal',
      { opacity: 0, y: 10 },
      { opacity: 1, y: 0, duration: 0.4, stagger: 0.1, delay: 0.2, ease: 'power2.out' }
    )
  },
  methods: {
    async handleReset() {
      if (this.password !== this.confirmPassword) {
        this.error = "Les mots de passe ne correspondent pas"
        return
      }
      
      this.isLoading = true
      this.message = ''
      this.error = ''
      try {
        await apiClient.post('/auth/reset-password', { 
          token: this.token,
          new_password: this.password 
        })
        this.message = "Mot de passe réinitialisé ! Redirection vers la connexion..."
        setTimeout(() => {
          this.$router.push('/login')
        }, 2000)
      } catch (err) {
        this.error = err.message || "Une erreur est survenue"
      } finally {
        this.isLoading = false
      }
    }
  }
}
</script>

<style scoped>
/* Same styles as ForgotView */
.auth-container {
  min-height: 100vh;
  background: var(--bg-cosmic);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Inter', sans-serif;
  padding: 2rem;
  overflow: hidden;
  position: relative;
}

.auth-container::before {
  content: '';
  position: absolute;
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(224, 38, 255, 0.1) 0%, transparent 70%);
  top: -150px;
  right: -150px;
  z-index: 0;
}

.auth-box {
  background: var(--glass-bg);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  padding: 3.5rem;
  border-radius: 32px;
  box-shadow: var(--glass-shadow);
  border: 1px solid var(--glass-border);
  width: 100%;
  max-width: 480px;
  position: relative;
  z-index: 10;
}

.auth-title {
  font-size: 2.2rem;
  font-weight: 800;
  text-align: center;
  margin-bottom: 1rem;
  background: var(--accent-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -1px;
}

.auth-subtitle {
  color: var(--text-secondary);
  text-align: center;
  margin-bottom: 2.5rem;
  font-size: 0.95rem;
  font-weight: 500;
  line-height: 1.6;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.8rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.form-group label {
  font-weight: 700;
  color: var(--text-secondary);
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.glow-input {
  padding: 1.1rem 1.4rem;
  border: 1px solid var(--glass-border);
  border-radius: 16px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.03);
  color: var(--text-primary);
  font-weight: 500;
}

.glow-input:focus {
  outline: none;
  border-color: var(--accent-secondary);
  background: rgba(255, 255, 255, 0.08);
  box-shadow: 0 0 20px rgba(0, 212, 255, 0.2);
}

.auth-btn {
  background: var(--accent-gradient);
  color: white;
  border: none;
  padding: 1.2rem;
  border-radius: 16px;
  font-size: 1.1rem;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 1rem;
  box-shadow: 0 10px 30px rgba(224, 38, 255, 0.3);
  text-transform: uppercase;
  letter-spacing: 1px;
}

.auth-btn:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 15px 40px rgba(224, 38, 255, 0.5);
  filter: brightness(1.1);
}

.auth-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: #334155;
  box-shadow: none;
}

.success-message {
  color: var(--accent-secondary);
  background: rgba(0, 212, 255, 0.05);
  border: 1px solid rgba(0, 212, 255, 0.2);
  padding: 1rem;
  border-radius: 12px;
  font-size: 0.95rem;
  text-align: center;
  backdrop-filter: blur(10px);
}

.error-message {
  color: #f87171;
  background: rgba(248, 113, 113, 0.05);
  border: 1px solid rgba(248, 113, 113, 0.2);
  padding: 1rem;
  border-radius: 12px;
  font-size: 0.95rem;
  text-align: center;
  backdrop-filter: blur(10px);
}

</style>
