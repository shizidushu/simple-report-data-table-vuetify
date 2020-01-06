from app.mongodb_models.user import User as DBUser
from typing import Optional, List
from app.fields.user import Permission
from app.fields.role import Role
from app.core.permission import enforcer
from app import crud


def get_all_roles() -> List[Role]:
    db_users = DBUser.objects()
    db_users_name = [db_user.Username for db_user in db_users]
    casbin_subjects = enforcer.get_all_subjects()
    casbin_grouping_policy = enforcer.get_grouping_policy()
    role_in_grouping_policy = [p[1] for p in casbin_grouping_policy]
    roles = list(set(casbin_subjects + role_in_grouping_policy) - set(db_users_name))
    all_roles = []
    for role in roles:
        # get user info of users belong to the role
        username_of_users_for_role = enforcer.get_users_for_role(role)
        users = [crud.user.get_user_base(username)
                 for username in username_of_users_for_role]

        # get permissions of the role
        role_policies = enforcer.get_filtered_policy(0, role)
        permissions = [dict(zip(['sub', 'obj', 'act'], perm))
                       for perm in role_policies]
        permissions = [Permission(**perm) for perm in permissions]

        # put those together
        all_roles.append(Role(name=role, users=users, permissions=permissions))
    return all_roles
