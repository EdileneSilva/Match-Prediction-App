// tests/unit/HistoryView.spec.js
import { mount } from '@vue/test-utils'
import HistoryView from '@/views/HistoryView.vue'

describe('HistoryView', () => {
    let wrapper

    beforeEach(() => {
        wrapper = mount(HistoryView)
    })

    // Test 1: Vérifie que la page d'historique s'affiche correctement
    it('renders the history page correctly', () => {
        expect(wrapper.find('.history-container').exists()).toBe(true) // Conteneur présent
        expect(wrapper.find('.page-title').text()).toBe('Historique des Prédictions') // Titre correct
    })

    // Test 2: Vérifie que le tableau d'historique s'affiche
    it('displays the history table', () => {
        expect(wrapper.find('.history-table').exists()).toBe(true)      // Tableau présent
        expect(wrapper.find('thead').exists()).toBe(true)              // En-tête présent
        expect(wrapper.find('tbody').exists()).toBe(true)              // Corps présent
    })

    // Test 3: Vérifie les en-têtes du tableau
    it('displays correct table headers', () => {
        const headers = wrapper.findAll('th')
        expect(headers).toHaveLength(5) // 5 colonnes attendues
        expect(headers[0].text()).toBe('Date')        // En-tête Date
        expect(headers[1].text()).toBe('Match')       // En-tête Match
        expect(headers[2].text()).toBe('Prédiction')  // En-tête Prédiction
        expect(headers[3].text()).toBe('Résultat')    // En-tête Résultat
        expect(headers[4].text()).toBe('Statut')      // En-tête Statut
    })

    // Test 4: Vérifie que les données d'historique s'affichent correctement
    it('displays history data correctly', () => {
        const rows = wrapper.findAll('tbody tr')
        expect(rows).toHaveLength(3) // 3 prédictions dans l'historique
        
        // Première ligne
        expect(rows[0].find('td').text()).toBe('12/03')      // Date
        expect(rows[0].findAll('td')[1].text()).toBe('PSG - OM') // Match
        expect(rows[0].findAll('td')[2].text()).toBe('2-1')  // Prédiction
        expect(rows[0].findAll('td')[3].text()).toBe('1-1')  // Résultat
    })

    // Test 5: Vérifie les icônes de statut
    it('displays status icons correctly', () => {
        const statusIcons = wrapper.findAll('.status-icon')
        expect(statusIcons).toHaveLength(3) // Une icône par ligne
        
        expect(statusIcons[0].classes()).toContain('incorrect') // Premier incorrect
        expect(statusIcons[0].text()).toBe('✗')
        
        expect(statusIcons[1].classes()).toContain('correct')   // Deuxième correct
        expect(statusIcons[1].text()).toBe('✓')
        
        expect(statusIcons[2].classes()).toContain('correct')   // Troisième correct
        expect(statusIcons[2].text()).toBe('✓')
    })

    // Test 6: Vérifie le calcul du score global
    it('calculates global score correctly', () => {
        expect(wrapper.vm.globalScore).toBe(67) // 2 corrects sur 3 = 66.66% arrondi à 67
        expect(wrapper.find('.score-value').text()).toBe('67%') // Affichage correct
    })

    // Test 7: Vérifie l'affichage du score global (CORRIGÉ)
    it('displays global score section', () => {
        expect(wrapper.find('.global-score').exists()).toBe(true)     // Section présente
        // Correction : enlever l'espace à la fin
        expect(wrapper.find('.score-label').text()).toBe('Score global :') // Label correct
        expect(wrapper.find('.score-value').exists()).toBe(true)      // Valeur présente
    })

    // Test 8: Vérifie que les données sont initialisées correctement
    it('has history data correctly initialized', () => {
        expect(wrapper.vm.historyData).toHaveLength(3) // 3 prédictions initiales
        expect(wrapper.vm.historyData[0].date).toBe('12/03') // Première date
        expect(wrapper.vm.historyData[0].isCorrect).toBe(false) // Premier incorrect
    })
})