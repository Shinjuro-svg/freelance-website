from django.shortcuts import render,redirect
from django.contrib import messages
import mysql.connector as sql
from django.db import IntegrityError
from django.shortcuts import render
from django.contrib import messages
import mysql.connector as sql
from django.db import IntegrityError

email = None
password = None
pk = None
username = None

def signup(request):
    if request.method == "POST":
        try:
            m = sql.connect(host="localhost", user="root", passwd="password123A$", database='freelance_table')
            cursor = m.cursor()

            fname = request.POST.get("fname", "")
            lname = request.POST.get("lname", "")
            gender = request.POST.get("gender", "")
            email = request.POST.get("email", "")
            password = request.POST.get("password", "")
            user_type = request.POST.get("userType", "")

            c = "INSERT INTO users1 (firstname, lastname, gender, email, password, user_type) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(c, (fname, lname, gender, email, password, user_type))
            m.commit()
            messages.success(request, 'You are registered successfully!')

        except Exception as e:
            messages.error(request, str(e))
            return render(request, 'SignUp.html', {"message":str(e)})

    return render(request, 'SignUp.html', {'messages': messages.get_messages(request)})

# creating for login page 
from django.db import IntegrityError

def login(request):
    global email, password, pk, user_id, username
    
    if request.method == 'POST':
        email = request.POST.get('username', '')
        password = request.POST.get('password', '')

        m = sql.connect(host="localhost", user="root", passwd="password123A$", database='freelance_table')
        cursor = m.cursor()

        query = "SELECT * FROM users1 WHERE email = %s AND password = %s"
        cursor.execute(query, (email, password))
        user = cursor.fetchone()

        if user:
            user_id = user[0]
            username = user[1]
            password = user[2]
            pk = user[0]
            u_type = user[6]

            if u_type == "freelancer":
                 return redirect("/Freelancer_Dashboard/")
            else:
                return redirect("/Client_Dashboard/")
        else:
            return render(request, 'Login.html', {'error_message': 'Invalid credentials'})

        

    return render(request, 'Login.html')


# creating views of freelance dashbaord
def freelance_dashbaord(request):
    global pk, username
    welcome_message = f"Welcome, {username}!"

    query = f"""
   
select * from clientjob,job_applied1
where clientjob.id = job_applied1.job_id and job_applied1.freelancer_id = {pk} AND clientjob.jobstatus = 1;

    """
    m = mysql.connector.connect(host="localhost", user="root", passwd="password123A$", database='freelance_table')
    cursor = m.cursor()
    cursor.execute(query)
    user_data = cursor.fetchall()
    print(user_data)
    return render(request, 'Freelancer_Dashboard.html',{"welcome_message": welcome_message,"job_data":user_data })

# Import the MySQL connector
import mysql.connector
from django.shortcuts import render

# Creating views for the Client dashboard
import mysql.connector
from django.shortcuts import render

def Client_dashboard(request):
    global jobtitle, jobd, jobr, budget, sdate, edate, userid,username
    
    if request.method == 'GET':
        print("hello")
        # Assuming you have a session variable named 'user_id' that holds the user's ID
        user_id = request.session.get('user_id')

        m = mysql.connector.connect(host="localhost", user="root", passwd="password123A$", database='freelance_table')
        cursor = m.cursor()
        
        query =  f" SELECT *  FROM clientjob  INNER JOIN users1 ON clientjob.userid = users1.userid  WHERE clientjob.userid = {pk} AND clientjob.jobstatus = 1;"
        cursor.execute(query)
        user_data = cursor.fetchall()
        print(user_data)
        
        if user_data:
            # jobtitle = user_data[0][1]
            # jobd = user_data[0][2]
            # jobr = user_data[0][3]
            # budget = user_data[0][4]
            # sdate = user_data[0][5]
            # edate = user_data[0][7]
            # userid = user_data[1][8]

            # Pass the retrieved data to the template context
            # context = {
            #     'jobtitle': jobtitle,
            #     'jobd': jobd,
            #     'jobr': jobr,
            #     'budget': budget,
            #     'sdate': sdate,
            #     'edate': edate,
            #     'userid': userid,
            # }
            projects = []
            for row in user_data:
                project = {
                'userid': row[0],
                'jobtitle': row[1],
                'jobd': row[2],
                'budget': row[4],
            }
                projects.append(project)
            total =len(projects)
            welcome_message = f"Welcome, {username}!"
            print(welcome_message,"welcome_ms")

            context = {'projects': projects,"welcome_message": welcome_message,"totals":total}
            
            
            
            
            
            return render(request, 'Client_Dashboard.html',context)

    # Return a response for the GET request when the form is not submitted
    welcome_message = f"Welcome, {username}!"
    print(welcome_message,"welcome_ms")
    return render(request, 'Client_Dashboard.html',{"welcome_message": welcome_message})



#creating viwes for home page 
def home_page(request):
    return render(request, 'Home.html')



def post_job(request):
    global email, password, pk

    if email is not None and password is not None and request.method == 'GET':
        return render(request, "Post_Job.html")

    if request.method == 'POST':
        # Retrieve form data
        job_title = request.POST.get("jobTitle", "")
        job_description = request.POST.get("jobDescription", "")
        job_requirements = request.POST.get("jobRequirements", "")
        budget = request.POST.get("budget", "")
        start_date = request.POST.get("startDate", "")
        end_date = request.POST.get("endDate", "")
        
        connection = sql.connect(host="localhost", user="root", passwd="password123A$", database='freelance_table')
        cursor = connection.cursor()

        # Insert data into the MySQL table
        query = "INSERT INTO clientjob (job_title, job_description, job_requirements, budget, start_date, end_date, userid,jobstatus) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"  # Replace 'some_column_name' with the actual column name

        # Assuming '1' is the value you want to insert into the 'some_column_name'
        cursor.execute(query, (job_title, job_description, job_requirements, budget, start_date, end_date, pk, 1))

        # Commit changes and close connection
        connection.commit()

        messages.success(request, 'Job posted successfully!')
        return render(request, 'Post_Job.html', {'messages': messages.get_messages(request)})

    # Return a response for the GET request
    return render(request, 'Post_Job.html')

