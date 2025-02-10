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


@app.route("/search/<string:location>")
def search(location):
    cafes_by_location = Cafe.query.filter_by(location=location).all()
    cafes_list = [cafe.to_dict() for cafe in cafes_by_location]

    if not cafes_list:  # Correct way to check for an empty list
        return jsonify({"error": "No cafes found for this location"}), 404  

    return jsonify(cafes_list)  # Return JSON data if cafes are found


    


# HTTP POST - Create Record

@app.route("/add", methods=["POST"])
def add_place():
    new_cafe = Cafe(
      name = request.form.get("name"),
      map_url= request.form.get("map_url"),
      img_url= request.form.get("img_url"),
      location= request.form.get("location"),
      has_sockets= request.form.get("has_sockets"),
      has_toilet= request.form.get("has_toilet"),
      has_wifi= request.form.get("has_wifi"),
      can_take_calls= request.form.get("can_take_calls"),
      seats= request.form.get("seats"),
      coffee_price=request.form.get("coffee_price")

    )
    db.session.add(new_cafe)

    db.session.commit()
    return jsonify({"message": "Cafe added successfully"})


# HTTP PUT/PATCH - Update Record

# HTTP DELETE - Delete Record





if __name__ == '__main__':
    app.run(debug=True)
