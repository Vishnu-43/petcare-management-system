from extensions import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        default="user"
    )


class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    species = db.Column(
        db.String(20),
        nullable=False
    )

    breed = db.Column(
        db.String(100),
        nullable=True
    )

    gender = db.Column(
        db.String(20),
        nullable=True
    )

    date_of_birth = db.Column(
        db.String(20),
        nullable=True
    )

    weight = db.Column(
        db.Float,
        nullable=True
    )

    image = db.Column(
        db.String(255),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

class Vaccination(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    pet_id = db.Column(
        db.Integer,
        db.ForeignKey("pet.id"),
        nullable=False
    )

    vaccine_name = db.Column(
        db.String(100),
        nullable=False
    )

    vaccination_date = db.Column(
        db.String(20),
        nullable=False
    )

    next_due_date = db.Column(
        db.String(20),
        nullable=True
    )

    notes = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )
class MedicalRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    pet_id = db.Column(
        db.Integer,
        db.ForeignKey("pet.id"),
        nullable=False
    )

    visit_date = db.Column(
        db.String(20),
        nullable=False
    )

    diagnosis = db.Column(
        db.String(255),
        nullable=False
    )

    treatment = db.Column(
        db.Text,
        nullable=True
    )

    veterinarian = db.Column(
        db.String(100),
        nullable=True
    )

    notes = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    pet_id = db.Column(
        db.Integer,
        db.ForeignKey("pet.id"),
        nullable=False
    )

    appointment_date = db.Column(
        db.String(20),
        nullable=False
    )

    appointment_time = db.Column(
        db.String(20),
        nullable=False
    )

    appointment_type = db.Column(
        db.String(100),
        nullable=False
    )

    veterinarian = db.Column(
        db.String(100),
        nullable=True
    )

    notes = db.Column(
        db.Text,
        nullable=True
    )

    status = db.Column(
        db.String(20),
        default="Scheduled"
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )
class GroomingCenter(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(150),
        nullable=False
    )

    owner_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=True
    )

    owner_photo = db.Column(
        db.String(255),
        nullable=True
    )

    center_image = db.Column(
        db.String(255),
        nullable=True
    )

    address = db.Column(
        db.String(255),
        nullable=False
    )

    latitude = db.Column(
        db.Float,
        nullable=True
    )

    longitude = db.Column(
        db.Float,
        nullable=True
    )

    phone = db.Column(
        db.String(20),
        nullable=True
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    opening_hours = db.Column(
        db.String(255),
        nullable=True
    )

    verification_document = db.Column(
        db.String(255),
        nullable=True
    )

    verification_status = db.Column(
        db.String(20),
        default="Pending"
    )

    rejection_reason = db.Column(
        db.Text,
        nullable=True
    )

    rating = db.Column(
        db.Float,
        default=0.0
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

class VeterinarianProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False,
        unique=True
    )

    profile_photo = db.Column(
        db.String(255),
        nullable=True
    )

    qualification = db.Column(
        db.String(150),
        nullable=True
    )

    registration_number = db.Column(
        db.String(100),
        nullable=True
    )

    specialization = db.Column(
        db.String(100),
        nullable=True
    )

    experience_years = db.Column(
        db.Integer,
        nullable=True
    )

    clinic_name = db.Column(
        db.String(150),
        nullable=True
    )

    clinic_address = db.Column(
        db.String(255),
        nullable=True
    )

    phone = db.Column(
        db.String(20),
        nullable=True
    )

    verification_document = db.Column(
        db.String(255),
        nullable=True
    )

    verification_status = db.Column(
        db.String(20),
        default="Pending"
    )

    rejection_reason = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

class GroomingService(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    center_id = db.Column(
        db.Integer,
        db.ForeignKey("grooming_center.id"),
        nullable=False
    )

    service_name = db.Column(
        db.String(100),
        nullable=False
    )

    price = db.Column(
        db.Float,
        nullable=True
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )