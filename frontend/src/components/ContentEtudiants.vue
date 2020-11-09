<template>
  <!-- Main Content -->
  <div id="content">
    <!-- Topbar -->
    <NavbarC> </NavbarC>
    <!-- End of Topbar -->

    <!-- Begin Page Content -->
    <div class="container-fluid">
      <!-- Page Heading -->
      <div class="d-sm-flex align-items-center justify-content-between mb-4">
        <h1 v-if="0==user.rank" class="h3 mb-0 text-gray-800">
          Etudiants
        </h1>
      </div>

      <!-- Content Row -->
      <div class="row mb-3" v-if="etudiantSelected !== null">
        <div class="col-md-6 text-left">
          <div>
            <b-card
              :title="etudiantSelected.nom"
              :sub-title="etudiantSelected.prenom"
            >
              
              

               

               

              <a
                v-on:click="trash()"
                class="d-none ml-2 text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm"
                ><i class="fas fa-trash-alt"></i
              ></a>
            </b-card>
          </div>
        </div>
        <div class="col-md-6">
          <b-card no-body class="full-width">
            <b-tabs card>
              <b-tab title="Candidature" active>
                 
              </b-tab>
              
            </b-tabs>
          </b-card>
        </div>
      </div>
      <!-- Content Row -->
      
      
    
      <!-- Content Row -->
      <div class="row">
        <!-- Content Column -->
        <div class="col-md-8 mb-4">
          <!-- Project Card Example -->
          <div class="card shadow mb-4">
            <div class="card-header py-3">
              <h6 class="m-0 font-weight-bold text-primary">Les étudiants</h6>
            </div>
            <div class="card-body">
              <div class="candidature-area">
                <ul class="list-group">
                  <li class="list-group-item" v-for="item in allEtudiants" :key="item.id" >
                    

                    <div v-if="user.rank==0" class="row align-items-center">
                      <div class="col-sm-2">
                        {{item.nom | capitalize}}
                        {{item.prenom | firstLetter}}.
                      </div>
                      <div class="col-sm-7">
                        
                      </div>
                      <div class="col-sm-3">
                        <a
                           
                          class="d-none ml-2 text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm"
                        >
                          <i class="fas fa-envelope fa-fw"></i>
                          <!-- Counter - Messages -->
                          <span
                            class="badge badge-danger badge-counter"
                            >{{item.ap}}</span
                          >
                        </a>

                        <a
                          v-on:click="setCandidature(item.id_candidature)"
                          class="d-none ml-2 text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm"
                          ><i class="fas fa-search"></i
                        ></a>
                        <a
                          v-on:click="trash(item)"
                          class="d-none ml-2 text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm"
                          ><i class="fas fa-trash-alt"></i
                        ></a>
                      </div>
                    </div>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-4 mb-4">
          <div class="card shadow mb-4">
            <div class="card-header py-3">
              <h6 class="m-0 font-weight-bold text-primary">
                Filtre Etuidants
              </h6>
            </div>
            <div class="card-body">
              <p class="d-inline">
                <vue-single-select
                  v-model="hasMessage"
                  placeholder="Messages"
                  :options="[{'titre':'OUI','id':true},{'titre':'NON','id':false}]"
                  option-label="titre"
                ></vue-single-select>
                <vue-single-select
                  name="maybe"
                  placeholder="Candidature"
                  v-model="hasCandidature"
                 :options="[{'titre':'OUI','id':true},{'titre':'NON','id':false}]"
                  option-label="titre"
                ></vue-single-select>
              
                <vue-single-select
                  name="maybe"
                  placeholder="Nom d'etudiant"
                  v-model="etudiantSelected"
                  :options="allEtudiants"
                  option-label="nom"
                ></vue-single-select>
              </p>
              <a class="d-none text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm mr-3"  >Exporter</a >
              <a class="d-none text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm mr-3"  >Ajouter</a >
              <a class="d-none text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm mr-3"  >Importer</a >
            </div>
          </div>
          <!-- Illustrations -->

          <!-- Approach -->
        </div>
      </div>

      <!-- Ecole -->
      
    </div>

    <!-- /.container-fluid -->
  </div>
  <!-- End of Main Content -->
</template>

<script>
  import { mapState, mapActions } from 'vuex';
  import NavbarC from './NavBarCustom.vue';
  import axios from 'axios';


  export default {
    name:"Content",
    components: {
    NavbarC
    },
    data() {
      return {
        email: '',
        password: '',
        allCandidatures:[],
        allEtudiants:[],
        hasMessage:null,
        etudiantSelected:null,
        hasCandidature:null

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
      ]),

     
    },
    methods: {
      ...mapActions([

      ]),
      
      
      fetchData () {
         
      axios({
            method: 'get',
            url: 'users/',
            auth: {
              username: this.user.mail,
              password: this.user.pwd
            }
        })
      .then(response => {

         this.allEtudiants=response.data
         console.debug(this.allEtudiants)


      })
      .catch(error => {
        console.debug(error)
      })

      axios({
            method: 'get',
            url: 'candidatures/',
            auth: {
              username: this.user.mail,
              password: this.user.pwd
            }
        })
      .then(response => {

         this.allCandidatures=response.data


      })
      .catch(error => {
        console.debug(error)
      })

       

    }


    },
    filters: {
      len: function(value){
          return value.length
      },
      lenComplete: function(value){
        var i=0


        value.forEach(element => {

          if (element.etat==4)
           i=i+1
        });

        //  this.firstD = this.timeConverter(min)
        return value.length - i
      },

      etat2pourcent: function(value){
          return value*20
      },
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

.candidature-area {
  /*   border: 1px solid #ccc; */
  background: white;
  max-height: 30vh;
  padding: 1em;
  overflow: auto;

  margin: 0 auto 2em auto;
}

</style>
