import ssl
from os import environ

from django.core.management import CommandError
from django.core.management.commands.runserver import Command as BaseRunserverCommand
from django.core.servers.basehttp import WSGIServer


class SSLWSGIServer(WSGIServer):
    default_certfile = None
    default_keyfile = None
    default_ca_certs = None
    default_ssl_version = ssl.PROTOCOL_TLS_SERVER

    def __init__(self, *args, **kwargs):
        certfile = kwargs.pop("certfile", None) or self.default_certfile
        keyfile = kwargs.pop("keyfile", None) or self.default_keyfile
        ca_certs = kwargs.pop("ca_certs", None) or self.default_ca_certs
        ssl_version = kwargs.pop("ssl_version", None) or self.default_ssl_version

        super().__init__(*args, bind_and_activate=False, **kwargs)

        if not certfile or not keyfile:
            raise ValueError(
                "SSL server requires BBWEB_SSL_CERTIFICATE_PATH and BBWEB_SSL_KEY_PATH."
            )

        context = ssl.SSLContext(ssl_version)
        context.load_cert_chain(certfile, keyfile)
        if ca_certs:
            context.load_verify_locations(ca_certs)

        self.socket = context.wrap_socket(self.socket, server_side=True)
        self.server_bind()
        self.server_activate()


class Command(BaseRunserverCommand):
    help = "Starts a lightweight web server with optional SSL."

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--ssl",
            action="store_true",
            dest="ssl",
            help="Enable HTTPS using the supplied certificate and key.",
        )
        parser.add_argument(
            "--cert",
            dest="cert",
            help="Path to the SSL certificate file.",
        )
        parser.add_argument(
            "--key",
            dest="key",
            help="Path to the SSL private key file.",
        )
        parser.add_argument(
            "--ca-cert",
            dest="ca_cert",
            help="Optional path to a CA bundle for SSL.",
        )

    def handle(self, *args, **options):
        self.ssl_enabled = options["ssl"] or environ.get(
            "BBWEB_SSL_ENABLE", "False"
        ).strip().lower() in ("1", "true", "yes", "on")
        self.ssl_certfile = options["cert"] or environ.get("BBWEB_SSL_CERTIFICATE_PATH")
        self.ssl_keyfile = options["key"] or environ.get("BBWEB_SSL_KEY_PATH")
        self.ssl_ca_certs = options["ca_cert"] or environ.get(
            "BBWEB_SSL_CA_CERTIFICATE_PATH"
        )

        if self.ssl_enabled:
            if not self.ssl_certfile or not self.ssl_keyfile:
                raise CommandError(
                    "SSL requires certificate and key paths via --cert/--key "
                    "or BBWEB_SSL_CERTIFICATE_PATH/BBWEB_SSL_KEY_PATH."
                )

            class CustomSSLServer(SSLWSGIServer):
                default_certfile = self.ssl_certfile
                default_keyfile = self.ssl_keyfile
                default_ca_certs = self.ssl_ca_certs

            self.server_cls = CustomSSLServer
            self.protocol = "https"

        return super().handle(*args, **options)
