<template>
  <div class="auth-container">
    <div class="auth-box">
      <h1 class="auth-title gsap-reveal">Mot de passe oublié</h1>
      <p class="auth-subtitle gsap-reveal">Saisissez votre email pour recevoir un lien de réinitialisation (simulé dans la console).</p>
      
      <form @submit.prevent="handleForgot" class="auth-form gsap-reveal">
        <div class="form-group">
          <label for="email">Email</label>
          <input 
            type="email" 
            id="email" 
            v-model="email" 
            placeholder="votre@email.com" 
            required
            class="glow-input"
          >
        </div>
        
        <div v-if="message" class="success-message">{{ message }}</div>
        <div v-if="error" class="error-message">{{ error }}</div>
        
        <button type="submit" class="auth-btn" :disabled="isLoading">
          {{ isLoading ? 'Envoi...' : 'Envoyer le lien' }}
        </button>
      </form>
      
      <div class="auth-footer gsap-reveal">
        <router-link to="/login" class="footer-link">Retour à la connexion</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { apiClient } from '@/api/client'
import { gsap } from 'gsap'

export default {
  name: 'ForgotView',
  data() {
    return {
      email: '',
      message: '',
      error: '',
      isLoading: false
    }
  },
  mounted() {
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
    async handleForgot() {
      this.isLoading = true
      this.message = ''
      this.error = ''
      try {
        const response = await apiClient.post('/auth/forgot-password', { email: this.email })
        this.message = response.message
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
  background: radial-gradient(circle, rgba(0, 212, 255, 0.15) 0%, transparent 70%);
  top: -150px;
  left: -150px;
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

.auth-footer {
  margin-top: 2.5rem;
  text-align: center;
}

.footer-link {
  color: var(--accent-secondary);
  text-decoration: none;
  font-size: 0.95rem;
  font-weight: 800;
  transition: all 0.3s ease;
}

.footer-link:hover {
  filter: brightness(1.2);
  text-shadow: 0 0 10px rgba(0, 212, 255, 0.4);
}

</style>
