.. butterfly_backup_web documentation master file, created by
   sphinx-quickstart on Tue Jun  3 17:09:02 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

butterfly_backup_web documentation
==================================


.. toctree::
   :maxdepth: 2
   :caption: Contents:

Presentation
------------

`Butterfly Backup <https://github.com/MatteoGuadrini/Butterfly-Backup>`__ is a modern backup program that can back up your files. It is a command line tool.

``butterfly_backup_web`` is a web interface of the Butterfly Backup command line tool.

Installation
------------

A simple installation is done directly from the repository.

.. code-block:: shell

      git clone https://github.com/MatteoGuadrini/butterfly-backup-web.git
      cd butterfly-backup-web
      pip install . --upgrade

Docker
------

Butterfly Backup Web is distribuited with containerization files. You can build the image:

.. code-block:: shell

      cd butterfly-backup-web
      docker build . -t bbweb:latest
      docker run -d -v /backup_catalog/:/tmp/backup/ -p 8080:8080 -e DJANGO_SUPERUSER_PASSWORD="MyComplexPassword0!" -e BB_CATALOG_PATH="/backup" localhost/bbweb:latest

If you want preserve the data, create a volume and map to container:

.. code-block:: shell

      # Create a volume
      docker volume create bbweb
      # Run container
      docker run -d -v bbweb:/tmp/backup/ -p 8080:8080 localhost/bbweb:0.1.0

Customize Docker image
**********************

Docker image born with enviroment variables; modifying these variables to customized experience:

.. code-block:: shell

      vim Dockerfile
      ...
      DJANGO_SUPERUSER_PASSWORD="Admin000!"
      DJANGO_SUPERUSER_USERNAME="admin"
      DJANGO_SUPERUSER_EMAIL="admin@bbweb.com"
      BB_CATALOG_PATH="/tmp/backup"
      ...

Environment variables
---------------------

The following environment variables are available for Butterfly Backup Web:

.. list-table:: Environment variables
   :header-rows: 1
   :widths: 20 50 30

   * - Variable
     - Description
     - Default
   * - BB_CATALOG_PATH
     - Backup catalog directory.
     - /tmp/backup
   * - DJANGO_SUPERUSER_USERNAME
     - Default admin username for the initial Docker image.
     - admin
   * - DJANGO_SUPERUSER_PASSWORD
     - Default admin password for the initial Docker image.
     - Admin000!
   * - DJANGO_SUPERUSER_EMAIL
     - Default admin email for the initial Docker image.
     - admin@bbweb.com
   * - BBWEB_SSL_ENABLE
     - Enable HTTPS and secure cookie/HSTS settings.
     - False
   * - BBWEB_SSL_CERTIFICATE_PATH
     - Path to the SSL certificate file used by the custom runserver command.
     - (none)
   * - BBWEB_SSL_KEY_PATH
     - Path to the SSL private key file used by the custom runserver command.
     - (none)
   * - BBWEB_SSL_CA_CERTIFICATE_PATH
     - Optional path to a CA bundle for HTTPS.
     - (none)
   * - BBWEB_SECURE_HSTS_SECONDS
     - The HSTS max-age value in seconds when SSL is enabled.
     - 31536000
   * - BBWEB_SECURE_HSTS_INCLUDE_SUBDOMAINS
     - Enable HSTS for subdomains when SSL is enabled.
     - True
   * - BBWEB_SECURE_HSTS_PRELOAD
     - Enable HSTS preload when SSL is enabled.
     - True

Configuration
-------------

To configure Butterfly Backup Web, edit your profile and insert your *catalog* backup:

.. code-block:: shell

      nano ~/.bashrc      # or .zshrc if you use zsh
      ...
      export BB_CATALOG_PATH=/tmp/backup
      ...

After this, import and create a database:

.. code-block:: shell
      
      source ~/.bashrc    # or .zshrc if you use zsh
      # Use bbweb command line
      bbweb migrate
      bbweb createsuperuser
      bbweb runserver 0.0.0.0:80
      # Use Python package
      python3 -m butterfly_backup_web migrate
      python3 -m butterfly_backup_web createsuperuser
      python3 -m butterfly_backup_web runserver 0.0.0.0:80
      # Optional HTTPS
      bbweb runserver --ssl 0.0.0.0:8443 --cert /path/to/server.crt --key /path/to/server.key
      # or use environment variables
      export BBWEB_SSL_ENABLE=1
      export BBWEB_SSL_CERTIFICATE_PATH=/path/to/server.crt
      export BBWEB_SSL_KEY_PATH=/path/to/server.key
      bbweb runserver 0.0.0.0:8443    # or 443 if you have permissions

