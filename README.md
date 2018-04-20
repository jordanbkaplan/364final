Jordan Kaplan 
final project 364


I DID ALL OF THESE------------------------------------------------------------------------------------------- 
**- [ x] Create a `README.md` file for your app that includes the full list of requirements from this page. The ones you have completed should be bolded or checked off. (You bold things in Markdown by using two asterisks, like this: `**This text would be bold** and this text would not be`)

- [ x] The `README.md` file should use markdown formatting and be clear / easy to read.

- [ x] The `README.md` file should include a 1-paragraph (brief OK) description of what your application does

- [x ] The `README.md` file should include a detailed explanation of how a user can user the running application (e.g. log in and see what, be able to save what, enter what, search for what... Give us examples of data to enter if it's not obviously stated in the app UI!)

- [ x] The `README.md` file should include a list of every module that must be installed with `pip` if it's something you installed that we didn't use in a class session. If there are none, you should note that there are no additional modules to install.

- [ x] The `README.md` file should include a list of all of the routes that exist in the app and the names of the templates each one should render OR, if a route does not render a template, what it returns (e.g. `/form` -> `form.html`, like [the list we provided in the instructions for HW2](https://www.dropbox.com/s/3a83ykoz79tqn8r/Screenshot%202018-02-15%2013.27.52.png?dl=0) and like you had to on the midterm, or `/delete -> deletes a song and redirects to index page`, etc).

### **Code Requirements**
***Note that many of these requirements of things your application must DO or must INCLUDE go together! Note also that*** ***you should read all of the requirements before making your application plan******.***

- [ x] Ensure that your `SI364final.py` file has all the setup (`app.config` values, import statements, code to run the app if that file is run, etc) necessary to run the Flask application, and the application runs correctly on `http://localhost:5000` (and the other routes you set up). **Your main file must be called** `SI364final.py`**, but of course you may include other files if you need.**

- [ x] A user should be able to load `http://localhost:5000` and see the first page they ought to see on the application.

- [ x] Include navigation in `base.html` with links (using `a href` tags) that lead to every other page in the application that a user should be able to click on. (e.g. in the lecture examples from the Feb 9 lecture, [like this](https://www.dropbox.com/s/hjcls4cfdkqwy84/Screenshot%202018-02-15%2013.26.32.png?dl=0) )

- [ x] Ensure that all templates in the application inherit (using template inheritance, with `extends`) from `base.html` and include at least one additional `block`.

- [ x] Must use user authentication (which should be based on the code you were provided to do this e.g. in HW4).

- [ x] Must have data associated with a user and at least 2 routes besides `logout` that can only be seen by logged-in users.

lists and list/<list_id>

- [ x] At least 3 model classes *besides* the `User` class.

authors, lists, books

- [ x] At least one one:many relationship that works properly built between 2 models.

authors:books

- [ x] At least one many:many relationship that works properly built between 2 models.

personalbooklists: books

- [ x] Successfully save data to each table.

- [ x] Successfully query data from each of your models (so query at least one column, or all data, from every database table you have a model for) and use it to effect in the application (e.g. won't count if you make a query that has no effect on what you see, what is saved, or anything that happens in the app).

- [ x] At least one query of data using an `.all()` method and send the results of that query to a template.

all_books

- [ x] At least one query of data using a `.filter_by(...` and show the results of that query directly (e.g. by sending the results to a template) or indirectly (e.g. using the results of the query to make a request to an API or save other data to a table).

querying the author for each book by filtering by the id

- [ x] At least one helper function that is *not* a `get_or_create` function should be defined and invoked in the application.

- [ x] At least two `get_or_create` functions should be defined and invoked in the application (such that information can be saved without being duplicated / encountering errors).

- [ x] At least one error handler for a 404 error and a corresponding template.

- [ x] At least one error handler for any other error (pick one -- 500? 403?) and a corresponding template.

- [ x] Include at least 4 template `.html` files in addition to the error handling template files.

all_books, all_authors, update, delete

  - [x ] At least one Jinja template for loop and at least two Jinja template conditionals should occur amongst the templates.

  for loop in all_book, if's in all books to say 0 books in database if none, and tell the user to make a list if there are none in the db

- [ x] At least one request to a REST API that is based on data submitted in a WTForm OR data accessed in another way online (e.g. scraping with BeautifulSoup that *does* accord with other involved sites' Terms of Service, etc).

google books

  - [x ] Your application should use data from a REST API or other source such that the application processes the data in some way and saves some information that came from the source *to the database* (in some way).

 finding the author and the description

- [ x] At least one WTForm that sends data with a `GET` request to a *new* page.

creating a list

- [ x] At least one WTForm that sends data with a `POST` request to the *same* page. (NOT counting the login or registration forms provided for you in class.)

creating a book

- [ x] At least one WTForm that sends data with a `POST` request to a *new* page. (NOT counting the login or registration forms provided for you in class.)

updating a read status it sends to a new page when update is clicked on all_books

- [ x] At least two custom validators for a field in a WTForm, NOT counting the custom validators included in the log in/auth code.

in the register form (@ cannot be the first character of the username, and the password needs to be longer than 7 characters)

- [ x] Include at least one way to *update* items saved in the database in the application (like in HW5).

you can update your read status in all_books

- [ x] Include at least one way to *delete* items saved in the database in the application (also like in HW5).

you can delete your lists as a user in \lists

- [ x] Include at least one use of `redirect`.

lists

- [ x] Include at least two uses of `url_for`. (HINT: Likely you'll need to use this several times, really.)

theyre all over

- [ x] Have at least 5 view functions that are not included with the code we have provided. (But you may have more! *Make sure you include ALL view functions in the app in the documentation and navigation as instructed above.*)**
--------------------------------------------------------------------------------------------------------------
DID NOT DO THESE
## Additional Requirements for additional points -- an app with extra functionality!

**Note:** Maximum possible % is 102%.

- [ ] (100 points) Include a use of an AJAX request in your application that accesses and displays useful (for use of your application) data.
- [ ]  (100 points) Create, run, and commit at least one migration.
- [ ] (100 points) Include file upload in your application and save/use the results of the file. (We did not explicitly learn this in class, but there is information available about it both online and in the Grinberg book.)
- [ ]  (100 points) Deploy the application to the internet (Heroku) — only counts if it is up when we grade / you can show proof it is up at a URL and tell us what the URL is in the README. (Heroku deployment as we taught you is 100% free so this will not cost anything.)
- [ ]  (100 points) Implement user sign-in with OAuth (from any other service), and include that you need a *specific-service* account in the README, in the same section as the list of modules that must be installed.





Brief description:
This application is a way for people keep track of where they are in different books like a digital bookmark.  It can also hold the past books that you have read and which books you would like to read.  You can update the status of your book such as 'midway through, page 88' etc.  A user can also create lists of books to give as recommendations or keep a list of books to read next.

Different users can log in and create different lists of books that they themselves want to read next or keep lists of genres of books that they really enjoy such as 'favorite horror novels' or any other way they want to organize their books that they have read, are reading, or want to read

no extra modules to install that were not used in class


404-->404.html
500-->500.html
/login-->login.html
/logout-->index.html
/register-->register.html
/--> index.html
/all_books-->all_books.html
/update/<book>->update_item.html
/all_authors-->all_authors.html
/create_list-->create_list.html
/lists-->lists.html
/list/<list_id>-->one_list.html
/delete/(<lst>-->delete_item.html


