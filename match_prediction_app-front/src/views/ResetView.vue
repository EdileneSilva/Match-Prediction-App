<template>
  <div class="auth-container">
    <div class="auth-box">
      <h1 class="auth-title">Nouveau mot de passe</h1>
      <p class="auth-subtitle">Saisissez votre nouveau mot de passe.</p>
      
      <form @submit.prevent="handleReset" class="auth-form">
        <div class="form-group">
          <label for="password">Nouveau mot de passe</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            placeholder="••••••••" 
            required
            class="form-input"
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
            class="form-input"
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
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 1rem;
}

.auth-box {
  background: white;
  padding: 2.5rem;
  border-radius: 16px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.2);
  width: 100%;
  max-width: 400px;
}

.auth-title {
  font-size: 1.75rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 0.5rem;
  text-align: center;
}

.auth-subtitle {
  color: #666;
  text-align: center;
  margin-bottom: 2rem;
  font-size: 0.9rem;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 600;
  color: #555;
  font-size: 0.9rem;
}

.form-input {
  padding: 0.75rem 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
}

.auth-btn {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  padding: 0.875rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  margin-top: 1rem;
}

.auth-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.auth-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.success-message {
  color: #28a745;
  background: #d4edda;
  padding: 0.75rem;
  border-radius: 8px;
  font-size: 0.9rem;
}

.error-message {
  color: #dc3545;
  background: #f8d7da;
  padding: 0.75rem;
  border-radius: 8px;
  font-size: 0.9rem;
}
</style>
