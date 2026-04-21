<template>
  <div class="auth-container">
    <div class="decorative-player gsap-reveal-player">
      <img src="@/assets/neon-player.png" alt="Neon Soccer Player" />
    </div>
    <div class="auth-card">
      <div class="logo gsap-stagger">
        <img src="@/assets/logo.png" alt="Logo" class="logo-img" />
      </div>
      
      <h2 class="auth-title gsap-stagger">Inscription</h2>

      <div v-if="errorMessage" class="error-message gsap-stagger">
        {{ errorMessage }}
      </div>
      
      <form class="auth-form" @submit.prevent="handleRegister">
        <div class="form-group gsap-stagger">
          <label for="name">Nom complet</label>
          <input 
            type="text" 
            id="name" 
            v-model="name" 
            placeholder="Entrez votre nom complet"
            required
            class="glow-input"
          >
        </div>
        
        <div class="form-group gsap-stagger">
          <label for="email">Email</label>
          <input 
            type="email" 
            id="email" 
            v-model="email" 
            placeholder="Entrez votre email"
            required
            class="glow-input"
          >
        </div>
        
        <div class="form-group gsap-stagger">
          <label for="password">Mot de passe</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            placeholder="Entrez votre mot de passe"
            required
            class="glow-input"
          >
        </div>
        
        <div class="form-group gsap-stagger">
          <label for="confirmPassword">Confirmer le mot de passe</label>
          <input 
            type="password" 
            id="confirmPassword" 
            v-model="confirmPassword" 
            placeholder="Confirmez votre mot de passe"
            required
            class="glow-input"
          >
        </div>
        
        <div class="form-options gsap-stagger">
          <label class="checkbox-container">
            <input type="checkbox" v-model="agreeTerms">
            <span class="checkmark"></span>
            J'accepte les conditions d'utilisation
          </label>
        </div>
        
        <button type="submit" class="auth-btn gsap-stagger">Créer un compte</button>
      </form>
      
      <div class="auth-footer gsap-stagger">
        <span>Déjà un compte?</span>
        <router-link to="/login" class="login-link">Se connecter</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { apiClient } from '@/api/client'
import { gsap } from 'gsap'

