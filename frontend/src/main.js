import Vue from 'vue'
import App from './App.vue'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import router from './router'
import store from './store'
import '@fortawesome/fontawesome-free/css/all.css'
import '@fortawesome/fontawesome-free/js/all.js'
import VueSingleSelect from "vue-single-select"
import vSelect from 'vue-select'
import 'vue-select/dist/vue-select.css';
import Axios from 'axios'

Vue.component('v-select', vSelect)
Vue.component('vue-single-select', VueSingleSelect);
Vue.use(BootstrapVue, {bsidebar:{width:'200px'}})
 
Vue.config.productionTip = false

Axios.defaults.baseURL = 'http://localhost:5000/api/'



new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
