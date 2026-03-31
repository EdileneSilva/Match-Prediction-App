import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import PredictionView from '../views/PredictionView.vue'
import HistoryView from '../views/HistoryView.vue'
import ProfileView from '../views/ProfileView.vue'
import ForgotView from '../views/ForgotView.vue'
import LandingView from '../views/LandingView.vue'
import ResetView from '../views/ResetView.vue'
import StatisticsView from '../views/StatisticsView.vue'

const routes = [
  {
    path: '/',
    name: 'landing',
    component: LandingView,
    meta: { guestOnly: true, transition: 'fade' }
  },
  {
    path: '/dashboard',
    name: 'home',
    component: HomeView,
    meta: { requiresAuth: true, transition: 'slide' }
  },
  {
    path: '/statistics',
    name: 'statistics',
    component: StatisticsView,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { guestOnly: true, transition: 'fade' }
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView,
    meta: { guestOnly: true, transition: 'fade' }
  },
  {
    path: '/predictions',
    name: 'predictions',
    component: PredictionView,
    meta: { requiresAuth: true, transition: 'scale' }
  },
  {
    path: '/history',
    name: 'history',
    component: HistoryView,
    meta: { requiresAuth: true, transition: 'slide' }
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProfileView,
    meta: { requiresAuth: true, transition: 'slide' }
  },
  {
    path: '/forgot-password',
    name: 'forgot-password',
    component: ForgotView,
    meta: { guestOnly: true, transition: 'fade' }
  },
  {
    path: '/reset-password',
    name: 'reset-password',
    component: ResetView,
    meta: { guestOnly: true, transition: 'fade' }
  },
  {
    path: '/exit',
    name: 'exit',
    beforeEnter: (to, from, next) => {
      localStorage.removeItem('token');
      next('/login');
    }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')

  if (to.meta.requiresAuth && !token) {
    next({ name: 'login' })
  } else if (to.meta.guestOnly && token) {
    next({ name: 'home' })
  } else {
    next()
  }
})

export default router