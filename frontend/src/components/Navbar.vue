<template>
  <v-app-bar app clipped-left dense>
    <v-app-bar-nav-icon @click="handleDrawerToggle" />

    <v-img
      alt="Vuetify Logo"
      class="shrink mr-2"
      contain
      :src="`${publicPath}logo.svg`"
      transition="scale-transition"
      width="40"
    />

    <v-toolbar-title>Simple Report</v-toolbar-title>

    <v-spacer></v-spacer>


    <v-menu attach offset-y>
      <template v-slot:activator="{ on }">
        <v-btn outlined v-on="on">
          <v-icon left>mdi-account-circle</v-icon>
          {{ username }}
        </v-btn>
      </template>
      <v-list>
        <v-list-item @click="logout">
          <v-list-item-title>Logout</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>

    <v-btn fab text @click="changeTheme">
      <v-icon :color="`${!ActivateLightTheme && 'yellow'}`" :light="true">mdi-brightness-4</v-icon>
    </v-btn>
  </v-app-bar>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  name: "Navbar",
  data() {
    return {
      publicPath: process.env.BASE_URL
    }
  },
  computed: {
    ...mapGetters(["username", "truename", "ActivateLightTheme"])
  },
  methods: {
   changeTheme() {
     this.$store.dispatch("app/changeTheme");
    },
    handleDrawerToggle() {
      this.$emit("side-icon-click");
    },
    logout() {
      this.$store
        .dispatch("user/logout")
        .then(() => {
          this.$router.push("/login");
        })
    }
  }
};
</script>
