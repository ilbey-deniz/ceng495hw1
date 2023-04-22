<template>
    <div class="app">
        <v-toolbar color="indigo" dark>
            <v-app-bar-nav-icon></v-app-bar-nav-icon>

            <v-toolbar-title>cowShop</v-toolbar-title>

            <v-spacer></v-spacer>

            <v-btn icon="mdi-magnify"></v-btn>
        </v-toolbar>
        <v-container fluid>
            <v-row dense>
                <v-col>
                    <v-img :src="product.image">
                        <v-card-title class="text-black" v-text="product.name"></v-card-title>
                    </v-img>
                </v-col>
            </v-row>
        </v-container>
        

    </div>
</template>
<script>
import { io } from "socket.io-client";

export default {
    name: "ProductView",
    data: () => ({
        socket: null,
        product: {}
    }),
    beforeMount() {
        this.socket = io();
        console.log(this.$route.params)
        this.socket.emit("get product", this.$route.params.id);
        this.socket.on('get product answer', (response) => {
            this.product = response
        });
    },
    unmounted() {
        this.socket.off('get product answer')
        this.socket.disconnect()
    }
}
</script>