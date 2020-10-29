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
            <h1 class="h3 mb-0 text-gray-800">Les Formations</h1>
             </div>

          <!-- Content Row -->
           
          <!-- Content Row -->
          <div class="row mb-3" v-if="formation !== null">
             
                <div class="col-md-6 text-left">

                  <div>
                    <b-card :title="formation.specialite" :sub-title="formation.site_web_url">
                      <b-card-text>
                        {{formation.description}}
                      </b-card-text>

                      <b-card-text>Brochure : <span class="font-italic">{{formation.brochure_url}}</span></b-card-text>
                      <b-card-text>Profils recherchés : <span class="font-italic">GMP / GIM</span></b-card-text>
                      <b-card-text>Alternance : <span class="font-italic">{{formation.alternance | bool2txt}}</span></b-card-text>
                      <b-card-text>Type : <span class="font-italic">{{formation.type_formation| bool2type}}</span></b-card-text>
                      
                      <a href="#" class="card-link">Signaler une erreur</a>
                       
                    </b-card>
                  </div>
                </div>
                <div class="col-md-6">

                      <b-card no-body class="full-width" >
                      <b-tabs card>
                        <b-tab title="Responsable"  active  class="text-left">
                          <b-card-text>Nom: <span class="font-italic">{{formation.responsable.prenom_responsable | capitalize}} {{formation.responsable.nom_responsable | capitalize}}</span></b-card-text>
                          <b-card-text>Mail: <span class="font-italic">{{formation.responsable.mail_responsable | capitalize}} </span></b-card-text>
                          <b-card-text>Telephone: <span class="font-italic">{{formation.responsable.telephone_responsable }} </span></b-card-text>

                        </b-tab>
                        <b-tab title="Dans la même école" >
                              <ul class="list-group">

                            <li v-for="item in formation.formations" :key="item.id_formation" class="list-group-item d-flex justify-content-between align-items-center">
                              {{ item.specialite }}
                              <b-button type="button" variant="primary" :to="'Formation/'+item.id_formation"><i class="fas fa-search"></i></b-button>
                            </li>
                         </ul>
                        </b-tab>
                        <b-tab title="Forum" >
                          <div class="text-left">
                    <b-card>
                         <b-card-text>Visio: <span class="font-italic">{{formation.ForumInfo.lien_visio }}</span></b-card-text>
                          <b-card-text>Video: <span class="font-italic">{{formation.ForumInfo.lien_video }} </span></b-card-text>
                          
                       
                    </b-card>
                  </div>
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
                      <div class="col-sm-3">Formation</div>
                      <div class="col-sm-2">Type</div>
                      <div class="col-sm-2">Alternance</div>
                      <div class="col-sm-2">Ecole</div>
                      <div class="col-sm-2">Detail</div>
                  </div>
                </div>
              </div>
              <div v-for="item in formations" :key="item.id_formation" class="card mt-1 mb-3 border border-top-0 border-right-0 border-bottom-0 border-danger rounded-0" >
                <div class="card-body shadow">
                   <div class="row align-items-center ">
                     <div class="col-sm-3">{{item.specialite}}</div>
                      <div class="col-sm-2">{{item.type_formation |bool2type}}</div>
                      <div class="col-sm-2">{{item.alternance | bool2txt}}</div>
                      <div class="col-sm-2">{{item.nom_ecole}}</div>
                      <div class="col-sm-2"><button type="button" class="btn btn-primary" v-on:click="setFormation(item.id_formation)"><i class="fas fa-search"></i></button></div>
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
                            :required="true" 
                    ></vue-single-select>
                    <vue-single-select
                        name="maybe"
                placeholder="Formation"
                            v-model="fruit"
                            :options="formations"
                            :required="true" 
                    ></vue-single-select>

                    <vue-single-select
                        name="maybe"
                placeholder="Ville"
                            v-model="fruit"
                            :options="villes"
                            :required="true" 
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
        formations:[],
        formation : null
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
      setFormation: function(value){
        this.formations.forEach(element => {
          console.debug("id "+element.id_formation+"/"+value)
          if(element.id_formation == value)
            this.formation = element
            
        });
        
        console.debug("formation "+this.formation)
      },
      fetchData () {
        console.debug(this.user.mail+" "+this.user.pwd)
        axios({
            method: 'get',
            url: 'http://127.0.0.1:5000/api/formations/',
            auth: {
              username: this.user.mail,
              password: this.user.pwd
            }
        })
      .then(response => {
         console.debug(response.data)
         this.formations=response.data

         if (this.$route.params.id != null)
            this.setFormation(this.$route.params.id);
      })
      .catch(error => {
        console.debug(error)
      })
    }
    }
    ,
    filters: {
      bool2txt : function(value){
        if (value)
          return "Oui";
        else  
          return "Non";
      },
      bool2type : function(value){
        if (value)
          return "Publique";
        else  
          return "Privée";
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
  @import "../../../node_modules/bootstrap/scss/bootstrap.scss";
  @import "../assets/sb-admin-2.min.css";

 .border {
    border-width:5px !important;
}
 
</style>