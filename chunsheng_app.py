from flask import Flask

from serv import content,get_set_anything

app = Flask(__name__)
app.register_blueprint(content.content)
app.register_blueprint(get_set_anything.gsa)

if __name__ == '__main__':
    app.run("0.0.0.0", 9527, debug=True)
