
from flask import (
    Flask, render_template, redirect,
    url_for, flash, request, session
)

from config import Config
from services.auth_service import AuthService
from services.appointment_service import AppointmentService
from repositories.service_repository import ServiceRepository
from datetime import datetime


app = Flask(__name__)
app.config.from_object(Config)

auth_service = AuthService()
appointment_service = AppointmentService()
service_repository = ServiceRepository()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/test")
def test():
    return "Flask is working and ready for the Appointment Scheduling System!"


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if password != confirm_password:
            flash("Passwords do not match.")
            return redirect(url_for("register"))

        try:
            auth_service.register(
                full_name,
                email,
                phone,
                password
            )

            flash("Registration successful! You can now log in.")
            return redirect(url_for("login"))

        except ValueError as error:
            flash(str(error))
            return redirect(url_for("register"))

        except Exception as error:
            print("Registration error:", error)
            flash("Something went wrong. Please try again.")
            return redirect(url_for("register"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        try:
            result = auth_service.login(email, password)

            session["user_id"] = result["user_id"]
            session["full_name"] = result["user"].full_name
            session["role"] = result["user"].role
            session["dashboard_message"] = result["dashboard_message"]

            if session["role"] == "admin":
                return redirect(url_for("admin_dashboard"))

            return redirect(url_for("customer_dashboard"))

        except Exception as error:
            print("Login error:", error)
            flash("Invalid email or password.")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/customer/dashboard")
def customer_dashboard():
    if "user_id" not in session or session.get("role") != "customer":
        flash("Please log in as a customer.")
        return redirect(url_for("login"))

    return render_template("customer_dashboard.html")


@app.route("/admin/dashboard")
def admin_dashboard():
    if "user_id" not in session or session.get("role") != "admin":
        flash("Please log in as an administrator.")
        return redirect(url_for("login"))

    keyword = request.args.get("search", "").strip()

    if keyword:
        appointments = appointment_service.search_appointments(keyword)
    else:
        appointments = appointment_service.get_all_appointments()

    return render_template(
        "admin_dashboard.html",
        appointments=appointments,
        search=keyword
    )


@app.route("/admin/update-appointment/<int:appointment_id>", methods=["POST"])
def update_appointment(appointment_id):

    if "user_id" not in session or session.get("role") != "admin":
        flash("Please log in as an administrator.")
        return redirect(url_for("login"))

    new_status = request.form.get("status")

    try:
        appointment_service.update_appointment_status(
            appointment_id,
            session["user_id"],
            new_status
        )

        flash(f"Appointment {new_status} successfully!")

    except Exception as error:
        print("Appointment update error:", error)
        flash(str(error))

    return redirect(url_for("admin_dashboard"))


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("login"))


@app.route("/my-appointments")
def my_appointments():

    if "user_id" not in session or session.get("role") != "customer":
        flash("Please log in as a customer.")
        return redirect(url_for("login"))

    appointments = appointment_service.get_customer_appointments(
        session["user_id"]
    )

    return render_template(
        "my_appointments.html",
        appointments=appointments
    )


@app.route("/cancel-appointment/<int:appointment_id>", methods=["POST"])
def cancel_appointment(appointment_id):

    if "user_id" not in session or session.get("role") != "customer":
        flash("Please log in as a customer.")
        return redirect(url_for("login"))

    try:
        appointment_service.cancel_customer_appointment(
            appointment_id,
            session["user_id"]
        )

        flash("Your appointment has been cancelled successfully.")

    except Exception as error:
        print("Cancellation error:", error)
        flash(str(error))

    return redirect(url_for("my_appointments"))


@app.route("/book-appointment", methods=["GET", "POST"])
def book_appointment():

    if "user_id" not in session or session.get("role") != "customer":
        flash("Please log in as a customer.")
        return redirect(url_for("login"))

    if request.method == "POST":
        try:
            service_id = int(request.form.get("service_id"))

            appointment_date = datetime.strptime(
                request.form.get("appointment_date"),
                "%Y-%m-%d"
            ).date()

            start_time = datetime.strptime(
                request.form.get("start_time"),
                "%H:%M"
            ).time()

            notes = request.form.get("notes", "").strip()

            appointment_service.create_booking(
                session["user_id"],
                service_id,
                appointment_date,
                start_time,
                notes
            )

            flash("Your appointment has been booked successfully!")
            return redirect(url_for("my_appointments"))

        except ValueError as error:
            flash(str(error))

        except Exception as error:
            print("Booking error:", error)
            flash("Unable to book your appointment. Please try again.")

    services = service_repository.get_all_services()

    return render_template(
        "book_appointment.html",
        services=services
    )


if __name__ == "__main__":
    app.run(debug=True)
