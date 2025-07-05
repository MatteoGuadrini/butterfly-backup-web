from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from bbweb.settings import CATALOG_PATH
from bbweb.forms import BackupForm
from bb import read_catalog
from pathlib import Path
import subprocess
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
    backups = dict()
    template = loader.get_template("home.html")
    context = {
        "backups": backups,
        "catalog": CATALOG_PATH,
    }
    try:
        config = get_catalog()
    except CatalogError as err:
        messages.error(request, err)
        return HttpResponse(template.render(context, request))
    for section in config.sections():
        backups[section] = {
            "name": config.get(section, "name", fallback=None),
            "type": config.get(section, "type", fallback=None),
            "os": config.get(section, "os", fallback=None),
            "timestamp": config.get(section, "timestamp", fallback=None),
            "status": config.get(section, "status", fallback="0"),
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
    extension = ".log"
    for action in ("backup", "restore", "export"):
        # Get path of specific section
        log_file = os.path.join(
            config.get(section, "path", fallback="/"), f"{action}{extension}"
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


@login_required
def backup(request):
    if request.method == "POST":
        form = BackupForm(request.POST)
        if form.is_valid():
            data = {
                # Process the form data
                "computer": form.cleaned_data["computer"],
                "user": form.cleaned_data["user"],
                "port": form.cleaned_data["port"],
                "mode": form.data["mode"],
                "data": form.cleaned_data["data"],
                "type_": form.cleaned_data["type_"],
                "retention_days": form.cleaned_data["retention_days"],
                "retention_number": form.cleaned_data["retention_number"],
                "compress": form.cleaned_data["compress"],
                "skip_error": form.cleaned_data["skip_error"],
                "checksum": form.cleaned_data["checksum"],
                "acl": form.cleaned_data["acl"],
                "retry": form.cleaned_data["retry"],
                "wait": form.cleaned_data["wait"],
            }
            # Compose mandatory command
            cmds = [
                "bb",
                "backup",
                "--destination",
                CATALOG_PATH,
                "--computer",
                data.get("computer"),
                "--user",
                data.get("user"),
                "--mode",
                data.get("mode"),
                "--data",
                data.get("data"),
                "--type",
                data.get("type_"),
            ]
            # Add optional commands
            if data.get("port"):
                cmds.append("--ssh-port")
                cmds.append(data.get("port"))
            if data.get("retention_days"):
                cmds.append("--retention")
                cmds.append(data.get("retention_days"))
                if data.get("retention_number"):
                    cmds.append(data.get("retention_number"))
            if data.get("compress"):
                cmds.append("--compress")
            if data.get("skip_error"):
                cmds.append("--skip-error")
            if data.get("checksum"):
                cmds.append("--checksum")
            if data.get("acl"):
                cmds.append("--acl")
            if data.get("retry"):
                cmds.append("--retry")
                cmds.append(data.get("retry"))
                if data.get("wait"):
                    cmds.append("--wait")
                    cmds.append(data.get("wait"))
            # Start subprocess
            subprocess.run(
                cmds, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=3
            )
            messages.success(request, "Backup started. See catalog.")
    else:
        form = BackupForm()
    return render(request, "backup.html", {"form": form})


# endregion
