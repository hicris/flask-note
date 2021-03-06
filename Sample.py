# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, flash, redirect, url_for, make_response, abort
from werkzeug.routing import BaseConverter
from werkzeug.utils import secure_filename
from flask_script import Manager
from os import path
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter
Bootstrap(app)
nav = Nav()

app.config.from_pyfile('config')

manager = Manager(app)

nav.register_element('top', Navbar(u'Flask入门',
                                   View(u'主页', 'index'),
                                   View(u'关于', 'about'),
                                   View(u'服务', 'services'),
                                   View(u'项目', 'projects'),
                                   ))
nav.init_app(app)


@app.route('/')
def index():
    return render_template('index.html',
                           title='Welcome')


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
def projects():
    return 'The project page'


@app.route('/login', methods=['GET', 'POST'])
def login():
    from forms import LoginForm
    form = LoginForm()
    flash(u'登录成功')
    return render_template('login.html', title=u'登录', form=form)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        basepath = path.abspath(path.dirname(__file__))
        upload_path = path.join(basepath, 'static/uploads/')
        f.save(upload_path + secure_filename(f.filename))
        return redirect(url_for('upload'))
    return render_template('upload.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.template_test('current_link')
def is_current_link(link):
    return link == request.path


# @manager.command
# def dev():
#     from livereload import Server
#     live_server = Server(app.wsgi_app)
#     live_server.watch('**/*.*')
#     live_server.serve(open_url=True)

@app.template_filter('md')
def markdown_to_html(txt):
    from markdown import markdown
    return markdown(txt)


def read_md(filename):
    with open(filename) as md_file:
        content = reduce(lambda x, y: x + y, md_file.readlines())
        return content.decode('utf-8')


@app.context_processor
def inject_methods():
    return dict(read_md=read_md)


if __name__ == '__main__':
    app.run(debug=True)
    # manager.run()
