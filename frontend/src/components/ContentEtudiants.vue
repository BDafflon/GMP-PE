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
        <div>
        <b-button
         v-if="user.rank==0"
          type="button"
          variant="primary"
          class="mr-2"
          v-on:click="exporter()"
    
          ><i class="fas fa-download"></i
        > Exporter</b-button>
        <b-button
         v-if="user.rank==0"
          type="button"
          variant="primary"
          v-on:click="supprimer()"
    
          ><i class="fas fa-trash-alt"></i
        > Supprimer</b-button>
        </div>
      </div>

      <!-- Content Row -->
      <div class="row mb-3" v-if="etudiant !== null">
        <div class="col-md-6 text-left">
          <div>
            <b-card
              :title="etudiant.nom"
              :sub-title="etudiant.prenom"
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
                  <ul class="list-group">
                  <li
                    v-for="item in candidatures"
                    :key="item.id_candidature"
                    class="list-group-item d-flex justify-content-between align-items-center"
                  >
                    {{ item.ecole.nom }} - {{item.formation.nom}}

                    <b-button
                      type="button"
                      variant="primary"
                      :to="'Formation/'+item.id_formation"
                      ><i class="fas fa-search"></i
                    ></b-button>
                  </li>
                </ul>
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
              <div class="area">
                <ul class="list-group">
                  <li class="list-group-item" v-for="item in allEtudiants" :key="item.id" >
                    

                    <div v-if="user.rank==0" class="row align-items-center">
                      <div class="col-sm-2">
                        {{item.nom | capitalize}}
                        {{item.prenom | firstLetter}}.
                      </div>
                      <div class="col-sm-7">
                        {{item.mail}} - {{item.groupeTD}}
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
                          v-on:click="setEtudiant(item)"
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
              
              <a class="d-none text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm mr-3" v-b-modal.modal-ajoutetuidant >Ajouter</a >
               
            </div>
          </div>
          <!-- Illustrations -->

          <!-- Approach -->
        </div>
      </div>

      <!-- Ecole -->
      
    </div>

    <!-- /.container-fluid -->
    <Modal v-on:refreche="fetchData()">></Modal>
  </div>
  
  <!-- End of Main Content -->
</template>

<script>
  import { mapState, mapActions } from 'vuex';
  import NavbarC from './NavBarCustom.vue';
  import axios from 'axios';
  import Modal from './modal/modalEtudiant.vue'



  export default {
    name:"Content",
    components: {
    NavbarC,
    Modal
    },
    data() {
      return {
        email: '',
        password: '',
        allCandidatures:[],
        allEtudiants:[],
        hasMessage:null,
        etudiantSelected:null,
        hasCandidature:null,
        etudiant:null,
        candidatures:null

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
      setEtudiant (etu){
          this.etudiant = etu
          this.candidatures=null
          axios({
            method: 'get',
            url: 'candidatures_user/'+etu.id,
            auth: {
              username: this.user.mail,
              password: this.user.pwd
            }
        })
      .then(response => {

         this.candidatures=response.data
         window.scrollTo(0,0);
         

      })
      .catch(error => {
        console.debug(error)
      })

      },
      exporter(){
          this.fetchData()
          let csvContent="data:text/csv;charset=utf-8,id;nom;prenom;mail;pass;td;\n"
          this.allEtudiants.forEach(element => {
              console.debug(element)
              csvContent+=element.id+";"+element.nom+";"+element.prenom+";"+element.mail+";;"+element.groupeTD+";\n"
          })
          const data = encodeURI(csvContent);
          const link = document.createElement("a");
          link.setAttribute("href", data);
          link.setAttribute("download", "export.csv");
          link.click();
      }
      ,
      supprimer(){
        if(confirm('Etes vous sur de vouloir supprimer les étudiants (definitif) ?')){
          axios({
            method: 'delete',
            url: 'user/all',
            auth: {
              username: this.user.mail,
              password: this.user.pwd
            }
        })
      .then(response => {
         console.debug(response.data)
          this.fetchData()
      })
      .catch(error => {
        console.debug(error)
      })    
        }
      },
      trash(etu){
          if(confirm('Etes vous sur de vouloir supprimer cet etuidant (definitif) ?')){
                    axios({
                      method: 'delete',
                      url: 'userd/'+etu.id,
                      auth: {
                        username: this.user.mail,
                        password: this.user.pwd
                      }
                  })
                .then(response => {
                  console.debug(response.data)
                    this.fetchData()
                })
                .catch(error => {
                  console.debug(error)
                })
                  }
      },
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

 

</style>
