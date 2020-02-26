import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)


export default new Vuex.Store({
  state: {
    user: null
  },
  getters: {
    getUser: state => {
      return state.user
    },
    isAuthenticated: state => {
      return state.user !== null
    }
  },
  mutations: {
    increment (state) {
      state.count++
    }
  }
})
