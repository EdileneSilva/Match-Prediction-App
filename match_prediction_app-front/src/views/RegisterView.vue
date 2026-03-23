<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="logo">
  <img src="@/assets/logo.png" alt="Logo" class="logo-img" />
</div>
      
      <h2 class="auth-title">Inscription</h2>

      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>
      
      <form class="auth-form" @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="name">Nom complet</label>
          <input 
            type="text" 
            id="name" 
            v-model="name" 
            placeholder="Entrez votre nom complet"
            required
          >
        </div>
        
        <div class="form-group">
          <label for="email">Email</label>
          <input 
            type="email" 
            id="email" 
            v-model="email" 
            placeholder="Entrez votre email"
            required
          >
        </div>
        
        <div class="form-group">
          <label for="password">Mot de passe</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            placeholder="Entrez votre mot de passe"
            required
          >
        </div>
        
        <div class="form-group">
          <label for="confirmPassword">Confirmer le mot de passe</label>
          <input 
            type="password" 
            id="confirmPassword" 
            v-model="confirmPassword" 
            placeholder="Confirmez votre mot de passe"
            required
          >
        </div>
        
        <div class="form-options">
          <label class="checkbox-container">
            <input type="checkbox" v-model="agreeTerms">
            <span class="checkmark"></span>
            J'accepte les conditions d'utilisation
          </label>
        </div>
        
        <button type="submit" class="auth-btn">Créer un compte</button>
      </form>
      
      <div class="auth-footer">
        <span>Déjà un compte?</span>
        <router-link to="/login" class="login-link">Se connecter</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { apiClient } from '@/api/client'

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
  methods: {
    async handleRegister() {
      if (this.password !== this.confirmPassword) {
        this.errorMessage = 'Les mots de passe ne correspondent pas'
        return
      }
      
      if (!this.agreeTerms) {
        this.errorMessage = 'Vous devez accepter les conditions d\'utilisation'
        return
      }
      
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
  background: linear-gradient(135deg, #667eea, #764ba2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  padding: 1rem;
}

.auth-card {
  background: white;
  border-radius: 12px;
  padding: 3rem 2.5rem;
  width: 100%;
  max-width: 420px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid #e0e0e0;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 2rem;
  text-align: center;
}

.auth-title {
  font-size: 2rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 2rem;
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
  color: #555;
  font-size: 0.95rem;
}

.form-group input {
  padding: 0.875rem 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: #fafafa;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
  background: white;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-options {
  margin-top: 0.5rem;
}

.checkbox-container {
  display: flex;
  align-items: flex-start;
  cursor: pointer;
  font-size: 0.9rem;
  color: #666;
  position: relative;
  line-height: 1.4;
}

.checkbox-container input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
}

.checkmark {
  width: 18px;
  height: 18px;
  border: 2px solid #ddd;
  border-radius: 4px;
  margin-right: 8px;
  margin-top: 2px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.checkbox-container input:checked ~ .checkmark {
  background: #667eea;
  border-color: #667eea;
}

.checkbox-container input:checked ~ .checkmark::after {
  content: '✓';
  color: white;
  font-size: 12px;
  font-weight: bold;
}

.auth-btn {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  padding: 1rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 1rem;
}

.auth-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.auth-footer {
  text-align: center;
  margin-top: 2rem;
  color: #666;
  font-size: 0.9rem;
}

.login-link {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
  margin-left: 5px;
  transition: color 0.3s ease;
}

.login-link:hover {
  color: #5a6fd8;
  text-decoration: underline;
}

.logo-img {
  height: 1.5rem;
  width: auto;
}

@media (max-width: 480px) {
  .auth-card {
    padding: 2rem 1.5rem;
  }
  
  .auth-title {
    font-size: 1.75rem;
  }
}
</style>