
<template>
  <div class="greetings">
    <h1 class="green">{{ msg }}</h1>
    <h3>
      You’ve successfully created a project with
      <button @click="hello"> hello </button> +
      <a href="https://vuejs.org/" target="_blank" rel="noopener">Vue 3</a>.
    </h3>
  </div>
</template>

<script setup>
defineProps({
  msg: {
    type: String,
    required: true
  }
})
</script>


<script>
import { io } from "socket.io-client";

export default {
  name: "HomeView",
  data() {
    return {
        socket: null
    }
  },
  beforeMount() {
    this.socket = io();
  },
  mounted() {
    this.socket.on("hello response", () => {
      console.log("connected");
    });
  },
  unmounted() {
    this.socket.disconnect();
  },

  methods: {
    hello() {
      this.socket.emit("hello");
    },
  },
};

</script>


<style scoped>
h1 {
  font-weight: 500;
  font-size: 2.6rem;
  top: -10px;
}

h3 {
  font-size: 1.2rem;
}

.greetings h1,
.greetings h3 {
  text-align: center;
}

@media (min-width: 1024px) {
  .greetings h1,
  .greetings h3 {
    text-align: left;
  }
}
</style>
