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
