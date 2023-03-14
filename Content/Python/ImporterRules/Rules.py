from abc import ABC
from ImporterRules.Actions import ImportActionBase
from ImporterRules.Queries import QueryBase
import unreal
from typing import List
from traceback import format_exc

class ImportRuleBase(ABC):
    """Base class for rules, to be applied """

    def apply(self, factory: unreal.Factory, created_object: unreal.Object) -> bool:
        raise NotImplemented
    
class Rule(ImportRuleBase):
    """Import Rule class to apply actions if designated queries are true."""

    def __init__(self, queries:List[QueryBase], actions:List[ImportActionBase], requires_all:bool=False) -> None:
        self.queries = queries
        self.actions = actions
        self.requires_all = requires_all

    def apply(self, factory: unreal.Factory, created_object: unreal.Object) -> bool:
        results = [query.test(factory, created_object) for query in self.queries]

        if self.requires_all:
            if not all(results):
                return False
        else:
            if not any(results):
                return False

        try:
            action_results = [action.apply(factory, created_object) for action in self.actions]
        except Exception as err:
            unreal.log_error(f"Failed to run actions on {created_object.get_name()}")
            error_message = format_exc()
            unreal.log_error(error_message)
            unreal.EditorDialog.show_message(title="Import Action Error", message=f"{error_message}", message_type=unreal.AppMsgType.OK, default_value=unreal.AppReturnType.OK)
            return False
        return all(action_results)