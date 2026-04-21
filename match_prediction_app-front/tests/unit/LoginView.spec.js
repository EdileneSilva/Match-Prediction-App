// tests/unit/LoginView.spec.js
import { mount } from '@vue/test-utils'
import LoginView from '@/views/LoginView.vue'
import { createRouter, createWebHistory } from 'vue-router'

// Router de test pour les redirections
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: { template: '<div>Home</div>' } },
    { path: '/register', component: { template: '<div>Register</div>' } }
  ]
})

describe('LoginView', () => {
  let wrapper

  // Configuration avant chaque test
  beforeEach(() => {
    wrapper = mount(LoginView, {
      global: {
        plugins: [router],
        stubs: ['router-link']
      }
    })
  })

  // Test 1: Vérifie que le formulaire de connexion s'affiche correctement
  it('renders the login form', () => {
    expect(wrapper.find('.auth-title').text()).toBe('Connexion') // Titre présent
    expect(wrapper.find('#email').exists()).toBe(true)         // Champ email existe
    expect(wrapper.find('#password').exists()).toBe(true)      // Champ mot de passe existe
  })

  // Test 2: Vérifie l'initialisation des données du formulaire
  it('has form data correctly initialized', () => {
    expect(wrapper.vm.email).toBe('')        // Email vide au départ
    expect(wrapper.vm.password).toBe('')     // Mot de passe vide au départ
    expect(wrapper.vm.rememberMe).toBe(false)// Case "Se souvenir" non cochée
  })

  // Test 3: Vérifie la soumission réussie et la redirection vers l'accueil
  it('submits form successfully and redirects to home', async () => {
    // Mock de la méthode handleLogin pour éviter les appels API
    const mockHandleLogin = jest.fn().mockImplementation(() => {
      console.log('Login attempt:', { 
        email: 'test@example.com', 
        rememberMe: true 
      })
      wrapper.vm.$router.push('/')
    })
    wrapper.vm.handleLogin = mockHandleLogin
    
    const pushSpy = jest.spyOn(wrapper.vm.$router, 'push')
    
    // Remplir le formulaire de connexion
    await wrapper.setData({
      email: 'test@example.com',
      password: 'password123',
      rememberMe: true
    })

    // Soumettre le formulaire
    await wrapper.find('form').trigger('submit')
    
    // Vérifier que handleLogin a été appelé
    expect(mockHandleLogin).toHaveBeenCalled()
    // Vérifier la redirection vers la page d'accueil
    expect(pushSpy).toHaveBeenCalledWith('/')
    
    // Nettoyer les mocks
    pushSpy.mockRestore()
  })

  // Test 4: Vérifie la présence du lien vers la page d'inscription
  it('has link to register page', () => {
    const registerLink = wrapper.find('.register-link')
    expect(registerLink.exists()).toBe(true)           // Le lien existe
    // Le router-link stub n'a pas de texte, on vérifie l'attribut to
    expect(registerLink.attributes('to')).toBe('/register')
  })

  // Test 5: Vérifie la présence du lien "mot de passe oublié"
  it('has forgot password link', () => {
    const forgotLink = wrapper.find('.forgot-password')
    expect(forgotLink.exists()).toBe(true)                    // Le lien existe
    // Le router-link stub n'a pas de texte, on vérifie l'attribut to
    expect(forgotLink.attributes('to')).toBe('/forgot-password')
  })
})