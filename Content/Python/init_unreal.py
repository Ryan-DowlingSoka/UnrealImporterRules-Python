from unreal import log_error
from traceback import print_exc

# @NOTE: A good practice is to wrap your individual (and stand alone)
# and modules in following try clause, this allows your other modules
# to still run even if one of the modules has an error.

try:
    import Examples.post_import_texture2D_settings
except Exception as err:
    log_error("Plugin Importer Rules failed to initialize.")
    print_exc()
