<template>
 
 

             
              <!-- Illustrations -->
              <div class="card shadow mb-4">
                <div class="card-header py-3">
                  <h6 class="m-0 font-weight-bold text-primary">Candidature rapide</h6>
                </div>
                <div class="card-body">
                    <p class="d-inline">
                         <vue-single-select
                        name="maybe"
                placeholder="Ecole"
                            v-model="ecoleSelected"
                            :options="allecoles"
                            :required="true" 
                            option-label="nom_ecole" 
                    ></vue-single-select>
                    <vue-single-select
                        name="maybe"
                placeholder="Formation"
                            v-model="formation"
                            :options="formations"
                            :required="true" 
                            option-label="specialite" 
                    ></vue-single-select>
                    </p>
                    <a v-if="formation != null" :href="'/candidature/-1/'+formation.id_formation" class="d-none text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm">Nouvelle candidature</a>
                </div>
              </div>

              <!-- Approach -->
              

            
           
      <!-- End of Main Content -->

      
      
</template>

<script>
  import { mapState, mapActions } from 'vuex';
   
  import axios from 'axios';
   

  export default {
    name:"Content",
    components: {
    
    },
    data() {
      return {
        email: '',
        password: '',
         
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
     
      fetchData () {
          
        
      axios({
            method: 'get',
            url: 'http://127.0.0.1:5000/api/formations/',
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
            url: 'http://127.0.0.1:5000/api/ecoles/',
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

    
    } 
  }
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss">
   
  @import "../assets/custom.scss";
  @import "node_modules/bootstrap/scss/bootstrap.scss";
  @import "../assets/sb-admin-2.min.css";


 

</style>