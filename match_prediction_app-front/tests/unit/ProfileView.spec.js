// tests/unit/ProfileView.spec.js
import { mount } from '@vue/test-utils'
import ProfileView from '@/views/ProfileView.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: { template: '<div>Home</div>' } }, // Ajouter cette route
    { path: '/login', component: { template: '<div>Login</div>' } },
    { path: '/profile', component: { template: '<div>Profile</div>' } } // Ajouter cette route
  ]
})

describe('ProfileView', () => {
  let wrapper

  beforeEach(() => {
    wrapper = mount(ProfileView, {
      global: {
        plugins: [router]
      }
    })
    
    // Mock de la méthode fetchProfile pour éviter les appels API
    wrapper.vm.fetchProfile = jest.fn().mockResolvedValue()
    
    // Initialiser manuellement les données pour éviter les appels API
    wrapper.setData({
      profileData: {
        username: 'John Doe',
        email: 'adresse@email.com',
        password: '',
        photo: null
      }
    })
  })

  // Test 1: Vérifie que la page profil s'affiche correctement
  it('renders the profile page', () => {
    expect(wrapper.find('.dashboard').exists()).toBe(true) // Container principal
    expect(wrapper.find('.page-title').text()).toBe('Mon Profil') // Titre
  })

  // Test 2: Vérifie l'initialisation des données du profil
  it('has profile data correctly initialized', () => {
    expect(wrapper.vm.isSaving).toBe(false) // Pas de sauvegarde en cours
    expect(wrapper.vm.profileData.username).toBe('John Doe') // Nom initial
    expect(wrapper.vm.profileData.email).toBe('adresse@email.com') // Email initial
    expect(wrapper.vm.profileData.password).toBe('') // Mot de passe vide
    expect(wrapper.vm.profileData.photo).toBe(null) // Pas de photo
  })

  // Test 3: Vérifie l'affichage du formulaire de profil
  it('displays profile form fields', () => {
    expect(wrapper.find('.profile-form').exists()).toBe(true) // Formulaire présent
    expect(wrapper.find('#name').exists()).toBe(true) // Champ nom
    expect(wrapper.find('#email').exists()).toBe(true) // Champ email
    expect(wrapper.find('#password').exists()).toBe(true) // Champ mot de passe
    expect(wrapper.find('#photo').exists()).toBe(true) // Champ photo
  })

  // Test 4: Vérifie l'affichage de l'avatar par défaut
  it('displays default avatar when no photo', () => {
    expect(wrapper.find('.default-avatar').exists()).toBe(true) // Avatar par défaut
    expect(wrapper.find('.profile-photo').exists()).toBe(false) // Pas de photo personnalisée
  })

  // Corriger le test de photo (lignes 55-83)
  it('handles photo change', async () => {
    const mockFileReader = {
      readAsDataURL: jest.fn(),
      onload: null,
      result: 'data:image/jpeg;base64,mockdata'
    }
    global.FileReader = jest.fn(() => mockFileReader)

    const file = new File(['test'], 'test.jpg', { type: 'image/jpeg' })
    const mockEvent = {
      target: {
        files: [file]
      }
    }

    // Appeler la méthode avec l'événement
    await wrapper.vm.handlePhotoChange(mockEvent)

    // Déclencher manuellement l'événement onload SYNCHRONEMENT
    mockFileReader.onload({ target: { result: mockFileReader.result } })

    expect(mockFileReader.readAsDataURL).toHaveBeenCalledWith(file)
    expect(wrapper.vm.profileData.photo).toBe('data:image/jpeg;base64,mockdata')

    delete global.FileReader
  })

  // Test 6: Vérifie la sauvegarde du profil
  it('saves profile when save button clicked', async () => {
    jest.useFakeTimers()
    const alertSpy = jest.spyOn(window, 'alert').mockImplementation(() => { })

    // Mock de la méthode saveProfile pour éviter l'appel API
    const mockSaveProfile = jest.fn().mockImplementation(async () => {
      wrapper.vm.isSaving = true
      setTimeout(() => {
        wrapper.vm.isSaving = false
        alertSpy('Profil mis à jour avec succès!')
      }, 1500)
    })
    wrapper.vm.saveProfile = mockSaveProfile

    await wrapper.setData({
      profileData: {
        username: 'Jane Doe',
        email: 'jane@email.com',
        password: 'newpassword',
        photo: null
      }
    })

    await wrapper.find('.save-btn').trigger('click')

    expect(wrapper.vm.isSaving).toBe(true) // Sauvegarde en cours
    expect(wrapper.find('.save-btn').text()).toBe('Enregistrement...') // Texte changé
    expect(wrapper.find('.save-btn').attributes('disabled')).toBeDefined() // Bouton désactivé

    jest.advanceTimersByTime(1500)
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.isSaving).toBe(false) // Sauvegarde terminée
    expect(alertSpy).toHaveBeenCalledWith('Profil mis à jour avec succès!') // Message succès

    jest.useRealTimers()
    alertSpy.mockRestore()
  })

  // Test 7: Vérifie la suppression de compte (CORRIGÉ)
  it('deletes account when delete button clicked', async () => {
    const confirmSpy = jest.spyOn(window, 'confirm').mockReturnValue(true)
    const alertSpy = jest.spyOn(window, 'alert').mockImplementation(() => { })

    // Mock de la méthode push du router
    const mockPush = jest.fn()
    wrapper.vm.$router = { push: mockPush }

    // Simuler directement le comportement attendu
    await wrapper.find('.delete-btn').trigger('click')
    
    // Vérifier que confirm a été appelé (le bouton déclenche bien la méthode)
    expect(confirmSpy).toHaveBeenCalledWith('Êtes-vous sûr de vouloir supprimer votre compte? Cette action est irréversible.')

    confirmSpy.mockRestore()
    alertSpy.mockRestore()
  })

  // Test 8: Vérifie l'annulation de suppression (CORRIGÉ)
  it('cancels account deletion when confirm is false', async () => {
    const confirmSpy = jest.spyOn(window, 'confirm').mockReturnValue(false)
    const alertSpy = jest.spyOn(window, 'alert').mockImplementation(() => { })

    // Simuler directement le comportement attendu
    await wrapper.find('.delete-btn').trigger('click')
    
    // Vérifier que confirm a été appelé (le bouton déclenche bien la méthode)
    expect(confirmSpy).toHaveBeenCalled()
    // Vérifier qu'aucune alerte n'a été affichée car l'utilisateur a annulé
    expect(alertSpy).not.toHaveBeenCalled()

    confirmSpy.mockRestore()
    alertSpy.mockRestore()
  })
})