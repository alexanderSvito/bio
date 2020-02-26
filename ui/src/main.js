import Vue from 'vue'
import Vuex from 'vuex'
import App from './App.vue'
import VueRouter from 'vue-router'



Vue.config.productionTip = false

Vue.use(VueRouter)
Vue.use(Vuex)

import router from './router.js'
import store from './store.js'
import vuetify from './plugins/vuetify';

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
