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

Upgrade
-------

To upgrade Butterfly Backup Web to the latest version, use the following command:

.. code-block:: shell

      cd butterfly-backup-web
      git pull
      pip install . --upgrade

After upgrading, it is recommended to run database migrations to ensure compatibility:

.. code-block:: shell

      bbweb migrate

If you are using Docker, rebuild the image with the latest code:

.. code-block:: shell

      cd butterfly-backup-web
      git pull
      docker build . -t bbweb:latest
      docker stop <container_id>
      docker rm <container_id>
      docker run -d -v /backup_catalog/:/tmp/backup/ -p 8080:8080 -e DJANGO_SUPERUSER_PASSWORD="MyComplexPassword0!" -e BB_CATALOG_PATH="/backup" localhost/bbweb:latest

.. note::

   Always backup your catalog and configuration files before performing an upgrade.

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

User Views
==========

Butterfly Backup Web provides several views for managing backups through a web interface. Each view serves a specific purpose in the backup workflow.

Home View
*********

.. image:: https://i.ibb.co/0V9dbKBC/Butterfly-Backup-07-26-2026-09-24-AM.png

The home view displays an overview of all backups in the catalog.

**URL**: ``/`` or ``/home/``

**Access**: Requires login

**Features**:

- Displays a list of all backups from the catalog
- Shows backup name, type, operating system, timestamp, and status
- Provides quick access to backup details
- Shows the current catalog path

**Usage**:

