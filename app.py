from flask import Flask
from flask import render_template
app = Flask(__name__)


@app.route('/')
def base():
    return render_template('capture.html')


@app.route('/capture')
def capture():
    return render_template('capture.html')

if __name__ == '__main__':
    app.run(debug=True)
