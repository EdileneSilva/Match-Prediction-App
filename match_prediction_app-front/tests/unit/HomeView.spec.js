// tests/unit/HomeView.spec.js
import { mount } from '@vue/test-utils'
import HomeView from '@/views/HomeView.vue'

describe('HomeView', () => {
    let wrapper

    // Configuration avant chaque test
    beforeEach(() => {
        wrapper = mount(HomeView)
    })

    // Test 1: Vérifie que le dashboard s'affiche correctement
    it('renders the dashboard', () => {
        expect(wrapper.find('.dashboard').exists()).toBe(true) // Conteneur principal présent
    })

    // Test 2: Vérifie l'affichage des cartes d'information
    it('displays info cards', () => {
        const cards = wrapper.findAll('.card')
        expect(cards).toHaveLength(3) // 3 cartes d'info attendues

        // Vérification de la première carte (Score utilisateur)
        expect(cards[0].find('h3').text()).toBe('Score utilisateur') // Titre correct
        expect(cards[0].find('.score').text()).toBe('85 pts')       // Score correct

        // Vérification de la deuxième carte (Matchs)
        expect(cards[1].find('h3').text()).toBe('Matchs')           // Titre correct
        expect(cards[1].find('p').text()).toBe('12 Matchs prédits') // Nombre correct

        // Vérification de la troisième carte (Statistiques)
        expect(cards[2].find('h3').text()).toBe('Statistiques')     // Titre correct
        expect(cards[2].find('p').text()).toBe('74% Réussite')      // Pourcentage correct
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
        expect(matches[0].find('.match-percentage').text()).toBe('65%')       // Pourcentage
        expect(matches[0].find('.view-btn').text()).toBe('Voir')              // Bouton

        // Vérification du deuxième match (Lyon vs Lille)
        expect(matches[1].find('.match-teams').text()).toContain('Lyon')      // Équipe 1
        expect(matches[1].find('.match-teams').text()).toContain('Lille')     // Équipe 2
        expect(matches[1].find('.match-percentage').text()).toBe('52%')       // Pourcentage
    })

    // Test 5: Vérifie que chaque match a un bouton "Voir"
    it('has view buttons for each match', () => {
        const viewButtons = wrapper.findAll('.view-btn')
        expect(viewButtons).toHaveLength(3) // 3 boutons attendus
        viewButtons.forEach(button => {
            expect(button.text()).toBe('Voir') // Texte correct pour chaque bouton
        })
    })
    // Test 6: Vérifie les icônes des cartes
    it('displays card icons correctly', () => {
        const cardIcons = wrapper.findAll('.card-icon')
        expect(cardIcons).toHaveLength(3)
        expect(cardIcons[0].text()).toBe('📊') // Icône score
        expect(cardIcons[1].text()).toBe('⚽') // Icône matchs
        expect(cardIcons[2].text()).toBe('📈') // Icône statistiques
    })
})