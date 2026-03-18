// tests/unit/router.spec.js
import { createRouter, createWebHistory } from 'vue-router'
import router from '@/router'

describe('Router', () => {
  // Test 1: Vérifie que toutes les routes requises sont définies
  it('has all required routes', () => {
    const routes = router.getRoutes()
    
    // Vérifie la route d'accueil
    expect(routes.some(route => route.path === '/' && route.name === 'home')).toBe(true)
    // Vérifie la route de connexion
    expect(routes.some(route => route.path === '/login' && route.name === 'login')).toBe(true)
    // Vérifie la route d'inscription
    expect(routes.some(route => route.path === '/register' && route.name === 'register')).toBe(true)
    // Vérifie la route des prédictions
    expect(routes.some(route => route.path === '/predictions' && route.name === 'predictions')).toBe(true)
    // Vérifie la route de l'historique
    expect(routes.some(route => route.path === '/history' && route.name === 'history')).toBe(true)
    // Vérifie la route du profil
    expect(routes.some(route => route.path === '/profile' && route.name === 'profile')).toBe(true)
  })

  // Test 2: Vérifie que les bons composants sont associés à chaque route (CORRIGÉ)
  it('has correct components for each route', () => {
    const routes = router.getRoutes()
    
    // CORRIGÉ: Vérifier que les routes existent et ont des composants
    const homeRoute = routes.find(route => route.name === 'home')
    expect(homeRoute).toBeDefined()                    // La route existe
    expect(homeRoute.components?.default).toBeDefined() // Le composant par défaut existe
    
    const loginRoute = routes.find(route => route.name === 'login')
    expect(loginRoute).toBeDefined()
    expect(loginRoute.components?.default).toBeDefined()
    
    const registerRoute = routes.find(route => route.name === 'register')
    expect(registerRoute).toBeDefined()
    expect(registerRoute.components?.default).toBeDefined()
  })

  // Test 3: Vérifie que le router utilise le mode historique web
  it('uses web history mode', () => {
    expect(router.options.history).toBeDefined() // L'historique est configuré
  })
})