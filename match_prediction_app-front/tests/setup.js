import { config } from '@vue/test-utils'

config.global.stubs = {
  'router-link': true,
  'router-view': true
}

// Mocks API complets
global.fetch = jest.fn((url) => {
  if (url.includes('/history')) {
    return Promise.resolve([
      { date: '2024-03-12', match: 'PSG vs Marseille', prediction: '2-1', actual: '2-0', isCorrect: false },
      { date: '2024-03-13', match: 'Lyon vs Nice', prediction: '1-1', actual: '1-1', isCorrect: true },
      { date: '2024-03-14', match: 'Monaco vs Bordeaux', prediction: '3-0', actual: '3-1', isCorrect: true }
    ])
  }
  if (url.includes('/dashboard') || url.includes('/matches')) {
    return Promise.resolve({
      data: [
        { id: 1, homeTeam: 'PSG', awayTeam: 'Marseille', time: '20:00' },
        { id: 2, homeTeam: 'Lyon', awayTeam: 'Nice', time: '21:00' },
        { id: 3, homeTeam: 'Monaco', awayTeam: 'Bordeaux', time: '19:00' }
      ]
    })
  }
  return Promise.resolve({ data: [] })
})