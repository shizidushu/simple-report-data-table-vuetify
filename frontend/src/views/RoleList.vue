<template>
  <v-container>
    <v-card>
      <v-card-title>
        Role List
        <v-spacer></v-spacer>
        <v-text-field
          v-model="search"
          append-icon="search"
          label="Search"
          single-line
          hide-details
        ></v-text-field>
      </v-card-title>
      <v-data-table
        :search="search"
        :headers="headers"
        :items="
          allRoles.map(function(role) {
            role.perm_summary = role.permissions.map(function(perm) {
              return get_value_of_path_info_by_key({
                obj: perm.obj,
                act: perm.act,
                key: 'summary'
              });
            });

            role.user_showname = role.users.map(function(user) {
              return user.AdminName + '(' + user.TrueName + ')';
            });
            return role;
          })
        "
      >
        <template v-slot:item.perm_summary="{ value }">
          <v-row>
            <ul v-for="(perm, index) in value" :key="index">
              <li>{{ perm }}</li>
            </ul>
          </v-row>
        </template>

        <template v-slot:item.user_showname="{ value }">
          <v-row>
            <ul v-for="(user, index) in value" :key="index">
              <li>{{ user }}</li>
            </ul>
          </v-row>
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  data() {
    return {
      search: "",
      headers: [
        { text: "Role Name", value: "name" },
        { text: "Permission", value: "perm_summary" },
        { text: "User", value: "user_showname" }
      ]
    };
  },
  computed: {
    ...mapGetters(["data_table_path_info", "allRoles"])
  },
  methods: {
    get_value_of_path_info_by_key({ obj, act, key }) {
      if (act == "view") {
        return obj;
      }
      let path = this.data_table_path_info.filter(function(p) {
        return p.path == obj && p.method == act;
      });
      return path[0][key];
    }
  },
  mounted() {
    this.$store.dispatch("role/getAllRoles");
  }
};
</script>
