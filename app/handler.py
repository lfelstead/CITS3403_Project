from app import app, db
from flask import Flask, render_template

@app.errorhandler(404)
def error_404(error):
    return render_template("errors/404.html"), 404