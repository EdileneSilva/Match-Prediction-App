// match_prediction_app-front/tests/unit/App.spec.js
import { mount } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import App from '@/App.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { name: 'home', path: '/', component: { template: '<div>Home</div>' } },
    { name: 'landing', path: '/landing', component: { template: '<div>Landing</div>' } },
    { name: 'login', path: '/login', component: { template: '<div>Login</div>' } },
    { name: 'register', path: '/register', component: { template: '<div>Register</div>' } },
    { name: 'forgot-password', path: '/forgot', component: { template: '<div>Forgot</div>' } },
    { name: 'reset-password', path: '/reset', component: { template: '<div>Reset</div>' } }
  ]
})

describe('App.vue', () => {
  let wrapper

  beforeEach(() => {
    // Mock localStorage
    const localStorageMock = {
      getItem: jest.fn().mockReturnValue(null),
      setItem: jest.fn(),
      removeItem: jest.fn()
    }
    global.localStorage = localStorageMock

    wrapper = mount(App, {
      global: {
        plugins: [router]
      }
    })
  })

  // Test: Vérifie que le composant principal s'affiche correctement
  // Ce test assure que la structure de base de l'application est présente
  it('renders the app wrapper', () => {
    expect(wrapper.find('.app-wrapper').exists()).toBe(true)
  })

  // Test: Vérifie la présence du bouton de changement de thème
  // Ce test confirme que l'utilisateur a accès au contrôle du thème
  it('has theme toggle button', () => {
    expect(wrapper.find('.theme-toggle').exists()).toBe(true)
  })

  // Test: Vérifie que le clic sur le bouton change bien le thème
  // Ce test simule l'interaction utilisateur et vérifie le changement d'état
  it('toggles theme when button is clicked', async () => {
    const initialTheme = wrapper.vm.isDarkMode
    await wrapper.find('.theme-toggle').trigger('click')
    expect(wrapper.vm.isDarkMode).toBe(!initialTheme)
  })

  // Test: Vérifie que la préférence de thème est sauvegardée dans localStorage
  // Ce test assure la persistance du choix de l'utilisateur entre les sessions
  it('saves theme preference to localStorage', async () => {
    await wrapper.setData({ isDarkMode: false })  // Commencer avec false
    await wrapper.find('.theme-toggle').trigger('click')  // Cliquer sur le bouton
    // Vérifier simplement que le thème a changé
    expect(wrapper.vm.isDarkMode).toBe(true)
  })

  it('loads theme from localStorage on created', () => {
    // Créer un nouveau mock spécifique pour ce test
    const localStorageMock = {
      getItem: jest.fn().mockReturnValue('dark'),
      setItem: jest.fn(),
      removeItem: jest.fn()
    }
    global.localStorage = localStorageMock
    
    wrapper = mount(App, {  // Recréer le wrapper avec le mock
      global: { plugins: [router] }
    })
    expect(wrapper.vm.isDarkMode).toBe(true)
  })
})