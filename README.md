National Export Trade Promotion

- Frontend
- Backend
- Mobile App

A government initiative to promote export of quality products through Information Technology

This API requires the following

- Python 3 and above
- SQLAlchemy(Alchemical)
- SQL Server
- Flask APIFairy

Other dependencies can be found in the "requirements.txt" file

To install(assumption:- Python already installed, SQL Server Setup):

`pip install -r requirements.txt`

Adjust environment variables in `.env` file

 - `Database credentials`
 - `FLASK_ENVIRONMENT` this should change to production
 - In 'api/app.py' file, change this line `def create_app(config_class=Config):` to `def create_app(config_class=Production)`: