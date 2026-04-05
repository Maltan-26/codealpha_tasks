import os
from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-change-in-production-food-ngo")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "donations.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class DonationRequest(db.Model):
    __tablename__ = "donation_requests"

    id = db.Column(db.Integer, primary_key=True)
    donor_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(40), nullable=False)
    food_type = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.String(120), nullable=False)
    pickup_address = db.Column(db.Text, nullable=False)
    preferred_date = db.Column(db.String(40), nullable=False)
    message = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class NgoInterest(db.Model):
    __tablename__ = "ngo_interest"

    id = db.Column(db.Integer, primary_key=True)
    org_name = db.Column(db.String(200), nullable=False)
    contact_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(40), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    notes = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/donate", methods=["POST"])
def donate():
    donor_name = request.form.get("donor_name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    food_type = request.form.get("food_type", "").strip()
    quantity = request.form.get("quantity", "").strip()
    pickup_address = request.form.get("pickup_address", "").strip()
    preferred_date = request.form.get("preferred_date", "").strip()
    message = request.form.get("message", "").strip()

    required = {
        "donor_name": donor_name,
        "email": email,
        "phone": phone,
        "food_type": food_type,
        "quantity": quantity,
        "pickup_address": pickup_address,
        "preferred_date": preferred_date,
    }
    if not all(required.values()):
        flash("Please fill in all required fields.", "danger")
        return redirect(url_for("index") + "#donate")

    row = DonationRequest(
        donor_name=donor_name,
        email=email,
        phone=phone,
        food_type=food_type,
        quantity=quantity,
        pickup_address=pickup_address,
        preferred_date=preferred_date,
        message=message,
    )
    db.session.add(row)
    db.session.commit()
    flash(
        "Thank you! Your donation request was received. An NGO partner will contact you soon.",
        "success",
    )
    return redirect(url_for("index") + "#donate")


@app.route("/ngo-register", methods=["POST"])
def ngo_register():
    org_name = request.form.get("org_name", "").strip()
    contact_name = request.form.get("contact_name", "").strip()
    email = request.form.get("ngo_email", "").strip()
    phone = request.form.get("ngo_phone", "").strip()
    city = request.form.get("city", "").strip()
    notes = request.form.get("ngo_notes", "").strip()

    if not all([org_name, contact_name, email, phone, city]):
        flash("Please complete all NGO registration fields.", "danger")
        return redirect(url_for("index") + "#ngos")

    row = NgoInterest(
        org_name=org_name,
        contact_name=contact_name,
        email=email,
        phone=phone,
        city=city,
        notes=notes,
    )
    db.session.add(row)
    db.session.commit()
    flash("Thanks! We will verify your organization and get in touch.", "success")
    return redirect(url_for("index") + "#ngos")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
