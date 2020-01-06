/* eslint-disable */
import request from "@/utils/request";
import { get_implicit_permissions_for_user } from "@/api/perm";

const state = {
  openapi_json: {},
  data_table_path_info: [],
  data_table_path_info_of_current_user: []
};

const mutations = {
  SET_OPENAPI_JSON: (state, data) => {
    state.openapi_json = data;
  },
  SET_DATA_TABLE_PATH_INFO: (state, data) => {
    state.data_table_path_info = data;
  },
  SET_DATA_TABLE_PATH_INFO_OF_CURRENT_USER: (state, data) => {
    state.data_table_path_info_of_current_user = data;
  }
};

const actions = {
  get_openapi_json({ commit }) {
    let openapi_url =
      process.env.VUE_APP_BASE_API.replace("/api/v1", "") + `/openapi.json`;
    return new Promise((resolve, reject) => {
      request
        .get(openapi_url)
        .then(function(response) {
          const { data } = response;
          commit("SET_OPENAPI_JSON", data);
          resolve(data);
        })
        .catch(error => {
          reject(error);
        });
    });
  },
  get_data_table_path_info(
    { state, commit, rootState, dispatch },
    tag_name = "DataTable"
  ) {
    return new Promise(async (resolve, reject) => {
      const data = await dispatch("get_openapi_json");

      // get the permissions of current user
      let perms_response = await get_implicit_permissions_for_user(
        rootState.user.username
      );
      let current_user_perms = perms_response.data.map(i => i[1]);

      const { paths, tags } = data;

      let data_table_path_info = [];

      // extract path info of specified tag to an array
      for (let p in paths) {
        let single_path = paths[p];

        // keep only methods that contains the specificed tag
        for (let m in single_path) {
          let single_method = single_path[m];

          if (!single_method.tags.includes(tag_name)) delete single_path[m];
        }

        // delete path info that doesn'the specificed tag in its method
        if (Object.keys(single_path).length == 0) {
          delete paths[p];
        }

        // check the current user has access to p or not
        let hasAccess = current_user_perms.includes(p);

        // if there are multiple method in a path, flatten it
        for (let m in single_path) {
          // only keeps tags not called specificed tag, because it is redundant;
          single_path[m]["tags"].splice(
            single_path[m]["tags"].indexOf(tag_name),
            1
          );

          // must remove `/api/v1/` from path
          // base url has included it
          data_table_path_info.push({
            ...single_path[m],
            path: p,
            method: m,
            hasAccess: hasAccess
          });
        }
      }

      // data table path info; ready to use as v-data-table `items` prop
      // put all information need to use when display it to user as infoItems
      data_table_path_info.map(function(path) {
        let infoItems = {};

        // don't use this approach anymore
        // gather tag or its description (if has) into topic/subtopic
        // let topics = path.tags.map(function(tag) {
        //   let tag_schema = tags.find(t => t.name == tag);
        //   if (tag_schema) {
        //     return tag_schema.description;
        //   } else {
        //     return tag;
        //   }
        // });
        let topics = path.tags
        let topic = topics.pop();
        let subtopic = topics.pop();

        infoItems = {
          topic: topic,
          subtopic: subtopic,
          summary: path["summary"],
          description: path["description"],
          operationId: path["operationId"]
        };

        path.infoItems = infoItems;
      });

      // add formSchema if parameters exist
      data_table_path_info.map(function(path) {
        if (path.parameters) {
          path.formSchema = [];
          path.parameters.map(function(param) {
            // param.schema.additionalProperties includes name,
            // it will take overwrite name in param.name
            if (param.schema.additionalProperties) {
              let paramSchema = Object.assign(
                {},
                { name: param.name },
                param.schema.additionalProperties
              );
              path.formSchema.push(paramSchema);
            }
          });
        }
      });

      commit("SET_DATA_TABLE_PATH_INFO", data_table_path_info);

      resolve(data_table_path_info);
    });
  },
  get_data_table_path_info_of_current_user({ commit, state, dispatch }) {
    return new Promise(async (resolve, reject) => {
      let data_table_path_info = await dispatch("get_data_table_path_info");
      let data_table_path_info_of_current_user = data_table_path_info.filter(
        item => {
          return item.hasAccess;
        }
      );
      commit(
        "SET_DATA_TABLE_PATH_INFO_OF_CURRENT_USER",
        data_table_path_info_of_current_user
      );
      resolve(data_table_path_info);
    });
  }
};

export default {
  namespaced: true,
  state,
  mutations,
  actions
};
