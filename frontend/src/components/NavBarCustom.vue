<template>
 
<nav class="navbar navbar-expand navbar-light bg-white topbar mb-4 static-top shadow">

          <!-- Sidebar Toggle (Topbar) -->
          <button id="sidebarToggleTop" class="btn btn-link d-md-none rounded-circle mr-3">
            <i class="fa fa-bars"></i>
          </button>

          <!-- Topbar Search -->
          <form class="d-none d-sm-inline-block form-inline mr-auto ml-md-3 my-2 my-md-0 mw-100 navbar-search">
            <div class="input-group">
              <input type="text" class="form-control bg-light border-0 small" placeholder="Search for..." aria-label="Search" aria-describedby="basic-addon2">
              <div class="input-group-append">
                <button class="btn btn-primary" type="button">
                  <i class="fas fa-search fa-sm"></i>
                </button>
              </div>
            </div>
          </form>

          <!-- Topbar Navbar -->
          <ul class="navbar-nav ml-auto">

            <!-- Nav Item - Search Dropdown (Visible Only XS) -->
            <li class="nav-item dropdown no-arrow d-sm-none">
              <a class="nav-link dropdown-toggle" href="#" id="searchDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                <i class="fas fa-search fa-fw"></i>
              </a>
              <!-- Dropdown - Messages -->
              <div class="dropdown-menu dropdown-menu-right p-3 shadow animated--grow-in" aria-labelledby="searchDropdown">
                <form class="form-inline mr-auto w-100 navbar-search">
                  <div class="input-group">
                    <input type="text" class="form-control bg-light border-0 small" placeholder="Search for..." aria-label="Search" aria-describedby="basic-addon2">
                    <div class="input-group-append">
                      <button class="btn btn-primary" type="button">
                        <i class="fas fa-search fa-sm"></i>
                      </button>
                    </div>
                  </div>
                </form>
              </div>
            </li>

             

            <!-- Nav Item - Messages -->
            <li class="nav-item dropdown no-arrow mx-1">
              <a class="nav-link dropdown-toggle" href="#" id="messagesDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                
                <!-- Counter - Messages -->
                 {{user.prenom | capitalize }} {{user.nom | firstLetter}}.
              </a>
              <!-- Dropdown - Messages -->
               
            </li>

            <!-- Nav Item - Messages -->
            <li class="nav-item dropdown no-arrow mx-1">
              <a class="nav-link dropdown-toggle" href="/candidature" id="messagesDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                <i class="fas fa-envelope fa-fw"></i>
                <!-- Counter - Messages -->
                <span v-if="nbMessage!=0" class="badge badge-danger badge-counter">{{nbMessage}}</span>
              </a>
              <!-- Dropdown - Messages -->
               
            </li>

            <div class="topbar-divider d-none d-sm-block"></div>

            <!-- Nav Item - User Information -->
          <li class="nav-item dropdown no-arrow mx-1">
              <a class="nav-link dropdown-toggle" href="/user" id="messagesDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                <i class="fas fa-user-cog"></i>
              </a>
              <!-- Dropdown - Messages -->
               
            </li>

            
            <div class="topbar-divider d-none d-sm-block"></div>
              <li class="nav-item dropdown no-arrow mx-1">
              <a class="nav-link dropdown-toggle" href="/logout"   role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                <i class="fas fa-sign-out-alt"></i>
                <!-- Counter - Messages -->
                 
              </a>
              <!-- Dropdown - Messages -->
               
            </li>


          </ul>

        </nav>

      
      
</template>

<script>
  import { mapState, mapActions } from 'vuex';
  import axios from 'axios';

  export default {
    data() {
      return {
        email: '',
        password: '',
        nbMessage:0
      }
    },
    created () {
        this.fetchData()
  
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
      ,
      fetchData () {
        axios({
            method: 'get',
            url: 'actionpe/count_user/'+this.user.id,
            auth: {
              username: this.user.mail,
              password: this.user.pwd
            }
        })
      .then(response => {

         this.nbMessage=response.data.nb
         console.debug("nb ",response.data)

      })
      .catch(error => {
        console.debug(error)
      })

      }
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
  @import "node_modules/bootstrap/scss/bootstrap.scss";
  @import "../assets/sb-admin-2.min.css";


 

</style>