import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import PredictionView from '../views/PredictionView.vue'
import HistoryView from '../views/HistoryView.vue'
import ProfileView from '../views/ProfileView.vue'
import ForgotView from '../views/ForgotView.vue'
import ResetView from '../views/ResetView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView
  },
  {
    path: '/predictions',
    name: 'predictions',
    component: PredictionView
  },
  {
    path: '/history',
    name: 'history',
    component: HistoryView
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProfileView
  },
  {
    path: '/forgot-password',
    name: 'forgot-password',
    component: ForgotView
  },
  {
    path: '/reset-password',
    name: 'reset-password',
    component: ResetView
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
  routes
})

export default router