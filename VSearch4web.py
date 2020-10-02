from flask import Flask, render_template, request, redirect, escape, session, copy_current_request_context

# file imported and used as a library
#import vsearchsearch4letter
import vsearch
# create context manager
from DBCm import UseDatabase, ConnectionError, CredentialsError, SQLError

# file imported and used as a library - to check if user is logged in or not
from checker import check_logged_in

from threading import Thread

# create flask object
app = Flask(__name__)
app.secret_key = 'SetPassword'

# database connection string
app.config[
    'dbconfig'] = "Driver={SQL Server Native Client 11.0}; Server=DESKTOP-MQUOJBL;Database=vsearchlogDB;Trusted_Connection=yes;"


# insert record in database
# function is defined in the function - 1. insert record in database 2. display reocrods in the page
# threading is used to make the process faster
@app.route('/search4', methods=['POST'])
def doserach() -> 'html':
    @copy_current_request_context
    def log_request(req: 'Flask_Request', results: str) -> None:
        """Log details of the web request and the results."""

        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL_INSERT = """insert into log_table
                (phrase, letters, ip, browser_string, results)
                values
                (?, ?, ?, ?, ?)"""

            cursor.execute(_SQL_INSERT,
                           (req.form['phrase'], req.form['letter'], req.remote_addr, req.user_agent.browser,
                            results,))

    phrase = request.form['phrase']
    letter = request.form['letter']
    title = 'Here are your results:'
    results = str(vsearch.search4letter(phrase, letter))
    try:
        #log_request(request, results)
        t = Thread(target=log_request, args=(request, results))
        t.start()
    except Exception as err:
        print('*****Login failed with the error: ', str(err))
    return render_template('results.html', the_title=title, the_phrase=phrase, the_letters=letter,
                           the_results=results, )


# default page, accept word for word check
@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_title='Welcome to search4letters on the web!!')


# show stored records from database
# used exception handling
@app.route('/viewlog')
@check_logged_in
def view_the_log() -> 'html':
    contents = []
    try:
        # used context manager
        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL = """select phrase, letters, ip, browser_string, results from log_table"""
            cursor.execute(_SQL)
            contents = cursor.fetchall()

        titles = ['Phrase', 'Letters', 'IP', 'Browser Used', 'Results']
        return render_template('viewlog.html', the_title='View Log', the_row_titles=titles, the_data=contents, )
    except ConnectionError as ierr:
        print('Is your database switched on? error: ', str(ierr))
    except CredentialsError as cerr:
        print('User/id issues error: ', str(cerr))
    except SQLError as serr:
        print('Is your query correct', str(serr))
    except Exception as err:
        print('Something went wrong: ', str(err))


# login to the application: sets session value - can see logs
@app.route('/login')
def do_login() -> str:
    session['logged_in'] = True
    return 'You have logged in to the system successfully'


# logout from application: cannot see logs
@app.route('/logout')
def do_logout() -> str:
    session.pop('logged_in', None)
    return 'You have logged out from the system successfully'


# start of the code
# comment app.run() at the time of deplying site on the cloud
if __name__ == '__main__':
    app.run(debug=True)
