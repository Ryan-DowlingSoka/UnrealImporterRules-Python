# MIT License

# Copyright (c) 2023 Ryan DowlingSoka

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from abc import ABC
from ImporterRules.Actions import ImportActionBase
from ImporterRules.Queries import QueryBase
import unreal
from typing import List
from traceback import format_exc

class ImportRuleBase(ABC):
    """Base class for rules, to be applied """

    def __init__(self, apply_on_reimport:bool=False) -> None:
        self.apply_on_reimport = apply_on_reimport

    def apply(self, factory: unreal.Factory, created_object: unreal.Object) -> bool:
        raise NotImplemented
    
class Rule(ImportRuleBase):
    """Import Rule class to apply actions if designated queries are true."""

    def __init__(self, queries:List[QueryBase], actions:List[ImportActionBase], requires_all:bool=False, apply_on_reimport:bool=False) -> None:
        super().__init__(apply_on_reimport)
        self.queries = queries
        self.actions = actions
        self.requires_all = requires_all

    def apply(self, factory: unreal.Factory, created_object: unreal.Object) -> bool:
        results = [query.test(factory, created_object) for query in self.queries]

        if len(results) > 0:
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