
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from datetime import datetime
from extensions import db

app = Flask(__name__)

# Flask secret key
app.config["SECRET_KEY"] = "petcare-development-secret-key"

# SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///petcare.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"


from models import (
    User,
    Pet,
    Vaccination,
    MedicalRecord,
    Appointment,
    GroomingCenter,
    GroomingService,
)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def home():
    return "PetCare Management System is running!"


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            return render_template(
                "register.html",
                error="Passwords do not match."
            )

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return render_template(
                "register.html",
                error="Email is already registered."
            )

        password_hash = generate_password_hash(password)

        new_user = User(
            name=name,
            email=email,
            password_hash=password_hash,
            role="user"
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)

            return redirect(url_for("dashboard"))

        return render_template(
            "login.html",
            error="Invalid email or password."
        )

    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():

    pets = Pet.query.filter_by(user_id=current_user.id).all()

    return render_template("dashboard.html", pets=pets)


@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("login"))


@app.route("/pets/add", methods=["GET", "POST"])
@login_required
def add_pet():

    if request.method == "POST":

        name = request.form["name"]
        species = request.form["species"]
        breed = request.form["breed"]
        gender = request.form["gender"]
        date_of_birth = request.form["date_of_birth"]
        weight = request.form["weight"]

        new_pet = Pet(
            user_id=current_user.id,
            name=name,
            species=species,
            breed=breed,
            gender=gender,
            date_of_birth=date_of_birth,
            weight=float(weight) if weight else None,
        )

        db.session.add(new_pet)
        db.session.commit()

        return redirect(url_for("dashboard"))

    return render_template("add_pet.html")


@app.route("/pets/<int:pet_id>")
@login_required
def pet_profile(pet_id):

    pet = Pet.query.filter_by(
        id=pet_id,
        user_id=current_user.id
    ).first_or_404()

    return render_template("pet_profile.html", pet=pet)


@app.route("/pets/<int:pet_id>/vaccinations", methods=["GET", "POST"])
@login_required
def vaccinations(pet_id):

    pet = Pet.query.filter_by(
        id=pet_id,
        user_id=current_user.id
    ).first_or_404()

    if request.method == "POST":

        vaccine_name = request.form["vaccine_name"]
        vaccination_date = request.form["vaccination_date"]
        next_due_date = request.form["next_due_date"]
        notes = request.form["notes"]

        new_vaccination = Vaccination(
            pet_id=pet.id,
            vaccine_name=vaccine_name,
            vaccination_date=vaccination_date,
            next_due_date=next_due_date,
            notes=notes,
        )

        db.session.add(new_vaccination)
        db.session.commit()

        return redirect(
            url_for("vaccinations", pet_id=pet.id)
        )

    vaccination_records = (
        Vaccination.query
        .filter_by(pet_id=pet.id)
        .order_by(Vaccination.vaccination_date.desc())
        .all()
    )

    return render_template(
        "vaccinations.html",
        pet=pet,
        vaccinations=vaccination_records
    )


@app.route("/pets/<int:pet_id>/medical-records", methods=["GET", "POST"])
@login_required
def medical_records(pet_id):

    pet = Pet.query.filter_by(
        id=pet_id,
        user_id=current_user.id
    ).first_or_404()

    if request.method == "POST":

        visit_date = request.form["visit_date"]
        diagnosis = request.form["diagnosis"]
        treatment = request.form["treatment"]
        veterinarian = request.form["veterinarian"]
        notes = request.form["notes"]

        new_record = MedicalRecord(
            pet_id=pet.id,
            visit_date=visit_date,
            diagnosis=diagnosis,
            treatment=treatment,
            veterinarian=veterinarian,
            notes=notes,
        )

        db.session.add(new_record)
        db.session.commit()

        return redirect(
            url_for("medical_records", pet_id=pet.id)
        )

    medical_records_list = (
        MedicalRecord.query
        .filter_by(pet_id=pet.id)
        .order_by(MedicalRecord.visit_date.desc())
        .all()
    )

    return render_template(
        "medical_records.html",
        pet=pet,
        medical_records=medical_records_list
    )


