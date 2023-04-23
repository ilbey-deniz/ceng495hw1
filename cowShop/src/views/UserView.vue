<template>
    <div class="app">
        <h1>User: {{ this.username }}</h1>
        <h2>Average Rating: {{ this.avg_rating.toFixed(2) }}/5</h2>
        <v-container fluid>
            <v-row>
                <v-col>
                    <v-list lines="two">
                        <v-subheader>Reviews</v-subheader>
                        <v-list-item v-for="review in reviews" :key="review._id" :title="review.done_by_username"
                            :subtitle="review.text">
                            <template v-slot:append>
                                <router-link :to="{ name: 'ProductView', params: { id: review.product_id.$oid } }">
                                    <v-btn size="small">View Product</v-btn>
                                </router-link>
                                <v-btn @click="deleteReview(review.product_id)">
                                    <v-icon small>mdi-delete</v-icon>
                                </v-btn>
                            </template>
                        </v-list-item>
                    </v-list>
                </v-col>
            </v-row>
        </v-container>

    </div>
</template>

<script>
import { io } from "socket.io-client";

export default {
    name: "UserView",
    data() {
        return {
            username: "",
            reviews: [],
            ratings: [],
            avg_rating: 0,
            socket: null,
            user_id: "",
        }
    },
    beforeMount() {
        if (localStorage.getItem("token") == null)
            this.$router.push("/login")
        this.user_id = this.parseJwt(localStorage.getItem("token"))["sub"]
        console.log(this.user_id)
        if (this.user_id != this.$route.params.id)
            this.$router.push("/login")
    },
    mounted() {
        this.socket = io();
        this.socket.emit("get user", this.$route.params.id);
        this.socket.on('get user answer', (response) => {
            this.username = response
        });
        this.socket.emit("get user reviews", this.$route.params.id);
        this.socket.on('get user reviews answer', (response) => {
            this.reviews = response
        });
        this.socket.emit("get user ratings", this.$route.params.id);
        this.socket.on('get user ratings answer', (response) => {
            this.ratings = response
            this.avgRating()
        });
        this.socket.on("delete review answer", (response) => {
            if (response.status == "success")
                this.$router.go()
        });
    },
    unmounted() {
        this.socket.disconnect();
    },
    methods: {
        deleteReview(product_id) {
            let req = {
                done_by: this.$route.params.id,
                product_id: product_id
            }
            this.socket.emit("delete review", req);
        },
        avgRating() {
            let sum = 0
            for (let i = 0; i < this.ratings.length; i++) {
                sum += this.ratings[i].rating
            }
            this.avg_rating = this.ratings.length ? sum / this.ratings.length : 0
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
}
</script>