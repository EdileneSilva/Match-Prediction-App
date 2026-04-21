// tests/unit/HomeView.spec.js
import { mount } from '@vue/test-utils'
import HomeView from '@/views/HomeView.vue'

describe('HomeView', () => {
    let wrapper

    // Configuration avant chaque test
    beforeEach(() => {
        wrapper = mount(HomeView)
        // Mock des données pour les tests
        wrapper.setData({
            isLoading: false,
            upcomingMatches: [
                {
                    fixture_id: 1,
                    home_team: { name: 'PSG', logo: '/psg.png' },
                    away_team: { name: 'Marseille', logo: '/marseille.png' },
                    confidence_percent: 65,
                    is_derby: true
                },
                {
                    fixture_id: 2,
                    home_team: { name: 'Lyon', logo: '/lyon.png' },
                    away_team: { name: 'Lille', logo: '/lille.png' },
                    confidence_percent: 52,
                    is_derby: false
                },
                {
                    fixture_id: 3,
                    home_team: { name: 'Monaco', logo: '/monaco.png' },
                    away_team: { name: 'Nice', logo: '/nice.png' },
                    confidence_percent: 71,
                    is_derby: false
                }
            ],
            standings: [],
            roundName: "Matchs du jour"
        })
    })

    // Test 1: Vérifie que le dashboard s'affiche correctement
    it('renders the dashboard', () => {
        expect(wrapper.find('.dashboard').exists()).toBe(true) // Conteneur principal présent
    })

    // Test 2: Vérifie l'affichage des cartes d'information
    it('displays info cards', () => {
        // Le composant HomeView n'a pas de cartes .card, on vérifie les sections présentes
        const matchesSection = wrapper.find('.matches-section')
        const rankingSection = wrapper.find('.ranking-section')
        
        expect(matchesSection.exists()).toBe(true) // Section matchs présente
        expect(rankingSection.exists()).toBe(true) // Section classement présente
    })

    // Test 3: Vérifie l'affichage de la section des matchs
    it('displays matches section', () => {
        const matchesSection = wrapper.find('.matches-section')
        expect(matchesSection.exists()).toBe(true)                    // Section existe
        expect(matchesSection.find('h2').text()).toBe('Matchs du jour') // Titre correct
    })

    // Test 4: Vérifie l'affichage des matchs individuels
    it('displays match items', () => {
        const matches = wrapper.findAll('.match-item')
        expect(matches).toHaveLength(3) // 3 matchs attendus

        // Vérification du premier match (PSG vs Marseille)
        expect(matches[0].find('.match-teams').text()).toContain('PSG')       // Équipe 1
        expect(matches[0].find('.match-teams').text()).toContain('vs')        // "vs" présent
        expect(matches[0].find('.match-teams').text()).toContain('Marseille') // Équipe 2
        expect(matches[0].find('.view-btn').text()).toBe('Analyser')              // Bouton

        // Vérification du deuxième match (Lyon vs Lille)
        expect(matches[1].find('.match-teams').text()).toContain('Lyon')      // Équipe 1
        expect(matches[1].find('.match-teams').text()).toContain('Lille')     // Équipe 2
    })

    // Test 5: Vérifie que chaque match a un bouton "Analyser"
    it('has view buttons for each match', () => {
        const viewButtons = wrapper.findAll('.view-btn')
        expect(viewButtons).toHaveLength(3) // 3 boutons attendus
        viewButtons.forEach(button => {
            expect(button.text()).toBe('Analyser') // Texte correct pour chaque bouton
        })
    })
    // Test 6: Vérifie les éléments de la page
    it('displays page elements correctly', () => {
        // Vérifier le titre principal
        expect(wrapper.find('h1').exists()).toBe(true)
        expect(wrapper.find('h1').text()).toContain('Prédisez le Futur du Football')
        
        // Vérifier les badges
        expect(wrapper.find('.season-badge').exists()).toBe(true)
        expect(wrapper.find('.season-badge').text()).toBe('Ligue 1 McDonald\'s')
        
        // Vérifier le bouton de rafraîchissement
        expect(wrapper.find('.refresh-btn').exists()).toBe(true)
    })
})