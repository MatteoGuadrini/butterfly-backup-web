from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from bbweb.settings import CATALOG_PATH
from bb import read_catalog
import os


# region exceptions
class CatalogError(Exception): ...


# endregion


@login_required
def home(request):
    catalog_file = os.path.join(CATALOG_PATH, ".catalog.cfg")
    if not os.path.exists(catalog_file):
        raise CatalogError(f"catalog doesn't exists: {catalog_file}")
    backups = dict()
    config = read_catalog(catalog_file)
    for section in config.sections():
        backups[section] = {
            "name": config.get(section, "name", fallback=None),
            "type": config.get(section, "type", fallback=None),
            "os": config.get(section, "os", fallback=None),
            "timestamp": config.get(section, "timestamp", fallback=None),
            "start": config.get(section, "start", fallback=None),
            "end": config.get(section, "end", fallback=None),
            "status": config.get(section, "status", fallback="0"),
        }
    template = loader.get_template("home.html")
    context = {
        "backups": backups,
        "catalog": catalog_file,
    }
    return HttpResponse(template.render(context, request))
