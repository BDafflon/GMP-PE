<template>
  <!-- Sidebar -->
    <ul class="navbar-nav bg-gradient-primary sidebar sidebar-dark accordion" id="accordionSidebar">

      <!-- Sidebar - Brand -->
      <a class="sidebar-brand d-flex align-items-center justify-content-center" href="index.html">
        <div class="sidebar-brand-icon rotate-n-15">
           
        </div>
        <div class="sidebar-brand-text mx-3">PE-GMP <sup>2020</sup></div>
      </a>

      <!-- Divider -->
      <hr class="sidebar-divider my-0">

      <!-- Nav Item - Dashboard -->
      <li class="nav-item active">
        <a class="nav-link" href="/">
          <i class="fas fa-fw fa-tachometer-alt mr-2"></i>
          <span>Tableau de bord</span></a>
      </li>

      <!-- Divider -->
      <hr class="sidebar-divider">
      <div class="sidebar-heading">
        Candidatures
      </div>
      <!-- Heading -->
      <div v-if="2==user.rank" >
      <!-- Nav Item - Pages Collapse Menu -->
      <li class="nav-item active">
        <a class="nav-link" href="/candidature/">
          <i class="fas fa-file-alt mr-2"></i>
          <span>Mes candidatures</span></a>
      </li>

       
      
      </div>
      <div v-else> 
        <li class="nav-item active">
                <a class="nav-link" href="/candidature/">
                  <i class="fas fa-file-alt mr-2"></i>
                  <span>Les candidatures</span></a>
              </li>
              <li class="nav-item active">
                <a class="nav-link" href="/etuidants">
                  <i class="fas fa-user-cog mr-2"></i>
                  <span>Les étudiants</span></a>
              </li>
         

      </div>
      <!-- Divider -->
      <hr class="sidebar-divider">

      <!-- Heading -->
      <div class="sidebar-heading">
        Poursuite d'etudes
      </div>

      <!-- Nav Item - Pages Collapse Menu -->
      <li class="nav-item active">
        <a class="nav-link" href="/guide">
          <i class="fas fa-book mr-2"></i>
          <span>Guide</span></a>
      </li>

      <li class="nav-item active">
        <a class="nav-link" href="/forum">
          <i class="fas fa-book mr-2"></i>
          <span>Forum</span></a>
      </li>

      <!-- Nav Item - Charts -->
      <li class="nav-item active">
        <a class="nav-link" href="/ecole">
          <i class="fas fa-university mr-2"></i>
          <span>Les écoles</span></a>
      </li>

      <!-- Nav Item - Tables -->
      <li class="nav-item active">
        <a class="nav-link" href="/formation">
          <i class="fas fa-graduation-cap mr-2"></i>
          <span>Les formations</span></a>
      </li>

       
      <!-- Divider -->
      <hr class="sidebar-divider d-none d-md-block">

      <!-- Sidebar Toggler (Sidebar) -->
      <li class="nav-item active">
        <a class="nav-link" href="/logout">
          <i class="fas fa-sign-out-alt mr-2"></i>
          <span>Déconnexion</span></a>
      </li>

    </ul>
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
         
      ])
    },
    filters: {
      capitalize: function (value) {
        if (!value) return ''
        value = value.toString()
        return value.charAt(0).toUpperCase() + value.slice(1)
      },
      firstLetter: function (value) {
        if (!value) return ''
        value = value.toString()
        return value.charAt(0).toUpperCase() 
      }
    }
  }
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss">
  @import "../assets/custom.scss";
  @import "../assets/sb-admin-2.min.css";
  @import "node_modules/bootstrap/scss/bootstrap.scss";

.sidenav {
  height: 100%;
  width: 160px;
  position: fixed;
  z-index: 1;
  top: 0;
  left: 0;
  background-color: #111;
  overflow-x: hidden;
  padding-top: 20px;
  margin-top: 50px;
}

.sidenav a {
  padding: 6px 8px 6px 16px;
  text-decoration: none;
  font-size: 25px;
  color: #818181;
  display: block;
}

.sidenav a:hover {
  color: #f1f1f1;
}

</style>