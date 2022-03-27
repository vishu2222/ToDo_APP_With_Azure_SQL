from flask import Flask, render_template, request, redirect
import pyodbc, keys


app = Flask(__name__, template_folder='templates')
server = keys.server
database = keys.database
username = keys.username 
password = keys.password

# Routes
@app.route("/", methods=["GET", "POST"])
def home():
    cnxn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    if request.method == "POST":
        item = request.form['Taskcontent']
        sql_command = 'INSERT INTO todo (content) values (' + "'" + item + "'" + ')'
        try:
            cursor.execute(sql_command)
            cnxn.commit()
            cnxn.close()
            return redirect("/") 
        except:
            return "<p>There was an error adding the task</p>"
    else:
        sql_command = 'select * from todo'
        cursor.execute(sql_command)
        result = cursor.fetchall()
        cnxn.close()
        return render_template("index.html", tasks = result)

# delete
@app.route("/delete/<int:id>")
def delete(id):
    cnxn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    sql_command = "DELETE FROM todo WHERE todo.id = '" + str(id) + "'" 
    cursor.execute(sql_command)
    cnxn.commit()
    cnxn.close()
    return redirect("/") 


# Update
@app.route("/update/<int:id>", methods = ["GET","POST"])
def update(id):
    if request.method == "POST":
        item = request.form['content']
        print(item)
        try:
            cnxn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
            cursor = cnxn.cursor()
            sql_command = "UPDATE todo SET todo.content = '" + item + "' WHERE todo.id = '" + str(id) + "'" 
            cursor.execute(sql_command)
            cnxn.commit()
            cnxn.close()
            return redirect("/")
        except: return "<p> Unable to update </p>"
    else:
        cnxn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = cnxn.cursor()
        sql_command = "SELECT * FROM todo WHERE todo.id = '" + str(id) + "'" 
        # sql_command = "SELECT * FROM todo WHERE todo.id = {}".format(id) 
        cursor.execute(sql_command)
        result = cursor.fetchall()
        return render_template("update.html", tasks= result[0])

if __name__ == "__main__":
    app.run(debug=True)