from flask import Flask, render_template as rend, session, request
import hashlib, binascii, os, pymysql,secrets
app = Flask(__name__)
#todo connecta rétt
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
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
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
@app.route("/signup")
def signup():
    return rend("signup.html",code=None)
@app.route("/signup/create",methods=['POST'])
def addusr():
    r=request.form
    print(r)
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    if request.form['username'] in map(lambda x: x[0], rows):
        pass
    cursor.execute("""INSERT INTO users (user, pass, nafn) VALUES
    (%s, %s, %s);""" % 
    (connection.escape(request.form['username']),
    connection.escape(hash_password(request.form['password'])),
    connection.escape(request.form['name'])))
    return rend("signup.html",code=0)

@app.route("/login")
def login_page():
    return rend("login.html",code = None)
@app.route("/login/process",methods=['POST'])
def login():
    r=request.form
    cursor.execute("""select * from users where user=%s;""" % (
        connection.escape(request.form['username'])))
    rows = cursor.fetchall()
    if rows:
        user = rows[0]
        session["user"] = {"name":user[0],"pass":user[1],"nafn":user[2]}
        print(user)
    else: 
        print("no")
        return rend("login.html", code=1)
    return rend("login.html", code=0)

if __name__ == '__main__':
    app.run()