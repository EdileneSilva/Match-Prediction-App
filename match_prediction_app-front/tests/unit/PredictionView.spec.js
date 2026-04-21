// match_prediction_app-front/tests/unit/PredictionView.spec.js
import { mount } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import PredictionView from '@/views/PredictionView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/predict', component: PredictionView },
    { path: '/', component: { template: '<div>Home</div>' } }
  ]
})

describe('PredictionView.vue', () => {
  let wrapper

  beforeEach(() => {
    wrapper = mount(PredictionView, {
      global: {
        plugins: [router]
      }
    })
    
    // Mock de la méthode qui charge les équipes pour éviter les appels API
    wrapper.vm.fetchTeams = jest.fn().mockResolvedValue([])
    
    // Mock des équipes pour éviter les appels API
    wrapper.setData({
      teams: [
        { id: 1, name: 'PSG', logo_url: 'psg.png' },
        { id: 2, name: 'OM', logo_url: 'om.png' },
        { id: 3, name: 'Lyon', logo_url: 'lyon.png' }
      ],
      error: null
    })
  })

  // Test 1: Vérifie que la vue de prédiction s'affiche correctement
  it('renders the prediction view', () => {
    expect(wrapper.find('.dashboard').exists()).toBe(true)
    expect(wrapper.find('.page-title').text()).toBe('Arena de Prédiction')
    expect(wrapper.find('.prediction-container').exists()).toBe(true)
  })

  // Test 2: Vérifie l'initialisation des données
  it('has correct initial data', () => {
    expect(wrapper.vm.selectedTeam1).toBe(null)
    expect(wrapper.vm.selectedTeam2).toBe(null)
    expect(wrapper.vm.isPredicting).toBe(false)
    expect(wrapper.vm.predictionResult).toBe(null)
    // L'erreur peut exister à cause de l'appel API dans mounted
    expect(wrapper.vm.teams).toHaveLength(3)
  })

  // Test 3: Vérifie la présence des sélecteurs d'équipes
  it('displays team selectors', () => {
    expect(wrapper.find('#team1').exists()).toBe(true)
    expect(wrapper.find('#team2').exists()).toBe(true)
    expect(wrapper.findAll('.team-select')).toHaveLength(2)
    expect(wrapper.findAll('.team-card')).toHaveLength(2)
  })

  // Test 4: Vérifie que le bouton est désactivé au départ
  it('disables predict button initially', () => {
    const predictBtn = wrapper.find('.predict-btn-hero')
    expect(predictBtn.attributes('disabled')).toBeDefined()
  })

  // Test 5: Vérifie que le bouton s'active quand deux équipes différentes sont sélectionnées
  it('enables predict button when teams are selected', async () => {
    await wrapper.setData({
      selectedTeam1: { id: 1, name: 'PSG', logo_url: 'psg.png' },
      selectedTeam2: { id: 2, name: 'OM', logo_url: 'om.png' }
    })
    
    const predictBtn = wrapper.find('.predict-btn-hero')
    expect(predictBtn.attributes('disabled')).toBeUndefined()
  })

  // Test 6: Vérifie l'interdiction de sélectionner la même équipe
  it('prevents selecting same team', async () => {
    await wrapper.setData({
      selectedTeam1: { id: 1, name: 'PSG', logo_url: 'psg.png' },
      selectedTeam2: { id: 1, name: 'PSG', logo_url: 'psg.png' }
    })
    
    const predictBtn = wrapper.find('.predict-btn-hero')
    expect(predictBtn.attributes('disabled')).toBeDefined()
    
    // Vérifier que le message d'erreur s'affiche
    expect(wrapper.text()).toContain('Veuillez choisir deux équipes différentes')
  })

  // Test 7: Vérifie le lancement de prédiction
  it('launches prediction when button clicked', async () => {
    // Mock de la méthode launchPrediction
    const mockLaunchPrediction = jest.fn()
    wrapper.vm.launchPrediction = mockLaunchPrediction
    
    await wrapper.setData({
      selectedTeam1: { id: 1, name: 'PSG', logo_url: 'psg.png' },
      selectedTeam2: { id: 2, name: 'OM', logo_url: 'om.png' }
    })
    
    await wrapper.find('.predict-btn-hero').trigger('click')
    expect(mockLaunchPrediction).toHaveBeenCalled()
  })

  // Test 8: Vérifie l'affichage de l'arène de scanning
  it('shows scanning arena during prediction', async () => {
    await wrapper.setData({
      selectedTeam1: { id: 1, name: 'PSG', logo_url: 'psg.png' },
      selectedTeam2: { id: 2, name: 'OM', logo_url: 'om.png' },
      isPredicting: true
    })
    
    expect(wrapper.find('.scanning-arena').exists()).toBe(true)
    expect(wrapper.find('.scanning-title').text()).toBe('Analyse Neuronale en cours...')
    expect(wrapper.find('.prediction-container').exists()).toBe(false)
  })

  // Test 9: Vérifie l'affichage des résultats
  it('displays prediction results', async () => {
    const mockResult = {
      team1Win: 60,
      draw: 25,
      team2Win: 15
    }
    
    await wrapper.setData({
      selectedTeam1: { id: 1, name: 'PSG', logo_url: 'psg.png' },
      selectedTeam2: { id: 2, name: 'OM', logo_url: 'om.png' },
      isPredicting: false,
      predictionResult: mockResult
    })
    
    expect(wrapper.find('.results-container').exists()).toBe(true)
    expect(wrapper.find('.winner-name').text()).toBe('PSG') // PSG gagne avec 60%
    expect(wrapper.find('.reveal-badge').text()).toBe('Vainqueur Probable')
  })

  // Test 10: Vérifie les boutons d'action après prédiction
  it('shows action buttons after prediction', async () => {
    await wrapper.setData({
      selectedTeam1: { id: 1, name: 'PSG', logo_url: 'psg.png' },
      selectedTeam2: { id: 2, name: 'OM', logo_url: 'om.png' },
      isPredicting: false,
      predictionResult: { team1Win: 60, draw: 25, team2Win: 15 }
    })
    
    expect(wrapper.find('.reset-btn').exists()).toBe(true)
    expect(wrapper.find('.reset-btn').text()).toContain('Nouvelle Analyse')
  })

  // Test 11: Vérifie la méthode de réinitialisation
  it('resets arena correctly', async () => {
    // Mock de la méthode resetArena
    const mockResetArena = jest.fn()
    wrapper.vm.resetArena = mockResetArena
    
    await wrapper.setData({
      selectedTeam1: { id: 1, name: 'PSG', logo_url: 'psg.png' },
      selectedTeam2: { id: 2, name: 'OM', logo_url: 'om.png' },
      predictionResult: { team1Win: 60, draw: 25, team2Win: 15 }
    })
    
    await wrapper.find('.reset-btn').trigger('click')
    expect(mockResetArena).toHaveBeenCalled()
  })

  
  // Test 13: Vérifie l'affichage des logos d'équipes
  it('displays team logos when selected', async () => {
    await wrapper.setData({
      selectedTeam1: { id: 1, name: 'PSG', logo_url: 'psg.png' },
      selectedTeam2: { id: 2, name: 'OM', logo_url: 'om.png' }
    })
    
    const logos = wrapper.findAll('.team-logo-giant')
    expect(logos).toHaveLength(2)
    expect(logos[0].attributes('src')).toBe('psg.png')
    expect(logos[1].attributes('src')).toBe('om.png')
  })
})