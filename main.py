from flask import Flask, render_template, request
import requests
import smtplib

app = Flask(__name__)

posts = requests.get("https://api.npoint.io/acff52dcf8c2092e3bbd").json()

# GMAIL settings
MY_EMAIL = YOUR_EMAIL
MY_PASSWORDS = YOUR_PASSWORDS


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post['id'] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        data = request.form
        send_email(data['name'], data['email'], data['phone'], data['message'])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


def send_email(name, email, phone, message):
    email_message = f"Subject: New message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}".encode("utf-8")
    print(email_message)
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORDS)
        connection.sendmail(MY_EMAIL, email, msg=email_message)


if __name__ == "__main__":
    app.run(debug=True)
