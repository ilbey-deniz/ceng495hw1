<template>
    <div class="d-flex align-center justify-center" style="height: 100vh">
        <v-sheet width="400" class="mx-auto">
            <v-form fast-fail @submit.prevent="submit">
                <v-text-field variant="outlined" v-model="username" label="User Name"></v-text-field>
                <v-text-field variant="outlined" v-model="password" type="password" label="Password"></v-text-field>
                <v-text-field variant="outlined" v-model="passwordMatch" type="password" label="Re-type Password"></v-text-field>
                <v-select
                    label="User Type"
                    :items="['Admin', 'Regular']"
                ></v-select>

                <div class="mt-2" v-show="user_exists">
                    <p class="text-body-2" >User with specified username already exists.</p>
                </div>
  
                <v-btn type="submit" color="primary" block class="mt-2">Sign Up</v-btn>
  
            </v-form>
            <div class="mt-2">
                <p class="text-body-2">Already have an account? <a href="/login">Login</a></p>
            </div>
        </v-sheet>
    </div>
  </template>
  
<script>
import { io } from "socket.io-client";
  
  export default {
    name: "Signup",
    data() {
      return {
          valid: false,
          username: '',
          e_mail: '',
          password: '',
          passwordMatch: '',
          user_exists: false,
          missing_credentials: false,
          usernameRules: [
              v => !!v || 'username is required',
              v => v.length <= 20 || 'username must be less than 20 characters',
          ],
  
          e_mailRules: [
              v => !!v || 'e_mail is required',
              v => /.+@.+/.test(v) || 'E-mail must be valid',
          ],
  
          passwordRules: [
              v => !!v || 'password is required',
          ],
          passwordMatchRules: [
              v => !!v || 'password needs to be re-entered',
              v => v === this.password || 'passwords must match',
          ],
          socketIoSocket: null
      }
    },
    beforeMount() {
      this.socketIoSocket = io();
      this.token = localStorage.getItem("token");
        if (this.token !== null) {
          this.socketIoSocket.emit('token check', this.token);
          this.socketIoSocket.on("token check answer", (data) => {
            if(data["status"] === "success"){
              this.$router.push("/yonetim");
            }
            else{
              this.$router.push("/signup");
            }
          })
        }
        else{
          this.$router.push("/signup");
        }
      
    },
    mounted() {
        this.socketIoSocket.on("register answer", (data) => {
        if (data["status"] === "success") {
            localStorage.setItem("token", data["token"]);
            this.$router.push("/yonetim");
        }
        else{
            if(data["message"] === "userExists"){
                this.user_exists = true;
                setTimeout(() => {
                    this.user_exists = false;
                }, 5000);
            }
            else if(data["message"] === "missingCredentials"){
                this.missing_credentials = true;
                setTimeout(() => {
                    this.missing_credentials = false;
                }, 5000);
            }
        }
        })
      
    },
    methods: {
      submit() {
        if (this.username !== "" && this.password !== "" && this.e_mail !== "") {
              let check_data = {
                  "username": this.username,
                  "mail": this.e_mail,
                  "password": this.password
              }
              this.socketIoSocket.emit('register', check_data);
        }
      }
        
    },
    destroyed(){
      this.socketIoSocket.disconnect();
    }
  }
  </script>
  