<template>
  <div>
    <b-modal id="modal-ajoutecole" size="lg" title="Ajouter une école">
      <div class="row" v-if="user.rank == 0">
        <b-form-group class="col-sm-12" label="Fichier (csv) :" label-for="file-small" label-size="sm">
          <b-form-file v-model="file1" class="d-inline" accept=".csv" ></b-form-file>
           <b-button @click="sendFile" class="d-inline mt-2 mr-2 btn btn-primary" type="submit">Envoyer</b-button>
        </b-form-group>
      </div>
       <div class="row">
          <div class="col-sm-7 mycontent-left" >
                <form class="mt-3" @submit.prevent="ecoleSubmit">
                  <div class="form-row">
                    <div class="col">
                      <input v-model="nomEcole" type="text" class="form-control" placeholder="Nom de l'ecole" required>
                    </div>
                    <div class="col">
                      <input v-model="complementEcole" type="text" class="form-control" placeholder="complement_ecole">
                    </div>
                  </div>
                  <div class="form-group">
                    <label for="exampleFormControlTextarea1">Desirption</label>
                    <textarea v-model="description" class="form-control" id="exampleFormControlTextarea1" rows="3" ></textarea>
                  </div>
                  <div class="form-row mt-4">
                    <div class="col">
                      <select v-model="type" class="form-control" id="exampleFormControlSelect1" placeholder="Type" required>
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
                  placeholder="Rechercher une adresse"
                  v-model="selectedAdress"
                  :options="adresses"
                  option-label="full"
                  :required="true"
                ></vue-single-select> 
                <a @click="addAdress = !addAdress" class="d-inline ml-2 text-white mt-2 d-sm-inline-block btn btn-sm btn-primary shadow-sm">
                  <i class="fas fa-plus"></i>
                  </a>
                <form v-if="addAdress" @submit.prevent="adressSubmit" class="mt-3">
                  <div class="form-row">
                    <div class="col-sm-3">
                      <input v-model="numRue" type="text" class="form-control" placeholder="Num rue" required>
                    </div>
                    <div class="col-sm-9">
                      <input v-model="nomRue" type="text" class="form-control" placeholder="Nom rue" required>
                    </div>
                  </div>
                  <div class="form-row mt-4">
                    <div class="col">
                      <input v-model="codePostal" type="text" class="form-control" placeholder="Code postal" required>
                    </div>
                    <div class="col">
                      <input v-model="ville" type="text" class="form-control" placeholder="Ville" required>
                    </div>
                  </div>
                  <div class="form-row mt-4">
                    <div class="col">
                      <input v-model="pays" type="text" class="form-control" placeholder="Pays" required> 
                    </div>
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
        adresses : [],
        selectedAdress : null,
        addAdress : false,
        nomEcole : null,
        complementEcole : null,
        description : null,
        type : -1,
        pays : null,
        ville : null,
        codePostal : null,
        nomRue : null,
        numRue : null,
        file1:null


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
      sendFile(){
          const reader = new FileReader();
           

          reader.readAsText(this.file1);
         
          reader.onload = evt => {
          let text = evt.target.result;
          var ecolesTab = []

          var ecolesCSV = text.split(/\r?\n/);
           ecolesCSV.forEach(element => {
             var ecole = element.split(';')
             ecolesTab.push(ecole)
           });

          //empty string at end?
          for (var i=1;i<ecolesTab.length;i++){
            if(ecolesTab[i].length >= 10){
              
              this.numRue = ecolesTab[i][5]
              this.nomRue = ecolesTab[i][6]
              this.codePostal = ecolesTab[i][7]
              this.ville = ecolesTab[i][8]
              this.pays = ecolesTab[i][9]

              
              
               
              this.nomEcole = ecolesTab[i][1]
              this.type = ecolesTab[i][4]
              this.description = ecolesTab[i][2]
              this.complementEcole = ecolesTab[i][3]

              this.registrationEcole(ecolesTab[i][5],ecolesTab[i][6],ecolesTab[i][8],ecolesTab[i][7],ecolesTab[i][9],ecolesTab[i][1],ecolesTab[i][4],ecolesTab[i][2],ecolesTab[i][4])
            }
            
          }
        }
          
      },
      registrationEcole(numRue,nomRue,ville,cp,pays,nomEcole,type,description,complementEcole){
        axios({
            method: 'post',
            url: 'adresse/registration',
            data: {

              num_rue : numRue,
              nom_rue : nomRue,
              ville : ville,
              cp : cp,
              pays : pays

            },
            auth: {
              username: this.user.mail,
              password: this.user.pwd
            }
          })
          .then(response => {
              console.debug(response)
              this.selectedAdress = response.data
              axios({
                method: 'post',
                url: 'ecole/registration',
                data: {

                  nom_ecole : nomEcole,
                  id_type_ecole : type,
                  description : description,
                  complement : complementEcole,
                  id_adresse_ecole : response.data.id_adresse

                },
                auth: {
                  username: this.user.mail,
                  password: this.user.pwd
                }
              })
              .then(response => {

                  console.debug(response)
                  
                  this.$emit('refreche')
                  




              })
              .catch(error => {
                console.debug(error)
                this.fetchData()
                this.$emit('refreche')
              })

          })
          .catch(error => {
            console.debug(error)
            this.fetchData()
             this.$emit('refreche')
          })
          this.$bvModal.hide('modal-ajoutecole')
          this.$emit('refreche')

      },
      ecoleSubmit() {
        console.debug("ecole "+this.selectedAdress.id_adresse)
        this.addAdress = false
        axios({
            method: 'post',
            url: 'ecole/registration',
            data: {

              nom_ecole : this.nomEcole,
              id_type_ecole : this.type,
              description : this.description,
              complement : this.complementEcole,
              id_adresse_ecole : this.selectedAdress.id_adresse

            },
            auth: {
              username: this.user.mail,
              password: this.user.pwd
            }
          })
          .then(response => {

              console.debug(response)
              
              this.$emit('refreche')
              this.$bvModal.hide('modal-ajoutecole')




          })
          .catch(error => {
            console.debug(error)
            this.fetchData()
          })
      },
      adressSubmit() {
         
        this.addAdress = false
        console.debug(this.numRue+" "+this.nomRue+" "+this.ville+" "+this.codePostal+" "+this.pays)
         axios({
            method: 'post',
            url: 'adresse/registration',
            data: {

              num_rue : this.numRue,
              nom_rue : this.nomRue,
              ville : this.ville,
              cp : this.codePostal,
              pays : this.pays

            },
            auth: {
              username: this.user.mail,
              password: this.user.pwd
            }
          })
          .then(response => {
              console.debug(response)
              this.selectedAdress = response.data
              
              this.fetchData()
              return this.selectedAdress 




          })
          .catch(error => {
            console.debug(error)
            this.fetchData()
            return null
          })
      },
      ...mapActions([

      ]),
     
      fetchData () {
          
      axios({
            method: 'get',
            url: 'adresses/',
            auth: {
              username: this.user.mail,
              password: this.user.pwd
            }
        })
      .then(response => {
        this.adresses=[]
        console.debug(response.data)
        response.data.forEach(element => {
          
          
          element['full'] = element['num_rue'] +" "+ element["nom_rue"]+" "+ element["ville"]+" "+ element["cp"]+" "+ element["pays"]
          this.adresses.push(element)
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
