from flask import Flask, render_template, request
import pyodbc # Installed by pip
import os


## Form request; here we will use the functions for CRUD,
## and display the result on our website/index page.
app = Flask(__name__)

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])

def showindexpage() : # Function to show index page.

    global conn, cursor
    conn = pyodbc.connect(Trusted_Connection = 'yes', driver = '{SQL Server}', server = 'DESKTOP-VKU3EK5', database = 'CarDB') # Connection to DB.
    cursor = conn.cursor() # Creates a list/table for our data with DB connection.

    if request.method == 'POST' :
        if request.form['myaction'] == "Create car" :
            addcar()
        elif request.form['myaction'] == "Update car" :
            updatecar()
        else :
            deletecar()

    ## Shows a list of all the cars.
    cursor.execute("SELECT * FROM Car") # SQL statement; saves data to our list from DB.
    allcars = cursor.fetchall() # Fetch all the rows one at a time.

    ## Show the cars with the fastest speed. 
    cursor.execute("SELECT * FROM Car ORDER BY MaxSpeed DESC") # SQL statement; saves data to our list from DB.
    fastestcar = cursor.fetchone() # Fetch only one row.

    conn.close() # Close connection.
    return render_template('index.html', carlist = allcars, carspeed = fastestcar)



#####################

## Create car function.
def addcar() : # Addcar function.

    try :
        # Defines variables that will hold data for a car.
        carmodel = request.form['model']
        carmaxspeed = request.form['speed']

        cursor.execute("INSERT INTO Car VALUES (?, ?)", carmodel, carmaxspeed) # ?; is a substitude for our defined variables. 
        conn.commit() # Remember to commit all changes else the data won't be saved. 
    except Exception as ex :
        print("There was an error : ", ex)
    
#####################

## Update car function.
def updatecar() : # Updatecar function.

    try :
        # Defines variables that will hold data for a car.
        carid = request.form['id']
        carmodel = request.form['model']
        carmaxspeed = request.form['speed']

        cursor.execute("UPDATE Car SET Model = ?, MaxSpeed = ? WHERE CarID = ?", carmodel, carmaxspeed, carid) # Remember the WHERE.
        conn.commit() # Remember to commit all changes else the data won't be saved. 
    except Exception as ex :
        print("There was an error : ", ex)

#####################

## Delete car function.
def deletecar() : # Deletecar function.

    try :
        # Defines a variable to store the ID for a specific car.
        carid = request.form['id']

        cursor.execute("DELETE FROM Car WHERE CarID = ?", carid) # Remember the WHERE; else it deletes all the Cars.
        conn.commit() # Remember to commit all changes else the data won't be saved. 
    except Exception as ex :
        print("There was an error : ", ex)

#####################


## Run the application server on localhost: 4449; set it on properties - debug - portnumber.
if __name__ == '__main__' : # If we are a stand alone program, then run this application.
    app.run('localhost', 4449)
