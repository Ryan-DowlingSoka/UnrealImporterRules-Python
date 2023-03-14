import unreal
from typing import Dict, List
from ImporterRules.Rules import ImportRuleBase


class ImporterRulesManager(object):
    """Manager class to make it easier to add importer rules registrations."""

    def __init__(self) -> None:
        self.import_subsystem = unreal.get_editor_subsystem(unreal.ImportSubsystem)
        if self.import_subsystem:
            self.import_subsystem.on_asset_post_import.add_callable(
                self.on_asset_post_import
            )
        self.rules: Dict[type, List[ImportRuleBase]] = {}

    def on_asset_post_import(self, factory: unreal.Factory, created_object: unreal.Object):
        unreal.log(created_object)
        for supported_class in self.rules.keys():
            unreal.log(supported_class)
            if isinstance(created_object, supported_class):
                unreal.log("true")
                for rule in self.rules[supported_class]:
                    unreal.log(rule)
                    rule.apply(factory, created_object)

    def register_rule(self, class_type: type, rule: ImportRuleBase):
        if class_type in self.rules:
            self.rules[class_type].append(rule)
        else:
            self.rules[class_type] = [rule]

    def register_rules(self, class_type: type, rules: List[ImportRuleBase]):
        if class_type in self.rules:
            self.rules[class_type] += rules
        else:
            self.rules[class_type] = rules


importer_rules_manager = ImporterRulesManager()
