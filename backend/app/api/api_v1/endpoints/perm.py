from typing import List
from fastapi import APIRouter, Query, Body, Depends, HTTPException
from starlette.responses import Response
from starlette.requests import Request
from starlette.status import HTTP_201_CREATED

from app.core.permission import enforcer

router = APIRouter()


@router.get("/get_all_subjects/", description="GetAllSubjects 获取当前策略中显示的主题列表。")
def get_all_subjects():
    return enforcer.get_all_subjects()


@router.get("/get_all_named_subjects/", description="GetAllNamedSubjects 获取当前命名策略中显示的主题列表。")
def get_all_named_subjects(ptype: str):
    return enforcer.get_all_named_subjects(ptype)


@router.get("/get_all_objects/", description="GetAllObjects 获取当前策略中显示的对象列表。")
def get_all_objects():
    return enforcer.get_all_objects()


@router.get("/get_all_named_objects/", description="GetAllNamedObjects 获取当前命名策略中显示的对象列表。")
def get_all_named_objects():
    return enforcer.get_all_named_objects()


@router.get("/get_all_actions/", description="GetAllActions 获取当前策略中显示的操作列表。")
def get_all_actions():
    return enforcer.get_all_actions()


@router.get("/get_all_named_actions/", description="GetAllNamedActions 获取当前命名策略中显示的操作列表。")
def get_all_named_actions():
    return enforcer.get_all_named_actions()


@router.get("/get_all_roles/", description="GetAllRoles获取当前策略中显示的角色列表。")
def get_all_roles():
    return enforcer.get_all_roles()


@router.get("/get_all_named_roles/", description="GetAllRoles获取当前策略中显示的角色列表。")
def get_all_named_roles():
    return enforcer.get_all_named_roles()


@router.get("/get_policy/", description="GetPolicy 获取策略中的所有授权规则。")
def get_policy():
    return enforcer.get_policy()


@router.get("/get_filtered_policy/", description="GetFilteredPolicy 获取策略中的所有授权规则，可以指定字段筛选器。")
def get_filtered_policy(field_index: int, field_values: List[str] = Query(...)):
    return enforcer.get_filtered_policy(field_index, *field_values)


@router.get("/get_named_policy/", description="GetNamedPolicy 获取命名策略中的所有授权规则。")
def get_named_policy(ptype: str):
    return enforcer.get_named_policy(ptype)


@router.get("/get_filtered_named_policy/", description="GetFilteredNamedPolicy 获取命名策略中的所有授权规则，可以指定字段过滤器。")
def get_filtered_named_policy(ptype: str, field_index: int, field_values: List[str] = Query(...)):
    return enforcer.get_filtered_named_policy(ptype, field_index, *field_values)


@router.get("/get_grouping_policy/", description="GetGroupingPolicy 获取策略中的所有角色继承规则。")
def get_grouping_policy():
    return enforcer.get_grouping_policy()


@router.get("/get_filtered_grouping_policy/", description="GetFilteredGroupingPolicy 获取策略中的所有角色继承规则，可以指定字段筛选器。")
def get_filtered_grouping_policy(field_index: int, field_values: List[str] = Query(...)):
    return enforcer.get_filtered_grouping_policy(field_index, *field_values)


@router.get("/get_named_grouping_policy/", description="GetNamedGroupingPolicy 获取策略中的所有角色继承规则。")
def get_named_grouping_policy(ptype: str):
    return enforcer.get_named_grouping_policy(ptype)


@router.get("/get_filtered_named_grouping_policy/", description="GetFilteredNamedGroupingPolicy 获取策略中的所有角色继承规则。")
def get_filtered_named_grouping_policy(ptype: str, field_index: int, field_values: List[str] = Query(...)):
    return enforcer.get_filtered_named_grouping_policy(ptype, field_index, *field_values)


@router.get("/has_policy/", description="HasPolicy 确定是否存在授权规则。")
def has_policy(params: List[str] = Query(...)):
    return enforcer.has_policy(*params)


@router.get("/has_named_policy/", description="HasNamedPolicy 确定是否存在命名授权规则。")
def has_named_policy(ptype: str, params: List[str] = Query(...)):
    return enforcer.has_named_policy(ptype, *params)


@router.post("/add_policy/", description="AddPolicy 向当前策略添加授权规则。 如果规则已经存在，函数返回false，并且不会添加规则。 否则，函数通过添加新规则并返回true。")
def add_policy(params: List[str] = Query(...)):
    return enforcer.add_policy(*params)


