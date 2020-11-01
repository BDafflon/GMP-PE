<template>
<div id="login" class="text-center">
  <div class="login w-100 p-3"> 
     

    <form class="form-signin " @submit.prevent="loginSubmit"  style="max-width: 330px" >
       
      <h1 class="h3 mb-5 font-weight-normal"  >Poursuite d'étude GMP</h1>
      
      <label for="inputEmail" class="sr-only">Email address</label>
      <input v-model="email" type="email" id="inputEmail" class="form-control" placeholder="Email address" required autofocus>
      <label for="inputPassword" class="sr-only">Password</label>
      <input v-model="password" type="password" id="inputPassword" class="form-control" placeholder="Password" required>
       
      <button class="btn btn-lg btn-primary btn-block mt-4" type="submit">Connexion</button>
      <div class="mt-4">
        <a href="#"  >mot de passe oublié</a>
      </div>
      
    </form>

    </div>
  </div>

  
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
    computed: {
      ...mapState([
        'loggingIn',
        'loginError',
        'accessToken'
      ])
    },
    methods: {
      ...mapActions([
        'doLogin'
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


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss">
  @import "../assets/custom.scss";
  @import "node_modules/bootstrap/scss/bootstrap.scss";

  .login {
  height: 100vh;  
  display: -ms-flexbox;
  display: -webkit-box;
  display: flex;
  -ms-flex-align: center;
  -ms-flex-pack: center;
  -webkit-box-align: center;
  align-items: center;
  -webkit-box-pack: center;
  justify-content: center;
  padding-top: 40px;
  padding-bottom: 40px;
  background-color: #f5f5f5;
}

.form-signin {
  width: 100%;
  max-width: 330px;
  padding: 15px;
  margin: 0 auto;
}
.form-signin .checkbox {
  font-weight: 400;
}
.form-signin .form-control {
  position: relative;
  box-sizing: border-box;
  height: auto;
  padding: 10px;
  font-size: 16px;
}
.form-signin .form-control:focus {
  z-index: 2;
}
.form-signin input[type="email"] {
  margin-bottom: -1px;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
}
.form-signin input[type="password"] {
  margin-bottom: 10px;
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}

</style>