# Asset Importer Rules - Python Edition

This repo is an example of how you can use python to do rules based modifications to assets post import.

## How to use

First, add a new python module in a plugin or project `/Python/`. The name doesn't matter, you can use the `Content/Python/Examples/post_import_texture2D_settings.py` as an example file.

in this file you'll need to `import unreal` and `from ImporterRules import *` which will give you access to the example framework.

You'll then add your first set of rules to the system.

The format of the rules is as follows:

```python
importer_rules_manager.register_rules(
    unreal.{{ClassName}},
    [
        Rule(
            queries=[
                {{QueryType}}({{QueryArgs}}),
                ...
            ],
            actions=[
                {{ActionType}}({{ActionArgs}}),
                ...
            ],
            requires_all={{True|False}}
        ),
        ...
    ]
)
```

Then in an `init_unreal.py` a /python/ folder import the module and the rules will get registered.

> If you wish to try out the example file, you can uncomment the include in the plugin's init_unreal.py

### Example File

This example file shows a simple set of rules applying to imported assets of the type: "Texture2D"
By importing this module in an init_unreal these rules will get applied to any newly imported assets.

First we need to import the importer rules related classes and unreal for the class type.

```python
from ImporterRules import *
import unreal
```

The importer_rules_manager handles the post_import delegate. So we register_rules through that. The first argument is the type of classes that these rules should be applied to.

```python
importer_rules_manager.register_rules(
    class_type = unreal.Texture2D,
```

Next we have an array of rules.

The first rule is simple, it takes any textures ending with _n and applies the flip_green_channel property as false.
You might do something like this if you want to switch from DirectX to OpenGL normals.
There is only one rule, so the requires_all parameter is irrelevant.

```python
    rules = [
        Rule(
            queries=[
                SourcePath(file_name_ends_with="_n"),
            ],
            actions=[SetEditorProperties(flip_green_channel=False)],
        ),
```

This second rule shows how you can put several queries together. Because the requires_all parameter is 'False' this rule will fire if ANY of the source path queries are true. So if the texture ends with `_n, _o, _h, _r, _m` then this rule will remove the sRGB property from those textures.

```python
        Rule(
            queries=[
                SourcePath(file_name_ends_with="_n"),
                SourcePath(file_name_ends_with="_o"),
                SourcePath(file_name_ends_with="_h"),
                SourcePath(file_name_ends_with="_r"),
                SourcePath(file_name_ends_with="_m"),
            ],
            actions=[SetEditorProperties(srgb=False)],
            requires_all=False
        ),
```

The third rule is targeting more specifically. While the previous rules have been requires_all = False, this rule is True so now both the SourcePath and DestinationPath queries must come back true for the action to be applied. In this example the texture must have the suffix `_d` and be in a folder named /TestFolder/ somewhere in its path hierarchy to pass. You can see that the SetEditorProperties takes two property names as well.

```python
        Rule(
            queries=[
                SourcePath(file_name_ends_with="_d"),
                DestinationPath(path_contains="/TestFolder/"),
            ],
            actions=[SetEditorProperties(srgb=False, lod_bias=5)],
            requires_all=True
        ),
```

This rule is similar to the previous, but the SetEditorProperties has been broken up into two actions, just like queries you aren't limited to one action at a time.

```python
        Rule(
            queries=[
                SourcePath(file_name_ends_with="_test"),
                DestinationPath(path_contains="/TestFolder/"),
            ],
            actions=[SetEditorProperties(srgb=False), SetAssetTags({"obsolete":True})],
            requires_all=True
        ),
    ],
)
```

## Framework breakdown

`Rules` are made out of `Queries` and `Actions`

### Queries

A query is a test that can be run on the recently imported `Factory` or `Created Object` to determine if the subsequent actions should run.

For example the `Queries.SourcePath` class is a query that lets you do a series of string tests against the source path of the asset.

To create a query type of your own, you simply need to inherit from the `Queries.QueryBase` and implement the `def test(self, factory: unreal.Factory, created_object: unreal.Object) -> bool` function.

Use the `__init__` function of your new class to allow the user to create user parameters.

Most queries, if they contain multiple different types of tests, should also implement a `self.requires_all` boolean class member this signifies whether or not all the tests in the query must be past or if only one must pass.

For example in the `Queries.SourcePath` there are several tests:

```python
file_name_starts_with: str = "",
file_name_ends_with: str = "",
file_name_contains: str = "",
full_path_contains: str = "",
extensions: List[str] = [],
requires_all: bool = False,
case_sensitive: bool = False,
```

The first 4 parameters are tests on the file name or path. The fifth is a list of valid extensions. The final two are modifiers on the tests. `case_sensitive` is used to have all string comparisons be done in `lower()` case. `requires_all` is the modifier mentioned above, if true `all` of the tests above must pass, if false `any` of the tests must pass. 

These queries are then instantiated in the `queries` parameter of a `Rule`