# Beblow is RBAC API. Refer to https://casbin.org/docs/zh-CN/rbac-api

@router.get("/get_roles_for_user/", description="GetRolesForUser 获取用户具有的角色。")
def get_roles_for_user(user: str):
    return enforcer.get_roles_for_user(user)


@router.get("/get_users_for_role/", description="GetUsersForRole 获取具有角色的用户。")
def get_users_for_role(role: str):
    return enforcer.get_users_for_role(role)


@router.get("/has_role_for_user/", description="HasRoleForUser 确定用户是否具有角色。")
def has_role_for_user(user: str, role: str) -> bool:
    return enforcer.has_role_for_user(user, role)


@router.post("/add_role_for_user/", description="AddRoleForUser 为用户添加角色。 如果用户已经拥有该角色（aka不受影响），则返回false。")
def add_role_for_user(user: str, role: str):
    return enforcer.add_role_for_user(user, role)


@router.post("/delete_role_for_user/", description="DeleteRoleForUser 删除用户的角色。 如果用户没有该角色（aka不受影响），则返回false。")
def delete_role_for_user(user: str, role: str):
    return enforcer.delete_role_for_user(user, role)


@router.post("/delete_roles_for_user/", description="DeleteRolesForUser 删除用户的所有角色。 如果用户没有任何角色（aka不受影响），则返回false。")
def delete_roles_for_user(user: str):
    return enforcer.delete_roles_for_user(user)


@router.post("/delete_user/", description="DeleteUser 删除一个用户。 如果用户不存在，则返回false（也就是说不受影响）。")
def delete_user(user: str):
    return enforcer.delete_user(user)


@router.post("/delete_role/", description="DeleteRole 删除一个角色。")
def delete_role(role: str):
    return enforcer.delete_role(role)


@router.post("/delete_permission/", description="DeletePermission 删除权限。 如果权限不存在，则返回false（aka不受影响）。")
def delete_permission(permission: List[str] = Query(...)):
    return enforcer.delete_permission(*permission)


@router.post("/add_permission_for_user/", description="AddPermissionForUser 为用户或角色添加权限。 如果用户或角色已经拥有该权限（aka不受影响），则返回false。")
def add_permission_for_user(user: str, permission: List[str] = Query(...)):
    return enforcer.add_permission_for_user(user, *permission)


@router.post("/delete_permission_for_user/", description="DeletePermissionForUser 删除用户或角色的权限。 如果用户或角色没有权限（aka不受影响），则返回false。")
def delete_permission_for_user(user: str, permission: List[str] = Query(...)):
    return enforcer.delete_permission_for_user(user, *permission)


@router.post("/delete_permissions_for_user/", description="DeletePermissionsForUser 删除用户或角色的权限。 如果用户或角色没有任何权限（aka不受影响），则返回false。")
def delete_permissions_for_user(user: str):
    return enforcer.delete_permissions_for_user(user)


@router.get("/get_permissions_for_user/", description="GetPermissionsForUser 获取用户或角色的权限。")
def get_permissions_for_user(user: str):
    return enforcer.get_permissions_for_user(user)


@router.get("/has_permission_for_user/", description="HasPermissionForUser 确定用户是否具有权限。")
def has_permission_for_user(user: str, permission: List[str] = Query(...)):
    return enforcer.has_permission_for_user(user, *permission)


@router.get("/has_permission_for_user/")
def get_implicit_roles_for_user(user: str, domain=None):
    """
    GetImplicitRolesForUser 获取用户具有的隐式角色。 与GetRolesForUser() 相比，该函数除了直接角色外还检索间接角色。


    For example:

    g, alice, role:admin

    g, role:admin, role:user


    GetRolesForUser("alice") can only get: ["role:admin"].
    But GetImplicitRolesForUser("alice") will get: ["role:admin", "role:user"].
    """
    return enforcer.get_implicit_roles_for_user(user, domain=None)


@router.get("/get_implicit_permissions_for_user/")
def get_implicit_permissions_for_user(user: str, domain=None):
    """
    GetImplicitPermissionsForUser gets implicit permissions for a user or role.

    Compared to GetPermissionsForUser(), this function retrieves permissions for inherited roles.


    For example:

    p, admin, data1, read

    p, alice, data2, read

    g, alice, admin


    GetPermissionsForUser("alice") can only get: [["alice", "data2", "read"]].

    But GetImplicitPermissionsForUser("alice") will get: [["admin", "data1", "read"], ["alice", "data2", "read"]].
    """
    return enforcer.get_implicit_permissions_for_user(user, domain=None)
