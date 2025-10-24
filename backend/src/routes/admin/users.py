from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.models import User
from src.models.user import UserRole
from src.routes.admin_auth import admin_required

blueprint = Blueprint('users', __name__, url_prefix='/admin')

@blueprint.route('/users/')
@admin_required
def users():
    """List all users"""
    users = User.list()
    return render_template('admin/users/users.html', users=users)

@blueprint.route('/users/new/', methods=['GET', 'POST'])
@admin_required
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
            return redirect(url_for('admin_users.users'))
        except Exception as e:
            flash(f'Error creating user: {str(e)}', 'error')
    
    return render_template('admin/users/user_form.html', user=None)

@blueprint.route('/users/<int:user_id>/edit/', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    """Edit user"""
    user = User.get(id=user_id)
    if not user:
        flash('User not found!', 'error')
        return redirect(url_for('admin_users.users'))
    
    if request.method == 'POST':
        try:
            user.username = request.form['username']
            user.email = request.form['email']
            user.role = UserRole.ADMIN if request.form.get('role') == 'admin' else UserRole.CUSTOMER
            user.save()
            flash('User updated successfully!', 'success')
            return redirect(url_for('admin_users.users'))
        except Exception as e:
            flash(f'Error updating user: {str(e)}', 'error')
    
    return render_template('admin/users/user_form.html', user=user)
