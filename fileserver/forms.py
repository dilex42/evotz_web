from wtforms import Form, validators, StringField, PasswordField, FileField, DateTimeField, TextAreaField

class CredentialsForm(Form) :
    username = StringField('Username', [validators.Length(min=1, max=25)])
    password = PasswordField('Password', [validators.Length(min=3)])

class UploadForm(Form) :
    file = FileField('File')
    description = TextAreaField('Description', [validators.Length(max=42)])
    expires = DateTimeField('Expires at',[validators.DataRequired()])