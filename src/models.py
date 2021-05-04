from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username":self.username,
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(80), unique=True, nullable=False)
    terrain = db.Column(db.String(120), unique=False, nullable=False)
    climate = db.Column(db.String(80), unique=False, nullable=False)
    diameter = db.Column(db.Integer, unique=False, nullable=False)      
    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "terrain":self.terrain,
            "climate":self.climate,
            "Diameter":self.diameter
                  # do not serialize the password, its a security breach
        }      
class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(80), unique=True, nullable=False)
    birth = db.Column(db.String(120), unique=False, nullable=False)
    gender = db.Column(db.String(80), unique=False, nullable=False)
    height = db.Column(db.Integer, unique=False, nullable=False)      
    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth":self.birth,
            "gender":self.gender,
            "height":self.height
                  # do not serialize the password, its a security breach
        }              
class Favorite(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    idUser=db.Column(db.Integer, db.ForeignKey("user.id"))
    idCharacter=db.Column(db.Integer, db.ForeignKey("character.id"))
    idPlanet=db.Column(db.Integer, db.ForeignKey("planet.id"))
    user = db.relationship("User", lazy='subquery', backref=db.backref("Favorite", cascade="all,delete"))
    planet = db.relationship("Planet", lazy='subquery', backref=db.backref("Favorite", cascade="all,delete"))    
    character = db.relationship("Character", lazy='subquery', backref=db.backref("Favorite", cascade="all,delete"))   

    def __repr__(self):
        return '<Favorite %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "idUser":self.idUser,
            "idCharacter":self.idCharacter,
            "idPlanet":self.idPlanet
            
                  # do not serialize the password, its a security breach
        }          