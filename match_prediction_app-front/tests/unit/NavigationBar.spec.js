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
        wrapper = mount(NavigationBar, {
            global: {
                plugins: [router]
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
        expect(navItems).toHaveLength(5) // 5 liens de navigation attendus
        
        expect(navItems[0].text()).toBe('Dashboard')          // Texte correct
        expect(navItems[1].text()).toBe('Prédictions')        // Texte correct
        expect(navItems[2].text()).toBe('Historique')         // Texte correct
        expect(navItems[3].text()).toBe('Profil')             // Texte correct
        expect(navItems[4].text()).toBe('Exit')               // Texte correct
    })

    // Test 3: Vérifie que le lien "Exit" a un style spécial
    it('has exit link with special styling', () => {
        const exitLink = wrapper.find('.nav-item.exit')
        expect(exitLink.exists()).toBe(true)   // Lien avec classe "exit" existe
        expect(exitLink.text()).toBe('Exit')   // Texte correct
    })

    // Test 4: Vérifie que les liens router-link fonctionnent correctement
    it('has working router links', () => {
        const navItems = wrapper.findAll('.nav-item')
        
        // Vérifier que ce sont des router-link
        expect(navItems[0].findComponent({ name: 'RouterLink' }).exists()).toBe(true)
        expect(navItems[1].findComponent({ name: 'RouterLink' }).exists()).toBe(true)
        expect(navItems[2].findComponent({ name: 'RouterLink' }).exists()).toBe(true)
        expect(navItems[3].findComponent({ name: 'RouterLink' }).exists()).toBe(true)
        expect(navItems[4].findComponent({ name: 'RouterLink' }).exists()).toBe(true)
    })

    // Test 5: Vérifie les destinations des liens via les composants RouterLink
    it('has correct link destinations', () => {
        const navItems = wrapper.findAll('.nav-item')
        
        // Vérifier les propriétés des router-link
        expect(navItems[0].findComponent({ name: 'RouterLink' }).props().to).toBe('/') // Dashboard
        expect(navItems[1].findComponent({ name: 'RouterLink' }).props().to).toBe('/predictions') // Prédictions
        expect(navItems[2].findComponent({ name: 'RouterLink' }).props().to).toBe('/history') // Historique
        expect(navItems[3].findComponent({ name: 'RouterLink' }).props().to).toBe('/profile') // Profil
        expect(navItems[4].findComponent({ name: 'RouterLink' }).props().to).toBe('/exit') // Exit
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