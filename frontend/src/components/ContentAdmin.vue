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
          Tableau de bord d'administration
        </h1>
      </div>

      <!-- Content Row -->

      <!-- Content Row -->

      <!-- Content Row -->
      <div class="row">
        <!-- Content Column -->
        <div class="col-md-8 mb-4">
          <!-- Project Card Example -->
          <div class="card shadow mb-4">
            <div class="card-header py-3">
              <h6 class="m-0 font-weight-bold text-primary">Candidatures</h6>
            </div>
            <div class="card-body">
              <div class="candidature-area">
                <ul class="list-group">
                  {{allCandidatures}}
                  <li class="list-group-item" v-for="item in allCandidatures" :key="item.id_candidature" >
                    

                    <div v-if="user.rank==0" class="row align-items-center">
                      <div class="col-sm-2">
                        {{item.nom_etudiant.nom | capitalize}}
                        {{item.nom_etudiant.prenom | firstLetter}}.
                      </div>
                      <div class="col-sm-7">
                        {{item.ecole.nom}} - {{item.formation.nom}}
                      </div>
                      <div class="col-sm-3">
                        <a
                          v-if="item.ap != 0"
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
                Filtre Candidature
              </h6>
            </div>
            <div class="card-body">
              <p class="d-inline">
                <vue-single-select
                  v-model="selectAlternance"
                  placeholder="Messages"
                  :options="[{'titre':'OUI','id':true},{'titre':'NON','id':false}]"
                  option-label="titre"
                ></vue-single-select>
                <vue-single-select
                  name="maybe"
                  placeholder="Ecole"
                  v-model="ecoleSelected"
                  :options="allEcoles"
                  option-label="nom_ecole"
                ></vue-single-select>
                <vue-single-select
                  name="maybe"
                  placeholder="Formation"
                  v-model="selectedFormation"
                  :options="allFormations"
                  option-label="specialite"
                ></vue-single-select>
                <vue-single-select
                  name="maybe"
                  placeholder="Nom d'etudiant"
                  v-model="etudiantSelected"
                  :options="allEtudiants"
                  option-label="specialite"
                ></vue-single-select>
              </p>
              <a
                class="d-none text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm"
                >Exporter</a
              >
            </div>
          </div>
          <!-- Illustrations -->

          <!-- Approach -->
        </div>
      </div>

      <div class="row">
        <!-- Content Column -->
        <div class="col-md-8 mb-4">
          <!-- Project Card Example -->
          <div class="card shadow mb-4">
            <div class="card-header py-3">
              <h6 class="m-0 font-weight-bold text-primary">Formation</h6>
            </div>
            <div class="card-body">
              <div class="candidature-area">
                <ul class="list-group">
                  
                  <li class="list-group-item" v-for="item in allFormations" :key="item.id_formation" >
                   
                     

                    <div v-if="user.rank==0" class="row align-items-center">
                      <div class="col-sm-4">
                       {{item.specialite}}
                      </div>
                      <div class="col-sm-5">
                       {{item.nom_ecole}}
                      </div>
                      <div class="col-sm-3">
                        <a
                          v-if="item.ap != 0"
                          class="d-none ml-2 text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm">
                          <i class="fas fa-envelope fa-fw"></i>
                          <!-- Counter - Messages -->
                         
                        </a>
                        <a
                          v-if="item.ap != 0"
                          class="d-none ml-2 text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm">
                          <i class="fas fa-envelope fa-fw"></i>
                          <!-- Counter - Messages -->
                         
                        </a>


                         
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
                Filtre Formation
              </h6>
            </div>
            <div class="card-body">
              <p class="d-inline">
                <vue-single-select
                  v-model="selectAlternance"
                  placeholder="A valider"
                  :options="[{'titre':'OUI','id':true},{'titre':'NON','id':false}]"
                  option-label="titre"
                ></vue-single-select>
                <vue-single-select
                  name="maybe"
                  placeholder="A Modifier"
                  v-model="ecoleSelected"
                  :options="allEcoles"
                  option-label="nom_ecole"
                ></vue-single-select>
                <vue-single-select
                  name="maybe"
                  placeholder="Ecole"
                  v-model="ecoleSelected"
                  :options="allEcoles"
                  option-label="specialite"
                ></vue-single-select>
                <vue-single-select
                  name="maybe"
                  placeholder="Formation"
                  v-model="selectedFormation"
                  :options="allFormations"
                  option-label="specialite"
                ></vue-single-select>
                <vue-single-select
                  name="maybe"
                  placeholder="Ville"
                  v-model="selectedFormation"
                  :options="allFormations"
                  option-label="specialite"
                ></vue-single-select>
              </p>
              <a
                class="d-none text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm"
                >Exporter</a
              >
              <a
                class="d-none text-white mt-2 mr-2 ml-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm"
                >Importer</a
              >
            </div>
          </div>
          <!-- Illustrations -->

          <!-- Approach -->
        </div>
      </div>

      <!-- Ecole -->
      <div class="row">
        <!-- Content Column -->
        <div class="col-md-8 mb-4">
          <!-- Project Card Example -->
          <div class="card shadow mb-4">
            <div class="card-header py-3">
              <h6 class="m-0 font-weight-bold text-primary">Ecole</h6>
            </div>
            <div class="card-body">
              <div class="candidature-area">
                <ul class="list-group">
                  <li  class="list-group-item" v-for="item in allEcoles" :key="item.id_ecole" >
             
                    <div class="row align-items-center">
                      
                       
                      <div class="col-sm-4">
                        {{item.nom_ecole}}
                      </div>
                      <div class="col-sm-4">
                       {{item.adresse.ville}}
                      </div>
                      <div class="col-sm-4">
                       <a
                          v-if="item.ap != 0"
                          class="d-none ml-2 text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm">
                          <i class="fas fa-envelope fa-fw"></i>
                          <!-- Counter - Messages -->
                         
                        </a>
                         <a
                          v-if="item.ap != 0"
                          class="d-none ml-2 text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm">
                          <i class="fas fa-envelope fa-fw"></i>
                          <!-- Counter - Messages -->
                         
                        </a>
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
              <h6 class="m-0 font-weight-bold text-primary">Filtre Ecole</h6>
            </div>
            <div class="card-body">
              <p class="d-inline">
                <vue-single-select
                  v-model="selectAlternance"
                  placeholder="A valider"
                  :options="[{'titre':'OUI','id':true},{'titre':'NON','id':false}]"
                  option-label="titre"
                ></vue-single-select>
                <vue-single-select
                  name="maybe"
                  placeholder="A Modifier"
                  v-model="ecoleSelected"
                  :options="allEcoles"
                  option-label="nom_ecole"
                ></vue-single-select>
              </p>
              <a
                class="d-none text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm"
                >Exporter</a
              >
              <a
                class="d-none text-white mt-2 mr-2 ml-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm"
                >Importer</a
              >
            </div>
          </div>
          <!-- Illustrations -->

          <!-- Approach -->
        </div>
      </div>
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
        allEcoles:[],
        allFormations:[],
        selectAlternance : null,
        selectedFormation : null,
        ecoleSelected:null,
        etudiantSelected : null,
        allEtudiants:[]

       
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
            url: 'formations/',
            auth: {
              username: this.user.mail,
              password: this.user.pwd
            }
        })
      .then(response => {

         this.allFormations=response.data
         console.debug(this.allFormations)


      })
      .catch(error => {
        console.debug(error)
      })

      axios({
            method: 'get',
            url: 'ecoles/',
            auth: {
              username: this.user.mail,
              password: this.user.pwd
            }
        })
      .then(response => {

         this.allEcoles=response.data


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
