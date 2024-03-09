from flask import Flask, render_template, redirect, url_for, request, session
import json
from datetime import timedelta
import random

app = Flask(__name__)
app.secret_key = 'thisisakey'

subject_colors = {
    "Math": "#99caff",
    "Social": "#ffc099",
    "Science": "#bbff99",
    "Language Arts": "#ff9999",
    "Other": "#e699ff",
}

COLORS = [
    ['#DF7FD7', '#f2a9ec', '#591854'],
    ['#E3CAC8', '#DF8A82', '#5E3A37'],
    ['#E6845E', '#E05118', '#61230B'],
    ['#E0B050', '#E6CB97', '#614C23'],
    ['#9878AD', '#492661', '#C59BE0'],
    ['#787BAD', '#141961', '#9B9FE0'],
    ['#78A2AD', '#104F61', '#9BD1E0'],
    ['#78AD8A', '#0A6129', '#9BE0B3'],
    ['#AD8621', '#6B5621', '#E0AD2B'],
    ['#2effbd', '#00e69d', '#12946b'],
]

def render():
    f = open('users.json')
    users = json.load(f)
    display = ""
    for user in users:
        colors = users[user]['c']
        display += f"""<div class='userrow'><div class='pfp' style='background-color: { colors[1] }; color: { colors[2] }; border: 2px solid { colors[0] };' id='loggedin'><p class='letter'>{user[0].upper()}</p></div><p class='un' style='display: inline-block; padding-left: 10px;'>{user} | {users[user]['name']} | {users[user]['t']} Account</p><a id='delete' onclick='rem(""" + '"' + user + '"' + """)' style='cursor:pointer;'>Delete</a></div><br><br>"""
    return display

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=10080) # 7 Days

@app.route('/')
def index():
    try:
        f = open('users.json')
        users = json.load(f)
        if session['username'] != None:
            return render_template('index.html', username=session['username'], colors=users[session['username']]['c'], t=users[session['username']]['t'], users=users)
    except:
        return render_template('index.html', username="Guest", colors=['#d6d6d6','#d6d6d6','#d6d6d6'])

@app.route('/profile', defaults={'user': ''})
@app.route('/profile/<user>')
def profile(user):
    if user == '':
        try:
            f = open('users.json')
            users = json.load(f)
            if session['username'] != None:
                return render_template('profile.html', username=session['username'], colors=users[session['username']]['c'], users=users, urs=True, tags=users[session['username']]['tags'], age = getage(users[session['username']]['grade']))
        except:
            return redirect(url_for('login'))
    else:
        f = open('users.json')
        users = json.load(f)
        urs = session['username'] == user
        try:
            tags=users[user]['tags']
        except:
            tags = []
        return render_template('profile.html', username=user, colors=users[user]['c'], users=users, urs=urs, tags=tags, age = getage(users[user]['grade']))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    try:
        f = open('users.json')
        users = json.load(f)
        if session['username'] != None and session['username']['u'] == 'admin' and session['username']['p'] == 'admin123':
            display = render()
            return render_template('admin.html', users=users, n=len(users))
    except:
        return redirect(url_for('login'))

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    try:
        f = open('users.json')
        users = json.load(f)
        if session['username'] != None and session['username']['u'] == 'admin' and session['username']['p'] == 'admin123':
            user = request.args.get('user')
            display = ""
            users.pop(user)
            with open('users.json', 'w') as f:
                json.dump(users, f)
            return redirect(url_for('admin'))
    except:
        return redirect(url_for('index'))

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    try:
        f = open('users.json')
        users = json.load(f)
        newusername = request.args.get('newusername')
        newname = request.args.get('newname')
        user = request.args.get('user')
        age = request.args.get('age')
        grade = getgrade(age)
        if session['username'] == user:
            c0 = request.args.get('color0')
            c1 = request.args.get('color1')
            c2 = request.args.get('color2')
            oldtype = users[user]['t']
            oldp = users[user]['p']
            users = {newusername if k == user else k:v for k,v in users.items()}
            users[newusername] = {'name': newname, 'p': oldp, 'c':  [f"#{c0}", f"#{c1}", f"#{c2}"], 't': oldtype, "tags": users[newusername]['tags'], "grade": grade}
            session['username'] = newusername
            with open('users.json', 'w') as f:
                json.dump(users, f)
            return redirect(url_for('profile'))
        elif session['username'] != None and session['username']['u'] == 'admin' and session['username']['p'] == 'admin123':
            newtype = request.args.get('newtype')
            oldc = users[user]['c']
            oldp = users[user]['p']
            users = {newusername if k == user else k:v for k,v in users.items()}
            users[newusername] = {'name': newname, 'p': oldp, 'c': oldc, 't': newtype, "tags": users[newusername]['tags'], "grade": grade}
            with open('users.json', 'w') as f:
                json.dump(users, f)
            return redirect(url_for('admin'))
    except:
        return redirect(url_for('index'))

