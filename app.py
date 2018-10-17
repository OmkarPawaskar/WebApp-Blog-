from flask import Flask, render_template, request, session
from flask.helpers import make_response
from src.common.database import Database
from src.models.blog import Blog
from src.models.user import User
from src.models.post import Post


app = Flask(__name__,template_folder='src/templates') #__name__ is built in variable which contains '__main__'
#we need to set secure secret key - to ensure data sent in cookie is secure
#If app.secret_key isn't set, Flask will not allow you to set or access the session dictionary.
app.secret_key = "omii"

@app.route('/')
def home_template():
    return render_template('home.html')

@app.route('/login') #www.mysite.com/api/login or 127.0.0.1:4995/login  -> whenever there is endpoint '/login' in url it will run hello_method()
def login_template():
    return render_template('login.html')


@app.route('/register')  # www.mysite.com/api/register
def register_template():
    return render_template('register.html')    

@app.before_first_request #so before logging in we initialize the database
def initialize_database():
    Database.initialize()

@app.route('/auth/login',methods = ['POST'] )
def login_user():
    email = request.form['email'] 
    password = request.form['password']

    if User.login_valid(email,password):
        User.login(email)
    else:#if we enter email that is not present in database
        session['email'] = None #need to redirect user to register in this step ..work pending
    
    return render_template("profile.html",email = session['email']) #since we want data coming from application

@app.route('/auth/register',methods = ['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']

    User.register(email,password)
    return render_template("profile.html", email=session['email'])


@app.route('/blogs/<string:user_id>')
@app.route('/blogs')
def user_blogs(user_id = None):
    if user_id is not None:    
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_email(session['email'])
        
    blogs = user.get_blogs()
    return render_template("user_blogs.html",blogs = blogs,email = user.email)

@app.route('/blogs/new',methods = ['POST','GET'])#POST when user sends data ,GET when user arrives at endpoint
def create_new_blog():
    if request.method == 'GET':
        return render_template('new_blog.html') #if users accesses page directly
    else:
        title = request.form['title']
        description = request.form['description']
        user = User.get_by_email(session['email'])

        new_blog = Blog(user.email, title, description, user._id)
        new_blog.save_to_mongo()

       # return render_template('user_blogs')
        return make_response(user_blogs(user._id)) #can be useful to write blog for someone else ie as co-author


@app.route('/posts/<string:blog_id>')
def blog_posts(blog_id):
    blog = Blog.from_mongo(blog_id)
    posts = blog.get_posts()

    return render_template('posts.html', posts = posts, blog_title = blog.title, blog_id = blog_id)


# POST when user sends data ,GET when user arrives at endpoint
@app.route('/posts/new/<string:blog_id>', methods=['POST', 'GET'])
def create_new_post(blog_id):
    if request.method == 'GET':
        # if users accesses page directly
        return render_template('new_post.html',blog_id = blog_id)
    else:
        title = request.form['title']
        content = request.form['content']
        user = User.get_by_email(session['email'])

        new_post = Post(blog_id, title, content, user.email)
        new_post.save_to_mongo()

       # return render_template('user_blogs')
        # can be useful to write blog for someone else ie as co-author
        return make_response(blog_posts(blog_id))

if __name__ == '__main__': #when we want to run app from 0 or start
   # app.run()
    app.run(port= 5000)