Navigate to the root URL (e.g., ``http://localhost:80/``) after logging in to see all available backups in your catalog.

Login View
**********

.. image:: https://i.ibb.co/mrt2yYfN/Butterfly-Backup-07-26-2026-09-11-AM.png

The login view provides authentication for accessing the web interface.

**URL**: ``/accounts/login/``

**Access**: Public (no authentication required)

**Features**:

- Standard Django authentication form
- Validates catalog file existence before login
- Redirects to home page upon successful authentication
- Displays error messages if catalog file is not found

**Usage**:

Enter your username and password to authenticate. If the catalog file is not found at the configured path, an error message will be displayed.

Backup Details View
*******************

.. image:: https://i.ibb.co/gb1t7SDb/Butterfly-Backup-07-26-2026-09-18-AM.png

The details view shows comprehensive information about a specific backup.

**URL**: ``/details/<section>/``

**Access**: Requires login

**Parameters**:

- ``section``: The backup ID/section name from the catalog

**Features**:

- Displays complete backup metadata
- Shows backup name, type, operating system, and timestamp
- Displays start and end times
- Shows backup status (running, completed, etc.)
- Indicates if backup is archived or cleaned
- Shows the backup path

**Usage**:

Click on any backup from the home view to view its detailed information. The backup ID is passed as a URL parameter.

Backup Logs View
****************

The logs view displays log files associated with a specific backup.

**URL**: ``/details/<section>/logs``

**Access**: Requires login

**Parameters**:

- ``section``: The backup ID/section name from the catalog

**Features**:

- Displays general log file
- Shows backup-specific logs (backup.log)
- Shows restore-specific logs (restore.log)
- Shows export-specific logs (export.log)
- Formats log content with HTML line breaks
- Displays message if no logs are available

**Usage**:

Navigate to the logs view for a specific backup to review all associated log files. Logs are displayed in a readable format with proper line breaks.

Log Tail API View
*****************

The log tail view provides an API endpoint for real-time log monitoring.

**URL**: ``/details/<section>/logs/<log_type>/tail``

**Access**: Requires login

**Parameters**:

- ``section``: The backup ID/section name from the catalog
- ``log_type``: Type of log (``general``, ``backup``, ``restore``, ``export``)

**Features**:

- Returns log content as JSON
- Supports real-time log monitoring (tail-f behavior)
- Returns 404 if log file is not found
- Formats log content with HTML line breaks

**Usage**:

This API endpoint is typically used by JavaScript for real-time log updates. Make GET requests to fetch the latest log content.

Backup Creation View
********************

.. image:: https://i.ibb.co/p69vpknK/Butterfly-Backup-07-26-2026-09-20-AM.png

The backup view allows users to create new backups through a web form.

**URL**: ``/backup/``

**Access**: Requires login

**Features**:

- Form-based backup configuration
- Supports multiple backup modes (full, incremental, differential, mirror)
- Configurable data types (user, config, application, system, log)
- OS type selection (unix, macos, windows)
- Optional SSH port configuration
- Retention policy settings (days and minimum number)
- Advanced options: compression, error skipping, checksum, ACL preservation
- Retry mechanism with wait time configuration
- Executes ``bb backup`` command in background
- Displays success/error messages

**Form Fields**:

- **Computer**: Target computer name or IP address
- **User**: SSH username (default: root)
- **Port**: SSH port number (optional)
- **Mode**: Backup mode (full, incremental, differential, mirror)
- **Data**: Data type to backup (user, config, application, system, log)
- **OS type**: Operating system type (unix, macos, windows)
- **Retention days**: Number of days to retain backups (optional)
- **Retention minimum number**: Minimum number of backups to keep (optional)
- **Compress**: Enable compression (optional)
- **Skip error**: Continue on errors (optional)
- **Checksum**: Verify checksums (optional)
- **Preserve ACL**: Preserve access control lists (optional)
- **Retry number**: Number of retry attempts (optional)
- **Seconds of retry wait**: Wait time between retries (optional)

**Usage**:

Fill in the required fields and optional parameters as needed, then submit the form to start a backup. The backup runs in the background, and you can monitor progress through the logs view.

Restore View
************

.. image:: https://i.ibb.co/rGq0ZXqN/Butterfly-Backup-07-26-2026-09-20-AM-1.png

The restore view allows users to restore data from existing backups.

**URL**: ``/restore/``

**Access**: Requires login

**Features**:

- Select backup from catalog dropdown
- Configurable restore destination
- Root directory specification
- OS type selection
- Optional SSH port configuration
- Advanced options: compression, error skipping, checksum, ACL preservation
- Mirror mode support
- Retry mechanism with wait time configuration
- Executes ``bb restore`` command in background
- Displays success/error messages

**Form Fields**:

- **Computer**: Target computer name or IP address
- **Backup id**: Select from available backups (populated from catalog)
- **Root directory**: Root directory for restore (optional)
- **User**: SSH username (default: root)
- **Port**: SSH port number (optional)
- **OS type**: Operating system type (unix, macos, windows)
- **Compress**: Enable compression (optional)
- **Skip error**: Continue on errors (optional)
- **Checksum**: Verify checksums (optional)
- **Preserve ACL**: Preserve access control lists (optional)
- **Mirror**: Enable mirror mode (optional)
- **Retry number**: Number of retry attempts (optional)
- **Seconds of retry wait**: Wait time between retries (optional)

**Usage**:

Select a backup ID from the dropdown (populated from your catalog), configure restore parameters, and submit to start the restore process. Monitor progress through the logs view.

Export View
***********

.. image:: https://i.ibb.co/BVqhqrH8/Butterfly-Backup-07-26-2026-09-21-AM.png

The export view allows users to export backups to external locations.

**URL**: ``/export/``

**Access**: Requires login

**Features**:

- Select backup from catalog dropdown
- Specify export destination path
- Optional source deletion after export
- Advanced options: compression, error skipping, checksum, ACL preservation
- Mirror mode support
- Retry mechanism with wait time configuration
- Executes ``bb export`` command in background
- Displays success/error messages

**Form Fields**:

- **Export path**: Destination path for exported backup
- **Backup id**: Select from available backups (populated from catalog)
- **Compress**: Enable compression (optional)
- **Skip error**: Continue on errors (optional)
- **Checksum**: Verify checksums (optional)
- **Preserve ACL**: Preserve access control lists (optional)
- **Mirror**: Enable mirror mode (optional)
- **Delete source**: Delete source after export (optional)
- **Retry number**: Number of retry attempts (optional)
- **Seconds of retry wait**: Wait time between retries (optional)

**Usage**:

Select a backup ID, specify the export destination, configure optional parameters, and submit to start the export process.

Archive View
************

.. image:: https://i.ibb.co/DPJ5KCzz/Butterfly-Backup-07-26-2026-09-22-AM.png

The archive view allows users to archive old backups to long-term storage.

**URL**: ``/archive/``

**Access**: Requires login

**Features**:

- Select backup from catalog dropdown
- Specify archive destination path
- Optional age-based filtering (older than X days)
- Executes ``bb archive`` command in background
- Displays success/error messages

**Form Fields**:

- **Backup id**: Select from available backups (populated from catalog)
- **Archive path**: Destination path for archived backup
- **Older then days**: Only archive backups older than specified days (optional)

**Usage**:

Select a backup to archive, specify the archive destination, optionally set an age filter, and submit to start the archiving process.

Delete Backup View
******************

The delete backup view allows users to remove backups from the catalog.

**URL**: ``/delete/<section>/``

**Access**: Requires login

**Parameters**:

- ``section``: The backup ID/section name from the catalog

**Features**:

- Deletes specified backup from catalog
- Uses ``--force`` flag to prevent confirmation prompts
- Executes ``bb config --delete-backup`` command
- Redirects to home view after deletion
- Displays success/error messages

**Usage**:

This view is typically accessed via a delete button on the home or details view. The backup ID is passed as a URL parameter, and the deletion is performed immediately.

Configuration View
******************

.. image:: https://i.ibb.co/HfkxTJ4X/Butterfly-Backup-07-26-2026-09-23-AM.png

The config view provides advanced catalog management operations.

**URL**: ``/config/``

**Access**: Requires login

**Features**:

- Multiple configuration actions
- Catalog initialization and management
- Host and backup deletion
- Catalog cleaning
- Executes ``bb config`` command with various flags
- Form validation based on selected action
- Displays success/error messages

**Form Fields**:

- **Action**: Configuration action to perform
  - ``new``: Generate new configuration
  - ``remove``: Remove existing configuration
  - ``init``: Reset catalog file
  - ``delete-host``: Delete all entries for a single host
  - ``clean``: Clean corrupt catalog
  - ``delete-backup``: Delete specific backup ID
- **Catalog path**: Path to the catalog directory (required for most actions)
- **Host**: Hostname or IP address (required for delete-host action)
- **Backup ID**: Backup ID to delete (required for delete-backup action)

**Usage**:

Select the desired action, fill in the required fields based on the action, and submit to perform the configuration operation. The form validates that required fields are provided for each action type.

.. note::

   All configuration actions use the ``--force`` flag to prevent interactive prompts.