from flask import Flask, render_template, request
from werkzeug.routing import BaseConverter

class RegexConverter(BaseConverter):
    def __init__(self,url_map,*items):
        super(RegexConverter,self).__init__(url_map)
        self.regex = items[0]

app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter

@app.route('/')
def hello_world():
    return render_template('index.html',title='Welcome')

@app.route('/services')
def services():
    return 'Service'

@app.route('/about')
def about():
    return 'About'

@app.route('/user/<regex("[a-z]{4}"):user_id>')
def user(user_id):
    return 'User %s' % user_id

@app.route('/projects/')
@app.route('/our-works/')
def projects():
    return 'The project page'

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
    else:
        username = request.args.get('username','')
    return render_template('login.html',method=request.method)

if __name__ == '__main__':
    app.run(debug=True)