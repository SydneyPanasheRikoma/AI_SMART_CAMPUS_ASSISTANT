"""
Database models for AI Smart Campus Assistant
Uses SQLAlchemy ORM for database interactions
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """Student/User model"""
    __tablename__ = 'users'
    
    student_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    department = db.Column(db.String(100))
    roll_number = db.Column(db.String(50), unique=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    complaints = db.relationship('Complaint', backref='student', lazy='dynamic', cascade='all, delete-orphan')
    qr_codes = db.relationship('QRCode', backref='student', lazy='dynamic', cascade='all, delete-orphan')
    notifications = db.relationship('Notification', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def get_id(self):
        """Override get_id for Flask-Login"""
        return str(self.student_id)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.name}>'


class Admin(UserMixin, db.Model):
    """Admin model"""
    __tablename__ = 'admins'
    
    admin_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='admin')
    department = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_id(self):
        """Override get_id for Flask-Login"""
        return f'admin_{self.admin_id}'
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Admin {self.name}>'


class Category(db.Model):
    """Category model"""
    __tablename__ = 'categories'
    
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), unique=True, nullable=False)
    department = db.Column(db.String(100))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Category {self.category_name}>'


class Complaint(db.Model):
    """Complaint model"""
    __tablename__ = 'complaints'
    
    ticket_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.student_id'), nullable=False, index=True)
    category = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), default='Medium')
    status = db.Column(db.String(50), default='Pending', index=True)
    ai_category = db.Column(db.String(100))
    sentiment_score = db.Column(db.Float)
    predicted_resolution_time = db.Column(db.Integer)  # in hours
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    resolved_at = db.Column(db.DateTime)
    assigned_to = db.Column(db.String(100))
    resolution_notes = db.Column(db.Text)
    
    # Relationships
    history = db.relationship('ComplaintHistory', backref='complaint', lazy='dynamic', cascade='all, delete-orphan')
    notifications = db.relationship('Notification', backref='complaint', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Complaint {self.ticket_id}>'
    
    def to_dict(self):
        """Convert complaint to dictionary"""
        return {
            'ticket_id': self.ticket_id,
            'student_id': self.student_id,
            'student_name': self.student.name if self.student else 'Unknown',
            'category': self.category,
            'description': self.description,
            'priority': self.priority,
            'status': self.status,
            'ai_category': self.ai_category,
            'sentiment_score': self.sentiment_score,
            'predicted_resolution_time': self.predicted_resolution_time,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
            'assigned_to': self.assigned_to,
            'resolution_notes': self.resolution_notes
        }


class ComplaintHistory(db.Model):
    """Complaint history/tracking model"""
    __tablename__ = 'complaint_history'
    
    history_id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('complaints.ticket_id'), nullable=False, index=True)
    status = db.Column(db.String(50), nullable=False)
    updated_by = db.Column(db.String(100))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    comments = db.Column(db.Text)
    
    def __repr__(self):
        return f'<ComplaintHistory {self.history_id}>'


class QRCode(db.Model):
    """QR Code model for quick complaint submission"""
    __tablename__ = 'qr_codes'
    
    qr_id = db.Column(db.Integer, primary_key=True)
    qr_code = db.Column(db.String(100), unique=True, nullable=False, index=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.student_id'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<QRCode {self.qr_code}>'


class Notification(db.Model):
    """Notification model"""
    __tablename__ = 'notifications'
    
    notification_id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('complaints.ticket_id'), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.student_id'), index=True)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(50))
    is_read = db.Column(db.Boolean, default=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Notification {self.notification_id}>'
