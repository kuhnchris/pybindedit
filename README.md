# pybindedit
A webbrowser-esque editor for BIND configuration files.

**Please only use with localhost:8000, do not try to expose this to the outside world... (for obvious reasons)**

## First steps
To finish the setup of the project, run the following command(s):
```
# this runs migrations and creates db.sqlite3
python pybindedit/manage.py migrate
```

## User authentication
To make it possible for user(s) to login, they need to be super-user(s).

Execute the following command to create a superuser:
```bash
python pybindedit/manage.py createsuperuser
```
Follow the prompt as requested.

### Todos:
* [ ] Implement ```BIND9``` restart
* [ ] Add ```docker-compose.yml```
* [ ] Implement ```save``` functionallity
* [ ] Implement ```edit``` button
* [x] Implement ```user auth```
* [x] Keep ```.gitignore``` up to date
* [ ] Test / PyTest / Unit Test(s)
* [ ] Document & comment source code 