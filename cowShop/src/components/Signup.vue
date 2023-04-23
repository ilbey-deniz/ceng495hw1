<template>
  <div class="d-flex align-center justify-center" style="height: 100vh">
    <v-sheet width="400" class="mx-auto">
      <v-form fast-fail @submit.prevent="submit">
        <v-text-field variant="outlined" v-model="username" label="User Name"></v-text-field>
        <v-text-field variant="outlined" v-model="password" type="password" label="Password"></v-text-field>
        <v-text-field variant="outlined" v-model="passwordMatch" type="password" label="Re-type Password"></v-text-field>
        <v-select label="User Type" :items="['Admin', 'Regular']" v-model="user_type"></v-select>

        <div class="mt-2" v-show="user_exists">
          <p class="text-body-2">User with specified username already exists.</p>
        </div>

        <v-btn type="submit" :color="primary" block class="mt-2">Sign Up</v-btn>

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
      user_type: '',
      password: '',
      passwordMatch: '',
      user_exists: false,
      missing_credentials: false,
      usernameRules: [
        v => !!v || 'username is required',
        v => v.length <= 20 || 'username must be less than 20 characters',
      ],
      passwordRules: [
        v => !!v || 'password is required',
      ],
      passwordMatchRules: [
        v => !!v || 'password needs to be re-entered',
        v => v === this.password || 'passwords must match',
      ],
      socket: null
    }
  },
  beforeMount() {
    this.socket = io();
    

  },
  mounted() {
    this.socket.on("register answer", (data) => {
      if (data["status"] === "success") {
        localStorage.setItem("token", data["token"]);
        this.$router.go("/");
      }
      else {
        if (data["message"] === "userExists") {
          this.user_exists = true;
          setTimeout(() => {
            this.user_exists = false;
          }, 5000);
        }
        else if (data["message"] === "missingCredentials") {
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

      let check_data = {
        username: this.username,
        password: this.password,
        is_admin: this.user_type === "Admin",
      }
      this.socket.emit('register', check_data);
    }


  },
  unmounted() {
    this.socket.disconnect();
  }
}
</script>
  