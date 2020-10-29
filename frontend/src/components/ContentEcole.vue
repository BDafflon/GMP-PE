<template>
 

      <!-- Main Content -->
      <div id="content">
        
        <!-- Topbar -->
          <NavbarC> </NavbarC>
        <!-- End of Topbar -->

        <!-- Begin Page Content -->
        <div class="container-fluid">

          <!-- Page Heading -->
          <div class="d-sm-flex align-items-center justify-content-between  ">
            <h1 class="h3 mb-0 text-gray-800 p-2">Les Ecoles </h1> 
            
          </div>
              
          <!-- Content Row -->
           
          <!-- Content Row -->
          <div class="row mb-3" v-if="ecole !== null">
             
                <div class="col-md-6 text-left">

                  <div>
                    <b-card :title="ecole.nom_ecole" :sub-title="ecole.complement_ecole" >
                      <b-card-text>
                        {{ecole.descirption}}
                      </b-card-text>

                      <b-card-text>Type : <span class="font-italic">{{ecole.id_type_ecole}}</span></b-card-text>
                      <b-card-text>Profils recherchés : <span class="font-italic">GMP / GIM</span></b-card-text>
                       
                      <a href="#" class="card-link">Signaler une erreur</a>
                       
                    </b-card>
                  </div>
                </div>
                <div class="col-md-6">
                     
                      <b-card no-body class="full-width" >
                      <b-tabs card>
                        <b-tab title="Adresse"  active >
                          <iframe :src="'https://www.google.com/maps/embed/v1/place?key=AIzaSyA0s1a7phLN0iaD6-UE7m4qP-z21pH0eSc&q='+ecole.adresse.num_rue+'+'+ecole.adresse.nom_rue+'+'+ecole.adresse.ville+'+'+ecole.adresse.pays" width="100%" height="500" frameborder="0" style="border:0" allowfullscreen></iframe>
                        </b-tab>
                        <b-tab title="Formation" >
                          

                             

                          <ul class="list-group">

                            <li v-for="item in ecole.formation" :key="item.id_formation" class="list-group-item d-flex justify-content-between align-items-center">
                              {{ item.specialite }}
                              <b-button type="button" variant="primary" :to="'Formation/'+item.id_formation"><i class="fas fa-search"></i></b-button>
                            </li>
  
                          </ul>

                        </b-tab>
                        <b-tab title="Statistique" >
                          <div class="text-left">
                    <b-card   sub-title="2019-2020">
                       <b-card-text>Nombre de candidatures : <span class="font-italic">149</span></b-card-text>

                       <b-card-text>Nombre de recurutés : <span class="font-italic">7</span></b-card-text>

                      <b-card-text> Moyenne du dernier : <span class="font-italic">15/20</span></b-card-text>
                      <b-card-text> Classement du dernier :  <span class="font-italic">7/265</span></b-card-text>

                       
                    </b-card>
                  </div>
                        </b-tab>
                      </b-tabs>
                    </b-card>
                   


                    
                       
                </div>
          
          </div>
           

          <!-- Content Row -->
          <div class="row">

            <!-- Content Column -->
            <div class="col-md-8 mb-4">

              <!-- Project Card Example -->
              <div class="card">
                <div class="card-body text-light bg-dark">
                   <div class="row">
                      <div class="col-sm-3">Ecole</div>
                      <div class="col-sm-3">Type</div>
                      <div class="col-sm-4">Ville</div>
                      <div class="col-sm-2">Détail</div>
                  </div>
                </div>
              </div>
              <div v-for="item in ecoles" :key="item.id_ecole" class="card mt-1 mb-3 border border-top-0 border-right-0 border-bottom-0 border-danger rounded-0" >
                
                <div class="card-body shadow">
                   <div class="row align-items-center ">
                      <div class="col-sm-3">{{item.nom_ecole}}</div>
                      <div class="col-sm-3">{{item.id_type_ecole}}</div>
                      <div class="col-sm-4">{{item.adresse.ville}}</div>
                      <div class="col-sm-2"><button type="button" class="btn btn-primary" v-on:click="setEcole(item.id_ecole)"><i class="fas fa-search"></i></button></div>
                  </div>
                </div>
              </div>

               
 
               

            </div>

            <div class="col-md-4 mb-4">

              <!-- Illustrations -->
              <div class="card shadow mb-4">
                <div class="card-header py-3">
                  <h6 class="m-0 font-weight-bold text-primary">Filtre</h6>
                </div>
                <div class="card-body">
                    <p class="d-inline">
                         <vue-single-select
                        name="maybe"
                placeholder="Ecole"
                            v-model="fruit"
                            :options="ecoleNames"
                            
                    ></vue-single-select>
                    <vue-single-select
                        name="maybe"
                placeholder="Formation"
                            v-model="fruit"
                            :options="formations"
                             
                    ></vue-single-select>

                    <vue-single-select
                        name="maybe"
                placeholder="Ville"
                            v-model="fruit"
                            :options="villes"
                            
                    ></vue-single-select>
                    
                    </p>
                    <button type="button" class="btn btn-primary">Valider</button>
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
  import axios from 'axios'
  
  export default {
    components: {
    NavbarC
    },
    data() {
      return {
        email: '',
        password: '',
        ecoles:[{"nom":"INSA","complement":"Reseau INSA","description":"Haec dum oriens diu perferret, caeli reserato tepore Constantius consulatu suo septies et Caesaris ter egressus Arelate Valentiam petit, in Gundomadum et Vadomarium fratres Alamannorum reges arma moturus, quorum crebris excursibus vastabantur confines limitibus terrae Gallorum.","ville":"20 Avenue Albert Einstein, 69100 Villeurbanne"},{"nom":"IUT"}],
        ecoleNames : [],
        formations : [],
        subecoles : [],
        ecole : null
      }
    },
    created () {
      this.fetchData()
      
    },
    computed: {
      ...mapState([
        'loggingIn',
        'loginError',
        'accessToken',
        'logged',
        'user'
      ])
    },
    methods: {
      ...mapActions([
         
      ]),
      setEcole: function(value){
        this.ecoles.forEach(element => {
          console.debug("id "+element.id_ecole+"/"+value)
          if(element.id_ecole == value)
            this.ecole = element
            
        });
        
        console.debug("ecole "+this.ecole)
      },
      fetchData () {
        console.debug(this.user.mail+" "+this.user.pwd)
        axios({
            method: 'get',
            url: 'http://127.0.0.1:5000/api/ecoles/',
            auth: {
              username: this.user.mail,
              password: this.user.pwd
            }
        })
      .then(response => {
         console.debug(response.data)
         this.ecoles=response.data

         if (this.$route.params.id != null)
            this.setEcole(this.$route.params.id);
      })
      .catch(error => {
        console.debug(error)
      })
    }
    }
    ,
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
  @import "../../../node_modules/bootstrap/scss/bootstrap.scss";
  @import "../assets/sb-admin-2.min.css";

 .border {
    border-width:5px !important;
}
 
</style>