<template>
  <v-container>
    <v-card>
      <v-card-title>
        User List
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
        :items="usersItems"
        show-expand
        :single-expand="singleExpand"
        :expanded.sync="expanded"
        item-key="AdminName"
      >
        <template v-slot:item.role_names="{ item }">
          <v-row>
            <ul v-for="role in item.role_names" :key="role">
              <li>{{ role }}</li>
            </ul>
          </v-row>
        </template>
        <template v-slot:expanded-item="{ headers, item }">
          <td
            :colspan="headers.length"
            v-if="Object.keys(item.implicit_permissions).length > 0"
          >
            <v-card>
              <v-card-title>
                Implicit Permissions
                <v-spacer></v-spacer>
                <v-text-field
                  v-model="expanded_table_search[item.ID]"
                  append-icon="search"
                  label="Search"
                  single-line
                  hide-details
                ></v-text-field>
              </v-card-title>
              <v-data-table
                :headers="expanded_table_headers"
                :items="
                  item.implicit_permissions.map(function(perm) {
                    perm.summary = get_value_of_path_info_by_key({
                      obj: perm.obj,
                      act: perm.act,
                      key: 'summary'
                    });
                    perm.description = get_value_of_path_info_by_key({
                      obj: perm.obj,
                      act: perm.act,
                      key: 'description'
                    });
                    return perm;
                  })
                "
                :search="expanded_table_search[item.ID]"
              >
                <template v-slot:item.description="{ item }">
                  <MarkdownDisplay :markdown="item.description" />
                </template>
              </v-data-table>
            </v-card>
          </td>
        </template>

        <template v-slot:item.action="{ item }">
          <v-icon small class="mr-2" @click.stop="edit_role(item)">edit</v-icon>
        </template>
      </v-data-table>
    </v-card>

    <v-dialog v-model="dialog" persistent max-width="800px">
      <v-card>
        <v-progress-linear
          :indeterminate="progressIndeterminate"
          color="teal"
        ></v-progress-linear>
        <v-card-title>Edit Role</v-card-title>
        <v-card-text>
          <v-container>
            <v-autocomplete
              chips
              multiple
              v-model="roleSelect"
              :items="roleItems"
            ></v-autocomplete>
          </v-container>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="close">Cancel</v-btn>
          <v-btn text @click="save">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { mapGetters } from "vuex";
import {
  get_all_subjects,
  get_grouping_policy,
  add_role_for_user,
  delete_role_for_user
} from "@/api/perm";
import MarkdownDisplay from "@/components/MarkdownDisplay";
export default {
  components: { MarkdownDisplay },
  data() {
    return {
      search: "",
      expanded: [],
      singleExpand: false,
      headers: [
        { text: "ID", value: "ID" },
        { text: "用户名", value: "AdminName" },
        { text: "昵称", value: "NickName" },
        { text: "中文名", value: "TrueName" },
        { text: "是否锁定", value: "IsLock" },
        { text: "角色", value: "role_names" },
        { text: "操作", value: "action", sortable: false }
        // {text: '隐式角色', value: 'implicit_roles'},
        // {text: '权限', value: 'permissions'},
        // { text: "隐式权限", value: "implicit_permissions" }
      ],
      expanded_table_search: {},
      expanded_table_headers: [
        { text: "sub", value: "sub" },
        { text: "obj", value: "obj" },
        { text: "act", value: "act" },
        { text: "summary", value: "summary" },
        { text: "description", value: "description" }
      ],
      dialog: false,
      roleSelect: null,
      roleItems: null,
      roleItem: null,
      progressIndeterminate: false
    };
  },
  computed: {
    ...mapGetters(["allUsers", "data_table_path_info"]),
    usersItems: function() {
      return this.allUsers.map(user => {
        return [
          "ID",
          "AdminName",
          "NickName",
          "TrueName",
          "IsLock",
          "role_names",
          "implicit_roles",
          "permissions",
          "implicit_permissions"
        ].reduce((obj, key) => {
          if (user && user.hasOwnProperty(key)) {
            obj[key] = user[key];
          }
          return obj;
        }, {});
      });
    }
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
    },
    async edit_role(item) {
      // get all roles
      const subjects_response = await get_all_subjects();
      let subject_names = subjects_response.data;
      const groupingPolic = await get_grouping_policy();
      const rolesInGroupPolicy = [
        ...new Set(groupingPolic.data.map(p => p[1]))
      ];
      let allRoles = [...new Set(subject_names.concat(rolesInGroupPolicy))];
      let user_names = this.allUsers.map(function(user) {
        return user.AdminName;
      });
      // for now, subjects should only contains role names
      // but I do this for logic smooth
      let user_roles = allRoles.filter(x => !user_names.includes(x));

      this.roleItems = user_roles;
      this.roleItem = item;
      // set selected to be current role_names
      this.roleSelect = item.role_names;
      this.dialog = true;
    },
    close() {
      this.dialog = false;
    },
    async save() {
      this.progressIndeterminate = true;
      if (this.roleItem.role_names != this.roleSelect) {
        // delete roles that removed from select
        for (let i = 0; i < this.roleItem.role_names.length; i++) {
          if (!this.roleSelect.includes(this.roleItem.role_names[i])) {
            // console.log(this.roleItem.AdminName);
            await delete_role_for_user(
              this.roleItem.AdminName,
              this.roleItem.role_names[i]
            );
            // console.log("deleted", this.roleItem.role_names[i]);
          }
        }

        // add roles that added from select
        for (let i = 0; i < this.roleSelect.length; i++) {
          if (!this.roleItem.role_names.includes(this.roleSelect[i])) {
            // console.log(this.roleItem.AdminName);
            // console.log(this.roleSelect[i]);
            await add_role_for_user(
              this.roleItem.AdminName,
              this.roleSelect[i]
            );
            // console.log("added", this.roleSelect[i]);
          }
        }

        // refresh data to update TableList view
        await this.$store.dispatch(
          "data_table/get_data_table_path_info_of_current_user"
        );
        // get users again to update the view
        await this.$store.dispatch("user/getAllUsers");
        await this.$store.dispatch("user/getUserRoles");
        await this.$store.dispatch("user/getRoutesForUser", {
          routes: this.$router.options.routes
        });
        await this.$store.dispatch("user/getSidebarRoutesForUser", {
          routes: this.$router.options.routes
        });
      }
      this.progressIndeterminate = false;
      this.dialog = false;
    }
  },
  mounted() {
    this.$store.dispatch("user/getAllUsers");
  }
};
</script>
