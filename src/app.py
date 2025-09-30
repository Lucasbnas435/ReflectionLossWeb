import os

from dotenv import load_dotenv
from flask import Flask, render_template

from src.controllers import register_controllers

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "static", "files")
register_controllers(app)


@app.errorhandler(Exception)
def error_handler(error):
    print(f"Ocorreu um erro: {str(error)}")
    return render_template("tela_erro.html"), 500


if __name__ == "__main__":
    app.run(debug=True)