@app.route("/pets/<int:pet_id>/appointments", methods=["GET", "POST"])
@login_required
def appointments(pet_id):

    pet = Pet.query.filter_by(
        id=pet_id,
        user_id=current_user.id
    ).first_or_404()

    if request.method == "POST":

        appointment_date = request.form["appointment_date"]
        appointment_time = request.form["appointment_time"]
        appointment_type = request.form["appointment_type"]
        veterinarian = request.form["veterinarian"]
        notes = request.form["notes"]

        new_appointment = Appointment(
            pet_id=pet.id,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            appointment_type=appointment_type,
            veterinarian=veterinarian,
            notes=notes,
        )

        db.session.add(new_appointment)
        db.session.commit()

        return redirect(
            url_for("appointments", pet_id=pet.id)
        )

    # Get all appointments for this pet
    all_appointments = Appointment.query.filter_by(
        pet_id=pet.id
    ).all()

    upcoming_appointments = []
    appointment_history = []

    now = datetime.now()

    for appointment in all_appointments:

        try:
            appointment_datetime = datetime.strptime(
                f"{appointment.appointment_date} {appointment.appointment_time}",
                "%Y-%m-%d %H:%M"
            )

            if (
                appointment_datetime >= now
                and appointment.status == "Scheduled"
            ):
                upcoming_appointments.append(appointment)
            else:
                appointment_history.append(appointment)

        except ValueError:
            appointment_history.append(appointment)

    # Sort upcoming appointments from nearest to latest
    upcoming_appointments.sort(
        key=lambda a: (a.appointment_date, a.appointment_time)
    )

    # Sort history from latest to oldest
    appointment_history.sort(
        key=lambda a: (a.appointment_date, a.appointment_time),
        reverse=True
    )

    return render_template(
        "appointments.html",
        pet=pet,
        upcoming_appointments=upcoming_appointments,
        appointments=appointment_history,
    )
@app.route("/appointments/<int:appointment_id>/cancel", methods=["POST"])
@login_required
def cancel_appointment(appointment_id):

    appointment = Appointment.query.get_or_404(appointment_id)

    pet = Pet.query.filter_by(
        id=appointment.pet_id,
        user_id=current_user.id
    ).first_or_404()

    appointment.status = "Cancelled"

    db.session.commit()

    return redirect(
        url_for("appointments", pet_id=pet.id)
    )
@app.route("/appointments/<int:appointment_id>/complete", methods=["POST"])
@login_required
def complete_appointment(appointment_id):

    appointment = Appointment.query.get_or_404(appointment_id)

    pet = Pet.query.filter_by(
        id=appointment.pet_id,
        user_id=current_user.id
    ).first_or_404()

    appointment.status = "Completed"

    db.session.commit()

    return redirect(
        url_for("appointments", pet_id=pet.id)
    )


# Create database tables
with app.app_context():
    db.create_all()

@app.route("/add-sample-grooming")
def add_sample_grooming():

    center1 = GroomingCenter(
        name="Happy Paws Grooming",
        address="Perumbavoor",
        latitude=10.106,
        longitude=76.473,
        phone="9876543210",
        rating=4.6
    )

    center2 = GroomingCenter(
        name="Pet Paradise",
        address="Aluva",
        latitude=10.107,
        longitude=76.351,
        phone="9876543211",
        rating=4.4
    )

    center3 = GroomingCenter(
        name="Paw Care Centre",
        address="Kochi",
        latitude=9.931,
        longitude=76.267,
        phone="9876543212",
        rating=4.7
    )

    db.session.add_all([
        center1,
        center2,
        center3
    ])

    db.session.commit()

    services = [
        GroomingService(
            center_id=center1.id,
            service_name="Bathing",
            price=500,
            description="Basic pet bathing service"
        ),
        GroomingService(
            center_id=center1.id,
            service_name="Haircut",
            price=700,
            description="Professional pet haircut"
        ),
        GroomingService(
            center_id=center1.id,
            service_name="Nail Trimming",
            price=200,
            description="Pet nail trimming"
        ),

        GroomingService(
            center_id=center2.id,
            service_name="Bathing",
            price=600,
            description="Pet bathing and cleaning"
        ),
        GroomingService(
            center_id=center2.id,
            service_name="Full Grooming",
            price=1000,
            description="Complete grooming package"
        ),

        GroomingService(
            center_id=center3.id,
            service_name="Haircut",
            price=800,
            description="Professional haircut"
        ),
        GroomingService(
            center_id=center3.id,
            service_name="Full Grooming",
            price=1200,
            description="Complete pet grooming"
        )
    ]

    db.session.add_all(services)
    db.session.commit()

    return "Sample grooming centers and services added successfully!"

@app.route("/grooming-centers")
@login_required
def grooming_centers():

    centers = GroomingCenter.query.all()

    return render_template(
        "grooming_centers.html",
        centers=centers
    )

@app.route("/grooming-centers/<int:center_id>")
@login_required
def grooming_center_details(center_id):

    center = GroomingCenter.query.get_or_404(center_id)

    services = GroomingService.query.filter_by(
        center_id=center.id
    ).all()

    return render_template(
        "grooming_center_details.html",
        center=center,
        services=services
    )

if __name__ == "__main__":
    app.run(debug=True)
