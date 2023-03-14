from abc import ABC
import unreal
from traceback import format_exc
from typing import Dict, Any


class ImportActionBase(ABC):
    """Base import action class stub."""

    def apply(self, factory: unreal.Factory, created_object: unreal.Object) -> bool:
        raise NotImplemented


class SetEditorProperties(ImportActionBase):
    """Generic import action to set editor properties with the set_editor_properties(dict) function."""

    def __init__(self, **kwargs) -> None:
        self.editor_properties = kwargs
    
    def apply(self, factory: unreal.Factory, created_object: unreal.Object) -> bool:
        if created_object is None:
            return False
        created_object.set_editor_properties(self.editor_properties)
        unreal.log( f"Applied the following editor properties to {created_object.get_full_name()}")
        unreal.log( self.editor_properties )
        return True
    

class SetAssetTags(ImportActionBase):
    """Generic import action to set asset tag data on the asset on import."""

    def __init__(self, asset_tags:Dict[str,Any]) -> None:
        self.asset_tags = asset_tags
    
    def apply(self, factory: unreal.Factory, created_object: unreal.Object) -> bool:
        if created_object is None:
            return False
        
        eas = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
        if eas:
            for key,value in self.asset_tags.items():
                eas.set_metadata_tag(created_object, key, str(value))

        return True
