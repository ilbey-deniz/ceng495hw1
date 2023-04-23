<template>
  <v-toolbar color="indigo" dark>
    <v-app-bar-nav-icon></v-app-bar-nav-icon>

    <router-link to="/">
      <v-toolbar-title class="text-white">cowShop</v-toolbar-title>
    </router-link>

    <v-spacer></v-spacer>


    <v-btn icon="mdi-account" @click="user"></v-btn>
    <v-btn icon="mdi-wrench" @click="admin"></v-btn>
    <v-btn v-if=this.logged_in icon="mdi-logout" @click="logout"></v-btn>
  </v-toolbar>
  <router-view />
</template>

<script>
export default {
  name: "App",
  beforeMount() {
    if (localStorage.getItem('token') != null)
      this.logged_in = true
    else
      this.logged_in = false
  },
  data: () => ({
    logged_in: false,

  }),
  methods: {
    logout() {
      localStorage.removeItem('token')
      this.logged_in = false
      this.$router.push("/")
    },
    admin() {
      this.$router.push("/admin")
    },
    user() {
      this.$router.push("/login")
    },

  }
}


</script>
