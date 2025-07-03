from django import forms


class BackupForm(forms.Form):
    computer = forms.CharField(label="Computer name or ip", max_length=100)
    user = forms.CharField(label="Username", max_length=100, initial="root")
    port = forms.IntegerField(label="SSH port number", initial=22)
    mode = forms.ChoiceField(
        choices=(
            ("1", "full"),
            ("2", "incremental"),
            ("3", "differential"),
            ("4", "mirror"),
        ),
        label="Mode",
        required=True,
        initial="2",
    )
    data = forms.ChoiceField(
        choices=(
            ("1", "user"),
            ("2", "config"),
            ("3", "application"),
            ("4", "system"),
            ("5", "log"),
        ),
        label="Data",
        required=True,
    )
    type_ = forms.ChoiceField(
        choices=(
            ("1", "unix"),
            ("2", "macos"),
            ("3", "windows"),
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
