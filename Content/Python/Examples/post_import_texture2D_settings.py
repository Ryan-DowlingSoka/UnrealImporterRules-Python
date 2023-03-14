'''
This example file shows a simple set of rules applying to imported assets of the type: "Texture2D"
By importing this module in an init_unreal these rules will get applied to any newly imported assets.
'''

from ImporterRules import *
import unreal

importer_rules_manager.register_rules(
    class_type = unreal.Texture2D,
    rules = [
        # The first rule is simple, it takes any textures ending with _n and applies the flip_green_channel property as false.
        # You might do something like this if you want to switch from DirectX to OpenGL normals.
        # There is only one rule, so the requires_all parameter is irrelevant.
        Rule(
            queries=[
                SourcePath(file_name_ends_with="_n"),
            ],
            actions=[SetEditorProperties(flip_green_channel=False)],
        ),

        # This second rule shows how you can put several queries together. Because the requires_all parameter is 'False'
        # this rule will fire if ANY of the source path queries are true. So if the texture ends with _n, _o, _h, _r, _m
        # then this rule will remove the sRGB property from those textures.
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

        # The third rule is targeting more specifically. While the previous rules have been requires_all = False, this rule is True
        # so now both the SourcePath and DestinationPath queries must come back true for the action to be applied.
        # In this example the texture must have the suffix _d and be in a folder named /TestFolder/ somewhere in its path hierarchy
        # to pass.
        # You can see that the SetEditorProperties takes two property names as well.
        Rule(
            queries=[
                SourcePath(file_name_ends_with="_d"),
                DestinationPath(path_contains="/TestFolder/"),
            ],
            actions=[SetEditorProperties(srgb=False, lod_bias=5)],
            requires_all=True
        ),

        # This rule is similar to the previous, but the SetEditorProperties has been broken up into two actions, just like queries
        # you aren't limited to one action at a time.
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

unreal.log("Registered Texture Post Import Rules!")