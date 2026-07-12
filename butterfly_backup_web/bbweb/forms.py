import os
import json
from datetime import datetime
from django import forms
from bb import read_catalog
from .settings import CATALOG_PATH


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


def catalog_error_message():
    catalog_file = os.path.join(CATALOG_PATH, ".catalog.cfg")
    timestamp = datetime.now().strftime("%d/%b/%Y %H:%M:%S")
    print(f'[{timestamp}] "Catalog file not found: {catalog_file}"')


# endregion


class BackupForm(forms.Form):
    computer = forms.CharField(label="Computer name or ip", max_length=100)
    user = forms.CharField(label="Username", max_length=100, initial="root")
    port = forms.IntegerField(label="SSH port number", required=False)
    mode = forms.ChoiceField(
        choices=(
            ("full", "full"),
            ("incremental", "incremental"),
            ("differential", "differential"),
            ("mirror", "mirror"),
        ),
        label="Mode",
        required=True,
        initial="incremental",
    )
    data = forms.ChoiceField(
        choices=(
            ("user", "user"),
            ("config", "config"),
            ("application", "application"),
            ("system", "system"),
            ("log", "log"),
        ),
        label="Data",
        required=True,
    )
    type_ = forms.ChoiceField(
        choices=(
            ("unix", "unix"),
            ("macos", "macos"),
            ("windows", "windows"),
        ),
        label="OS type",
        required=True,
    )
    retention_days = forms.IntegerField(label="Retention days", required=False)
    retention_number = forms.IntegerField(
        label="Retention minimum number", required=False
    )
    compress = forms.BooleanField(label="Compress", required=False)
    skip_error = forms.BooleanField(label="Skip error", required=False)
    checksum = forms.BooleanField(label="Checksum", required=False)
    acl = forms.BooleanField(label="Preserve ACL", required=False)
    retry = forms.IntegerField(label="Retry number", required=False)
    wait = forms.IntegerField(label="Seconds of retry wait", required=False)


class RestoreForm(forms.Form):
    computer = forms.CharField(label="Computer name or ip", max_length=100)
    backup_id = forms.ChoiceField(choices=[], label="Backup id", required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            config = get_catalog()
            _catalog = tuple(
                reversed(
                    [
                        (
                            bckid,
                            bckid,
                            config.get(bckid, "name", fallback=""),
                            config.get(bckid, "status", fallback=""),
                            config.get(bckid, "timestamp", fallback=""),
                            config.get(bckid, "type", fallback=""),
                            config.get(bckid, "os", fallback=""),
                        )
                        for bckid in config
                        if bckid.lower() != "default"
                    ]
                )
            )
            self.fields["backup_id"].choices = [(item[0], item[0]) for item in _catalog]
            self.fields["backup_id"].widget.attrs.update(
                {"data-backup-info": json.dumps(_catalog)}
            )
            if _catalog:
                self.fields["backup_id"].initial = _catalog[0][0]
        except CatalogError:
            catalog_error_message()

    root_dir = forms.CharField(label="Root directory", max_length=100, required=False)
    user = forms.CharField(label="Username", max_length=100, initial="root")
    port = forms.IntegerField(label="SSH port number", required=False)
    type_ = forms.ChoiceField(
        choices=(
            ("unix", "unix"),
            ("macos", "macos"),
            ("windows", "windows"),
        ),
        label="OS type",
        required=True,
    )
    compress = forms.BooleanField(label="Compress", required=False)
    skip_error = forms.BooleanField(label="Skip error", required=False)
    checksum = forms.BooleanField(label="Checksum", required=False)
    acl = forms.BooleanField(label="Preserve ACL", required=False)
    mirror = forms.BooleanField(label="Mirror", required=False)
    retry = forms.IntegerField(label="Retry number", required=False)
    wait = forms.IntegerField(label="Seconds of retry wait", required=False)


class ExportForm(forms.Form):
    export_path = forms.CharField(label="Export path", max_length=100)
    backup_id = forms.ChoiceField(choices=[], label="Backup id", required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            config = get_catalog()
            _catalog = tuple(
                reversed(
                    [
                        (
                            bckid,
                            bckid,
                            config.get(bckid, "name", fallback=""),
                            config.get(bckid, "status", fallback=""),
                            config.get(bckid, "timestamp", fallback=""),
                            config.get(bckid, "type", fallback=""),
                            config.get(bckid, "os", fallback=""),
                        )
                        for bckid in config
                        if bckid.lower() != "default"
                    ]
                )
            )
            self.fields["backup_id"].choices = [(item[0], item[0]) for item in _catalog]
            self.fields["backup_id"].widget.attrs.update(
                {"data-backup-info": json.dumps(_catalog)}
            )
            if _catalog:
                self.fields["backup_id"].initial = _catalog[0][0]
        except CatalogError:
            catalog_error_message()

    compress = forms.BooleanField(label="Compress", required=False)
    skip_error = forms.BooleanField(label="Skip error", required=False)
    checksum = forms.BooleanField(label="Checksum", required=False)
    acl = forms.BooleanField(label="Preserve ACL", required=False)
    mirror = forms.BooleanField(label="Mirror", required=False)
    cut = forms.BooleanField(label="Delete source", required=False)
    retry = forms.IntegerField(label="Retry number", required=False)
    wait = forms.IntegerField(label="Seconds of retry wait", required=False)


class ArchiveForm(forms.Form):
    backup_id = forms.ChoiceField(choices=[], label="Backup id", required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            config = get_catalog()
            _catalog = tuple(
                reversed(
                    [
                        (
                            bckid,
                            bckid,
                            config.get(bckid, "name", fallback=""),
                            config.get(bckid, "status", fallback=""),
                            config.get(bckid, "timestamp", fallback=""),
                            config.get(bckid, "type", fallback=""),
                            config.get(bckid, "os", fallback=""),
                        )
                        for bckid in config
                        if bckid.lower() != "default"
                    ]
                )
            )
            self.fields["backup_id"].choices = [(item[0], item[0]) for item in _catalog]
            self.fields["backup_id"].widget.attrs.update(
                {"data-backup-info": json.dumps(_catalog)}
            )
            if _catalog:
                self.fields["backup_id"].initial = _catalog[0][0]
        except CatalogError:
            catalog_error_message()

    days = forms.IntegerField(label="Older then days", required=False)
    archive_path = forms.CharField(label="Archive path", max_length=100)


class ConfigForm(forms.Form):
    action = forms.ChoiceField(
        choices=(
            ("new", "Generate new configuration"),
            ("remove", "Remove existing configuration"),
            ("init", "Reset catalog file"),
            ("delete-host", "Delete all entries for a single host"),
            ("clean", "Clean corrupt catalog"),
            ("delete-backup", "Delete specific backup ID"),
        ),
        label="Action",
        required=True,
    )
    catalog_path = forms.CharField(
        label="Catalog path",
        max_length=255,
        required=False,
        initial=CATALOG_PATH,
        help_text="Path to the catalog directory",
    )
    host = forms.CharField(
        label="Host",
        max_length=100,
        required=False,
        help_text="Hostname or IP address (for delete-host action)",
    )
    backup_id = forms.CharField(
        label="Backup ID",
        max_length=100,
        required=False,
        help_text="Backup ID to delete (for delete-backup action)",
    )
