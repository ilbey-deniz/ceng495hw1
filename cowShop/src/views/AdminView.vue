<template>
    <v-container fluid>
        <v-row>
            <v-col>
                <v-list lines="two">
                    <v-subheader>All Products</v-subheader>
                    <v-list-item v-for="product in products" :key="product._id" :title="product.name"
                        :subtitle="getSeller(product.seller)">
                        <template v-slot:append>
                            <router-link :to="{ name: 'ProductView', params: { id: product._id.$oid } }">
                                <v-btn size="small">View Product</v-btn>
                            </router-link>
                            <router-link :to="{ name: 'UserView', params: { id: product.seller.$oid } }">
                                <v-btn size="small">View Seller</v-btn>
                            </router-link>
                            <v-btn @click="deleteProduct(product._id.$oid)">
                                <v-icon small>mdi-delete</v-icon>
                            </v-btn>
                        </template>
                    </v-list-item>
                </v-list>
            </v-col>
            <v-col>
                <v-list lines="two">
                    <v-subheader>All Users</v-subheader>
                    <v-list-item v-for="user in users" :key="user._id" :title="user.username">
                        <template v-slot:append>
                            <router-link :to="{ name: 'UserView', params: { id: user._id.$oid } }">
                                <v-btn size="small">View User</v-btn>
                            </router-link>
                            <v-btn v-if="current_user_id != user._id.$oid" @click="deleteUser(user._id.$oid)">
                                <v-icon small>mdi-delete</v-icon>
                            </v-btn>
                        </template>
                    </v-list-item>
                </v-list>
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <h2>Add a new product</h2>
                <v-select v-model="product_type" :items="product_types"></v-select>
                <v-form v-if="product_type == 'Consumer Electronics'">
                    <v-text-field v-model="product['name']" label="Name"></v-text-field>
                    <v-text-field v-model="product['description']" label="Description"></v-text-field>
                    <v-text-field v-model="product['price']" label="Price"></v-text-field>
                    <v-text-field v-model="product['image']" label="Image src"></v-text-field>
                    <v-text-field v-model="product['seller']" label="Seller"></v-text-field>
                    <v-text-field v-model="spec['RAM']" label="RAM"></v-text-field>
                    <v-text-field v-model="spec['Screen Size']" label="Screen Size"></v-text-field>
                    <v-text-field v-model="spec['Storage']" label="Storage"></v-text-field>
                </v-form>
                <v-form v-if="product_type == 'Clothing'">
                    <v-text-field v-model="product['name']" label="Name"></v-text-field>
                    <v-text-field v-model="product['description']" label="Description"></v-text-field>
                    <v-text-field v-model="product['price']" label="Price"></v-text-field>
                    <v-text-field v-model="product['image']" label="Image src"></v-text-field>
                    <v-text-field v-model="product['seller']" label="Seller"></v-text-field>
                    <v-text-field v-model="product['color']" label="Color"></v-text-field>
                    <v-text-field v-model="product['size']" label="Size"></v-text-field>
                </v-form>
                <v-form v-if="product_type == 'Snacks'">
                    <v-text-field v-model="product['name']" label="Name"></v-text-field>
                    <v-text-field v-model="product['description']" label="Description"></v-text-field>
                    <v-text-field v-model="product['price']" label="Price"></v-text-field>
                    <v-text-field v-model="product['image']" label="Image src"></v-text-field>
                    <v-text-field v-model="product['seller']" label="Seller"></v-text-field>

                </v-form>
                <v-form v-if="product_type == 'Monitors'">
                    <v-text-field v-model="product['name']" label="Name"></v-text-field>
                    <v-text-field v-model="product['description']" label="Description"></v-text-field>
                    <v-text-field v-model="product['price']" label="Price"></v-text-field>
                    <v-text-field v-model="product['image']" label="Image src"></v-text-field>
                    <v-text-field v-model="product['seller']" label="Seller"></v-text-field>
                    <v-text-field v-model="spec['Screen Size']" label="Screen Size"></v-text-field>
                </v-form>
                <v-form v-if="product_type == 'Computer Components'">
                    <v-text-field v-model="product['name']" label="Name"></v-text-field>
                    <v-text-field v-model="product['description']" label="Description"></v-text-field>
                    <v-text-field v-model="product['price']" label="Price"></v-text-field>
                    <v-text-field v-model="product['image']" label="Image src"></v-text-field>
                    <v-text-field v-model="product['seller']" label="Seller"></v-text-field>
                    <v-text-field v-model="spec['RAM']" label="RAM"></v-text-field>

                </v-form>
                <v-btn :rules="addProductRules" @click="addProduct">Add Product</v-btn>
            </v-col>
            <v-col>
                <h2>To add a new user, you can proceed to Sign Up page*.</h2>
                <router-link :to="{ name: 'SignupView' }">
                    <v-btn size="small">GO TO SIGN UP</v-btn>
                </router-link>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import { io } from "socket.io-client";

export default {
    name: "AdminView",
    data() {
        return {
            token: "",
            current_user_id: "",
            addProductRules: [
                v => !!v || 'Product type is required',
                v => v == "Choose product type.." || 'Product type is required',
            ],
            users: [],
            products: [],
            socket: null,
            new_product: {},

            name: "",
            description: "",
            price: "",
            image: "",
            seller: "",
            spec: {},
            product: {},

            color: "",
            size: "",

            product_types: ["Consumer Electronics", "Clothing", "Snacks", "Monitors", "Computer Components"],
            product_type: ""

        }
    },
    beforeMount() {
        this.socket = io();
        this.token = localStorage.getItem("token");
        if (this.token == null) {
            this.$router.push("/login");
        }
        let parsed_token = this.parseJwt(this.token);
        this.current_user_id = parsed_token["sub"];
        this.socket.emit("is admin", parsed_token["sub"]);
        this.socket.on('is admin answer', (response) => {
            if(!response){
                this.$router.push("/login");
            }
        });
    },
    mounted() {
        this.socket = io();
        this.socket.emit("get users");
        this.socket.on('get users answer', (response) => {
            this.users = response
        });
        this.socket.emit("get products");
        this.socket.on('get products answer', (response) => {
            this.products = response
        });
        this.socket.on("add product answer", (response) => {
            this.$router.go()
        });
        this.socket.on("delete product answer", (response) => {
            this.$router.go()
        });
        this.socket.on("delete user answer", (response) => {
            this.$router.go()
        });
    },
    methods: {
        getSeller(seller_id) {
            for (let i = 0; i < this.users.length; i++) {
                if (this.users[i]._id.$oid == seller_id.$oid)
                    return this.users[i].username
            }
        },
        deleteProduct(product_id) {
            this.socket.emit("delete product", product_id);
        },
        deleteUser(user_id) {
            this.socket.emit("delete user", user_id);
        },
        addProduct() {

            if (["Snacks", "Clothing"].includes(this.product_type)) {
                delete this.product.spec
            }
            else {
                this.product.spec = this.spec
            }
            this.socket.emit("add product", this.product);
            this.product = {}
            this.spec = {}
            this.product_type = "Choose product type.."
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
        this.socket.disconnect()
    },
}

</script>