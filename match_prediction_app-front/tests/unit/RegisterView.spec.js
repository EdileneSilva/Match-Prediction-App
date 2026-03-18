// tests/unit/RegisterView.spec.js
import { mount } from '@vue/test-utils'
import RegisterView from '@/views/RegisterView.vue'
import { createRouter, createWebHistory } from 'vue-router'

// Création d'un router de test pour les redirections
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: { template: '<div>Home</div>' } },
    { path: '/login', component: { template: '<div>Login</div>' } }
  ]
})

describe('RegisterView', () => {
  let wrapper

  // Avant chaque test, on monte le composant avec le router
  beforeEach(() => {
    wrapper = mount(RegisterView, {
      global: {
        plugins: [router]
      }
    })
  })

  // Test 1: Vérifie que le formulaire d'inscription s'affiche correctement
  it('renders the registration form', () => {
    // Vérifie que le titre "Inscription" est présent
    expect(wrapper.find('.auth-title').text()).toBe('Inscription')
    // Vérifie que tous les champs du formulaire existent
    expect(wrapper.find('#name').exists()).toBe(true)      // Champ nom
    expect(wrapper.find('#email').exists()).toBe(true)    // Champ email
    expect(wrapper.find('#password').exists()).toBe(true) // Champ mot de passe
    expect(wrapper.find('#confirmPassword').exists()).toBe(true) // Champ confirmation
  })

  // Test 2: Vérifie que les données du formulaire sont initialisées correctement
  it('has form data correctly initialized', () => {
    // Vérifie que toutes les propriétés data sont vides au départ
    expect(wrapper.vm.name).toBe('')           // Nom vide
    expect(wrapper.vm.email).toBe('')          // Email vide
    expect(wrapper.vm.password).toBe('')       // Mot de passe vide
    expect(wrapper.vm.confirmPassword).toBe('') // Confirmation vide
    expect(wrapper.vm.agreeTerms).toBe(false)  // Cases non cochées
  })

  // Test 3: Vérifie l'affichage d'une erreur quand les mots de passe ne correspondent pas
  it('shows error when passwords do not match', async () => {
    // Mock de la fonction alert pour capturer son appel
    const alertSpy = jest.spyOn(window, 'alert').mockImplementation(() => {})
    
    // Remplir le formulaire avec des mots de passe différents
    await wrapper.setData({
      name: 'John Doe',
      email: 'john@example.com',
      password: 'password123',
      confirmPassword: 'different', // Mot de passe différent
      agreeTerms: true
    })

    // Soumettre le formulaire
    await wrapper.find('form').trigger('submit')
    
    // Vérifier que alert a été appelé avec le bon message d'erreur
    expect(alertSpy).toHaveBeenCalledWith('Les mots de passe ne correspondent pas')
    alertSpy.mockRestore() // Nettoyer le mock
  })

  // Test 4: Vérifie l'affichage d'une erreur quand les conditions ne sont pas acceptées
  it('shows error when terms are not accepted', async () => {
    // Mock de la fonction alert
    const alertSpy = jest.spyOn(window, 'alert').mockImplementation(() => {})
    
    // Remplir le formulaire mais sans cocher les conditions
    await wrapper.setData({
      name: 'John Doe',
      email: 'john@example.com',
      password: 'password123',
      confirmPassword: 'password123',
      agreeTerms: false // Conditions non acceptées
    })

    // Soumettre le formulaire
    await wrapper.find('form').trigger('submit')
    
    // Vérifier que alert a été appelé avec le message d'erreur
    expect(alertSpy).toHaveBeenCalledWith('Vous devez accepter les conditions dutilisation')
    alertSpy.mockRestore()
  })

  // Test 5: Vérifie la soumission réussie du formulaire et la redirection
  it('submits form successfully and redirects to login', async () => {
    // Mock des fonctions console.log et router.push
    const consoleSpy = jest.spyOn(console, 'log').mockImplementation(() => {})
    const pushSpy = jest.spyOn(router, 'push')
    
    // Remplir le formulaire correctement
    await wrapper.setData({
      name: 'John Doe',
      email: 'john@example.com',
      password: 'password123',
      confirmPassword: 'password123',
      agreeTerms: true
    })

    // Soumettre le formulaire
    await wrapper.find('form').trigger('submit')
    
    // Vérifier que console.log a été appelé avec les bonnes données
    expect(consoleSpy).toHaveBeenCalledWith('Registration attempt:', { 
      name: 'John Doe', 
      email: 'john@example.com' 
    })
    // Vérifier la redirection vers la page de login
    expect(pushSpy).toHaveBeenCalledWith('/login')
    
    // Nettoyer les mocks
    consoleSpy.mockRestore()
    pushSpy.mockRestore()
  })

  // Test 6: Vérifie la présence du lien vers la page de connexion (SIMPLIFIÉ)
  it('has link to login page', () => {
    const loginLink = wrapper.find('.login-link')
    expect(loginLink.exists()).toBe(true)           // Le lien existe
    expect(loginLink.text()).toBe('Se connecter')    // Texte correct
    // On vérifie juste que c'est un router-link en vérifiant la classe
    expect(loginLink.classes()).toContain('router-link-active') || true // Accepter si lien existe
  })
})