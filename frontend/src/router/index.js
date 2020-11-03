import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Dashbord from '../views/Dashbord.vue'
import store from '../store/index.js'
import Ecole from '../views/Ecole.vue'
import Logout from '../views/Logout.vue'
import Formation from '../views/Formation.vue'
import Candidature from '../views/Candidature.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Dashbord',
    component: Dashbord,
    meta: {
      requiresAuth: true,
      requiresAdmin: false
    }
  },
  {
    path: '/formation/:id?',
    name: 'Formation',
    component: Formation,
    meta: {
      requiresAuth: true,
      requiresAdmin: false
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: Home,
    meta: {
      requiresAuth: false,
      requiresAdmin: false
    }
  },
  {
    path: '/ecole/:id?',
    name: 'Ecole',
    component: Ecole,
    meta: {
      requiresAuth: true,
      requiresAdmin: false
    }
  },
  {
    path: '/candidature/:idC?/:idF?',
    name: 'Candidature',
    component: Candidature,
    meta: {
      requiresAuth: true,
      requiresAdmin: false
    }
  },
  {
    path: '/logout',
    name: 'Logout',
    component: Logout,
    meta: {
      requiresAuth: true,
      requiresAdmin: false
    }
  },
  {
    path: '/about',
    name: 'About',
    meta: {
      requiresAuth: true,
      requiresAdmin: false
    },

    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  console.debug("route "+to.name+" from"+from.name)
  if(to.name == null)
    next({ name: 'Login' })
  if(to.name == 'Login' && store.state.logged){
    next({ name: 'Dashbord' })
  }
  if (to.matched.some(record => record.meta.requiresAuth)) {
    
    console.debug("logged "+store.state.logged)
    // this route requires auth, check if logged in
    // if not, redirect to login page.
    if (!store.getters.logged) {
      console.debug("to loggin")
      next({ name: 'Login' })
    } else {
      next() // go to wherever I'm going
    }
  } else {
    next() // does not require auth, make sure to always call next()!
  }
})

export default router
