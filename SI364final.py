import os
import requests
import json

from flask import Flask, render_template, session, redirect, request, url_for, flash
from flask_script import Manager, Shell
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, PasswordField, BooleanField, SelectMultipleField, ValidationError
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from werkzeug.security import generate_password_hash, check_password_hash
import json
import requests
api_key='AIzaSyCwtkP5Jw8jtoR0CQ2CXBAdPmgw-Su60pI'
from flask_login import LoginManager, login_required, logout_user, login_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'hardtoguessstring'
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL') or "postgresql://localhost/SI364projectplanjordbkap" # TODO 364: You should edit this to correspond to the database name YOURUNIQNAMEHW4db and create the database of that name (with whatever your uniqname is; for example, my database would be jczettaHW4db). You may also need to edit the database URL further if your computer requires a password for you to run this.
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# App addition setups
manager = Manager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

# Login configurations setup
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app) # set up login manager


user_lists = db.Table('user_lists',db.Column('book_id',db.Integer, db.ForeignKey('book.id')),db.Column('personalbooklist_id',db.Integer, db.ForeignKey('personalbooklist.id')))


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    lists = db.relationship('PersonalBooklist', backref='User')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

## DB load function
## Necessary for behind the scenes login manager that comes with flask_login capabilities! Won't run without this.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) # returns User object or None

class Author(db.Model):
    __tablename__='authors'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(128),unique=True)

    def __repr__(self):
        return"{}(id:{})".format(self.name, self.id)

class Book(db.Model):
    __tablename__="book"
    id= db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(128))
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"))
    description=db.Column(db.String(1000))
    read=db.Column(db.String(128))
    def __repr__(self):
    	return"{}(author_id:{})".format(self.title, self.author_id)

class PersonalBooklist(db.Model):
    __tablename__="personalbooklist"
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    book = db.relationship('Book',secondary=user_lists,backref=db.backref('personalbooklist',lazy='dynamic'),lazy='dynamic')



class RegistrationForm(FlaskForm):
    email = StringField('Email:', validators=[Required(),Length(1,64)])
    username = StringField('Username (dont start with an @):',validators=[Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_@.]*$',0,'Usernames must have only letters, numbers, dots or underscores')])
    
    def validate_username(form, field):
        print (field.data[0])
        if field.data[0]=='@':
            raise ValidationError("Username must not start with an @ symbol")
    
    password = PasswordField('Password:',validators=[Required(),EqualTo('password2',message="Passwords must match")])
    
    def validate_password(form, field):
        if len(field.data) < 7:
            print (len(field.data))
            raise ValidationError("Password is not strong enough, it should have 8 or more characters")
    password2 = PasswordField("Confirm Password:",validators=[Required()])
    submit = SubmitField('Register User')

    #Additional checking methods for the form
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    # def validate_username(self,field):
    #     if User.query.filter_by(username=field.data).first():
    #         raise ValidationError('Username already taken')

# Provided
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1,64), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class BookSearchForm(FlaskForm):
    search = StringField("Enter The title of a Book", validators=[Required()])
    readStatus=StringField("What is your read status on this book? read, mid-way through, just started, etc", validators=[Required()])
    submit = SubmitField('Submit')

class CreateListForm(FlaskForm):
    name = StringField('What is the name of the list',validators=[Required()])
    book_picks = SelectMultipleField('What Books should be on the list')
    submit = SubmitField("Create List")


class UpdateButtonForm(FlaskForm):
    submit= SubmitField("Update read Status")

class UpdateInfoForm(FlaskForm):
    newStatus = StringField("What is the new status of this book?", validators=[Required()])
    update = SubmitField('Update Status')


class DeleteButtonForm(FlaskForm):
    delete= SubmitField('Delete')

def get_books_from_api(search_string):
    searched=search_string.replace(" ","+")
    parms = {"q":searched, 'key':api_key}
    r = requests.get(url="https://www.googleapis.com/books/v1/volumes", params=parms)
    params_dict=json.loads(r.text)
    return params_dict
	#uses the books api to reutrn book information that is wanted
 
def get_or_create_author_from_api(author_name):
    author=Author.query.filter_by(name=author_name).first()
    if author:
        return author
    else:
        auth=Author(name=author_name)
        db.session.add(auth)
        db.session.commit()
        return auth

	#takes input from the BookSearchForm as the name of the book and searches the google books api and pulls out the first book in the dictionary
	#then takes the author and creates the instance, it should check if the author is there first

def get_or_create_book_from_api(author, title, description, readStatus):
    boo=Book.query.filter_by(title=title).first()
    if boo:
        return boo
    else:
        get_or_create_author_from_api(author)
        auth=Author.query.filter_by(name=author).first()
        book1=Book(title=title, author_id=auth.id, description=description, read=readStatus)
        print (book1)
        db.session.add(book1)
        db.session.commit()
        return book1
	#takes the information from the search to then take the description, queried author id and then make the instance in the table
	


def get_book_by_id(id):
    bid=Book.query.filter_by(id=id).first()
    return bid
	#queries the book by the id



