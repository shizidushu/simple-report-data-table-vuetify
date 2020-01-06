<template>
  <v-navigation-drawer v-model="showDrawer" app clipped>
    <v-list dense shaped>
      <v-list-item-group color="primary">
        <template v-for="(route, index) in userSidebarRoutes">
          <template v-if="!route.hidden && route.children">
            <v-list-group
              value="true"
              :key="index"
              :prepend-icon="route.icon"
              no-action
            >
              <template v-slot:activator>
                <v-list-item-content>
                  <v-list-item-title v-text="route.name"></v-list-item-title>
                </v-list-item-content>
              </template>
              <template v-for="(cRoute, idx) in route.children">
                <template v-if="!cRoute.hidden">
                  <v-list-item
                    :to="{ name: cRoute.name }"
                    :key="idx"
                    color="primary"
                  >
                    <v-list-item-icon v-if="cRoute.icon">
                      <v-icon v-text="cRoute.icon"></v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title
                        v-text="cRoute.name"
                      ></v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </template>
              </template>
            </v-list-group>
          </template>
          <template v-else-if="!route.hidden">
            <v-list-item :to="{ name: route.name }" :key="index">
              <v-list-item-icon v-if="route.icon">
                <v-icon v-text="route.icon"></v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title v-text="route.name"></v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </template>
        </template>
      </v-list-item-group>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  name: "Sidebar",
  props: {
    showDrawer: Boolean
  },
  data() {
    return {
      levelOneRoute: []
    };
  },
  computed: {
    ...mapGetters(["userSidebarRoutes"])
  },
  watch: {
    "$store.state.user.userRoles": {
      handler(val) {
        if (val) {
          this.$store.dispatch("user/getSidebarRoutesForUser", {
            routes: this.$router.options.routes
          });
        }
      },
      // immediate: true,
      deep: true
    }
  }
};
</script>
