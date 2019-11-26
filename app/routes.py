import os
from flask_login import logout_user
from flask import render_template,redirect,request
from app.forms import LoginForm
from app import app
from .models import User,Post
from .__init__ import Base,Session,engine
from flask_login import current_user, login_user
from flask_login import login_required
from app.forms import RegistrationForm

from flask_mysqldb import MySQL
print("in routes")
#db = MySQL(app)
Base.metadata.create_all(engine)

# 3 - create a new session
session = Session()

@app.route('/index',methods=['POST','GET'])
@login_required
def index():
    user = current_user
    session = Session()
    posts = session.query(Post).filter_by(user_id=user.id).all()
    #posts = [
        #{
         #   'author': {'username': 'Rohit'},
          #  'body': 'I love Programming'
        #},
        #{
         #   'author': {'username': 'Myra'},
          #  'body': 'I like to dance'
        #}
    #]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route("/post",methods=['POST'])
@login_required
def makePost():
    session = Session()
    post = Post()
    print(request.form['post'])
    post.body = request.form['post']
    post.user_id = current_user.id
    session.add(post)
    session.commit()
    session.flush()
    session.close()
    return redirect("/index")




@app.route('/')
@app.route('/login',methods=['GET'])
def login():
    #if(current_user.is_authenticated()):
     #   redirect("/index")
    login = LoginForm()
    return render_template('login.html',title='sign in',form=login)


@app.route('/uploadimage',methods=['GET'])
@login_required
def uploadimagepage():
    return render_template('uploadimage.html',title="Connect to World")

@app.route('/imageupload',methods=['POST'])
@login_required
def imageUpload():
    session = Session()
    user = session.query(User).filter_by(username = current_user.username).first()
    print(os.path.join('socialmedia','static','uploadimage'))
    file = request.files['image']
    path = os.path.join('static','uploadimage')
    path = os.path.join(path,file.filename)
    file.save('app/static/uploadimage/'+file.filename)
    user.imagename = file.filename
    #session.query.update(User).values(imagename= file.filename).where(username=current_user.username)
    session.commit()
    session.flush()
    session.close()
    return redirect('index')
@app.route('/securelogin',methods=['POST'])
def securelogin():

       session = Session(expire_on_commit=False)  #After comminting the session gets expires ,sometimes orm refresh the object ,so set the property expire_on_commit=false
       login = LoginForm()
       user = session.query(User).filter_by(username=login.username.data).first()

       session.close()
       print(user is None)
       if user is None or not user.check_password(login.password.data):
             #flash('Invalid username or password')
             return redirect('login')

       login_user(user)

       return redirect("index")


       #user1 = User()
      # user1 = session.query(User).all()
       #for u in user1:
        #    print(u.id)
       #user1.username = login.username.data
       #user1.email = login.username.data
       #user.id = 101
       #user1.password = login.password.data
       #session.add(user1)

       #post = Post()
       #post.id = 111
       #post.body = login.username.data
       #post.user_id = 101
       #session.add(post)
       #post1 = session.query(Post).all()
       #post = post1[1]

       #print(post.id,post.body,post.user_id)
       #p = session.query(Post).all()
       #print(len(p))
       #usert = session.query(User).all()
       #print(len(usert))




       #session.commit()
       #session.flush()
       #session.close()
       #print(type(user))
       #return render_template('index.html', title='Home', user={'username':"deleted"}, posts="")

        #return login.username.data
       #return redirect("/index")

@app.route('/createaccount',methods=['POST'])
def registerUser():
 form = RegistrationForm()
 session = Session(expire_on_commit=False)
 user = User()
 user.username = form.username.data
 user.email = form.email.data
 user.set_password(form.password.data)
 session.add(user)
 session.commit()
 session.flush()
 session.close()
 login_user(user)
 return redirect("/login")


@app.route("/register1")
def registerFormRedirect():
    registeruser = RegistrationForm()
    return render_template('register.html',title='Create Account',form=registeruser)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('login')