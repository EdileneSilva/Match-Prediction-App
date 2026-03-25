<template>
  <footer class="footer">
    <div class="footer-container">
      <div class="footer-grid">
        <div class="footer-info">
          <div class="footer-logo">
            <div class="logo-icon">M</div>
            <span>Match Prediction</span>
          </div>
          <p>L'IA au service de l'analyse sportive de haut niveau.</p>
        </div>
        
        <div class="footer-links">
          <h4>Plateforme</h4>
          <ul>
            <li><a href="#features">Fonctionnalités</a></li>
            <li><a href="#">Ligue 1</a></li>
          </ul>
        </div>
        
        <div class="footer-links">
          <h4>Compte</h4>
          <ul>
            <li><RouterLink to="/login">Connexion</RouterLink></li>
            <li><RouterLink to="/register">Inscription</RouterLink></li>
          </ul>
        </div>
        
        <div class="footer-links">
          <h4>Légal</h4>
          <ul>
            <li><a href="#">Mentions légales</a></li>
            <li><a href="#">Confidentialité</a></li>
          </ul>
        </div>
      </div>
      
      <div class="footer-bottom">
        <p>&copy; {{ new Date().getFullYear() }} Match Prediction. Par team AI Mory Labs Tous droits réservés.</p>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  padding: 80px 2rem 40px;
  background: rgba(0, 0, 0, 0.3);
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
}

.footer-grid {
  display: grid;
  grid-template-columns: 2fr repeat(3, 1fr);
  gap: 4rem;
  margin-bottom: 4rem;
}

.footer-logo {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  margin-bottom: 1.5rem;
}

.logo-icon {
  width: 35px;
  height: 35px;
  background: #fbbf24;
  color: #764ba2;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1rem;
}

.footer-info p {
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.6;
  max-width: 250px;
}

h4 {
  color: white;
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

ul li {
  margin-bottom: 0.8rem;
}

ul li a {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: color 0.3s ease;
  font-size: 0.95rem;
}

ul li a:hover {
  color: white;
}

.footer-bottom {
  padding-top: 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  text-align: center;
}

.footer-bottom p {
  color: #718096;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .footer-grid {
    grid-template-columns: 1fr 1fr;
    gap: 3rem;
  }
}

@media (max-width: 480px) {
  .footer-grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
}
</style>
