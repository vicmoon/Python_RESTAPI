from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random



app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)



    def to_dict(self):
        dictionary = {}  # Corrected to a dictionary

        for column in self.__table__.columns:  # Fixed typo
            dictionary[column.name] = getattr(self, column.name)  # Proper indentation
        return dictionary



with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record


@app.route("/random")
def get_random():
    with app.app_context():
        all_cafes = Cafe.query.all()
        random_cafe = random.choice(all_cafes)
        return jsonify(cafe=random_cafe.to_dict())
    

        # return jsonify({
        #     "id" : random_cafe.id,
        #     "name": random_cafe.name,
        #     "map_url": random_cafe.map_url,
        #     "img_url": random_cafe.img_url,
        #     "location": random_cafe.location, 
        #     "seats":random_cafe.seats,
        #     "has_toilet": random_cafe.has_toilet,
        #     "has_wifi": random_cafe.has_wifi, 
        #     "has_sockets": random_cafe.has_sockets 

        # })
    

@app.route("/all")
def get_all():
    all_cafes = Cafe.query.all()
    cafes_list = [cafe.to_dict() for cafe in all_cafes]
    return jsonify(cafes_list)







        

# HTTP POST - Create Record

# HTTP PUT/PATCH - Update Record

# HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
