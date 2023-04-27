import prefix
import sqlite3

from flask import Flask, url_for, render_template, redirect, request, session, g

DATABASE='/SQL/controller_db.db'

# Create app to use in Flask application
app = Flask(__name__)
# Secret key for session object
app.secret_key = 'Hooli-Strike-Team'

################################################################################
## Global flag that simulates a logged in state for testing the modal window
## for the home page.
##
##   1. Set logged_in to either True or False
##   2. Navigate to home page:
##     a. When logged_in is set to True, the modal window is displayed
##     b. When logged_in is set to False, no modal window is displayed
##
## Note: to ensure that the correct page content is displayed, re-run
##       test_app.py whenever the value of logged_in is changed
##
logged_in = True


# Insert wrapper for handling PROXY when using csel.io virtual machine
prefix.use_PrefixMiddleware(app)   

# Test route to show prefix settings
@app.route('/prefix_url')  
def prefix_url():
    return 'The URL for this page is {}'.format(url_for('prefix_url'))

@app.route('/')
def home():
    # If login has been simulated, display modal window
    if logged_in:
        return render_template('home.html', show_logged_in_content=True)
    else:
        return render_template('home.html', show_logged_in_content=False)

    
    
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## 
#    AREA BELOW IS UNDER CONSTRUCTION - Micah
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## 
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db
    
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
    
@app.route('/create-account', methods = ['POST', 'GET'])
def create_account():
    if request.method == 'POST':
        addrec()
        # return render_template('create-account.html')
    else:
        return render_template('create-account.html')
        
        
@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            username = request.form['uname']
            password = request.form['psw']
            firstname = request.form['fname']
            lastname = request.form['lname']
            email = request.form['email'] 
            with sql.connect(DATABASE) as con: # fails here
                cur = con.cursor()
                cur.execute("""
                INSERT INTO students (name,addr,city,pin) 
                VALUES (?,?,?,?)",(nm,addr,city,pin) 
                """)
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            # msg = "error in insert operation"
            return render_template('create-account.html')
        finally:
            return render_template("login.html",msg = msg)
            con.close()


@app.route('/login')
def login():
    return render_template('login.html')

## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## 
#    AREA BELOW IS UNDER CONSTRUCTION - Micah
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## 







#testing for the Mistakes counter slider in settings 
mistakes_counter = False 


@app.route('/main')
def main():
    return render_template('main.html', mistakes_counter=mistakes_counter)

@app.route('/difficulty')
def show_difficulty():
    return render_template('difficulty.html')

@app.route('/rules')
def show_rules():
    return render_template('rules.html')


risk_taker = True # if the user has met the requirements for the Risk Taker badge
lone_wolf = False # if the user has met the requirements for the Lone Wolf badge 
puzzle_master = True # if the user has met the requirements for the Puzzle Master badge
speed_runner = False # if the user has met the requirements for the Speed Runner badge
inquisitor = True # if the user has met the requirements for the Inquisitor badge
conqueror = False # if the user has met the requirements for the Conqueror badge 

@app.route('/achievements')
def show_achievements():
    return render_template('achievements.html', risk_taker=risk_taker, lone_wolf=lone_wolf, puzzle_master=puzzle_master,
                            speed_runner=speed_runner, inquisitor=inquisitor, conqueror=conqueror)


@app.route('/settings')
def show_settings():
    return render_template('settings.html')
  
@app.route('/tutorial')
def show_tutorial():
    return render_template('tutorial.html')

################################################################################

if __name__ == '__main__':
  # app.run(host='0.0.0.0', port=3308)
    app.run(host='localhost', port=3308)