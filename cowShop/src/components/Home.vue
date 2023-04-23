<template>
    <v-card class="mx-auto">
        <v-container fluid>
            <v-row dense>
                <v-col v-for="card in products" :key="card.name" :cols="card.flex">
                    <v-card>
                        <v-img :src="card.image" class="align-end" gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
                            height="200px" cover>
                            <v-card-title class="text-white" v-text="card.name"></v-card-title>
                        </v-img>

                        <v-card-actions>
                            <router-link :to="{ name: 'ProductView',params: { id: card._id.$oid} }">
                                <v-btn size="small" color="surface-variant" variant="text">View Product</v-btn>
                            </router-link>

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
        products : []
    }),
    beforeMount() {
        this.socket = io();
    },
    mounted() {
        this.getProducts();
        this.socket.on('get products answer', (response) => {
            this.products = response
        });
    },
    methods: {
        getProducts(){
            this.socket.emit('get products');
        },
    },
    unmounted() {
        this.socket.off('get products answer')
        this.socket.disconnect()
    }
}
</script>