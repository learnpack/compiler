# This file was created to run the application on heroku using gunicorn.
# Read more about it here: https://devcenter.heroku.com/articles/python-gunicorn

from server import app as application

if __name__ == "__main__":
    application.run()
