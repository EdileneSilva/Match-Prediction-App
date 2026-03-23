<template>
  <div class="auth-container">
    <div class="auth-box">
      <h1 class="auth-title">Mot de passe oublié</h1>
      <p class="auth-subtitle">Saisissez votre email pour recevoir un lien de réinitialisation (simulé dans la console).</p>
      
      <form @submit.prevent="handleForgot" class="auth-form">
        <div class="form-group">
          <label for="email">Email</label>
          <input 
            type="email" 
            id="email" 
            v-model="email" 
            placeholder="votre@email.com" 
            required
            class="form-input"
          >
        </div>
        
        <div v-if="message" class="success-message">{{ message }}</div>
        <div v-if="error" class="error-message">{{ error }}</div>
        
        <button type="submit" class="auth-btn" :disabled="isLoading">
          {{ isLoading ? 'Envoi...' : 'Envoyer le lien' }}
        </button>
      </form>
      
      <div class="auth-footer">
        <router-link to="/login" class="footer-link">Retour à la connexion</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { apiClient } from '@/api/client'

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

.auth-footer {
  margin-top: 1.5rem;
  text-align: center;
}

.footer-link {
  color: #667eea;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
}

.footer-link:hover {
  text-decoration: underline;
}
</style>
