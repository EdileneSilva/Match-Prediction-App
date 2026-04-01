<template>
  <div class="auth-container">
    <div class="decorative-player gsap-reveal-player">
      <img src="@/assets/neon-player.png" alt="Neon Soccer Player" />
    </div>
    <div class="auth-card" ref="authCard">
      <div class="logo gsap-stagger">
        <img src="@/assets/logo.png" alt="Logo" class="logo-img" />
      </div>
      
      <h2 class="auth-title gsap-stagger">Connexion</h2>

      <div v-if="errorMessage" class="error-message gsap-stagger">
        {{ errorMessage }}
      </div>
      
      <form class="auth-form" @submit.prevent="handleLogin">
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
        
        <div class="form-options gsap-stagger">
          <label class="checkbox-container">
            <input type="checkbox" v-model="rememberMe">
            <span class="checkmark"></span>
            Se souvenir de moi
          </label>
          
          <router-link to="/forgot-password" class="forgot-password">Mot de passe oublié ?</router-link>
        </div>
        
        <button 
          type="submit" 
          class="auth-btn gsap-stagger magnetic-btn"
          ref="magneticBtn"
          @mousemove="handleMagneticMove"
          @mouseleave="handleMagneticLeave"
        >
          <span class="btn-text" ref="btnText">Se connecter</span>
        </button>
      </form>
      
      <div class="auth-footer gsap-stagger">
        <span>Pas de compte?</span>
        <router-link to="/register" class="register-link">Créer un compte</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { apiClient } from '@/api/client'
import gsap from 'gsap'

export default {
  name: 'LoginView',
  data() {
    return {
      email: '',
      password: '',
      rememberMe: false,
      errorMessage: '',
      xTo: null,
      yTo: null,
      xTextTo: null,
      yTextTo: null,
      ctx: null
    }
  },
  mounted() {
    this.ctx = gsap.context(() => {
      // Fade Up de la carte
      gsap.fromTo(this.$refs.authCard, 
        { y: 50, opacity: 0 }, 
        { y: 0, opacity: 1, duration: 1.2, ease: "power3.out" }
      )
      
      // Stagger des éléments internes
      gsap.fromTo('.gsap-stagger', 
        { y: 20, opacity: 0 }, 
        { 
          y: 0, 
          opacity: 1, 
          duration: 0.8, 
          stagger: 0.1, 
          ease: "power2.out", 
          delay: 0.3 
        }
      )

      // Animation du joueur décoratif
      gsap.fromTo('.gsap-reveal-player',
        { x: 100, opacity: 0, scale: 0.8 },
        { 
          x: 0, 
          opacity: 0.4, 
          scale: 1, 
          duration: 1.5, 
          ease: "power3.out",
          delay: 0.5
        }
      )

      // Bouton Magnétique GSAP quickTo
      const btn = this.$refs.magneticBtn
      const text = this.$refs.btnText
      if (btn && text) {
        this.xTo = gsap.quickTo(btn, "x", { duration: 0.4, ease: "power3" })
        this.yTo = gsap.quickTo(btn, "y", { duration: 0.4, ease: "power3" })
        this.xTextTo = gsap.quickTo(text, "x", { duration: 0.4, ease: "power3" })
        this.yTextTo = gsap.quickTo(text, "y", { duration: 0.4, ease: "power3" })
      }
    }, this.$el)
  },
  unmounted() {
    if (this.ctx) {
      this.ctx.revert()
    }
  },
  methods: {
    handleMagneticMove(e) {
      const btn = this.$refs.magneticBtn
      if (!btn) return
      const rect = btn.getBoundingClientRect()
      const x = (e.clientX - (rect.left + rect.width / 2)) * 0.3
      const y = (e.clientY - (rect.top + rect.height / 2)) * 0.3
      
      this.xTo(x)
      this.yTo(y)
      this.xTextTo(x * 0.5)
      this.yTextTo(y * 0.5)
    },
    handleMagneticLeave() {
      if (this.xTo) this.xTo(0)
      if (this.yTo) this.yTo(0)
      if (this.xTextTo) this.xTextTo(0)
      if (this.yTextTo) this.yTextTo(0)
    },
    async handleLogin() {
      // Feedback click scale down rapide
      gsap.to(this.$refs.magneticBtn, { scale: 0.95, duration: 0.1, yoyo: true, repeat: 1 })

      try {
        // Étape 1 : récupère le token
        const response = await apiClient.post('/auth/login', {
          email: this.email,
          password: this.password
        })
        localStorage.setItem('token', response.access_token)

        // Étape 2 : récupère les infos de l'utilisateur connecté
        const me = await apiClient.get('/auth/me')
        localStorage.setItem('user', JSON.stringify(me))

        this.$router.push('/')
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
  background-image: linear-gradient(rgba(10, 10, 26, 0.4), rgba(10, 10, 26, 0.4)), url("@/assets/stadium1.png");
  background-size: cover;
  background-position: center;
}

.auth-container::before {
  content: '';
  position: absolute;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(224, 38, 255, 0.2) 0%, transparent 70%);
  top: -100px;
  right: -100px;
  z-index: 0;
}

.auth-container::after {
  content: '';
  position: absolute;
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(0, 212, 255, 0.15) 0%, transparent 70%);
  bottom: -150px;
  left: -150px;
  z-index: 0;
}

.decorative-player {
  position: absolute;
  right: -5%;
  bottom: -10%;
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
  transform: scaleX(-1); /* Mirolité pour pointer vers le formulaire */
}

.auth-card {
  background: var(--glass-bg);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border: 1px solid var(--glass-border);
  border-radius: 32px;
  padding: 4rem 3.5rem;
  width: 100%;
  max-width: 480px;
  box-shadow: var(--glass-shadow);
  color: var(--text-primary);
  position: relative;
  z-index: 10;
}

.logo {
  margin-bottom: 2.5rem;
  text-align: center;
}

.auth-title {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 2.5rem;
  text-align: center;
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
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 0.5rem;
}

.checkbox-container {
  display: flex;
  align-items: center;
  cursor: pointer;
  font-size: 0.9rem;
  color: var(--text-secondary);
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
  margin-right: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
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

.forgot-password {
  color: var(--accent-secondary);
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 700;
  transition: all 0.3s ease;
}

.forgot-password:hover {
  filter: brightness(1.2);
  text-shadow: 0 0 10px rgba(0, 212, 255, 0.4);
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

.register-link {
  color: var(--accent-secondary);
  text-decoration: none;
  font-weight: 800;
  margin-left: 8px;
  transition: all 0.3s ease;
}

.register-link:hover {
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
  
  .form-options {
    flex-direction: column;
    gap: 1.5rem;
    align-items: flex-start;
  }
}

</style>