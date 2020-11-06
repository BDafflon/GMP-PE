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
            <h1 v-if="0==user.rank" class="h3 mb-0 text-gray-800">Tableau de bord d'administration</h1>

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
                <div  class="card-body">
                  <div class="candidature-area">
                  <ul class="list-group">
                    <li class="list-group-item" v-for="item in candidatures" :key="item.id_candidature"> 
                      <div v-if="user.rank==2" class="row align-items-center">
                        <div class="col-sm-2">
                          
                          <a v-on:click="up(item)" class="d-none text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm"><i class="fas fa-arrow-up"></i></a>
                          <a v-on:click="down(item)" class="d-none ml-1 text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm"><i class="fas fa-arrow-down"></i></a></div>
                        <div class="col-sm-7">
                             {{item.ecole.nom}} - {{item.formation.nom}}
                        </div>
                        <div class="col-sm-3">
                          <a v-if="item.ap != 0" class="d-none ml-2 text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm">
                            <i class="fas fa-envelope fa-fw"></i>
                            <!-- Counter - Messages -->
                            <span class="badge badge-danger badge-counter">{{item.ap}}</span>
                          </a>

                          <a v-on:click="setCandidature(item.id_candidature)"  class="d-none ml-2 text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm"><i class="fas fa-search"></i></a>
                          <a v-on:click="trash(item)"  class="d-none ml-2 text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm"><i class="fas fa-trash-alt"></i></a>

                        </div>
                      </div>

                      <div v-if="user.rank==0" class="row align-items-center">
                        <div class="col-sm-2">
                          {{item.nom_etudiant.nom | capitalize}} {{item.nom_etudiant.prenom | firstLetter}}.
                        </div>  
                        <div class="col-sm-7">
                             {{item.ecole.nom}} - {{item.formation.nom}}
                        </div>
                        <div class="col-sm-3">
                          <a v-if="item.ap != 0" class="d-none ml-2 text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm">
                            <i class="fas fa-envelope fa-fw"></i>
                            <!-- Counter - Messages -->
                            <span class="badge badge-danger badge-counter">{{item.ap}}</span>
                          </a>

                          <a v-on:click="setCandidature(item.id_candidature)"  class="d-none ml-2 text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm"><i class="fas fa-search"></i></a>
                          <a v-on:click="trash(item)"  class="d-none ml-2 text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm"><i class="fas fa-trash-alt"></i></a>

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
                  <h6 class="m-0 font-weight-bold text-primary">Filtre Candidature</h6>
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
                            :options="allecoles"
                            option-label="nom_ecole" 
                    ></vue-single-select>
                    <vue-single-select
                        name="maybe"
                placeholder="Formation"
                            v-model="formation"
                            :options="formations"
                            option-label="specialite" 
                    ></vue-single-select>
                    <vue-single-select
                        name="maybe"
                placeholder="Nom d'etudiant"
                            v-model="formation"
                            :options="formations"
                            option-label="specialite" 
                    ></vue-single-select>
                    </p>
                    <a class="d-none text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm">Exporter</a>
                
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
                <div  class="card-body">
                  <div class="candidature-area">
                  <ul class="list-group">
                    <li class="list-group-item" v-for="item in candidatures" :key="item.id_candidature"> 
                      <div v-if="user.rank==2" class="row align-items-center">
                        <div class="col-sm-2">
                          
                          <a v-on:click="up(item)" class="d-none text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm"><i class="fas fa-arrow-up"></i></a>
                          <a v-on:click="down(item)" class="d-none ml-1 text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm"><i class="fas fa-arrow-down"></i></a></div>
                        <div class="col-sm-7">
                             {{item.ecole.nom}} - {{item.formation.nom}}
                        </div>
                        <div class="col-sm-3">
                          <a v-if="item.ap != 0" class="d-none ml-2 text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm">
                            <i class="fas fa-envelope fa-fw"></i>
                            <!-- Counter - Messages -->
                            <span class="badge badge-danger badge-counter">{{item.ap}}</span>
                          </a>

                          <a v-on:click="setCandidature(item.id_candidature)"  class="d-none ml-2 text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm"><i class="fas fa-search"></i></a>
                          <a v-on:click="trash(item)"  class="d-none ml-2 text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm"><i class="fas fa-trash-alt"></i></a>

                        </div>
                      </div>

                      <div v-if="user.rank==0" class="row align-items-center">
                        <div class="col-sm-2">
                          {{item.nom_etudiant.nom | capitalize}} {{item.nom_etudiant.prenom | firstLetter}}.
                        </div>  
                        <div class="col-sm-7">
                             {{item.ecole.nom}} - {{item.formation.nom}}
                        </div>
                        <div class="col-sm-3">
                          <a v-if="item.ap != 0" class="d-none ml-2 text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm">
                            <i class="fas fa-envelope fa-fw"></i>
                            <!-- Counter - Messages -->
                            <span class="badge badge-danger badge-counter">{{item.ap}}</span>
                          </a>

                          <a v-on:click="setCandidature(item.id_candidature)"  class="d-none ml-2 text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm"><i class="fas fa-search"></i></a>
                          <a v-on:click="trash(item)"  class="d-none ml-2 text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm"><i class="fas fa-trash-alt"></i></a>

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
                  <h6 class="m-0 font-weight-bold text-primary">Filtre Formation</h6>
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
                            :options="allecoles"
                            option-label="nom_ecole" 
                    ></vue-single-select>
                    <vue-single-select
                        name="maybe"
                placeholder="Ecole"
                            v-model="formation"
                            :options="formations"
                            option-label="specialite" 
                    ></vue-single-select>
                    <vue-single-select
                        name="maybe"
                placeholder="Formation"
                            v-model="formation"
                            :options="formations"
                            option-label="specialite" 
                    ></vue-single-select>
                    <vue-single-select
                        name="maybe"
                placeholder="Ville"
                            v-model="formation"
                            :options="formations"
                            option-label="specialite" 
                    ></vue-single-select>
                    
                    
                    </p>
                    <a class="d-none text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm">Exporter</a>
                    <a class="d-none text-white mt-2 mr-2 ml-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm">Importer</a>
                
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
                <div  class="card-body">
                  <div class="candidature-area">
                  <ul class="list-group">
                    <li class="list-group-item" v-for="item in candidatures" :key="item.id_candidature"> 
                      <div v-if="user.rank==2" class="row align-items-center">
                        <div class="col-sm-2">
                          
                          <a v-on:click="up(item)" class="d-none text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm"><i class="fas fa-arrow-up"></i></a>
                          <a v-on:click="down(item)" class="d-none ml-1 text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm"><i class="fas fa-arrow-down"></i></a></div>
                        <div class="col-sm-7">
                             {{item.ecole.nom}} - {{item.formation.nom}}
                        </div>
                        <div class="col-sm-3">
                          <a v-if="item.ap != 0" class="d-none ml-2 text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm">
                            <i class="fas fa-envelope fa-fw"></i>
                            <!-- Counter - Messages -->
                            <span class="badge badge-danger badge-counter">{{item.ap}}</span>
                          </a>

                          <a v-on:click="setCandidature(item.id_candidature)"  class="d-none ml-2 text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm"><i class="fas fa-search"></i></a>
                          <a v-on:click="trash(item)"  class="d-none ml-2 text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm"><i class="fas fa-trash-alt"></i></a>

                        </div>
                      </div>

                      <div v-if="user.rank==0" class="row align-items-center">
                        <div class="col-sm-2">
                          {{item.nom_etudiant.nom | capitalize}} {{item.nom_etudiant.prenom | firstLetter}}.
                        </div>  
                        <div class="col-sm-7">
                             {{item.ecole.nom}} - {{item.formation.nom}}
                        </div>
                        <div class="col-sm-3">
                          <a v-if="item.ap != 0" class="d-none ml-2 text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm">
                            <i class="fas fa-envelope fa-fw"></i>
                            <!-- Counter - Messages -->
                            <span class="badge badge-danger badge-counter">{{item.ap}}</span>
                          </a>

                          <a v-on:click="setCandidature(item.id_candidature)"  class="d-none ml-2 text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm"><i class="fas fa-search"></i></a>
                          <a v-on:click="trash(item)"  class="d-none ml-2 text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm"><i class="fas fa-trash-alt"></i></a>

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
                            :options="allecoles"
                            option-label="nom_ecole" 
                    ></vue-single-select>
                    
                    
                    
                    </p>
                    <a class="d-none text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm">Exporter</a>
                    <a class="d-none text-white mt-2 mr-2 ml-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm">Importer</a>
                
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
        candidature:null,
        candidatures:[],
        firstD:Date.now(),
        allecoles:[],
        allFormation:[],
        ecole:null,
        formations:[],
        formation:null,
        edit: false,
        prof:null,
        matiere:null,
        avis:null,
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
            id_candidature : this.candidature.id_candidature

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
        axios({
              method: 'get',
              url: 'candidatures_user/'+this.user.id,
              auth: {
                username: this.user.mail,
                password: this.user.pwd
              }
          })
        .then(response => {
          console.debug('------------------------------------')
          console.debug(response.data)
          this.candidatures = response.data
          
            console.debug('+++++++++++++++++++++++++++++++')
            this.candidatures.forEach(element => {

              if(this.$route.params.idC == element.id_candidature || this.candidature.id_candidature == element.id_candidature )
                console.debug('!!!!!!!!!!!!!!!!!!!!!')
                this.candidature = element
                if (element.deadline_dossier != null)
                  this.candidature.deadline_dossier = this.timeConverter(element.deadline_dossier)
                if (element.date_candidature != null)
                  this.candidature.date_candidature = this.timeConverter(element.date_candidature)
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

.candidature-area {
/*   border: 1px solid #ccc; */
  background: white;
  max-height: 30vh;
  padding: 1em;
  overflow: auto;
   
  margin: 0 auto 2em auto;
  }

 

</style>