<template>
  <v-container fill-height>
    <Navbar @side-icon-click="handleDrawerVisiable"></Navbar>
    <v-content>
      <v-card class="mx-auto" max-width="500">
        <v-card-title>Error code：403</v-card-title>
        <v-card-subtitle>Sorry, you didn't have the permission to access.</v-card-subtitle>
        <v-card-actions>
          <v-btn @click="gohome">
            Back Home
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-content>
  </v-container>
</template>

<script>
import Navbar from "./Navbar";

export default {
  components: {
    Navbar
  },
  methods: {
    handleDrawerVisiable() {
      this.drawer = !this.drawer;
    },
    gohome() {
      this.$router.push({ name: "home" });
    }
  }
};
</script>

<!-- :key="key" force using created and mounted hook when path changes -->
