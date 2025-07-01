from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from bbweb.settings import CATALOG_PATH
from bb import read_catalog
from pathlib import Path
import os


# region exceptions
class CatalogError(Exception): ...


# endregion


# region functions
def get_catalog():
    catalog_file = os.path.join(CATALOG_PATH, ".catalog.cfg")
    if not os.path.exists(catalog_file):
        raise CatalogError(f"catalog doesn't exists: {catalog_file}")
    config = read_catalog(catalog_file)
    return config


# endregion


# region views
@login_required
def home(request):
    config = get_catalog()
    backups = dict()
    for section in config.sections():
        backups[section] = {
            "name": config.get(section, "name", fallback=None),
            "type": config.get(section, "type", fallback=None),
            "os": config.get(section, "os", fallback=None),
            "timestamp": config.get(section, "timestamp", fallback=None),
            "status": config.get(section, "status", fallback="0"),
        }
    template = loader.get_template("home.html")
    context = {
        "backups": backups,
        "catalog": CATALOG_PATH,
    }
    return HttpResponse(template.render(context, request))


@login_required
def details(request, section):
    config = get_catalog()
    backup = {
        "id": section,
        "name": config.get(section, "name", fallback=None),
        "type": config.get(section, "type", fallback=None),
        "os": config.get(section, "os", fallback=None),
        "timestamp": config.get(section, "timestamp", fallback=None),
        "start": config.get(section, "start", fallback=None),
        "end": config.get(section, "end", fallback=None),
        "status": config.get(section, "status", fallback="0"),
        "archived": config.get(section, "archived", fallback=False),
        "cleaned": config.get(section, "cleaned", fallback=False),
        "path": config.get(section, "path", fallback=False),
    }
    template = loader.get_template("details.html")
    context = {
        "backup": backup,
    }
    return HttpResponse(template.render(context, request))


@login_required
def logs(request, section):
    # Get whole catalog entries
    config = get_catalog()
    template = loader.get_template("logs.html")
    context = {}
    extention = ".log"
    for action in ("backup", "restore", "export"):
        # Get path of specific section
        log_file = os.path.join(
            config.get(section, "path", fallback="/"), f"{action}{extention}"
        )
        # Get part of path
        section_path = Path(log_file)
        section_root = section_path.parents[2]
        # Check if catalog root is the same
        if str(section_root) != CATALOG_PATH:
            new_root = Path(CATALOG_PATH)
            log_file = new_root.joinpath(section_path.relative_to(section_root))
            print(section_root)
            print(log_file)
        if os.path.isfile(log_file):
            context[action] = open(log_file).read().replace("\n", "<br>")
    if not context:
        context["no_log"] = "There are no logs."
    return HttpResponse(template.render(context, request))


# endregion
