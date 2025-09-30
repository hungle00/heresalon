from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from src.models import User
from src.models.user import UserRole
from functools import wraps

# Create blueprint for admin auth routes
admin_auth_bp = Blueprint('admin_auth', __name__, url_prefix='/admin')

@admin_auth_bp.route('/login/', methods=['GET', 'POST'])
def login():
    """Admin login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please enter all required information!', 'error')
            return render_template('auth/login.html')
        
        # Find user by username
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            # Check admin role
            if user.role in [UserRole.ADMIN, UserRole.MANAGER]:
                session['admin_id'] = user.id
                session['admin_username'] = user.username
                flash(f'Welcome {user.username}!', 'success')
                return redirect(url_for('admin_dashboard.dashboard'))
            else:
                flash('You do not have admin access!', 'error')
        else:
            flash('Invalid username or password!', 'error')
    
    return render_template('auth/login.html')

@admin_auth_bp.route('/logout/')
def logout():
    """Admin logout"""
    session.pop('admin_id', None)
    session.pop('admin_username', None)
    flash('Successfully logged out!', 'success')
    return redirect(url_for('admin_auth.login'))

@admin_auth_bp.route('/profile/')
def profile():
    """Admin profile page"""
    if 'admin_id' not in session:
        flash('Please login first!', 'error')
        return redirect(url_for('admin_auth.login'))
    
    user = User.get(id=session['admin_id'])
    if not user:
        flash('User not found!', 'error')
        return redirect(url_for('admin_auth.login'))
    
    return render_template('auth/profile.html', user=user)

@admin_auth_bp.route('/change-password/', methods=['GET', 'POST'])
def change_password():
    """Change admin password"""
    if 'admin_id' not in session:
        flash('Please login first!', 'error')
        return redirect(url_for('admin_auth.login'))
    
    user = User.get(id=session['admin_id'])
    if not user:
        flash('User not found!', 'error')
        return redirect(url_for('admin_auth.login'))
    
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not current_password or not new_password or not confirm_password:
            flash('Please enter all required information!', 'error')
            return render_template('auth/change_password.html')
        
        if not check_password_hash(user.password_hash, current_password):
            flash('Current password is incorrect!', 'error')
            return render_template('auth/change_password.html')
        
        if new_password != confirm_password:
            flash('New password and confirmation do not match!', 'error')
            return render_template('auth/change_password.html')
        
        if len(new_password) < 6:
            flash('Password must be at least 6 characters!', 'error')
            return render_template('auth/change_password.html')
        
        try:
            from werkzeug.security import generate_password_hash
            user.password_hash = generate_password_hash(new_password)
            user.save()
            flash('Password changed successfully!', 'success')
            return redirect(url_for('admin_auth.profile'))
        except Exception as e:
            flash(f'Error changing password: {str(e)}', 'error')
    
    return render_template('auth/change_password.html')

def admin_required(f):
    """Decorator to require admin role only"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please login to access this page!', 'error')
            return redirect(url_for('admin_auth.login'))
        
        user = User.get(id=session['admin_id'])
        if not user or user.role != UserRole.ADMIN:
            flash('You do not have permission to access this page!', 'error')
            return redirect(url_for('admin_dashboard.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def manager_or_admin_required(f):
    """Decorator to require manager or admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please login to access this page!', 'error')
            return redirect(url_for('admin_auth.login'))
        
        user = User.get(id=session['admin_id'])
        if not user or user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
            flash('You do not have permission to access this page!', 'error')
            return redirect(url_for('admin_dashboard.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

