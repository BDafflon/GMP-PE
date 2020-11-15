<template>
  <div>
    <b-modal id="modal-ajoutetuidant" size="lg" title="Ajouter un etuidant">
      <div class="row" v-if="user.rank == 0">
        <b-form-group class="col-sm-12" label="Fichier (csv) :" label-for="file-small" label-size="sm">
          <b-form-file v-model="file1" class="d-inline" accept=".csv" ></b-form-file>
           <b-button @click="sendFile" class="d-inline mt-2 mr-2 btn btn-primary" type="submit">Envoyer</b-button>
        </b-form-group>
      </div>
       <div class="row">
          <div class="col  mycontent-left" >
                <form class="mt-3" @submit.prevent="etudiantSubmit">
                  <div class="form-row">
                    <div class="col">
                      <input v-model="nom" type="text" class="form-control" placeholder="Nom" required>
                    </div>
                    <div class="col">
                      <input v-model="prenom" type="text" class="form-control" placeholder="Prenom" required>
                    </div>
                  </div>
                  <div class="form-row">
                    <div class="col">
                      <input v-model="mail" type="text" class="form-control" placeholder="mail" required>
                    </div>
                    <div class="col">
                      <input v-model="motdepasse" type="password" class="form-control" placeholder="mot de passe" required>
                    </div>
                  </div>
                  <div class="form-row">
                    <div class="col">
                      <input v-model="groupeTD" type="text" class="form-control" placeholder="Groupe TD" required>
                    </div>
                    <div class="col">
                      <input v-model="motdepasse2" type="password" class="form-control" placeholder="mot de passe confirmation" required>
                    </div>
                  </div>
                   
                  <div class="form-row mt-4">
                     
                    <div class="col">
                      <button class="btn btn btn-primary btn-block" type="submit">Ajouter</button>
                    </div>
                  </div>
                </form>


          </div>
          
        </div>


    </b-modal>

     
    
  </div>
</template>


<script>
  import { mapState, mapActions } from 'vuex';
  import axios from 'axios';


  export default {
    name:"Modal",
    components: {
   
    },
    data() {
      return {
        email: '',
        password: '',
        file1:null,
        nom:null,
        prenom:null,
        mail:null,
        motdepasse:null,
        groupeTD:null,
        genre:null,
        motdepasse2:null


      }
    },
    created () {
      
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
      sendFile(){
          const reader = new FileReader();
           

          reader.readAsText(this.file1);
         
          reader.onload = evt => {
          let text = evt.target.result;
          var etuidantTab = []

          var etudiantsCSV = text.split(/\r?\n/);
           etudiantsCSV.forEach(element => {
             var etu = element.split(';')
             etuidantTab.push(etu)
           });

          //empty string at end?
          for (var i=1;i<etuidantTab.length;i++){
            if(etuidantTab[i].length >= 7){
              
              

              this.registrationEtuidant(etuidantTab[i][1],etuidantTab[i][2],etuidantTab[i][3],etuidantTab[i][4],etuidantTab[i][5])
            }
            
          }
        }
          
      },
       registrationEtuidant(nom,prenom,mail,pass,td){
        axios({
                  method: 'post',
                  url: 'user/registration',
                  data: {

                    nom : nom,
                    prenom:prenom,
                    numero:0,
                    password:pass,
                    groupeTD : td,
                    mail : mail,
                    genre:0

                  },
                  auth: {
                    username: this.user.mail,
                    password: this.user.pwd
                  }
                })
                .then(response => {

                    console.debug(response)
                    
                    
                    this.$bvModal.hide('modal-ajoutetuidant')
                    this.$emit('refreche')



                })
                .catch(error => {
                  console.debug(error)
                  
                })
       },
      etudiantSubmit() {
        
        axios({
            method: 'post',
            url: 'user/registration',
            data: {

              nom : this.nom,
              prenom:this.prenom,
              numero:0,
              password:this.motdepasse,
              groupeTD : this.groupeTD,
              mail : this.mail,
              genre:0

            },
            auth: {
              username: this.user.mail,
              password: this.user.pwd
            }
          })
          .then(response => {

              console.debug(response)
              
              
              this.$bvModal.hide('modal-ajoutetuidant')




          })
          .catch(error => {
            console.debug(error)
            
          })
      },
      
      ...mapActions([

      ]),

    }
  }
</script>
<style lang="scss">
@import "../../assets/custom.scss";
@import "node_modules/bootstrap/scss/bootstrap.scss";
@import "../../assets/sb-admin-2.min.css";

.mycontent-left {
  border-right: 1px dashed #333;
}
</style>