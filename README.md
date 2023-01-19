National Export Trade Promotion - API

A government initiative to promote export of quality products through Information Technology

This API requires the following

- Python 3 and above
- SQL Server(Preferably MySQL)


Other dependencies will be installed via the "requirements.txt" file

To install(assumption:- Python already installed, SQL Server Setup):

From the console(CLI) create a virtual environment
`py -m venv venv` - `py` for python

Once the venv(virtual environment) has been created, activate by running the following

Windows - `.\venv\Script\activate`
Linux/MacOS - 

Once this is active, run the following to install system dependencies

`pip install -r requirements.txt`

Adjust environment variables in `.env` file

 - `Database credentials` - respectively depending on the working environment, production or development
 - Set the `BASE_URL`
 
Once all the above have been set(assumption you haven't messed up), run

`flask migrate` - create database migration
If you get any error that looks like the following:

`INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
ERROR [flask_migrate] Error: Target database is not up to date.`

Run this command to have this sorted;
`flask db stamp head`

Run `flask db migrate` again

I pressume this is successfull now, run the following to create db tables

`flask db upgrade`

At times, you will get errors pointing to flask_authorize during `db upgrade`,

Check in the `../migrations/versions` folder, open the most recent migration file

Under imports, add
`import flask_authorize`

Within your SQL Database, delete/drop previously created tables then,

Run `flask db upgrade again`

ppphhheeeewwww

Run `flask run` to start the application, then access it via the provided url,

If running by the defaults, the system can be accessed via
`http:127.0.0.1:5000/api/`

All good.