<template>
  <div class="auth-container">
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
        const response = await apiClient.post('/auth/login', {
          email: this.email,
          password: this.password
        })
        
        localStorage.setItem('token', response.access_token)
        localStorage.setItem('user', JSON.stringify(response.user))
        
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
  /* Premium Dark Mode Animated Gradient */
  background: linear-gradient(-45deg, #0f172a, #1e1b4b, #312e81, #0f172a);
  background-size: 400% 400%;
  animation: gradientBG 15s ease infinite;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  padding: 1rem;
  overflow: hidden;
}

@keyframes gradientBG {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.auth-card {
  /* Glassmorphism */
  background: rgba(15, 23, 42, 0.4);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 3rem 2.5rem;
  width: 100%;
  max-width: 420px;
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
  color: #f8fafc;
  transition: backdrop-filter 0.5s ease, background 0.5s ease, box-shadow 0.5s ease;
}

.auth-card:hover {
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.5);
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 2rem;
  text-align: center;
}

.auth-title {
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 2rem;
  text-align: center;
  background: linear-gradient(135deg, #fff, #94a3b8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.error-message {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #fca5a5;
  padding: 0.75rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
  text-align: center;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 500;
  color: #cbd5e1;
  font-size: 0.95rem;
}

.glow-input {
  padding: 0.875rem 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.03);
  color: #fff;
}

.glow-input::placeholder {
  color: #64748b;
}

.glow-input:focus {
  outline: none;
  border-color: #818cf8;
  background: rgba(255, 255, 255, 0.08);
  box-shadow: 0 0 15px rgba(99, 102, 241, 0.3);
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
  color: #cbd5e1;
  position: relative;
}

.checkbox-container input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
}

.checkmark {
  width: 18px;
  height: 18px;
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: 4px;
  margin-right: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  background: rgba(255,255,255,0.05);
}

.checkbox-container input:checked ~ .checkmark {
  background: #6366f1;
  border-color: #6366f1;
}

.checkbox-container input:checked ~ .checkmark::after {
  content: '✓';
  color: white;
  font-size: 12px;
  font-weight: bold;
}

.forgot-password {
  color: #818cf8;
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.3s ease, text-shadow 0.3s ease;
}

.forgot-password:hover {
  color: #a5b4fc;
  text-shadow: 0 0 8px rgba(165, 180, 252, 0.5);
}

.magnetic-btn {
  position: relative;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
  border: none;
  padding: 1rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  margin-top: 1rem;
  position: relative;
  z-index: 1;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
}

.magnetic-btn::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.2), transparent);
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: -1;
  border-radius: 8px;
}

.magnetic-btn:hover::before {
  opacity: 1;
}

.magnetic-btn:hover {
  box-shadow: 0 8px 25px rgba(99, 102, 241, 0.5);
}

.btn-text {
  display: inline-block;
  pointer-events: none;
}

.auth-footer {
  text-align: center;
  margin-top: 2rem;
  color: #94a3b8;
  font-size: 0.9rem;
}

.register-link {
  color: #818cf8;
  text-decoration: none;
  font-weight: 500;
  margin-left: 5px;
  transition: color 0.3s ease, text-shadow 0.3s ease;
}

.register-link:hover {
  color: #a5b4fc;
  text-shadow: 0 0 8px rgba(165, 180, 252, 0.5);
}

.logo-img {
  height: 2rem;
  width: auto;
  filter: drop-shadow(0 0 10px rgba(255,255,255,0.2));
}

@media (max-width: 480px) {
  .auth-card {
    padding: 2rem 1.5rem;
    background: rgba(15, 23, 42, 0.6);
    backdrop-filter: blur(20px);
  }
  
  .auth-title {
    font-size: 1.5rem;
  }
  
  .form-options {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
}
</style>