<template>
    <div class="app">
        <v-toolbar color="indigo" dark>
            <v-app-bar-nav-icon></v-app-bar-nav-icon>

            <v-toolbar-title>cowShop</v-toolbar-title>

            <v-spacer></v-spacer>

            <v-btn icon="mdi-magnify"></v-btn>
        </v-toolbar>

       
    </div>
</template>
<script>


export default {
  name: "ProductView",
  props: {
    id: {
      product_obj: Object,
    }
  },
  onMounted() {
    console.log(this.product_obj);
  }
} 
</script>