Other types of queries you could choose to complete might be tests on specific data in the asset. For example, `.fbx` files can have `MetadataTags` that can get created by software like Maya and saved into the files. You can use the `CheckAssetTag` query looking for particular metadata tags that are created at import time, and do specific actions based on whether or not that tag exists.

Complex boolean groupings like `query1 and query2 but not query3` aren't supported by the framework, buy could be done so easily by creating a `AND` or `OR` set of composite queries that could *wrap* other queries.

### Actions

Once an imported asset passes any associated queries then `Actions` are run on it. Actions are any arbitrary amount of work that you want to run on the Created Object (or anything else) when a query passes.

For example the `Actions.SetEditorProperties` can apply any amount of EditorProperties through the `.set_editor_properties(dict)` python function. It uses **kwargs so follows the pattern:

`SetEditorProperties(srgb=False, lod_bias=2)`

To create your own actions you simply need to inherit from `ImportActionBase` and implement the `def apply(self, factory: unreal.Factory, created_object: unreal.Object) -> bool:` function. This function should return `True` if successful, but note that the entire `apply` action is wrapped in a `try: except:` block.

As before you should use the `__init__` definition to create member variables for action configuration in most cases.

#### Actions.SetEditorProperties(**kwargs)

This is the most generic included action. Pass in any editor properties as parameter values. For example, for a texture you might pass in:

```SetEditorProperties(srgb=True)```

The naming of the editor properties that are available for a given class can by found in the stub definition of the unreal class. For example:

```text
Texture 2D

**C++ Source:**

- **Module**: Engine
- **File**: Texture2D.h

**Editor Properties:** (see get_editor_property/set_editor_property)

- ``address_x`` (TextureAddress):  [Read-Write] Address X:
    The addressing mode to use for the X axis.
- ``address_y`` (TextureAddress):  [Read-Write] Address Y:
    The addressing mode to use for the Y axis.
- ``adjust_brightness`` (float):  [Read-Write] Adjust Brightness:
    Static texture brightness adjustment (scales HSV value.)  (Non-destructive; Requires texture source art to be available.)
```

This action will fail if the target does not have the given property name or if the value is the wrong type.

#### Actions.SetAssetTags({TagKey:TagValue})

This action is for setting asset tags on import. It takes a dictionary of `str:Any` but be aware it runs `str()` on the value, so only types that can be cast to `str()` will be valid.

### Rules

Rules are simple enough, they are just a set of `Queries` and a set of `Actions`. If any/all `Queries` pass then *all* `Actions` are run. If `requires_all` is True, then *all* `Queries` must pass, if False, then a *single* `Query` is enough to cause the actions to run.

Rules are registered through the `Manager.importer_rules_manager` using `register_rule`.

Internally the `importer_rules_manager` wraps adding `on_asset_post_import` a delegate in `unreal.ImportSubsystem`

```python
self.import_subsystem = unreal.get_editor_subsystem(unreal.ImportSubsystem)
if self.import_subsystem:
    self.import_subsystem.on_asset_post_import.add_callable(
        self.on_asset_post_import
    )
```

If you'd like to build your own system you could either bind your rules directly to this delegate. There are some other useful delegates in the `ImportSubsystem` so take a look at these other delegates if you are interested in learning more.

## Notes

* There is a native C++ and Blueprints version of this pattern available at [https://github.com/Ryan-DowlingSoka/UnrealImporterRules-CPP](https://github.com/Ryan-DowlingSoka/UnrealImporterRules-CPP)

* The Unreal Python Path is set at each `/Python/` folder in each plugin and the project. As such, modules inside of modules such as `/Python/ImporterRules/.../` folders need to reference their siblings with `import ImporterRules.{{ModuleName}}`

* The `ImporterRules` imports all the queries and action classes, so you can use `from ImporterRules import *` as a handy shorthand to get the classes you need. If you make additional queries or actions, you should either put them in this file or just remember to import them manually.

* (Re)importing. All of the delegates related to importing in Unreal happen for reimporting too. You most likely don't want your rules to apply to assets that have already had the rules applied to them, so we need to detect if the current import is a reimport. There are two possible patterns for this: The first is to bind to pre-import, calculate what objects will be generated and if those packages already exist. This is a bummer because factories can do some pretty intense logic to determine what the names of the newly imported objects will be. The second (what this example project does) is to assign a MetadataTag to the asset if it has had rules applied to it already, and then rules can opt in to running despite if that tag exists. This second way is easier to implement, *but* does mean that reimporting existing assets from before when the plugin was created will have those rules applied. This might be beneficial in some cases, but do be careful. If you wanted to prevent that, you could run the `import_rules_manager._set_imported_asset_tag_action.apply()` function on all the assets in your content library as part of the installation process.

* This tutorial was made for `#notGDC 2023`! Check out some other great entries at [https://notgdc.io](https://notgdc.io)