export default {
  name: 'RegisterView',
  data() {
    return {
      name: '',
      email: '',
      password: '',
      confirmPassword: '',
      agreeTerms: false,
      errorMessage: ''
    }
  },
  mounted() {
    this.initGSAP()
    this.initMagneticButton()
  },
  methods: {
    initGSAP() {
      gsap.fromTo('.auth-card',
        { opacity: 0, scale: 0.9, y: 30 },
        { opacity: 1, scale: 1, y: 0, duration: 0.8, ease: 'back.out(1.2)' }
      )
      
      gsap.fromTo('.gsap-stagger', 
        { opacity: 0, x: -20 },
        { opacity: 1, x: 0, duration: 0.5, stagger: 0.1, ease: 'power2.out', delay: 0.2 }
      )

      gsap.fromTo('.gsap-reveal-player',
        { x: -100, opacity: 0, scale: 0.8 },
        { 
          x: 0, 
          opacity: 0.4, 
          scale: 1, 
          duration: 1.5, 
          ease: "power3.out",
          delay: 0.5
        }
      )
    },
    initMagneticButton() {
      const btn = document.querySelector('.auth-btn')
      if (!btn) return
      
      btn.addEventListener('mousemove', (e) => {
        const rect = btn.getBoundingClientRect()
        const x = e.clientX - rect.left - rect.width / 2
        const y = e.clientY - rect.top - rect.height / 2
        
        gsap.to(btn, {
          x: x * 0.3,
          y: y * 0.3,
          duration: 0.3,
          ease: 'power2.out'
        })
      })
      
      btn.addEventListener('mouseleave', () => {
        gsap.to(btn, { x: 0, y: 0, duration: 0.5, ease: 'elastic.out(1, 0.3)' })
      })
    },
    async handleRegister() {
      if (this.password !== this.confirmPassword) {
        this.errorMessage = 'Les mots de passe ne correspondent pas'
        return
      }
      
      if (!this.agreeTerms) {
        this.errorMessage = 'Vous devez accepter les conditions d\'utilisation'
        return
      }
      
      // Button click animation
      gsap.to('.auth-btn', { scale: 0.95, duration: 0.1, yoyo: true, repeat: 1 })
      
      try {
        await apiClient.post('/auth/register', {
          username: this.name, // Nom complet utilisé comme username pour l'instant
          email: this.email,
          password: this.password
        })
        
        this.$router.push('/login')
      } catch (error) {
        this.errorMessage = error.message
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
  background-image: linear-gradient(rgba(10, 10, 26, 0.4), rgba(10, 10, 26, 0.4)), url("@/assets/player1.jpg");
  background-size: cover;
  background-position: center;
}

.auth-container::before {
  content: '';
  position: absolute;
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(224, 38, 255, 0.15) 0%, transparent 70%);
  bottom: -150px;
  right: -150px;
  z-index: 0;
}

.decorative-player {
  position: absolute;
  left: -5%;
  top: -10%;
  width: 60%;
  max-width: 800px;
  z-index: 1;
  pointer-events: none;
  filter: blur(2px) brightness(0.8);
  opacity: 0.4;
  mask-image: radial-gradient(circle at center, black 30%, transparent 80%);
  -webkit-mask-image: radial-gradient(circle at center, black 30%, transparent 80%);
}

.decorative-player img {
  width: 100%;
  height: auto;
}

.auth-card {
  background: var(--glass-bg);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border-radius: 32px;
  padding: 3.5rem;
  width: 100%;
  max-width: 500px;
  box-shadow: var(--glass-shadow);
  border: 1px solid var(--glass-border);
  position: relative;
  z-index: 10;
}

.logo {
  margin-bottom: 2rem;
  text-align: center;
}

.auth-title {
  font-size: 2.5rem;
  font-weight: 800;
  text-align: center;
  margin-bottom: 2.5rem;
  background: var(--accent-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -1px;
}

.error-message {
  background: rgba(248, 113, 113, 0.1);
  border: 1px solid rgba(248, 113, 113, 0.2);
  color: #f87171;
  padding: 1rem;
  border-radius: 12px;
  margin-bottom: 2rem;
  font-size: 0.9rem;
  text-align: center;
  backdrop-filter: blur(10px);
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
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

.glow-input::placeholder {
  color: rgba(255, 255, 255, 0.3);
}

.glow-input:focus {
  outline: none;
  border-color: var(--accent-secondary);
  background: rgba(255, 255, 255, 0.08);
  box-shadow: 0 0 20px rgba(0, 212, 255, 0.2);
}

.form-options {
  margin-top: 0.5rem;
}

.checkbox-container {
  display: flex;
  align-items: flex-start;
  cursor: pointer;
  font-size: 0.9rem;
  color: var(--text-secondary);
  position: relative;
  line-height: 1.4;
  font-weight: 600;
}

.checkbox-container input {
  display: none;
}

.checkmark {
  width: 20px;
  height: 20px;
  border: 1px solid var(--glass-border);
  border-radius: 6px;
  margin-right: 12px;
  margin-top: 2px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  flex-shrink: 0;
  background: rgba(255, 255, 255, 0.05);
}

.checkbox-container input:checked ~ .checkmark {
  background: var(--accent-secondary);
  border-color: var(--accent-secondary);
  box-shadow: 0 0 10px rgba(0, 212, 255, 0.4);
}

.checkbox-container input:checked ~ .checkmark::after {
  content: 'L';
  transform: rotate(45deg) scaleX(-1);
  color: white;
  font-size: 12px;
  font-weight: 900;
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

.auth-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 15px 40px rgba(224, 38, 255, 0.5);
  filter: brightness(1.1);
}

.auth-footer {
  text-align: center;
  margin-top: 2.5rem;
  color: var(--text-secondary);
  font-size: 0.95rem;
  font-weight: 500;
}

.login-link {
  color: var(--accent-secondary);
  text-decoration: none;
  font-weight: 800;
  margin-left: 8px;
  transition: all 0.3s ease;
}

.login-link:hover {
  filter: brightness(1.2);
  text-shadow: 0 0 10px rgba(0, 212, 255, 0.4);
}

.logo-img {
  height: 3rem;
  width: auto;
  filter: drop-shadow(0 0 15px rgba(255, 255, 255, 0.2));
}

@media (max-width: 480px) {
  .auth-card {
    padding: 3rem 1.5rem;
  }
  
  .auth-title {
    font-size: 2rem;
  }
}

</style>