from glob import glob
import os
import pkg_resources

from tutor import hooks

from .__about__ import __version__


################# Configuration
config = {
    "defaults": {
        "VERSION": __version__,
        "VEM_S3_BUCKET": "openedxvideos",
        "ROOT_PATH": "upload"
    },
    "unique": {},
    "overrides": {}
}

################# Initialization tasks
hooks.Filters.COMMANDS_INIT.add_item((
    "lms",
    ("videoupload", "tasks", "lms", "init")
))

################# Boilerplate code
# Plugin templates
hooks.Filters.ENV_TEMPLATE_ROOTS.add_item(
    pkg_resources.resource_filename("tutorvideoupload", "templates")
)
hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    [
        ("videoupload/build", "plugins"),
        ("videoupload/apps", "plugins"),
    ],
)
# Load all patches from the "patches" folder
for path in glob(
    os.path.join(
        pkg_resources.resource_filename("tutorvideoupload", "patches"),
        "*",
    )
):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))

# Load all configuration entries
hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        (f"VIDEOUPLOAD_{key}", value)
        for key, value in config["defaults"].items()
    ]
)
hooks.Filters.CONFIG_UNIQUE.add_items(
    [
        (f"VIDEOUPLOAD_{key}", value)
        for key, value in config["unique"].items()
    ]
)
hooks.Filters.CONFIG_OVERRIDES.add_items(list(config["overrides"].items()))
