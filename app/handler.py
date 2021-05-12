from app import app, db
from flask import Flask, render_template

@app.errorhandler(404)
def error_404(error):
    return render_template("errors/404.html"), 404

@app.errorhandler(500)
def error_505(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

@app.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403