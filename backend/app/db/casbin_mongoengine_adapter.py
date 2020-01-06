# adapted from https://github.com/zhangbailong945/mongoengine_adapter
import casbin
from casbin import persist
from mongoengine import Document
from mongoengine import connect, disconnect
from mongoengine.fields import IntField, StringField
from mongoengine.queryset.visitor import Q

db_alias = 'casbin_db'

class CasbinRule(Document):
    '''
    CasbinRule model
    '''

    __tablename__ = "casbin_rule"

    ptype = StringField(required=True, max_length=255)
    v0 = StringField(max_length=255)
    v1 = StringField(max_length=255)
    v2 = StringField(max_length=255)
    v3 = StringField(max_length=255)
    v4 = StringField(max_length=255)
    v5 = StringField(max_length=255)

    meta = {'db_alias': db_alias}

    def __str__(self):
        arr = [self.ptype]
        for v in (self.v0, self.v1, self.v2, self.v3, self.v4, self.v5):
            if v is None:
                break
            arr.append(v)
        return ', '.join(arr)

    def __repr__(self):
        return '<CasbinRule {}: "{}">'.format(self.id, str(self))


class Adapter(persist.Adapter):
    """the interface for Casbin adapters."""

    def __init__(self, db=None, alias = 'casbin_db', **kwargs):
        connect(db, db_alias, **kwargs)

    def load_policy(self, model):
        '''
        implementing add Interface for casbin \n
        load all policy rules from mongodb \n
        '''
        lines = CasbinRule.objects()
        for line in lines:
            persist.load_policy_line(str(line), model)

    def _save_policy_line(self, ptype, rule):
        line = CasbinRule(ptype=ptype)
        for i, v in enumerate(rule):
            setattr(line, 'v{}'.format(i), v)
        line.save()

    def save_policy(self, model):
        '''
        implementing add Interface for casbin \n
        save the policy in mongodb \n
        '''
        for sec in ["p", "g"]:
            if sec not in model.model.keys():
                continue
            for ptype, ast in model.model[sec].items():
                for rule in ast.policy:
                    self._save_policy_line(ptype, rule)
        return True

    def add_policy(self, sec, ptype, rule):
        """add policy rules to mongodb"""
        self._save_policy_line(ptype, rule)

    def remove_policy(self, sec, ptype, rule):
        """delete policy rules from mongodb"""
        condition = dict(zip(['v0', 'v1', 'v2', 'v3', 'v4', 'v5'], rule))
        condition = {'ptype': ptype, **condition}
        query = CasbinRule.objects(__raw__=condition)
        r = query.delete()

        return True if r > 0 else False

    def remove_filtered_policy(self, sec, ptype, field_index, *field_values):
        """
        delete policy rules for matching filters from mongodb
        """
        condition = {'ptype': ptype}
        for i, v in enumerate(field_values):
            condition.update({'v{}'.format(field_index + i):  v})
        query = CasbinRule.objects(__raw__=condition)
        r = query.delete()

        return True if r > 0 else False

    # def __del__(self):
    #     disconnect(db_alias)

