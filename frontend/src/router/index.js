import Vue from "vue";
import NProgress from "nprogress";
import "nprogress/nprogress.css";

import VueRouter from "vue-router";
import Layout from "@/components/Layout";
import store from "@/store";

// add_role_for_user, get_users_for_role,
import { add_policy } from "@/api/perm";

// import request from "@/utils/request";
// import qs from "qs";

Vue.use(VueRouter);

const constantRoutes = [
  {
    path: "/login",
    component: () => import("@/views/Login"),
    name: "login",
  },
  {
    path: "/signup",
    component: () => import("@/views/Signup"),
    name: "signup"
  },
  {
    path: "/",
    component: Layout,
    name: "home",
    redirect: { name: "dashborad" },
    beforeEnter: (to, from, next) => {
      store.dispatch("data_table/get_data_table_path_info_of_current_user");
      next();
    },
    meta: {
      inSidebar: true
    },
    children: [
      {
        path: "/dashboard",
        name: "dashborad",
        component: () => import("@/views/Dashboard"),
        meta: {
          icon: "dashboard"
        }
      },
      {
        path: "/table_list",
        name: "tableList",
        component: () => import("@/views/TableList"),
        meta: {
          icon: "view_list"
        }
      },
      {
        path: "/datatable/:operationId",
        name: "dataTable",
        props: true,
        component: () => import("@/views/DataTable"),
        meta: {
          hidden: true
        }
      },
      // can have nested sidebar
      {
        path: "/admin",
        name: "admin",
        redirect: "/user_list",
        component: () => import("@/components/Nested"),
        meta: {
          icon: "featured_play_list",
          hidden: false,
          roles: ["role_root"]
        },
        children: [
          {
            path: "/user_list",
            name: "userList",
            component: () => import("@/views/UserList"),
            meta: {
              icon: "featured_play_list",
              hidden: false,
              roles: ["role_root"]
            }
          },
          {
            path: "/role_list",
            name: "roleList",
            component: () => import("@/views/RoleList"),
            meta: {
              icon: "featured_play_list",
              hidden: false,
              roles: ["role_root"]
            }
          }
        ]
      }
    ]
  },
  {
    path: "/nopermission",
    name: "noPermission",
    component: () => import("@/components/NoPermission")
  },
  {
    path: "*",
    name: "notFound",
    component: () => import("@/components/NotFound")
  }
];

const router = new VueRouter({
  mode: "history", // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
});

// let routeNames = [];
// function getRouteNames(routes) {
//   routes.forEach(function(route) {
//     routeNames.push(route.name);
//     if (route.children) {
//       getRouteNames(route.children);
//     }
//   });
// }

function extractRoutewithRoles(routes) {
  return routes
    .reduce((prev, curr) => {
      if (curr.meta && curr.meta.roles) {
        prev.push({ name: curr.name, roles: curr.meta.roles });
      }
      if (curr.children) {
        prev.push(extractRoutewithRoles(curr.children));
      }
      return prev;
    }, [])
    .reduce((a, b) => a.concat(b), []);
}

function extractNames(routes) {
  return [
    ...new Set(
      routes
        .reduce((prev, curr) => {
          prev.push(curr.name);
          if (curr.children) {
            prev.push(extractNames(curr.children));
          }
          return prev;
        }, [])
        .reduce((a, b) => a.concat(b), [])
    )
  ];
}

router.beforeEach((to, from, next) => {
  NProgress.start();
  const token = localStorage.getItem("token");

  if (to.path === "/login") {
    next();
  } else if (token) {
    let userRouteNames = extractNames(store.state.user.userRoutes);

    let routeNameWRoles = extractRoutewithRoles(
      router.app.$router.options.routes
    );
    routeNameWRoles.forEach(route => {
      route.roles.forEach(role => {
        add_policy([role, "view_" + route.name, "view"]);
      });
    });

    if (userRouteNames.includes(to.name)) {
      
      // refresh data to update TableList view
      store.dispatch("data_table/get_data_table_path_info_of_current_user");
      // get users again to update the view
      store.dispatch("user/getAllUsers");
      store.dispatch("user/getUserRoles");
      store.dispatch("user/getRoutesForUser", {
        routes: router.app.$router.options.routes
      });
      store.dispatch("user/getSidebarRoutesForUser", {
        routes: router.app.$router.options.routes
      });
      next();
    } else {
      // next();
      next({ name: "NoPermission" });
    }
  } else {
    next("/login");
  }
});

router.afterEach(() => {
  NProgress.done();
});

// do not do this; edit roles through ui is enough
// let allRolesInRoutesMeta = extractRoles(constantRoutes);

// // add all roles in route meta to users belong to role_root
// get_users_for_role("role_root").then(response => {
//   let allRoleRootUsers = response.data;
//   allRolesInRoutesMeta.map(role =>
//     allRoleRootUsers.map(user => {
//       add_role_for_user(user, role);
//     })
//   );
// });

export default router;
