from django import forms


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