.. note::

   When SSL is enabled, Butterfly Backup Web uses port **443** (standard HTTPS) or **8443** (alternative HTTPS). Port 443 requires elevated privileges, while port 8443 can be used without special permissions.


Systemd Service
---------------

If you use linux and systemd in your linux environment, you should configure a **bbweb** service, like this:

.. code-block:: shell

      sudo wget -O /usr/lib/systemd/system/bbweb.service https://raw.githubusercontent.com/MatteoGuadrini/butterfly-backup-web/refs/heads/main/systemd/bbweb.service
      sudo nano /usr/lib/systemd/system/bbweb.service

      [Unit]
      Description=Butterfly Backup Web
      After=multi-user.target

      [Service]
      Type=simple
      Restart=always
      ExecStart=/usr/bin/python3 -m butterfly_backup_web runserver 0.0.0.0:80
      Environment="BB_CATALOG_PATH=/tmp/backup"     # Modify with your catalog path

      [Install]
      WantedBy=multi-user.target

Now start and enable it:

.. code-block:: shell

      sudo systemctl daemon-reload
      sudo systemctl enable bbweb.service --now

Systemd Service with HTTPS
***************************

To enable HTTPS in your systemd service, update the service file with SSL environment variables and port:

.. code-block:: shell

      sudo nano /usr/lib/systemd/system/bbweb.service

      [Unit]
      Description=Butterfly Backup Web
      After=multi-user.target

      [Service]
      Type=simple
      Restart=always
      ExecStart=/usr/bin/python3 -m butterfly_backup_web runserver 0.0.0.0:8443
      Environment="BB_CATALOG_PATH=/tmp/backup"     # Modify with your catalog path
      Environment="BBWEB_SSL_ENABLE=1"
      Environment="BBWEB_SSL_CERTIFICATE_PATH=/path/to/server.crt"
      Environment="BBWEB_SSL_KEY_PATH=/path/to/server.key"

      [Install]
      WantedBy=multi-user.target

Then reload and restart the service:

.. code-block:: shell

      sudo systemctl daemon-reload
      sudo systemctl restart bbweb.service

Django Admin
------------

Butterfly Backup Web includes Django's built-in admin interface for managing users, groups, and other administrative tasks.

Accessing the Admin Interface
*****************************

To access the Django admin interface:

1. Navigate to ``/admin/`` on your web server (e.g., ``http://localhost:80/admin/`` or ``https://localhost:8443/admin/``)
2. Log in with your superuser credentials created during installation

Managing Users
**************

The admin interface allows you to manage user accounts with the following capabilities:

- **Create new users**: Add new user accounts with appropriate permissions
- **Edit existing users**: Modify user details, permissions, and group memberships
- **Delete users**: Remove user accounts from the system
- **Change passwords**: Reset or change user passwords

Changing User Passwords
========================

To change a user's password via the admin interface:

1. Navigate to the **Users** section in the admin panel
2. Click on the user you want to modify
3. Scroll to the "Password" field
4. Click the "Change password" link
5. Enter and confirm the new password
6. Click "Change password" to save

.. note::

   Superusers can also change passwords using the command line:

   .. code-block:: shell

      bbweb changepassword <username>

Managing Groups
**************

Django groups allow you to organize users and assign permissions to multiple users at once.

Creating and Managing Groups
=============================

To manage groups in the admin interface:

1. Navigate to the **Groups** section in the admin panel
2. Click "Add group" to create a new group
3. Enter a group name
4. Select the permissions you want to assign to the group
5. Click "Save" to create the group

To add users to a group:

1. Navigate to the **Users** section
2. Click on the user you want to modify
3. Scroll to the "Groups" field
4. Select the group(s) you want to add the user to
5. Click "Save" to apply the changes

Permissions
***********

Django provides a flexible permission system that can be managed through the admin interface:

- **View permissions**: See what permissions are available for each model
- **Assign permissions**: Grant specific permissions to users or groups
- **Custom permissions**: Create custom permissions for specific use cases

Common permissions include:

- **Add**: Permission to create new objects
- **Change**: Permission to modify existing objects
- **Delete**: Permission to remove objects
- **View**: Permission to view objects (if enabled)

Command Line User Management
*****************************

In addition to the web interface, you can manage users via command line:

Create a superuser:

.. code-block:: shell

      bbweb createsuperuser

Change a user's password:

.. code-block:: shell

      bbweb changepassword <username>

Create a regular user (requires Django shell):

.. code-block:: shell

      bbweb shell
      >>> from django.contrib.auth.models import User
      >>> User.objects.create_user('username', 'email@example.com', 'password')