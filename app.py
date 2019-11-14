from flask import Flask, render_template as rend, session, request
import hashlib, binascii, os, pymysql,secrets
app = Flask(__name__)

connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='pass.123', database='users', autocommit=True)
cursor = connection.cursor()
#alltaf gaman að fara overboard
app.secret_key = secrets.token_hex(255)
def authorize(user):
    pass
    #todo tengja við localhost, muna að breyta aftur

##stal smá kóða af fólki sem veit betur
def hash_password(password):
    #Hash a password for storing.
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')
 
def verify_password(stored_password, provided_password):
    #Verify a stored password against one provided by user
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

def verify():
    with connection: 
        cur = connection.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        for row in rows:
            print("{0} {1} {2}".format(row[0], row[1], row[2]))

@app.route('/')
def index():
    #todo setja up user verification
    if ~("user" in session):
        user = {"name":None,"pass":None,"email":None}
    else:
        user = session["user"]
    return rend("index.html", user=user)

@app.route("/login")
def login():
    #todo setja upp logins
    return index()

if __name__ == '__main__':
    app.run()