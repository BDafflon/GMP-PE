<template>
  <div>
     

     <b-modal id="modal-ajoutformation" size="lg" title="Ajouter une formation">
      <div class="row" v-if="user.rank == 0">
        <b-form-group class="col-sm-12" label="Fichier (csv) :" label-for="file-small" label-size="sm">
          <b-form-file v-model="file1" class="d-inline" accept=".csv" ></b-form-file>
           <b-button @click="sendFileFormation" class="d-inline mt-2 mr-2 btn btn-primary" type="submit">Envoyer</b-button>
        </b-form-group>
      </div>
       <div class="row">
          <div class="col-sm-7 mycontent-left" >
                <form class="mt-3" @submit.prevent="formationSubmit">
                  <div class="form-row">
                    <vue-single-select class="d-inline"
                  name="maybe"
                  placeholder="Rechercher une ecole"
                  v-model="selectedEcole"
                  :options="ecoles"
                  option-label="nom_ecole"
                  :required="true"
                ></vue-single-select> 
                  </div>
                  <div class="form-row">
                    <div class="col">
                      <input v-model="specialite" type="text" class="form-control" placeholder="Spécialité" required>
                    </div>
                    <div class="col">
                      <input v-model="siteweb" type="text" class="form-control" placeholder="Site web">
                    </div>
                    <div class="col">
                      <input v-model="brochure" type="text" class="form-control" placeholder="Brochure">
                    </div>
                  </div>
                  <div class="form-group">
                    <label for="exampleFormControlTextarea1">Desirption</label>
                    <textarea v-model="description" class="form-control" id="exampleFormControlTextarea1" rows="3" ></textarea>
                  </div>
                  <div class="form-row mt-4">
                    <div class="col">
                      <select v-model="niveau" class="form-control" id="exampleFormControlSelect1" placeholder="Niveau" required>
                        <option value="" selected disabled>Niveau</option>
                        <option value="2">Bac +2</option>
                        <option value="3">Bac +3</option>
                        <option value="5">Bac +5</option>
                        <option value="8">Bac +8</option>
                      </select>
                    </div>
                     <div class="col">
                      <select v-model="alternance" class="form-control" id="exampleFormControlSelect1" placeholder="Alternance" required>
                        <option value="-1" selected disabled>Alternance</option>
                        <option value="0">Oui</option>
                        <option value="1">Non</option>
                         
                      </select>
                    </div>
                    <div class="col">
        
                      <select  class="form-control" v-model="typeFormation">
                        <option value="-1" selected disabled>Type</option>
                        <option value="0">Publique</option>
                        <option value="1">Privée</option>
                      </select>
                    </div>
                    <div class="col">
                      <button class="btn btn btn-primary btn-block" type="submit">Ajouter</button>
                    </div>
                  </div>
                </form>


          </div>
          <div class="col-sm-5 mt-3">
                <vue-single-select class="d-inline"
                  name="maybe"
                  placeholder="Rechercher un responsable"
                  v-model="selectedResp"
                  :options="responsables"
                  option-label="full"
                  :required="true"
                ></vue-single-select> 
                <a @click="addResp = !addResp" class="d-inline ml-2 text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm">
                  <i class="fas fa-plus"></i>
                  </a>
                <form v-if="addResp" @submit.prevent="respSubmit" class="mt-3">
                  <div class="form-row">
                    <div class="col-sm-6">
                      <input v-model="nom" type="text" class="form-control" placeholder="Nom" required>
                    </div>
                    <div class="col-sm-6">
                      <input v-model="prenom" type="text" class="form-control" placeholder="Prenom" required>
                    </div>
                  </div>
                  <div class="form-row mt-4">
                    <div class="col">
                      <input v-model="mail" type="text" class="form-control" placeholder="Email" required>
                    </div>
                    <div class="col">
                      <input v-model="telephone" type="text" class="form-control" placeholder="Telephone" required>
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
        ecoles : [],
        responsables : [],
        selectedEcole : null,
        selectedResp : null,
        file1:null,
        addResp : false,

        //RESP
        nom : null,
        prenom : null,
        mail:null,
        telephone:null,

        //FORMATIO?
        specialite:null,
        brochure:null,
        description:null,
        niveau:"",
        alternance:-1,
        siteweb:null,
        typeFormation:-1




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
      sendFileFormation(){
          const reader = new FileReader();
           

          reader.readAsText(this.file1);
         
          reader.onload = evt => {
          let text = evt.target.result;
          var formations = []

          var formationsCSV = text.split(/\r?\n/);
           formationsCSV.forEach(element => {
             var formation = element.split(';')
             formations.push(formation)
           });

          //empty string at end?
          for (var i=1;i<formations.length;i++){
             
            if(formations[i].length >=12){
              console.debug(formations[i])
              this.formationFullSubmit(formations[i])
             
            }
            
          }
        }
          
      },
      formationFullSubmit(dataF){
        axios({
            method: 'post',
            url: 'responsable/registration',
            data: {

              nom_responsable : dataF[8],
              prenom_responsable : dataF[9],
              mail_responsable :  dataF[10],
              telephone_responsable :  dataF[11],


            },
            auth: {
              username: this.user.mail,
              password: this.user.pwd
            }
          })
          .then(response => {

              console.debug(response.data)
              
              axios({
                      method: 'post',
                      url: 'formation/registration',
                      data: {

                        specialite : dataF[2],
                        description : dataF[5],
                        site_web_url : dataF[3],
                        brochure_url : dataF[4],
                        alternance : dataF[6],
                        type_formation : 0,
                        niveau :dataF[7],
    
                        id_responsable : response.data.id_responsable,
                        id_ecole : dataF[1]


                      },
                      auth: {
                        username: this.user.mail,
                        password: this.user.pwd
                      }
                    })
                    .then(response => {

                        console.debug(response)
                        
                        this.fetchData()
                        this.$bvModal.hide('modal-ajoutformation')
                        this.$emit('refreche')
                        

                    })
                    .catch(error => {
                      console.debug(error)
                      this.fetchData()
                      this.$bvModal.hide('modal-ajoutformation')
                        this.$emit('refreche')
                    })

          })
          .catch(error => {
            console.debug(error)
            this.fetchData()
            this.$bvModal.hide('modal-ajoutformation')
                        this.$emit('refreche')
          })


      },
      formationSubmit(){
          axios({
                      method: 'post',
                      url: 'formation/registration',
                      data: {

                        specialite : this.specialite,
                        description : this.description,
                        site_web_url : this.siteweb,
                        brochure_url : this.brochure,
                        alternance : this.alternance,
                        type_formation : this.typeFormation,
                        niveau : this.niveau,
    
                        id_responsable : this.selectedResp.id_responsable,
                        id_ecole : this.selectedEcole.id_ecole


                      },
                      auth: {
                        username: this.user.mail,
                        password: this.user.pwd
                      }
                    })
                    .then(response => {

                        console.debug(response)
                        
                        this.fetchData()
                        this.$bvModal.hide('modal-ajoutformation')
                        this.$emit('refreche')




                    })
                    .catch(error => {
                      console.debug(error)
                      this.fetchData()
                    })
      },

      respSubmit(){
          this.addResp = false
        axios({
            method: 'post',
            url: 'responsable/registration',
            data: {

              nom_responsable : this.nom,
              prenom_responsable : this.prenom,
              mail_responsable : this.mail,
              telephone_responsable : this.telephone


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
      registrationFormation(){
        axios({
            method: 'post',
            url: 'adresse/registration',
            data: {

               

            },
            auth: {
              username: this.user.mail,
              password: this.user.pwd
            }
          })
          .then(response => {
              console.debug(response)
              this.selectedAdress = response.data
               
          })
          .catch(error => {
            console.debug(error)
            this.fetchData()
             this.$emit('refreche')
          })
          this.$bvModal.hide('modal-ajoutecole')
          this.$emit('refreche')

      },

      
      ...mapActions([

      ]),
     
      fetchData () {
          
      axios({
            method: 'get',
            url: 'ecoles/',
            auth: {
              username: this.user.mail,
              password: this.user.pwd
            }
        })
      .then(response => {
        this.ecoles = response.data
        


      })
      .catch(error => {
        console.debug(error)
      })

      axios({
            method: 'get',
            url: 'responsables/',
            auth: {
              username: this.user.mail,
              password: this.user.pwd
            }
        })
      .then(response => {
        this.responsables=[]
        response.data.forEach(element => {
          var resp = element
          resp['full'] = element.nom_responsable+" "+element.prenom_responsable
          this.responsables.push(resp)
        });
        

        


      })
      .catch(error => {
        console.debug(error)
      })


    }


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