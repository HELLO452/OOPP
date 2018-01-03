from flask import Flask, render_template, request, flash, redirect, url_for, session
from wtforms import Form, StringField, RadioField, SelectField, validators, PasswordField, FileField
from Dbs import Dbs
from Notdbs import Notdbs
import Functions

app = Flask(__name__)

@app.route('/home')
def home():
    if not session['logged_in']:
        return render_template('Login.html')
    else:
        if Functions.eligibility(session['user']) == 'ocbc easicredit and dbs cashline':
            word = 'Age and annual salary requirement met ocbc easicredit'
        elif Functions.eligibility(session['user']) == 'ocbc easicredit, dbs cashline and uob cashplus':
            word = 'Age and annual salary requirement met ocbc easicredit, dbs cashline and uob cashplus'
        elif Functions.eligibility(session['user']) == 'Age not met':
            word = 'Age requirement does not met'
        else:
            word = 'Annual income requirement does not met'

        return render_template('home.html', username=session['user'], lastlogin=session['lastlogin'], word=word)


@app.route('/vieweasicredit')
def easicredit():
    return render_template('view_easicredit.html', username=session['user'], lastlogin=session['lastlogin'], interest = Functions.show_interest(session['user'], 'OCBC Easicredit')[0])

@app.route('/viewcashline')
def viewpublications():
    return render_template('view_cashline.html', username=session['user'], lastlogin=session['lastlogin'])

class LoginForm(Form):
    username = StringField('SingPass ID', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])



class ApplicationForm(Form):

    overdrafttype = RadioField('Type Of Overdraft', choices=[('DBS Cashline', 'DBS Cashline'), ('OCBC Easicredit', 'OCBC Easicredit'), ('UOB Cashplus', 'UOB Cashplus')],default='DBS Cashline')

    acctype = RadioField('Salary Credited Under', choices=[('dbs/posb', 'DBS/POSB Acc'), ('uob/ocbc', 'UOB/OCBC Acc')], default='dbs/posb')

    if acctype == 'dbs':
        salarycreditacc = StringField('Salary Crediting Account', [
        validators.Length(min=1, max=9),
        validators.DataRequired()])
    else:
        salarycreditacc = StringField('Salary Crediting Account', [
        validators.Length(min=1, max=10),
        validators.DataRequired()])

    creditlimit = SelectField('Indicate Preferred Credit Limit', [validators.DataRequired()],
                              choices=[('', 'Select'), ('2000', '2000'), ('4000', '4000'),
                              ('6000', '6000'), ('8000', '8000'), ('10000', '10000')], default='')

    file1 = FileField('Upload the front side of NRIC', [validators.DataRequired()])

    file2 = FileField('Upload the back side of NRIC', [validators.DataRequired()])
    if acctype == 'uob/ocbc':
        document = RadioField('Select one of the following', [validators.DataRequired()],
                              choices=[("Latest 12 month's CPF Contribution History Statement", "a. Latest 12 month's CPF Contribution History Statement"),
                                       ('Latest Income Tax Notice of Asessment & latest Computerised Payslip', 'b. Latest Income Tax Notice of Asessment & latest Computerised Payslip')])
    else:
        document = RadioField('Select one of the following',
                              choices=[("Latest 12 month's CPF Contribution History Statement", "a. Latest 12 month's CPF Contribution History Statement"),
                                       ('Latest Income Tax Notice of Asessment & latest Computerised Payslip', 'b. Latest Income Tax Notice of Asessment & latest Computerised Payslip')])




@app.route('/newapplication', methods=['GET', 'POST'])
def new():
    form = ApplicationForm(request.form)
    if request.method == 'POST' and form.validate():
        if form.acctype.data == 'uob/ocbc':
            salarycreditacc = form.salarycreditacc.data
            acctype = form.acctype.data
            overdrafttype = form.overdrafttype.data
            creditlimit = form.creditlimit.data
            file1 = form.file1.data
            file2 = form.file2.data
            document = form.document.data

            application = Notdbs(salarycreditacc, creditlimit, acctype, overdrafttype, file1, file2, document)

            Functions.applicationdetail(application, session['user'])

            flash('Application Sucessfully.', 'success')

            return redirect(url_for('home'))
        else:
            salarycreditacc = form.salarycreditacc.data
            acctype = form.acctype.data
            creditlimit = form.creditlimit.data
            overdrafttype = form.overdrafttype.data
            file1 = form.file1.data
            file2 = form.file2.data

            application = Dbs(salarycreditacc, creditlimit, acctype, overdrafttype, file1, file2)

            Functions.applicationdetail(application, session['user'])

            flash('Application Sucessfully.', 'success')

            return redirect(url_for('home'))

    return render_template('create_application.html', form=form, username=session['user'], lastlogin=session['lastlogin'])




@app.route('/login', methods=['GET', 'POST'])

def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        if Functions.userlogin(username, password) == 'Incorrect password':
            error = 'Incorrect password'
            flash(error, 'danger')
            return render_template('Login.html', form=form)
        elif Functions.userlogin(username, password) == 'Invalid nric':
            error = 'Invalid nric'
            flash(error, 'danger')
            return render_template('Login.html', form=form)
        else:  # this is to set a session to indicate the user is login into the system.
            session['user'] = Functions.userlogin(username, password)[0]
            session['lastlogin'] = Functions.userlogin(username, password)[1] + "," + Functions.userlogin(username, password)[2]
            session['logged_in'] = True
            Functions.update_lastlogin(session['user'], username, password)
            return render_template('home.html', username=session['user'], lastlogin=session['lastlogin'])

    return render_template('Login.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run()
