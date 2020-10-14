import Main from './pages/Main.vue'
import Register from './pages/Register/Start.vue'
import RegisterEmail from './pages/Register/Email.vue'
import RegisterPhone from './pages/Register/Phone.vue'
import RegisterID from './pages/Register/ID.vue'
import RegisterPassword from './pages/Register/Password.vue'
import VueRouter from 'vue-router'


const routes = [
  { path: '/', component: Main, name: 'Main' },
  { path: '/register', component: Register, name: 'Register' },
  { path: '/register/email', component: RegisterEmail, name: 'RegisterEmail' },
  { path: '/register/phone', component: RegisterPhone, name: 'RegisterPhone' },
  { path: '/register/documents', component: RegisterID, name: 'RegisterID' },
  { path: '/register/password', component: RegisterPassword, name: 'RegisterPassword' }
]

export default new VueRouter({
  mode: 'history',
  routes // short for `routes: routes`
})
