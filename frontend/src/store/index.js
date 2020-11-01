import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import router from '../router'
import createPersistedState from 'vuex-persistedstate'

Vue.use(Vuex)

export default new Vuex.Store({
  plugins: [createPersistedState()],
  state: {
    accessToken: null,
    loggingIn: false,
    loginError: null,
    logged:null,
    user:null,
    pwd:""
  },
  getters: {
    logged: state => {
      console.debug(state.logged)
      return state.logged
    },
    user: state => {
      console.debug(state.logged)
      return state.user
    }},
  mutations: {
    logoutM:(state)=>{
      state.logged=false;
      state.accessToken=null;
      state.user=null;
    },
    setUser: (state,user)=>{
      state.user = user
    },
    setLogged: (state, m) => {
      console.debug(m)
      state.logged = m;
    },
    setPwd: (state, m) => {
      console.debug(m)
      state.user.pwd = m;
    },
    loginStart: state => state.loggingIn = true,
    loginStop: (state, errorMessage) => {
      state.loggingIn = false;
      state.loginError = errorMessage;
    },
    updateAccessToken: (state, accessToken) => {
      state.accessToken = accessToken;
    }
  },
  actions: {
    logout({ commit }){
      console.debug("logout action")
      commit('logoutM')
      router.push("/")
    },
    doLogin({ commit }, loginData) {
      commit('loginStart');
      
      
      axios.post('http://127.0.0.1:5000/api/token', {}, {
        auth: {
          username: loginData.email,
          password: loginData.password
        }
      })
      .then(response => {
        localStorage.setItem('accessToken', response.data.token);
        commit('loginStop', null);
        commit('setLogged', true);
        commit('setUser',response.data.user)
        commit('setPwd',loginData.password);
        commit('updateAccessToken', response.data.token);
        axios.defaults.headers.common['Authorization'] = response.data.token
        router.push("/")
         
      })
      .catch(error => {
        commit('loginStop', error.response.data.error);
        commit('updateAccessToken', null);
      })
    },
    fetchAccessToken({ commit }) {
      commit('updateAccessToken', localStorage.getItem('accessToken'));
    }
  }
})
