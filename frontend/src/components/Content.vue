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
            <h1 class="h3 mb-0 text-gray-800">Tableau de bord</h1>
             </div>

          <!-- Content Row -->
          <div class="row">

            <!-- Earnings (Monthly) Card Example -->
            <div class="col-xl-3 col-md-6 mb-4">
              <div class="card border-left-primary shadow h-100 py-2">
                <div class="card-body">
                  <div class="row no-gutters align-items-center">
                    <div class="col mr-2">
                      <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Nombre de dossier</div>
                      <div class="h5 mb-0 font-weight-bold text-gray-800">{{candidatures | len}}</div>
                    </div>
                    <div class="col-auto">
                      <i class="fas fa-calendar fa-2x text-gray-300"></i>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Earnings (Monthly) Card Example -->
            <div class="col-xl-3 col-md-6 mb-4">
              <div class="card border-left-success shadow h-100 py-2">
                <div class="card-body">
                  <div class="row no-gutters align-items-center">
                    <div class="col mr-2">
                      <div class="text-xs font-weight-bold text-success text-uppercase mb-1">Dossier non finalisés</div>
                      <div class="h5 mb-0 font-weight-bold text-gray-800">{{candidatures | lenComplete}}</div>
                    </div>
                    <div class="col-auto">
                      <i class="fas fa-hourglass-half fa-2x text-gray-300"></i>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Earnings (Monthly) Card Example -->
            

            <!-- Pending Requests Card Example -->
            <div class="col-xl-3 col-md-6 mb-4">
              <div class="card border-left-warning shadow h-100 py-2">
                <div class="card-body">
                  <div class="row no-gutters align-items-center">
                    <div class="col mr-2">
                      <div class="text-xs font-weight-bold text-warning text-uppercase mb-1">Messages</div>
                      <div class="h5 mb-0 font-weight-bold text-gray-800">1</div>
                    </div>
                    <div class="col-auto">
                      <i class="fas fa-comments fa-2x text-gray-300"></i>
                    </div>
                  </div>
                </div>
              </div>
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
                    <li class="list-group-item" v-for="item in candidatures" :key="item.id_candidature"> 
                      <div class="row align-items-center">
                        <div class="col-sm-2">
                          
                          <a v-on:click="up(item)" class="d-none text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm"><i class="fas fa-arrow-up"></i></a>
                          <a v-on:click="down(item)" class="d-none ml-1 text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm"><i class="fas fa-arrow-down"></i></a></div>
                        <div class="col-sm-8">
                             {{item.ecole.nom}} - {{item.formation.nom}}
                        </div>
                        <div class="col-sm-2">
                          <a :href="'/candidature/'+item.id_candidature+'/'+item.id_formation"   class="d-none ml-2 text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm"><i class="fas fa-search"></i></a>
                          <a v-on:click="trash(item)"  class="d-none ml-2 text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm"><i class="fas fa-trash-alt"></i></a>

                        </div>
                      </div>
                    </li>
                  </ul>
                   
                   
                   
                </div>
              </div>

               

            </div>

            <div class="col-md-4 mb-4">

              <!-- Illustrations -->
               <CandidatureRapide></CandidatureRapide>

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
   

  export default {
    name:"Content",
    components: {
    NavbarC,
    CandidatureRapide
    },
    data() {
      return {
        email: '',
        password: '',
        candidatures:[],
        firstD:Date.now(),
        allecoles:[],
        allFormation:[],
        ecole:null,
        formations:[],
        formation:null
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
        const today = new Date(value);
        const date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
        
        const dateTime = date ;
         
          return dateTime
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
          console.debug(response.data)
          this.candidatures = response.data
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