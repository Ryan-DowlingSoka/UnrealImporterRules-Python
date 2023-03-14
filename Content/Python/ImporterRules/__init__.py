"""
Importer Rules is a simple, bare bones, python frame work for handling data transformations on imported assets on import. 
A user can define a "Rule" by ascribing "Queries" that the incoming asset must match before subsequent "Actions" are applied.
You can write your own rules, queries, and actions or use the existing generic ones to modify assets that need updating.
"""

from ImporterRules.Manager import importer_rules_manager
from ImporterRules.Actions import SetEditorProperties, SetAssetTags
from ImporterRules.Queries import SourcePath, DestinationPath
from ImporterRules.Rules import Rule