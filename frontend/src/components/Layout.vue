<template>
  <v-container>
    <Sidebar :show-drawer="drawer"></Sidebar>
    <Navbar @side-icon-click="handleDrawerVisiable"></Navbar>
    <v-content>
      <v-alert v-bind="alertInfo.props" @input="toggleAlertValue">
        {{ alertInfo.defaultSlot }}
      </v-alert>
      <router-view :key="key"></router-view>
    </v-content>
  </v-container>
</template>

<script>
import Navbar from "./Navbar";
import Sidebar from "./Sidebar";

import { mapGetters, mapActions } from "vuex";

export default {
  name: "Layout",
  components: {
    Navbar,
    Sidebar
  },
  data() {
    return {
      drawer: true
    };
  },
  computed: {
    ...mapGetters(["alertInfo"]),
    key() {
      return this.$route.path;
    }
  },
  methods: {
    ...mapActions("app", ["toggleAlertValue", "changeShowAlert"]),
    handleDrawerVisiable() {
      this.drawer = !this.drawer;
    }
  }
};
</script>

<!-- :key="key" force using created and mounted hook when path changes -->