@app.route('/add', methods=['GET', 'POST'])
def add():
    try:
        f = open('users.json')
        users = json.load(f)
        if session['username'] != None and session['username']['u'] == 'admin' and session['username']['p'] == 'admin123':
            users[f"Test{len(users)+1}"] = {'name': f"Test Account{len(users)+1}", 'p': len(users), 'c': random.choice(COLORS), 't': 'Student'}
            with open('users.json', 'w') as f:
                json.dump(users, f)
            return redirect(url_for('admin'))
    except:
        return redirect(url_for('index'))

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    try:
        f = open('users.json')
        users = json.load(f)
        f = open('default.json')
        default = json.load(f)
        if session['username']['u'] == 'admin' and session['username']['p'] == 'admin123':
            users = default
            with open('users.json', 'w') as f:
                json.dump(users, f)
            return redirect(url_for('admin'))
    except:
        return redirect(url_for('index'))

@app.route('/delete-all', methods=['GET', 'POST'])
def deleteall():
    try:
        f = open('users.json')
        users = json.load(f)
        if session['username'] != None and session['username']['u'] == 'admin' and session['username']['p'] == 'admin123':
            users = {}
            with open('users.json', 'w') as f:
                json.dump(users, f)
            return redirect(url_for('admin'))
    except:
        return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        f = open('users.json')
        users = json.load(f)
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin123':
            session['username'] = {'u': username, 'p': password}
            return redirect(url_for('admin'))
        elif username in users and password == users[username]['p']:
            session['username'] = username
            return redirect(url_for('index'))
        error = "Invalid Credentials. Please try again."
    return render_template('login.html', error=error)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        f = open('users.json')
        users = json.load(f)
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        type = request.form.get('type')
        tags = request.form.getlist('tags[]')
        grade = request.form['grade']
        if username in users or username.lower() == 'admin':
            error = "This username is taken, please try another."
        elif password == '' or username == '' or name == '':
            error = "Empty field(s)."
        else:
            color = random.choice(COLORS)
            users[username] = {'name': name, 'p': password, 'c': color, 't': type, 'tags': [[i, subject_colors[i]] for i in tags], "grade": grade}
            with open('users.json', 'w') as f:
                json.dump(users, f)
            session['username'] = username
            return redirect(url_for('index'))
    return render_template('signup.html', error=error)

@app.route('/signout')
def signout():
    session.pop('username', default=None)
    return redirect(url_for('index'))

def getage(grade):
  grade = int(grade)
  if grade <= 12:
    age = grade + 5
  else:
    age = grade
  return age

def getgrade(age):
  age = int(age)
  if age <= 17:
    grade = age - 5
  else:
    grade = age
  return grade

@app.route('/matching')
def matching():
    try:
        if session['username'] != None:
            f = open('users.json')
            users = json.load(f)

            prelist = []
            currentstudent = session['username']

            for user in users:
                if users[user]['t'] == 'Tutor':
                    prelist.append(user)
            gradeofcur = getage(users[currentstudent]['grade'])
            matching_tutors = []

            for tutor in prelist:
                if getage(users[tutor]['grade']) < gradeofcur:
                    pass
                else:
                    tutor_fulfill = True
                    for subj in users[currentstudent]['tags']:
                        if subj[0] not in [tag[0] for tag in users[tutor]['tags']]:
                            tutor_fulfill = False
                            break
                    if tutor_fulfill:
                        matching_tutors.append(tutor)
            matches = {i: users[i] for i in matching_tutors}
            return render_template('matching.html', matches=matches, yourtags = users[currentstudent]['tags'])
    except:
        return redirect(url_for('login'))

app.jinja_env.cache = {}
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.run(debug=True, host='0.0.0.0')