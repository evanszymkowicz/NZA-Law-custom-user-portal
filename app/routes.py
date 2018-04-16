from app import app, db #import the app module and the app variable
from flask import render_template
from app.forms import LoginForm, RegistrationForm, ProfileUpdateForm, AdminSearchForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, UserRoles, Role
from werkzeug.urls import url_parse
import datetime

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/attorneys')
def attorneys():
    return render_template('attorneys.html')

@app.route('/what')
def what():
    return render_template('what.html')

@app.route('/where')
def where():
    return render_template('where.html')

@app.route('/whoweare')
def whoweare():
    return render_template('whoweare.html')

@app.route('/portal')
@login_required
def portal():
    return render_template('portal.html')

@app.route('/admin/add_user', methods=['GET', 'POST'])
@login_required
def admin_add():
    # check if user is actually admin
    id = current_user.id
    this_user = UserRoles.query.filter_by(user_id=id).first()
    if this_user.role_id != 7:
        return redirect(url_for('profile'))
    # create forms
    form = AddNewUserForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        roles = UserRoles(user_id=User.query.filter_by(email=user.email).first().id, role_id=int(form.role.data))
        db.session.add(roles)
        db.session.commit()
        flash('New user successfully created!')
        return redirect(url_for('admin'))

    return render_template('admin_add.html', form=form)

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    # check if user is actually admin
    id = current_user.id
    this_user = UserRoles.query.filter_by(user_id=id).first()
    if this_user.role_id != 7:
        return redirect(url_for('profile'))
    #create forms
    search_form = AdminSearchForm()
    update_form = AdminUpdateForm()
    delete_form = AdminDeleteForm()
    if delete_form.submit3.data and delete_form.delete.data=='REMOVE':
        # remove user
        delete_id = delete_form.user_id_delete.data
        UserRoles.query.filter_by(user_id=delete_id).delete()
        User.query.filter_by(id=delete_id).delete()
        db.session.commit()
        flash('User successfully removed.')
        return redirect(url_for('admin'))
    if search_form.submit1.data and search_form.validate():
        if search_form.email.data:
            user = User.query.filter_by(email=search_form.email.data).first()
            if user == None:
                flash('Sorry that email is not in the system.')
                return redirect(url_for('admin'))
            user = UserRoles.query.filter_by(user_id=user.id).first()
        else:
            flash('Sorry that email is not in the system.')
            return redirect(url_for('admin'))
        return render_template('admin.html', update_form=update_form, user=user, user_roles=None, search_form=None, delete_form=delete_form)
    if update_form.submit2.data and update_form.validate():
        user_id = update_form.user_id.data
        # if user id matches email of user trying to be edited, then allow the changes to occur, otherwise, don't and let them know they weren't editing the correct person, or the email already exists.
        user_role = UserRoles.query.filter_by(user_id=user_id).first()
        if user_role.user.email != update_form.email.data:
            # run a query to see if form email has same id as user being edited
            user_exists = User.query.filter_by(email=update_form.email.data).first()
            if user_exists == None:
                user_role.user.email = update_form.email.data
                user_role.role_id = int(update_form.role.data)
                user_role.user.first_name = update_form.first_name.data
                user_role.user.last_name = update_form.last_name.data
                db.session.commit()
                flash('User changes accepted!')
                return redirect(url_for('admin'))
            else:
                flash('A user with that e-mail already exists.')
            return redirect(url_for('admin'))
        else:
            user_role.role_id = int(update_form.role.data)
            user_role.user.first_name = update_form.first_name.data
            user_role.user.last_name = update_form.last_name.data
            db.session.commit()
            flash('User changes accepted!')
            return redirect(url_for('admin'))
    user_roles = UserRoles.query.all()
    return render_template('admin.html', user_roles=user_roles, search_form=search_form, update_form=None, user=None, delete_form=None)

# Profile route
@app.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    form = ProfileUpdateForm()
    user_role = UserRoles.query.filter_by(user_id=current_user.id).first()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        db.session.commit()
        flash('Thanks for updating your profile!')
        return redirect(url_for('profile'))
    return render_template('profile.html', user_role=user_role, form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Incorrect email or password. Please try again!')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title="Log In", form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        if len(User.query.all()) == 1:
            roles = UserRoles(user_id=User.query.filter_by(email=user.email).first().id, role_id=7)
        else:
            roles = UserRoles(user_id=User.query.filter_by(email=user.email).first().id, role_id=5)
        db.session.add(roles)
        db.session.commit()
        flash('Your account has been successfully created!')
        return redirect(url_for('login'))
    return render_template('login.html', title="Register", form=form)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_login = datetime.datetime.utcnow()
        current_user.active = True
        db.session.commit()

@app.route('/logout')
def logout():
    current_user.active = False
    logout_user()
    return redirect(url_for('login'))
