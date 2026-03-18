// tests/unit/PredictionView.spec.js
import { mount } from '@vue/test-utils'
import PredictionView from '@/views/PredictionView.vue'

describe('PredictionView', () => {
    let wrapper

    beforeEach(() => {
        wrapper = mount(PredictionView)
    })

    // Test 1: Vérifie que la page de prédiction s'affiche correctement
    it('renders the prediction page correctly', () => {
        expect(wrapper.find('.prediction-container').exists()).toBe(true) // Conteneur présent
        expect(wrapper.find('.page-title').text()).toBe('Prédiction de Match') // Titre correct
    })

    // Test 2: Vérifie que les sélecteurs d'équipes s'affichent
    it('displays team selectors correctly', () => {
        expect(wrapper.find('.selection-section').exists()).toBe(true)     // Section présente
        expect(wrapper.find('#team1').exists()).toBe(true)                 // Sélecteur équipe 1
        expect(wrapper.find('#team2').exists()).toBe(true)                 // Sélecteur équipe 2
        expect(wrapper.find('.vs-indicator').text()).toBe('VS')           // Indicateur VS
    })

    // Test 3: Vérifie que les équipes sont disponibles dans les listes
    it('has correct teams in select options', () => {
        const team1Options = wrapper.findAll('#team1 option')
        const team2Options = wrapper.findAll('#team2 option')
        
        expect(team1Options).toHaveLength(13) // 12 équipes + option vide
        expect(team2Options).toHaveLength(13) // 12 équipes + option vide
        
        expect(team1Options[1].text()).toBe('PSG') // Première équipe
        expect(team1Options[12].text()).toBe('Montpellier') // Dernière équipe
    })

    // Test 4: Vérifie l'état initial du formulaire
    it('has form correctly initialized', () => {
        expect(wrapper.vm.selectedTeam1).toBe('')      // Équipe 1 non sélectionnée
        expect(wrapper.vm.selectedTeam2).toBe('')      // Équipe 2 non sélectionnée
        expect(wrapper.vm.isPredicting).toBe(false)    // Pas en cours de prédiction
        expect(wrapper.vm.predictionResult).toBeNull()  // Pas de résultat
    })

    // Test 5: Vérifie que le bouton de prédiction est désactivé au départ
    it('disables predict button initially', () => {
        const predictBtn = wrapper.find('.predict-btn')
        expect(predictBtn.exists()).toBe(true)
        expect(predictBtn.attributes('disabled')).toBeDefined() // Bouton désactivé
        expect(predictBtn.text()).toBe('Lancer la prédiction IA') // Texte correct
    })

    // Test 6: Vérifie que le bouton s'active quand les équipes sont sélectionnées
    it('enables predict button when teams are selected', async () => {
        await wrapper.setData({
            selectedTeam1: 'PSG',
            selectedTeam2: 'Marseille'
        })
        
        const predictBtn = wrapper.find('.predict-btn')
        expect(predictBtn.attributes('disabled')).toBeUndefined() // Bouton activé
    })

    // Test 7: Vérifie le lancement de la prédiction
    it('launches prediction when button clicked', async () => {
        await wrapper.setData({
            selectedTeam1: 'PSG',
            selectedTeam2: 'Marseille'
        })
        
        const predictBtn = wrapper.find('.predict-btn')
        await predictBtn.trigger('click')
        
        expect(wrapper.vm.isPredicting).toBe(true) // En cours de prédiction
        expect(predictBtn.text()).toBe('Prédiction en cours...') // Texte modifié
        expect(predictBtn.attributes('disabled')).toBeDefined() // Bouton désactivé
    })

    // Test 8: Vérifie l'affichage des résultats après prédiction
    it('displays prediction results after completion', async () => {
        await wrapper.setData({
            selectedTeam1: 'PSG',
            selectedTeam2: 'Marseille',
            predictionResult: {
                team1Win: 65,
                draw: 20,
                team2Win: 15,
                probableScore: '2-1'
            }
        })
        
        expect(wrapper.find('.results-section').exists()).toBe(true) // Section résultats présente
        expect(wrapper.find('.results-section h2').text()).toBe('Résultat Prédiction') // Titre correct
    })

    // Test 9: Vérifie l'affichage des statistiques de prédiction
    it('displays prediction statistics correctly', async () => {
        await wrapper.setData({
            predictionResult: {
                team1Win: 65,
                draw: 20,
                team2Win: 15,
                probableScore: '2-1'
            }
        })
        
        const statValues = wrapper.findAll('.stat-value')
        expect(statValues[0].text()).toBe('65%') // Victoire équipe 1
        expect(statValues[1].text()).toBe('20%') // Match nul
        expect(statValues[2].text()).toBe('15%') // Victoire équipe 2
    })

    // Test 10: Vérifie l'affichage du score probable (CORRIGÉ)
    it('displays probable score correctly', async () => {
        await wrapper.setData({
            predictionResult: {
                team1Win: 65,
                draw: 20,
                team2Win: 15,
                probableScore: '2-1'
            }
        })
        
        // Correction : enlever l'espace à la fin
        expect(wrapper.find('.score-label').text()).toBe('Score probable :') // Sans espace
        expect(wrapper.find('.score-value').text()).toBe('2-1')
    })

    // Test 11: Vérifie la présence du bouton de sauvegarde
    it('has save prediction button', async () => {
        await wrapper.setData({
            predictionResult: {
                team1Win: 65,
                draw: 20,
                team2Win: 15,
                probableScore: '2-1'
            }
        })
        
        const saveBtn = wrapper.find('.save-btn')
        expect(saveBtn.exists()).toBe(true)
        expect(saveBtn.text()).toBe('Enregistrer prédiction')
    })

    // Test 12: Vérifie la sauvegarde de prédiction
    it('saves prediction when save button clicked', async () => {
        const consoleSpy = jest.spyOn(console, 'log').mockImplementation(() => {})
        const alertSpy = jest.spyOn(window, 'alert').mockImplementation(() => {})
        
        await wrapper.setData({
            selectedTeam1: 'PSG',
            selectedTeam2: 'Marseille',
            predictionResult: {
                team1Win: 65,
                draw: 20,
                team2Win: 15,
                probableScore: '2-1'
            }
        })
        
        await wrapper.find('.save-btn').trigger('click')
        
        expect(consoleSpy).toHaveBeenCalledWith('Saving prediction:', expect.any(Object))
        expect(alertSpy).toHaveBeenCalledWith('Prédiction enregistrée avec succès!')
        
        consoleSpy.mockRestore()
        alertSpy.mockRestore()
    })
})