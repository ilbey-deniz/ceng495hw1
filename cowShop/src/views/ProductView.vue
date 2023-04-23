<template>
    <div class="app">
        <v-toolbar color="indigo" dark>
            <v-app-bar-nav-icon></v-app-bar-nav-icon>

            <v-toolbar-title>cowShop</v-toolbar-title>

            <v-spacer></v-spacer>

            <v-btn icon="mdi-magnify"></v-btn>
        </v-toolbar>
        <v-container fluid>
            <v-row>
                <v-col>
                    <v-img :src="product.image"></v-img>

                </v-col>
                <v-col>
                    <v-card>
                        <v-card-title class="text-black" v-text="product.name"></v-card-title>
                        <v-card-text class="text-black" v-text="product.description"></v-card-text>
                        
                        <v-card-text class="text-black" v-text="product.price + ' TL'"></v-card-text>
                        <v-card-text class="text-black">
                            <router-link :to="{ name: 'UserView',params: { id: this.product.seller.$oid} }" v-text="'Seller: ' + seller"></router-link>
                        </v-card-text>
                        <v-card-text class="text-black" v-text="'Average rating: '+ this.avg_rating + '/5'"></v-card-text>
                        <v-rating
                            v-model="rating"
                            bg-color="orange-lighten-1"
                            color="blue"
                            @input="submitRating"
                        ></v-rating>
                        <v-list lines="one">
                            <v-subheader>Specs</v-subheader>
                            <v-list-item v-for="(value, name) in product.spec" :title="name" :subtitle="value"></v-list-item>
                        </v-list>
                        <v-card-text class="text-black" v-text="product.size"></v-card-text>
                        <v-card-text class="text-black" v-text="product.color"></v-card-text>
                    </v-card>

                    <v-list lines="two">
                        <v-subheader>Reviews</v-subheader>
                        <v-list-item v-for="review in reviews" :key="review._id" :title="review.done_by_username" :subtitle="review.text"></v-list-item>
                    </v-list>
                    <v-form @submit.prevent="submitReview" v-model="isFormValid">
                        <v-text-field v-model="comment" :rules="commentRules" label="Make a review" variant="outlined"></v-text-field>
                        <v-btn :disabled="!isFormValid" type="submit" color="primary" >ADD REVIEW</v-btn>
                    </v-form>
                    
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
        product: {},
        reviews: [],
        specs: false,
        seller: "",
        avg_rating: 0,
        rating: 0,
        commentRules: [
            v => (v && v.length > 10) || 'Review must be greater than 10 characters',
        ],
        comment: "",
        isFormValid: false,
    }),
    mounted() {
        this.socket = io();
        this.socket.emit("get product", this.$route.params.id);
        this.socket.on('get product answer', (response) => {
            this.product = response

            this.socket.emit("get user", this.product.seller.$oid);
            this.socket.on('get user answer', (response) => {
                this.seller = response
            });
        });

        this.socket.emit("get product review", this.$route.params.id);
        this.socket.on('get product review answer', (response) => {
            this.reviews = response
        });

        this.socket.emit("get product ratings", this.$route.params.id);
        this.socket.on('get product ratings answer', (response) => {
            let ratings = response
            let sum = 0
            for (let i = 0; i < ratings.length; i++) {
                sum += ratings[i].rating
            }
            this.avg_rating = ratings.length ? sum / ratings.length : 0
            this.rating= this.avg_rating

        });

        this.socket.on('submit review answer', (response) => {
            if (response.status == "success") {
                this.$router.go()
            }
            console.log(response)
        });

        this.socket.on('submit rating answer', (response) => {
            if(response.status == "success")
                this.$router.go()
            console.log(response)
        });
    },
    unmounted() {
        this.socket.disconnect()
    },
    methods: {
        submitReview() {
            this.socket.emit("submit review", {
                product_id: this.$route.params.id,
                text: this.comment,
            });
        },
        submitRating() {
            this.socket.emit("submit rating", {
                product_id: this.$route.params.id,
                rating: this.rating,
            });
        }
    }
}
</script>