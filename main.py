from app import app, db
import pymysql
pymysql.install_as_MySQLdb()

# Import blueprint
from other import other
from auth import auth

app.register_blueprint(other)
app.register_blueprint(auth)

if __name__ == '__main__':
    app.run()