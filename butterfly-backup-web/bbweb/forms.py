from django import forms


class BackupForm(forms.Form):
    computer = forms.CharField(label="Computer name or ip", max_length=100)
    user = forms.CharField(label="Username", max_length=100)
    port = forms.IntegerField(label="SSH port number")
    mode = forms.ChoiceField(
        choices=(
            ("1", "full"),
            ("2", "incremental"),
            ("3", "differential"),
            ("4", "mirror"),
        ),
        label="Mode",
        required=True,
    )
    data = forms.ChoiceField(
        choices=(
            ("1", "user"),
            ("2", "config"),
            ("3", "application"),
            ("4", "system"),
            ("5", "log")
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
    retention_days = forms.IntegerField(label="Retention days")
    retention_number = forms.IntegerField(label="Retention minimum number")
    compress = forms.BooleanField(label="Compress")
    skip_error = forms.BooleanField(label="Skip error")
    checksum = forms.BooleanField(label="Checksum")
    acl = forms.BooleanField(label="Preserve ACL")
    retry = forms.IntegerField(label="Retry number")
    wait = forms.IntegerField(label="Seconds of retry wait")
