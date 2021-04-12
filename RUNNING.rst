=======
Running
=======

Prerequisites
-------------

For the application to work, it is necessary to have an instance of `PostgreSQL <https://www.postgresql.org/>`_.


Running http server
-------------------

Set environment variables in command line or edit file: api/config.py. Then, run the application.

.. code-block:: shell

        $ worker-finance run

or

.. code-block:: shell

        $ DB_USER=postgres \
            DB_PASSWORD=postgres \
            DB_HOST=localhost \
            DB_PORT=5432 \
            DB_DBNAME=api \
            ENVIRONMENT=ProductionConfig \
            worker-finance run
