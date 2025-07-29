import os
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
    _catalog = tuple(
        [
            (bckid, bckid) for bckid in get_catalog() if bckid.lower() != "default"
        ].reverse()
    )
    computer = forms.CharField(label="Computer name or ip", max_length=100)
    backup_id = forms.ChoiceField(
        choices=_catalog, label="Backup id", required=True, initial=_catalog[0]
    )
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
    _catalog = tuple(
        [
            (bckid, bckid) for bckid in get_catalog() if bckid.lower() != "default"
        ].reverse()
    )
    export_path = forms.CharField(label="Export path", max_length=100)
    backup_id = forms.ChoiceField(
        choices=_catalog, label="Backup id", required=True, initial=_catalog[0]
    )
    compress = forms.BooleanField(label="Compress", required=False)
    skip_error = forms.BooleanField(label="Skip error", required=False)
    checksum = forms.BooleanField(label="Checksum", required=False)
    acl = forms.BooleanField(label="Preserve ACL", required=False)
    mirror = forms.BooleanField(label="Mirror", required=False)
    cut = forms.BooleanField(label="Delete source", required=False)
    retry = forms.IntegerField(label="Retry number", required=False)
    wait = forms.IntegerField(label="Seconds of retry wait", required=False)


class ArchiveForm(forms.Form):
    _catalog = tuple(
        [
            (bckid, bckid) for bckid in get_catalog() if bckid.lower() != "default"
        ].reverse()
    )
    backup_id = forms.ChoiceField(
        choices=_catalog, label="Backup id", required=True, initial=_catalog[0]
    )
    days = forms.IntegerField(label="Older then days", required=False)
    archive_path = forms.CharField(label="Archive path", max_length=100)
