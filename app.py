from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")


@app.route("/")
def home():

    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM projects ORDER BY id DESC")

    projects = cursor.fetchall()

    connection.close()

    return render_template("index.html", projects=projects)


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # Temporary login details
        if username == os.environ.get("ADMIN_USERNAME") and password == os.environ.get("ADMIN_PASSWORD"):
            session["admin_logged_in"] = True

            return redirect(url_for("admin_dashboard"))

        return """
        <h3>Invalid username or password</h3>
        <a href="/admin/login">Try Again</a>
        """

    return render_template("admin_login.html")


@app.route("/admin/dashboard")
def admin_dashboard():

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    return render_template("admin_dashboard.html")

@app.route("/admin/projects/add", methods=["GET", "POST"])
def add_project():

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]
        technologies = request.form["technologies"]
        github_link = request.form["github_link"]

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO projects
        (title, description, technologies, github_link)
        VALUES (?, ?, ?, ?)
        """, (title, description, technologies, github_link))

        connection.commit()
        connection.close()

        return redirect(url_for("admin_dashboard"))

    return render_template("add_project.html")

@app.route("/admin/logout")
def admin_logout():

    session.clear()

    return redirect(url_for("admin_login"))


if __name__ == "__main__":
    app.run(debug=True)