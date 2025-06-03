from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired


class UploadFileForm(FlaskForm):
    file = FileField(
        "File",
        validators=[
            InputRequired(),
            FileAllowed(["csv"], "Por favor, envie um arquivo csv"),
        ],
    )
    submit = SubmitField("Enviar arquivo")
