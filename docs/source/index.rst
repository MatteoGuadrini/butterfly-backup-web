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
      docker build . -t bbweb:0.1.0
      docker run -d -v /backup_catalog/:/tmp/backup/ -p 8080:8080 -e DJANGO_SUPERUSER_PASSWORD="MyComplexPassword0!" -e BB_CATALOG_PATH="/backup" localhost/bbweb:0.1.0

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

Configuration
-------------

To configure Butterfly Backup Web, edit your profile and insert you *catalog* backup:

.. code-block:: shell
      nano ~/.bashrc      # or .zshrc if you use zsh
      ...
      export BB_CATALOG_PATH=/backup
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
 