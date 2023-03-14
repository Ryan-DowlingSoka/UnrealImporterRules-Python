from abc import ABC
import unreal
from typing import List, cast
import os.path


class QueryBase(ABC):
    """Base class for import queries."""

    def test(self, factory: unreal.Factory, created_object: unreal.Object) -> bool:
        """Test the created object and factory against this query."""
        raise NotImplemented


class SourcePath(QueryBase):
    """Query an imported factory and file path"""

    def __init__(
        self,
        file_name_starts_with: str = "",
        file_name_ends_with: str = "",
        file_name_contains: str = "",
        full_path_contains: str = "",
        extensions: List[str] = [],
        requires_all: bool = False,
        case_sensitive: bool = False,
    ) -> None:
        self.case_sensitive = case_sensitive

        # if case sensitive we use the substring as is, if not we lowercase it for future comparisons.
        self.file_name_starts_with = (
            file_name_starts_with
            if self.case_sensitive
            else file_name_starts_with.lower()
        )
        self.file_name_ends_with = (
            file_name_ends_with if self.case_sensitive else file_name_ends_with.lower()
        )
        self.file_name_contains = (
            file_name_contains if self.case_sensitive else file_name_contains.lower()
        )
        self.full_path_contains = (
            full_path_contains if self.case_sensitive else full_path_contains.lower()
        )
        self.extensions = [ext.lower() for ext in extensions]
        self.requires_all = requires_all

    def test(self, factory: unreal.Factory, created_object: unreal.Object) -> bool:
        if created_object is None:
            return False

        # if the created_object doesn't implement asset_import_data we early out.
        if not has_editor_property(created_object, "asset_import_data"):
            return False

        asset_import_data = cast(
            unreal.AssetImportData, created_object.get_editor_property("asset_import_data")
        )
        file_path = asset_import_data.get_first_filename()

        # if case sensitive we use the filename raw, if not we lowercase for the future comparisons.
        file_path = file_path if self.case_sensitive else file_path.lower()
        file_name, extension = os.path.splitext(os.path.basename(file_path))

        results = []

        if self.file_name_starts_with:
            results.append(file_name.startswith(self.file_name_starts_with))

        if self.file_name_ends_with:
            results.append(file_name.endswith(self.file_name_ends_with))

        if self.file_name_contains:
            results.append(self.file_name_contains in file_name)

        if self.full_path_contains:
            results.append(self.full_path_contains in file_name)

        if self.extensions:
            results.append(extension in self.extensions)

        if self.requires_all:
            return all(results)

        return any(results)


class DestinationPath(QueryBase):

    """Query based on the path the created object ends up in."""

    def __init__(
        self,
        path_contains: str = "",
        case_sensitive: bool = False,
    ) -> None:
        self.case_sensitive = case_sensitive
        self.destination_path_contains = (
            path_contains if case_sensitive else path_contains.lower()
        )

    def test(self, factory: unreal.Factory, created_object: unreal.Object) -> bool:
        if created_object is None:  # Early out, can't do destination path comparisons.
            return False

        destination_path = (
            created_object.get_path_name()
            if self.case_sensitive
            else created_object.get_path_name().lower()
        )

        if self.destination_path_contains:
            return self.destination_path_contains in destination_path

        return False


def has_editor_property(created_object: unreal.Object, editor_property: str) -> bool:
    try:
        obj = created_object.get_editor_property(editor_property)
        return True
    except:
        return False