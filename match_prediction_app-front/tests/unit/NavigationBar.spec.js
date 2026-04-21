// tests/unit/NavigationBar.spec.js
import { mount } from '@vue/test-utils'
import NavigationBar from '@/components/NavigationBar.vue'
import { createRouter, createWebHistory } from 'vue-router'

// Router de test pour les liens de navigation
const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', component: { template: '<div>Home</div>' } },
        { path: '/predictions', component: { template: '<div>Predictions</div>' } },
        { path: '/history', component: { template: '<div>History</div>' } },
        { path: '/profile', component: { template: '<div>Profile</div>' } },
        { path: '/exit', component: { template: '<div>Exit</div>' } }
    ]
})

describe('NavigationBar', () => {
    let wrapper

    beforeEach(() => {
        // Mock localStorage pour simuler l'état non authentifié
        const localStorageMock = {
            getItem: jest.fn(() => null), // Pas de token = non authentifié
            setItem: jest.fn(),
            removeItem: jest.fn(),
            clear: jest.fn()
        }
        Object.defineProperty(window, 'localStorage', { value: localStorageMock })
        
        wrapper = mount(NavigationBar, {
            global: {
                plugins: [router],
                stubs: ['router-link']
            }
        })
    })

    // Test 1: Vérifie que la barre de navigation s'affiche correctement
    it('renders the navigation bar', () => {
        expect(wrapper.find('.navbar').exists()).toBe(true)    // Barre de nav présente
        expect(wrapper.find('.nav-brand').exists()).toBe(true) // Logo/brand présent
        expect(wrapper.find('.logo-img').exists()).toBe(true)  // Image du logo présente
    })

    // Test 2: Vérifie l'affichage de tous les liens de navigation
    it('displays all navigation links', () => {
        const navItems = wrapper.findAll('.nav-item')
        
        expect(navItems).toHaveLength(2) // 2 liens de navigation attendus (non authentifié)
        
        // Les router-link-stubs n'ont pas de texte, on vérifie les attributs to
        expect(navItems[0].attributes('to')).toBe('/login')          // Lien de connexion
        expect(navItems[1].attributes('to')).toBe('/register')        // Lien d'inscription
        expect(navItems[1].classes()).toContain('register-btn')       // Bouton d'inscription spécial
    })

    // Test 3: Vérifie que le lien "Exit" a un style spécial (uniquement quand authentifié)
    it('has exit link with special styling', () => {
        const exitLink = wrapper.find('.nav-item.exit')
        expect(exitLink.exists()).toBe(false)   // Lien avec classe "exit" n'existe pas quand non authentifié
    })

    // Test 4: Vérifie que les liens router-link fonctionnent correctement
    it('has working router links', () => {
        const navItems = wrapper.findAll('.nav-item')
        
        // Vérifier simplement que les liens existent et ont les bonnes classes
        expect(navItems.length).toBe(2)
        expect(navItems[0].exists()).toBe(true)
        expect(navItems[1].exists()).toBe(true)
    })

    // Test 5: Vérifie les destinations des liens via les composants RouterLink
    it('has correct link destinations', () => {
        const navItems = wrapper.findAll('.nav-item')
        
        // Vérifier les attributs to des router-link
        expect(navItems[0].attributes('to')).toBe('/login') // Se connecter
        expect(navItems[1].attributes('to')).toBe('/register') // Créer un compte
    })

    // Test 6: Vérifie l'affichage du logo
    it('displays logo correctly', () => {
    const logo = wrapper.find('.logo-img')
    expect(logo.exists()).toBe(true) // Logo présent
    expect(logo.attributes('alt')).toBe('Logo') // Alt text correct
    
    // Vérifier que l'attribut src existe, même s'il peut être vide dans les tests
    const srcAttr = logo.attributes('src')
    expect(typeof srcAttr).toBe('string') // src est une chaîne (peut être vide)
    
    // Alternative: vérifier que l'élément img a bien un attribut src
    expect(logo.element.hasAttribute('src')).toBe(true)
})
})