from pobuilds import app

@app.route('/list')
def list():
    return "List of Builds"
