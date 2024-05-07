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

import unreal
from typing import Dict, List
from ImporterRules.Rules import ImportRuleBase
from ImporterRules.Actions import SetAssetTags
from ImporterRules.Queries import CheckAssetTag


class ImporterRulesManager(object):
    """Manager class to make it easier to add importer rules registrations."""

    def __init__(self) -> None:
        self.import_subsystem = unreal.get_editor_subsystem(unreal.ImportSubsystem)
        if self.import_subsystem:
            self.import_subsystem.on_asset_post_import.add_callable(
                self.on_asset_post_import
            )
        self._rules: Dict[type, List[ImportRuleBase]] = {}
        self._set_imported_asset_tag_action = SetAssetTags({"importer_rules_applied":"True"})
        self._check_imported_asset_tag_action = CheckAssetTag("importer_rules_applied","True")

    def on_asset_post_import(
        self, factory: unreal.Factory, created_object: unreal.Object
    ):
        # previously had rules run on this asset:
        is_reimport = self._check_imported_asset_tag_action.test(factory, created_object)

        for supported_class in self._rules.keys():
            if isinstance(created_object, supported_class):
                for rule in self._rules[supported_class]:
                    if not is_reimport or rule.apply_on_reimport:
                        rule.apply(factory, created_object)
        self._set_imported_asset_tag_action.apply(factory, created_object)
        

    def register_rule(self, class_type: type, rule: ImportRuleBase):
        if class_type in self._rules:
            self._rules[class_type].append(rule)
        else:
            self._rules[class_type] = [rule]

    def register_rules(self, class_type: type, rules: List[ImportRuleBase]):
        if class_type in self._rules:
            self._rules[class_type] += rules
        else:
            self._rules[class_type] = rules


importer_rules_manager = ImporterRulesManager()
