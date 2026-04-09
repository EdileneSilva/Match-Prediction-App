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
        plugins: [router],
        stubs: ['router-link']
      }
    })
    
    // Mock the initGSAP method to prevent GSAP calls during tests
    wrapper.vm.initGSAP = jest.fn()
    wrapper.vm.initMagneticButton = jest.fn()
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
    
    // Vérifier que le message d'erreur est affiché dans le composant
    expect(wrapper.vm.errorMessage).toBe('Les mots de passe ne correspondent pas')
    expect(wrapper.find('.error-message').exists()).toBe(true)
    expect(wrapper.find('.error-message').text()).toBe('Les mots de passe ne correspondent pas')
  })

  // Test 4: Vérifie l'affichage d'une erreur quand les conditions ne sont pas acceptées
  it('shows error when terms are not accepted', async () => {
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
    
    // Vérifier que le message d'erreur est affiché dans le composant
    expect(wrapper.vm.errorMessage).toBe('Vous devez accepter les conditions d\'utilisation')
    expect(wrapper.find('.error-message').exists()).toBe(true)
    expect(wrapper.find('.error-message').text()).toBe('Vous devez accepter les conditions d\'utilisation')
  })

  // Test 5: Vérifie la soumission réussie du formulaire et la redirection
  it('submits form successfully and redirects to login', async () => {
    // Mock de la méthode handleRegister pour simuler une inscription réussie
    const mockHandleRegister = jest.fn().mockImplementation(() => {
      wrapper.vm.$router.push('/login')
    })
    wrapper.vm.handleRegister = mockHandleRegister
    
    const pushSpy = jest.spyOn(wrapper.vm.$router, 'push')
    
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
    
    // Vérifier que handleRegister a été appelé
    expect(mockHandleRegister).toHaveBeenCalled()
    // Vérifier la redirection vers la page de login
    expect(pushSpy).toHaveBeenCalledWith('/login')
    
    // Nettoyer les mocks
    pushSpy.mockRestore()
  })

  // Test 6: Vérifie la présence du lien vers la page de connexion
  it('has link to login page', () => {
    const loginLink = wrapper.find('.login-link')
    expect(loginLink.exists()).toBe(true)           // Le lien existe
    // Le router-link stub n'a pas de texte, on vérifie l'attribut to
    expect(loginLink.attributes('to')).toBe('/login')
  })
})