def clientjob(request):
    # sql ->  datas = cursor.fetchall()
    global pk
    connection = sql.connect(host="localhost", user="root", passwd="password123A$", database='freelance_table')
    cursor = connection.cursor()
    if request.method == 'POST': 
        job_id_to_mark_as_complete = request.POST.get('job_id')
        print("jjobb",job_id_to_mark_as_complete)
        mark_as_complete_query = f"UPDATE clientjob SET jobstatus = 0 WHERE id = {job_id_to_mark_as_complete};"
        cursor.execute(mark_as_complete_query)
        connection.commit()
        
        return redirect('/clientjob')
    
    query =  f" SELECT *  FROM clientjob  INNER JOIN users1 ON clientjob.userid = users1.userid  WHERE clientjob.userid = {pk} AND clientjob.jobstatus = 1;"
    cursor.execute(query)
    datas = cursor.fetchall()
    print(datas)
    return render(request, 'clientjob.html',{'datas':datas})    


def find_work(request):
    # sql ->  datas = cursor.fetchall()
    global pk
    connection = sql.connect(host="localhost", user="root", passwd="password123A$", database='freelance_table')
    cursor = connection.cursor()
    if request.method == 'POST': 
        job_id = request.POST.get('job_id')
        print("jjobb",job_id)
        query = f"""
        INSERT INTO job_applied1 (job_id, freelancer_id)
        VALUES ({job_id}, {pk});
        """
        cursor.execute(query)
        connection.commit()
        
        return redirect('/find_work')
    
    query =  f" SELECT *  FROM clientjob  INNER JOIN users1 ON clientjob.userid = users1.userid  WHERE clientjob.jobstatus = 1;"
    cursor.execute(query)
    datas = cursor.fetchall()
    print(datas)
    return render(request, 'find_work.html',{'datas':datas})    



    

def freelancer_Edit(request):
    global pk
    if request.method == 'POST':
        print(pk,"okkk")
        # user_id = request.user.id  # Assuming you have a user ID associated with the request
        # print(user_id)

        # Get the current connection's cursor
        connection = sql.connect(host="localhost", user="root", passwd="password123A$", database='freelance_table')
        cursor = connection.cursor()
        # Define the update query
        update_query = """
        UPDATE users1
        SET firstname = %s, email = %s, password = %s
        WHERE userid = %s
        """
        print(request.POST.get('username'),
            request.POST.get('email'),
            request.POST.get('password'))
        # Execute the update query with the provided parameters
        cursor.execute(update_query, (
            request.POST.get('username'),
            request.POST.get('email'),
            request.POST.get('password'),
            pk,
        ))
        connection.commit()
        print("here")
        messages.success(request, 'Your account information has been updated successfully!')
        return redirect('/Client_Edit')  # Use the correct name 'client_edit'

    return render(request, 'Freelancer_edit.html')










def Client_Edit(request):
    global pk
    if request.method == 'POST':
        print(pk,"okkk")
        # user_id = request.user.id  # Assuming you have a user ID associated with the request
        # print(user_id)

        # Get the current connection's cursor
        connection = sql.connect(host="localhost", user="root", passwd="password123A$", database='freelance_table')
        cursor = connection.cursor()
        # Define the update query
        update_query = """
        UPDATE users1
        SET firstname = %s, email = %s, password = %s
        WHERE userid = %s
        """
        print(request.POST.get('username'),
            request.POST.get('email'),
            request.POST.get('password'))
        # Execute the update query with the provided parameters
        cursor.execute(update_query, (
            request.POST.get('username'),
            request.POST.get('email'),
            request.POST.get('password'),
            pk,
        ))
        connection.commit()
        print("here")
        messages.success(request, 'Your account information has been updated successfully!')
        return redirect('/Client_Edit')  # Use the correct name 'client_edit'

    return render(request, 'Client_Edit.html')


def post_review(request):
    
    return render(request, 'Post_Review.html')

def job_history(request):
    # sql ->  datas = cursor.fetchall()
    global pk
    print(pk)
    connection = sql.connect(host="localhost", user="root", passwd="password123A$", database='freelance_table')
    cursor = connection.cursor()
   
    query =  f" SELECT *  FROM clientjob  INNER JOIN users1 ON clientjob.userid = users1.userid  WHERE clientjob.userid = {pk};"
    cursor.execute(query)
    datas = cursor.fetchall()
    print(datas)
    return render(request, 'job_history.html',{'datas':datas})    

def freelance_history(request):
    global pk, username
    welcome_message = f"Welcome, {username}!"

    query = f"""
   
select * from clientjob,job_applied1
where clientjob.id = job_applied1.job_id and job_applied1.freelancer_id = {pk};

    """
    m = mysql.connector.connect(host="localhost", user="root", passwd="password123A$", database='freelance_table')
    cursor = m.cursor()
    cursor.execute(query)
    user_data = cursor.fetchall()
    print(user_data)
    return render(request, 'freelancer_history.html',{"welcome_message": welcome_message,"job_data":user_data })

    
def freelancer_edit(request):
    
    return render(request, 'Post_Review.html')
