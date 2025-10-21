from flask import Flask
from api.patients.routes import patients_bp
from api.doctor.routes import doctors_bp


app = Flask(__name__)
app.register_blueprint(patients_bp)
app.register_blueprint(doctors_bp)
print(app.url_map)

if __name__ == "__main__":
    app.run(debug=True)
