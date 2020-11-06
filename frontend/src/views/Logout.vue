 
<template>
   <h1> logout </h1>
</template>

<script>
  import { mapState, mapActions } from 'vuex';

  export default {
    data() {
      return {
        email: '',
        password: ''
      }
    },
    created () {
      console.debug("create logout")
      this.logout();
  },
    computed: {
      ...mapState([
'apiurl',
        'loggingIn',
        'loginError',
        'accessToken',
        'logged',
        'user'
      ])
    },
    methods: {
      ...mapActions([
        'doLogin',
        'logout'
      ]),

      loginSubmit() {
        this.doLogin({
          email: this.email,
          password: this.password
        });
      }
    }
  }
</script>