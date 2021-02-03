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
        <h1 v-if="2==user.rank" class="h3 mb-0 text-gray-800">
          Mes candidatures
        </h1>
        <h1 v-if="0==user.rank" class="h3 mb-0 text-gray-800">
          Les candidatures
        </h1>
      </div>

      <!-- Content Row -->
      <div class="row mb-3" v-if="candidature != null">
        <div class="col-md-6 text-left">
          <div>
            <b-card
              :title="candidature.formation.ecole.nom_ecole"
              :sub-title="candidature.formation.specialite"
            >
            <b-card-text v-if="user.rank==0"
                >Nom :
                <span
                  class="font-italic"
                  >{{candidature.etudiant.nom}} {{candidature.etudiant.prenom}}</span
                ></b-card-text
              >
              <b-card-text v-if="!edit"
                >DeadLine :
                <span
                  class="font-italic"
                  >{{candidature.deadline_dossier}}</span
                ></b-card-text
              >
              <b-card-text v-if="!edit"
                >Date de la candidature :
                <span
                  class="font-italic"
                  >{{candidature.date_candidature}}</span
                ></b-card-text
              >

              <template v-if="edit">
                <div>
                  <label for="example-datepicker">DeadLine</label>
                  <b-form-datepicker
                    id="example-datepicker"
                    v-model="candidature.deadline_dossier"
                    class="mb-2"
                  ></b-form-datepicker>
                </div>
              </template>
              <template v-if="edit">
                <div>
                  <label for="example-datepicker">Date candidature</label>
                  <b-form-datepicker
                    id="example-datepicker2"
                    v-model="candidature.date_candidature"
                    class="mb-2"
                  ></b-form-datepicker>
                </div>
              </template>

              <b-card-text
                >Validation du service PE :
                <span
                  class="font-italic"
                  >{{candidature.validationPE}}</span
                ></b-card-text
              >

              <span
                ><a
                  v-if="!edit"
                  @click="edit = !edit"
                  class="d-none ml-2 text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm"
                  ><i class="far fa-edit"></i></a
              ></span>
              <span
                ><a
                  v-if="edit"
                  @click="updateCandidature()"
                  class="d-none ml-2 text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm"
                  ><i class="far fa-share-square"></i></a
              ></span>

              <a
                v-on:click="trash(candidature)"
                class="d-none ml-2 text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm"
                ><i class="fas fa-trash-alt"></i
              ></a>
            </b-card>
          </div>
        </div>
        <div class="col-md-6">
          <b-card no-body class="full-width">
            <b-tabs card>
              <b-tab title="Messages PE" active>
                <ChatComponent :candidature="candidature"></ChatComponent>
              </b-tab>
              <b-tab title="Avis enseignants">
                <ul v-if="user.rank==2" class="list-group">
                  <li
                    v-for="item in candidature.avis"
                    :key="item.id_avis"
                    class="list-group-item d-flex justify-content-between align-items-center"
                  >
                    [{{item.prof}} | {{item.matiere}}] {{ item.avis}}
                  </li>
                </ul>
                <ul v-if="user.rank==0" class="list-group">
                  <li
                    v-for="item in candidature.avis"
                    :key="item.id_avis"
                    class="list-group-item d-flex justify-content-between align-items-center"
                  >
                    [{{item.prof}} | {{item.matiere}}] {{ item.avis}}
                  </li>
                  <li
                    class="list-group-item d-flex justify-content-between align-items-center"
                  >
                    <section class="">
                      <form @submit.prevent="sendAvis()" id="person2-form">
                        <div class="row">
                          <div class="col-sm-2">
                            <input
                              v-model="prof"
                              type="text"
                              id="person2-input"
                              class="form-control"
                              placeholder="prof"
                              required
                              autofocus
                            />
                          </div>
                          <div class="col-sm-2">
                            <input
                              v-model="matiere"
                              type="text"
                              id="person2-input"
                              class="form-control"
                              placeholder="matiere"
                              required
                              autofocus
                            />
                          </div>
                          <div class="col-sm-6">
                            <input
                              v-model="avis"
                              type="text"
                              id="person2-input"
                              class="form-control"
                              placeholder="avis"
                              required
                              autofocus
                            />
                          </div>
                          <div class="col-sm-2">
                            <button
                              class="btn btn-primary btn-block"
                              type="submit"
                            >
                              OK
                            </button>
                          </div>
                        </div>
                      </form>
                    </section>
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
              <h6 class="m-0 font-weight-bold text-primary">Candidatures</h6>
            </div>
            <div class="card-body">
              <ul class="list-group">
                <li
                  class="list-group-item"
                  v-for="item in candidatures"
                  :key="item.id_candidature"
                >
              
                  <div v-if="user.rank==2" class="row align-items-center">
                    <div class="col-sm-2">
                      <a
                        v-on:click="up(item)"
                        class="d-none text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm"
                        ><i class="fas fa-arrow-up"></i
                      ></a>
                      <a
                        v-on:click="down(item)"
                        class="d-none ml-1 text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm"
                        ><i class="fas fa-arrow-down"></i
                      ></a>
                    </div>
                    <div class="col-sm-7">
                      {{item.formation.ecole.nom_ecole}} - {{item.formation.specialite}}
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

                  <div v-if="user.rank==0" class="row align-items-center">
                    <div class="col-sm-2">
                      {{item.etudiant.nom | capitalize}}
                      {{item.etudiant.prenom | firstLetter}}. - {{item.etudiant.groupeTD}}
                    </div>
                    <div class="col-sm-7">
                      {{item.formation.ecole.nom_ecole}} - {{item.formation.specialite}} - {{item.formation.ecole.adresse.ville}}
                    </div>
                    <div class="col-sm-3">
                      <a
                        
                        class="d-none ml-2 text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm"
                      >
                        <i class="fas fa-envelope fa-fw"></i>
                        <!-- Counter - Messages -->
                         
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

        <div class="col-md-4 mb-4">
          <!-- Illustrations -->
          <CandidatureRapide v-if="user.rank==2"></CandidatureRapide>
          
          <div v-if="user.rank==0" class="card shadow mb-4">
            <div class="card-header py-3">
              <h6 class="m-0 font-weight-bold text-primary">
                Filtre Etuidants
              </h6>
            </div>
            <div class="card-body">
              <p class="d-inline">
                <vue-single-select
                  name="maybe"
                  placeholder="Nom d'etudiant"
                  v-model="etudiantSelected"
                  :options="allEtudiants"
                ></vue-single-select>
                <vue-single-select
                  name="maybe"
                  placeholder="GroupeTD"
                  v-model="groupeTDSelected"
                 :options="allgroupeTD"
                ></vue-single-select>
              </p>
              
              <a class="d-none text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm mr-3" v-b-modal.modal-ajoutetuidant >Ajouter</a >
               
            </div>
          </div>
           
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
  import CandidatureRapide from './candidatureRapide.vue';
  import ChatComponent from './ChatComponent.vue'
 

  export default {
    name:"Content",
    components: {
    NavbarC,
    CandidatureRapide,
    ChatComponent
    },
    data() {
      return {
        email: '',
        password: '',
        candidature:null,
        allCandidatures:[],
        candidatures:[],
        firstD:Date.now(),
        allecoles:[],
        allFormation:[],
        allEtudiants:[],
        allgroupeTD:[],
        ecole:null,
        formations:[],
        formation:null,
        edit: false,
        prof:null,
        matiere:null,
        avis:null,
        
        groupeTDSelected:null
      }
    },
    created () {


        if(this.$route.params.idC == -1 && this.$route.params.idF != null){

          axios({
            method: 'post',
            url: 'candidature/registration',
            data: {

              id_etudiant : this.user.id,
              id_formation : this.$route.params.idF

            },
            auth: {
              username: this.user.mail,
              password: this.user.pwd
            }
          })
          .then(response => {

              console.debug(response.data.id_candidature)
              this.candidature = response.data
              this.fetchData()




          })
          .catch(error => {
            console.debug(error)
            this.fetchData()
          })
        }
  else{
        this.fetchData()
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
      ]),
      etudiantSelected : {
          
          set: function(val){
            console.debug(val)
            if (val == null)
              this.candidatures=this.allCandidatures
            else {
              this.candidatures=[]
              this.allCandidatures.forEach(element => {
                if(element.etudiant.nom==val){
                  this.candidatures.push(element)
                }
              });
            }
          },
          get:function(){
            return "null"
          }
          
      },
      ecoles: function(){


        return this.filtreEcole();
      }, 
       
      ecoleSelected: {
    // getter
        get: function () {
          return this.ecole
        },
        // setter
        set: function (newValue) {
          this.ecole = newValue
          this.formations =[]
          if (newValue != null){
          this.allFormation.forEach(element => {
            if(element['id_ecole'] == this.ecole.id_ecole)
              this.formations.push(element)
          });
          }
        }
      }
    },
    methods: {
      ...mapActions([

      ]),
      sendAvis: function(){
        console.debug(this.prof+" "+this.avis+" "+this.candidature.id_candidature)
        axios({
          method: 'post',
          url: 'avis/registration',
          data: {

            prof : this.prof,
            avis : this.avis,
            id_candidature : this.candidature.id_candidature,
            matiere : this.matiere

          },
          auth: {
            username: this.user.mail,
            password: this.user.pwd
          }
        })
        .then(response => {

            console.debug(response)

            this.fetchData()




        })
        .catch(error => {
          console.debug(error)
          this.fetchData()
        })
      },
      updateCandidature : function(){
          console.debug(this.candidature.date_candiature)
          this.edit = false
          axios({
            method: 'post',
            url: 'candidature/'+this.candidature.id_candidature,
            data: {

              id_etudiant : this.candidature.id_etudiant,
              date_candidature :Date.parse(this.candidature.date_candidature),
              deadline_dossier : Date.parse(this.candidature.deadline_dossier),
              validationPE : this.candidature.validationPE,
              id_formation : this.candidature.id_formation,
              nbVoeux : this.candidature.voeux
            },
            auth: {
              username: this.user.mail,
              password: this.user.pwd
            }
        })
      .then(response => {

          console.debug(response)

      })
      .catch(error => {
        console.debug(error)
      })

      },
    trash : function(event){
        if(confirm('Etes vous sur de vouloir supprimer cet candidature (definitif) ?')){
          axios({
            method: 'delete',
            url: 'candidature/'+event.id_candidature,
            auth: {
              username: this.user.mail,
              password: this.user.pwd
            }
        })
      .then(response => {
         console.debug(response.data)
          this.fetchDataCandidature()
      })
      .catch(error => {
        console.debug(error)
      })
        }
    },
    setCandidature : function(id){
      console.debug('+++++++++++SET Can++++++++++++++++++++'+id)
      console.debug(this.candidatures)
        this.candidatures.forEach(element => {
              if(id == element.id_candidature)
                this.candidature = element
                window.scrollTo(0,0);
                console.debug('+++++++++++FIND Can++++++++++++++++++++')
               if (element.deadline_dossier != null)
                  this.candidature.deadline_dossier = this.timeConverter(this.candidature.deadline_dossier)
                if (element.date_candidature != null)
                  this.candidature.date_candidature = this.timeConverter(this.candidature.date_candidature)
            });
    },
    up: function (event) {

      axios({
            method: 'get',
            url: 'candidature/up/'+event.id_candidature,
            auth: {
              username: this.user.mail,
              password: this.user.pwd
            }
        })
      .then(response => {
         console.debug(response.data)
          this.fetchDataCandidature()
      })
      .catch(error => {
        console.debug(error)
      })
    },
    down: function (event) {
      axios({
            method: 'get',
            url: 'candidature/down/'+event.id_candidature,
            auth: {
              username: this.user.mail,
              password: this.user.pwd
            }
        })
      .then(response => {
         console.debug(response.data)
          this.fetchDataCandidature()
      })
      .catch(error => {
        console.debug(error)
      })
    },
      etat2pourcentf(value){
        return value*20
      },
      getstat (value){

          if (value == 1)
            return "bg-danger"
          if(value==2)
            return "bg-warning"
          if(value==3)
            return "bg-info"
          if(value==4)
            return "bg-success"
          return "bg-secondary"
      },
      timeConverter(value){
        return new Date(value).toISOString().slice(0,10);
      },

      fetchDataCandidature(){
        let url='candidatures_user/'+this.user.id
        if(this.user.rank==0)
          url='candidatures/'
        axios({
              method: 'get',
              url: url,
              auth: {
                username: this.user.mail,
                password: this.user.pwd
              }
          })
        .then(response => {
          console.debug('------------------------------------')
          console.debug(response.data)
          this.allCandidatures = response.data
          this.candidatures=this.allCandidatures
          this.allEtudiants=[]
          this.allgroupeTD=[]

            console.debug('+++++++++++++++++++++++++++++++')
            this.candidatures.forEach(element => {
              console.debug(element.etudiant.nom)
              if(!this.allEtudiants.includes(element.etudiant.nom))
                this.allEtudiants.push(element.etudiant.nom)
              if(!this.allgroupeTD.includes(element.etudiant.groupeTD))
                this.allgroupeTD.push(element.etudiant.groupeTD)

              if(this.$route.params.idC == element.id_candidature || this.candidature!=null && this.candidature.id_candidature == element.id_candidature ){
                console.debug('!!!!!!!!!!!!!!!!!!!!!')
                this.candidature = element
                if (element.deadline_dossier != null)
                  this.candidature.deadline_dossier = this.timeConverter(element.deadline_dossier)
                if (element.date_candidature != null)
                  this.candidature.date_candidature = this.timeConverter(element.date_candidature)
              }
            });

        })
        .catch(error => {
          console.debug(error)
        })

      },
      fetchData () {
         this.fetchDataCandidature()

      axios({
            method: 'get',
            url: 'formations/',
            auth: {
              username: this.user.mail,
              password: this.user.pwd
            }
        })
      .then(response => {

         this.allFormation=response.data



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

         this.allecoles=response.data


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
