<template>
  <div class="d-flex align-center justify-center" style="height: 100vh">
    <v-sheet width="400" class="mx-auto">
      <v-form fast-fail @submit.prevent="submit">
        <v-text-field variant="outlined" v-model="username" label="User Name"></v-text-field>

        <v-text-field variant="outlined" v-model="password" type="password" label="Password"></v-text-field>

        <p class="text-body-2" v-show="no_such_user || wrong_password"> Wrong password or username.</p>
        <v-btn type="submit" color="primary" block class="mt-2">Login</v-btn>

      </v-form>
      <div class="mt-2">
        <p class="text-body-2">Don't have an account? <a href="/signup">Sign Up</a></p>
      </div>
    </v-sheet>
  </div>
</template>

<script>
import { io } from "socket.io-client";


export default {
  name: "Login",
  data() {
    return {
      valid: false,
      username: '',
      password: '',
      missing_credentials: false,
      wrong_password: false,
      no_such_user: false,

      passwordRules: [
        v => !!v || 'password is required',
      ],
      socket: null
    }
  },
  beforeMount() {
    this.socket = io();
    this.token = localStorage.getItem("token");
    if (this.token != null) {
        var payload = this.parseJwt(this.token)
        this.$router.push("/user/"+payload["sub"])
      }
  },
  mounted() {
    this.socket.on("login answer", (data) => {
      console.log(data);
      if (data["status"] === "success") {
        localStorage.setItem("token", data["token"]);
        this.$router.go("/");
      }
      else {
        if (data["message"] === "noSuchUser") {
          this.no_such_user = true;
          setTimeout(() => {
            this.no_such_user = false;
          }, 5000);
        }
        else if (data["message"] === "missingCredentials") {
          this.missing_credentials = true;
          setTimeout(() => {
            this.missing_credentials = false;
          }, 5000);
        }
        else if (data["message"] === "wrongPassword") {
          this.wrong_password = true;
          setTimeout(() => {
            this.wrong_password = false;
          }, 5000);
        }
      }
    })

  },
  methods: {
    submit() {
      if (this.username !== "" && this.password !== "") {
        let check_data = {
          "username": this.username,
          "password": this.password
        }
        this.socket.emit('login', check_data);
      }
    },
    parseJwt(token) {
      var base64Url = token.split('.')[1];
      var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      var jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function (c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
      }).join(''));

      return JSON.parse(jsonPayload);
    }

  },
  unmounted() {
    this.socket.disconnect();
  }
}
</script>
  