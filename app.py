from config import app, render_template, db
from classes import *

with app.app_context():
    db.create_all()
@app.route('/')
def index():  # put application's code here
    return render_template('index.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)