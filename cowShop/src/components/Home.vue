<template>
    <v-card class="mx-auto">

        <v-toolbar color="indigo" dark>
            <v-app-bar-nav-icon></v-app-bar-nav-icon>

            <v-toolbar-title>cowShop</v-toolbar-title>

            <v-spacer></v-spacer>

            <v-btn icon="mdi-magnify"></v-btn>
        </v-toolbar>

        <v-container fluid>
            <v-row dense>
                <v-col v-for="card in products" :key="card.name" :cols="card.flex">
                    <v-card>
                        <v-img :src="card.image" class="align-end" gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
                            height="200px" cover>
                            <v-card-title class="text-white" v-text="card.name"></v-card-title>
                        </v-img>

                        <v-card-actions>
                            <v-btn size="small" color="surface-variant" variant="text" @click="gotoProduct(card)">View Product</v-btn>
                            <v-spacer></v-spacer>
                            <v-btn size="small" color="surface-variant" variant="text" icon="mdi-heart"></v-btn>

                        </v-card-actions>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>
    </v-card>
</template>
  
<script>
import { io } from "socket.io-client";

export default {
    name: "Home",
    data: () => ({
        socket: null,
        cards: [
            { title: 'Pre-fab homes', src: 'https://cdn.vuetifyjs.com/images/cards/house.jpg', flex: 6 },
            { title: 'Favorite road trips', src: 'https://cdn.vuetifyjs.com/images/cards/road.jpg', flex: 6 },
            { title: 'Best airlines', src: 'https://cdn.vuetifyjs.com/images/cards/plane.jpg', flex: 6 },
        ],
        products : []
    }),
    beforeMount() {
        this.socket = io();
    },
    mounted() {
        this.getProducts();
        this.socket.on('get products answer', (response) => {
            console.log(response)
            this.products = response
        });
    },
    methods: {
        getProducts(){
            this.socket.emit('get products');
        },
        gotoProduct(product){
            this.$router.push({ name: 'ProductView', props:product, params: { id: product._id.$oid } });
        }
    }
}
</script>