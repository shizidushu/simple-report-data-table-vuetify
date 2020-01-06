<template>
  <div id="app">
    <v-app :dark="ActivateLightTheme">
      <router-view></router-view>
    </v-app>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  name: "App",
  // data() {
  //   return {
  //     setTheme: null
  //   }
  // },
  computed: {
    ...mapGetters(["ActivateLightTheme"])
  },
  watch: {
    "$store.state.app.ActivateLightTheme": {
      handler(val) {
        this.$vuetify.theme.dark = !val
      }
      , immediate: true, deep: true
    }
  }
};
</script>
