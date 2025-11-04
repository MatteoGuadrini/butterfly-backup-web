from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from pathlib import Path
import subprocess
import os
from .settings import CATALOG_PATH
from .forms import (
    BackupForm,
    RestoreForm,
    ExportForm,
    ArchiveForm,
    CatalogError,
    get_catalog,
)


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
    general_log = os.path.join(
        Path(config.get(section, "path", fallback="/")).parent, "general" + extension
    )
    if os.path.isfile(general_log):
        context["general"] = open(general_log).read().replace("\n", "<br>")
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
                str(CATALOG_PATH),
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
                "--log",
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
            try:
                subprocess.run(
                    cmds,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                messages.success(request, "Backup started. See catalog.")
            except subprocess.CalledProcessError as err:
                messages.error(request, f"Backup error: {err}.")
            except FileNotFoundError:
                messages.error(request, "Butterfly Backup doesn't installed")
    else:
        form = BackupForm()
    return render(request, "backup.html", {"form": form})


@login_required
def restore(request):
    if request.method == "POST":
        form = RestoreForm(request.POST)
        if form.is_valid():
            data = {
                # Process the form data
                "computer": form.cleaned_data["computer"],
                "user": form.cleaned_data["user"],
                "port": form.cleaned_data["port"],
                "backup_id": form.cleaned_data["backup_id"],
                "root_dir": form.cleaned_data["root_dir"],
                "type_": form.cleaned_data["type_"],
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
                "restore",
                "--destination",
                str(CATALOG_PATH),
                "--computer",
                data.get("computer"),
                "--user",
                data.get("user"),
                "--backup-id",
                data.get("backup_id"),
                "--type",
                data.get("type_"),
                "--log",
            ]
            # Add optional commands
            if data.get("port"):
                cmds.append("--ssh-port")
                cmds.append(data.get("port"))
            if data.get("mirror"):
                cmds.append("--mirror")
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
            try:
                subprocess.run(
                    cmds,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                messages.success(
                    request,
                    f"Restore started. See logs of backup-id:{data.get('backup_id')}.",
                )
            except subprocess.CalledProcessError as err:
                messages.error(request, f"Restore error: {err}.")
            except FileNotFoundError:
                messages.error(request, "Butterfly Backup doesn't installed")
    else:
        form = RestoreForm()
    return render(request, "restore.html", {"form": form})


@login_required
def export(request):
    if request.method == "POST":
        form = ExportForm(request.POST)
        if form.is_valid():
            data = {
                # Process the form data
                "backup_id": form.cleaned_data["backup_id"],
                "export_path": form.cleaned_data["export_path"],
                "cut": form.cleaned_data["cut"],
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
                "export",
                "--destination",
                str(CATALOG_PATH),
                "--backup-id",
                data.get("backup_id"),
                "--destination",
                data.get("export_path"),
                "--log",
            ]
            # Add optional commands
            if data.get("mirror"):
                cmds.append("--mirror")
            if data.get("compress"):
                cmds.append("--compress")
            if data.get("skip_error"):
                cmds.append("--skip-error")
            if data.get("checksum"):
                cmds.append("--checksum")
            if data.get("acl"):
                cmds.append("--acl")
            if data.get("cut"):
                cmds.append("--cut")
            if data.get("retry"):
                cmds.append("--retry")
                cmds.append(data.get("retry"))
                if data.get("wait"):
                    cmds.append("--wait")
                    cmds.append(data.get("wait"))
            # Start subprocess
            try:
                subprocess.run(
                    cmds,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                messages.success(
                    request,
                    f"Export started. See logs of backup-id:{data.get('backup_id')}.",
                )
            except subprocess.CalledProcessError as err:
                messages.error(request, f"Export error: {err}.")
            except FileNotFoundError:
                messages.error(request, "Butterfly Backup doesn't installed")
    else:
        form = ExportForm()
    return render(request, "export.html", {"form": form})


@login_required
def archive(request):
    if request.method == "POST":
        form = ArchiveForm(request.POST)
        if form.is_valid():
            data = {
                # Process the form data
                "backup_id": form.cleaned_data["backup_id"],
                "archive_path": form.cleaned_data["archive_path"],
                "days": form.cleaned_data["days"],
            }
            # Compose mandatory command
            cmds = [
                "bb",
                "archive",
                "--destination",
                str(CATALOG_PATH),
                "--backup-id",
                data.get("backup_id"),
                "--destination",
                data.get("archive_path"),
                "--log",
            ]
            # Start subprocess
            try:
                subprocess.run(
                    cmds,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                messages.success(
                    request,
                    "Archive started.",
                )
            except subprocess.CalledProcessError as err:
                messages.error(request, f"Archive error: {err}.")
            except FileNotFoundError:
                messages.error(request, "Butterfly Backup doesn't installed")
    else:
        form = ArchiveForm()
    return render(request, "archive.html", {"form": form})


# endregion
