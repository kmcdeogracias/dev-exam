import Vue from 'vue'
import Vuetify from 'vuetify'
import Router from 'vue-router'
import OpenFda from '@/components/OpenFda'
import 'vuetify/dist/vuetify.min.css'

Vue.use(Vuetify, {
  theme: {
    primary: '#3f51b5',
    secondary: '#b0bec5',
    accent: '#8c9eff',
    error: '#b71c1c'
  }
})

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'OpenFda',
      component: OpenFda
    }
  ]
})
