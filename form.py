from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class BookingForm(FlaskForm):
    name = StringField(
        'Namn och efternamn', 
        validators=[DataRequired(message="Namnet är obligatoriskt."), Length(max=400, message="Namnet får max vara 400 tecken.")],
    )
    phone = StringField(
        'Telefonnummer', 
        validators=[DataRequired(message="Telefonnumret är obligatoriskt."), Length(max=400, message="Telefonnumret får max vara 400 tecken.")],
    )
    email = StringField(
        'E-post', 
        validators=[DataRequired(message="E-post är obligatoriskt."), Email(message="Ange en giltig e-postadress."), Length(max=400, message="E-post får max vara 400 tecken.")],
    )
    description = TextAreaField(
        'Beskriv gärna dina önskemål', 
        validators=[Length(max=2000, message="Beskrivningen får max vara 2000 tecken.")]
    )
    submit = SubmitField('Boka barnvakt / pedagog')
