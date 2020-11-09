<template>
  <div id="wrapper">
    <Sidepanel msg="Welcome to Your Vue.js App"/>
    <div id="content-wrapper" class="d-flex flex-column">
    <Content />

    <Footer />
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import Sidepanel from '@/components/Sidepanel.vue'
 
import Content from '@/components/ContentEtudiants.vue'

import Footer from '@/components/Footer.vue'


export default {
  name: 'Etuidants',
  components: {
    Sidepanel,
    Content,
    Footer
  }
}
</script>
