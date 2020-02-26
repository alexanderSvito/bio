import Main from './pages/Main.vue'
import Register from './pages/Register.vue'
import VueRouter from 'vue-router'


const routes = [
  { path: '/', component: Main },
  { path: '/register', component: Register, name: 'Register' }
]

export default new VueRouter({
  mode: 'history',
  routes // short for `routes: routes`
})
