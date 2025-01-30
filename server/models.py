from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum
import re

db = SQLAlchemy()

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)  # Store hashed password
    
    # Many-to-many relationship with skills through SkillUser table
    user_skills = db.relationship('SkillUser', back_populates='user', cascade="all, delete-orphan")

    # Relationships with Swap model (User can swap skills with other users)
    swaps_as_user1 = db.relationship('Swap', foreign_keys='Swap.user1_id', back_populates='user1', lazy=True)
    swaps_as_user2 = db.relationship('Swap', foreign_keys='Swap.user2_id', back_populates='user2', lazy=True)

    # Set password (hashing before storing)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Verify password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Validate email format
    def validate_email(self):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            raise ValueError("Invalid email format")

    # Validate username length
    def validate_username(self):
        if len(self.username) < 3:
            raise ValueError("Username must be at least 3 characters long")

    def __repr__(self):
        return f"<User {self.username} - {self.email}>"

# Skill model
class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))

    # Many-to-many relationship with users through SkillUser table
    skill_users = db.relationship('SkillUser', back_populates='skill', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Skill {self.skill_name}>"

# SkillUser (Association Table) for Many-to-Many Relationship between User and Skill
class SkillUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    proficiency = db.Column(db.Integer)  # user-submittable attribute, e.g., rating
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationship references
    user = db.relationship('User', back_populates='user_skills')
    skill = db.relationship('Skill', back_populates='skill_users')

    def __repr__(self):
        return f"<SkillUser user {self.user_id} - skill {self.skill_id}, proficiency {self.proficiency}>"

# Swap Status Enum for better control over swap status
class SwapStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELED = "canceled"
    # Add other statuses as needed

# Swap model (One-to-Many Relationship: A Swap involves two users)
class Swap(db.Model):
    __tablename__ = 'swap'

    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.Enum(SwapStatus), nullable=False, default=SwapStatus.PENDING)

    # Relationship between Swap and Users
    user1 = db.relationship('User', foreign_keys=[user1_id], back_populates='swaps_as_user1')
    user2 = db.relationship('User', foreign_keys=[user2_id], back_populates='swaps_as_user2')

    def __repr__(self):
        return f"<Swap {self.id} between user {self.user1_id} and user {self.user2_id}, status {self.status}>"
