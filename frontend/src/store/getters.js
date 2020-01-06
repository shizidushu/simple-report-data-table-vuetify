const getters = {
  token: state => state.user.token,
  username: state => state.user.username,
  truename: state => state.user.truename,
  allUsers: state => state.user.allUsers,
  userRoles: state => state.user.userRoles,
  userRoutes: state => state.user.userRoutes,
  userSidebarRoutes: state => state.user.userSidebarRoutes,
  allRoles: state => state.role.allRoles,
  data_table_path_info: state => state.data_table.data_table_path_info,
  data_table_path_info_of_current_user: state =>
    state.data_table.data_table_path_info_of_current_user,
  ActivateLightTheme: state => state.app.ActivateLightTheme,
  showAlert: state => state.app.showAlert,
  alertInfo: state => state.app.alertInfo
};
export default getters;