def get_or_create_list(name, current_user, book_list):
    list1=PersonalBooklist.query.filter_by(name=name).first()
    if list1:
        return list1
    else:
        list1=PersonalBooklist(name=name, user_id=current_user.id,book=[])
        for a in book_list:
            list1.book.append(a)
        db.session.add(list1)
        db.session.commit()
        return list1
	#creates a list of books for the user if it is not already made

            
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/login',methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid username or password.')
    return render_template('login.html',form=form)
#self-explanatory

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('index'))
#self explanatory

@app.route('/register',methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,username=form.username.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now log in!')
        return redirect(url_for('login'))
    errors = [v for v in form.errors.values()]
    if len(errors) > 0:
        flash("!!!! ERRORS IN FORM SUBMISSION - " + str(errors))
    return render_template('register.html',form=form)
#self explanatory

@app.route('/', methods=['GET', 'POST'])
def index():
    form=BookSearchForm()
    if form.validate_on_submit():
        title=form.search.data
        readStatus=form.readStatus.data
        return_info=get_books_from_api(title)
        print (return_info)
        description=return_info['items'][0]['volumeInfo']['description']
        if len(description)>950:
            description=description[0:930]+ "..."
        author=return_info['items'][0]['volumeInfo']['authors'][0]
        get_or_create_book_from_api(author, title, description, readStatus)
        flash ("successfully added the book to the db")
        return render_template('index.html', form=form)
    return render_template('index.html',form=form)
	#searches for book information using the BookSearchForm then should send to the 
	#get or create author and book helper functions then send you to the all_books page

@app.route('/all_books')
def all_books():
    form = UpdateButtonForm()
    a=Book.query.all()
    num_books=len(a)
    all_names=[(book.title, book.description, book.read, Author.query.filter_by(id=book.author_id).first()) for book in a]
    return render_template('all_books.html',books=all_names,num_books=num_books, form=form)
	#this should show all of the books informaiton in the database using queries
	#will also have an update button after every book to update if the user has 
	#read the book yet or not and can see where they are at
@app.route('/update/<book>',methods=["GET","POST"])
def update(book):
    form = UpdateInfoForm()
    if form.validate_on_submit():
        new_status= form.newStatus.data
        str(book.replace("%20"," "))
        book1=Book.query.filter_by(title=book).first()
        book1.read=new_status
        db.session.commit()
        flash("updated rating of " + book)
    return render_template('update_item.html', item_name= book, form=form)
	#this will be where the user can actually update the read status of said item after
	#selecting said book from the all_books page

@app.route('/all_authors')
def all_authors():
    b=Author.query.all()
    all_authors=[(auth.name, len(Book.query.filter_by(author_id=auth.id).all())) for auth in b]
    return render_template('all_authors.html',all_authors=all_authors)
	#this should show all of the authors informaiton in the database using queries


@app.route('/create_list',methods=["GET","POST"])
@login_required
def create_list():
    form= CreateListForm()
    books=Book.query.all()
    choices=[(boo.id, boo.title) for boo in books]
    form.book_picks.choices = choices
    return render_template('create_list.html', form=form)
	#this should create a list using a selection of books and choices, an example of a list
	#could be 'books to read' or 'best horror'


@app.route('/lists',methods=["GET","POST"])
@login_required
def lists():
    form = DeleteButtonForm()
    fm=CreateListForm()
    try:
        if request.method=="GET":
            result=request.args
            books_chosen=result.getlist('book_picks')
            print (books_chosen)
            books_selected=[get_book_by_id(int(id)) for id in books_chosen]
            name1=result.get('name')
            get_or_create_list(name=name1, current_user=current_user, book_list=books_selected)
        lists=PersonalBooklist.query.filter_by(user_id=current_user.id).all()
        num_list=len(lists)
        return render_template('lists.html', lists=lists, form=form, num_lists=num_list)
    except:
        lists=PersonalBooklist.query.filter_by(user_id=current_user.id).all()
        num_list=len(lists)
        return render_template('lists.html', lists=lists, form=form, num_lists=num_list)
	#this will let you view all of the lists that you made
	# you can delete lists once you dont want them anymore

@app.route('/list/<list_id>')
def single_list(list_id):
    list_num=int(list_id)
    lista=PersonalBooklist.query.filter_by(id=list_num).first()
    books=lista.book.all()
    all_names=[(a.title, a.description, Author.query.filter_by(id=a.author_id).first()) for a in books]
    return render_template("one_list.html", lista=lista, books=all_names)
	#will let you see all of the lists of books that you currently have in the database and let 
@app.route('/delete/<lst>',methods=["GET","POST"])
def delete(lst):
    form=DeleteButtonForm()
    if form.validate_on_submit():
        list1 = PersonalBooklist.query.filter_by(name=str(lst)).first()
        db.session.delete(list1)
        db.session.commit()
        flash("list- " + lst +" -has been deleted")
        return redirect(url_for("lists")) # Replace with code
    return render_template('delete_item.html',item_name = lst, form = form)
	#this view function will let you delete the list if you choose to do so


if __name__ == '__main__':
    db.create_all()
    manager.run()


