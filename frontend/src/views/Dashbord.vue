<template>
  <div id="wrapper">
    <Sidepanel msg="Welcome to Your Vue.js App"/>
    <div id="content-wrapper" class="d-flex flex-column">
      
      <Content v-if="user.rank==2" />
       
       
      <ContentAdmin v-if="user.rank==0"  />
   

      <Footer />
      </div>
  </div>
</template>

<script>
// @ is an alias to /src
import Sidepanel from '@/components/Sidepanel.vue'
import Content from '@/components/Content.vue'
import ContentAdmin from '@/components/ContentAdmin.vue'
import Footer from '@/components/Footer.vue'
import { mapState, mapActions } from 'vuex';


export default {
  name: 'Dashbord',
  components: {
    Sidepanel,
    Content,
    Footer,
    ContentAdmin
  },
  computed: {
      ...mapState([
        'loggingIn',
        'loginError',
        'accessToken',
        'logged',
        'user'
      ])
  },
  methods: {

      ...mapActions([
         
      ])
  }
}
</script>
