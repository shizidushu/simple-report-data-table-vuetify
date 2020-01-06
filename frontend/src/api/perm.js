import request from "@/utils/request";
import qs from "qs";

export function get_implicit_permissions_for_user(user) {
  return request.get(`/perm/get_implicit_permissions_for_user`, {
    params: { user: user }
  });
}

export function get_all_roles() {
  return request.get(`/perm/get_all_roles`);
}

export function get_grouping_policy() {
  return request.get(`/perm/get_grouping_policy`);
}

export function get_users_for_role(role) {
  return request.get(`/perm/get_users_for_role`, {
    params: { role: role }
  });
}

export function add_policy(params) {
  return request.post(`/perm/add_policy`, null, {
    params: { params: params },
    paramsSerializer: params => {
      return qs.stringify(params, { indices: false });
    }
  });
}

export function get_all_subjects() {
  return request.get(`/perm/get_all_subjects`);
}

export function add_role_for_user(user, role) {
  return request.post(`/perm/add_role_for_user`, null, {
    params: { user: user, role: role }
  });
}

export function delete_role_for_user(user, role) {
  return request.post(`/perm/delete_role_for_user`, null, {
    params: { user: user, role: role }
  });
}
