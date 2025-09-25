from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.models import User
from src.models.user import UserRole

user_bp = Blueprint('users', __name__, url_prefix='/admin')

@user_bp.route('/users/')
def users():
    """List all users"""
    users = User.list()
    return render_template('admin/users.html', users=users)

@user_bp.route('/users/new/', methods=['GET', 'POST'])
def new_user():
    """Create new user"""
    if request.method == 'POST':
        try:
            user = User.create(
                username=request.form['username'],
                email=request.form['email'],
                password_hash=request.form.get('password_hash'),
                role=UserRole.ADMIN if request.form.get('role') == 'admin' else UserRole.CUSTOMER
            )
            flash('User created successfully!', 'success')
            return redirect(url_for('admin.users'))
        except Exception as e:
            flash(f'Error creating user: {str(e)}', 'error')
    
    return render_template('admin/user_form.html', user=None)

@user_bp.route('/users/<int:user_id>/edit/', methods=['GET', 'POST'])
def edit_user(user_id):
    """Edit user"""
    user = User.get(id=user_id)
    if not user:
        flash('User not found!', 'error')
        return redirect(url_for('admin.users'))
    
    if request.method == 'POST':
        try:
            user.username = request.form['username']
            user.email = request.form['email']
            user.role = UserRole.ADMIN if request.form.get('role') == 'admin' else UserRole.CUSTOMER
            user.save()
            flash('User updated successfully!', 'success')
            return redirect(url_for('admin.users'))
        except Exception as e:
            flash(f'Error updating user: {str(e)}', 'error')
    
    return render_template('admin/user_form.html', user=user) 