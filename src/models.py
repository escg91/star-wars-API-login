from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nombre = db.Column(db.String(80), unique=False, nullable=False)
    apellido = db.Column(db.String(80), unique=False, nullable=False)
    favoritos = db.relationship('Favoritos', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Personajes(db.Model):

    #Here we define columns for the table person
    #Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String (250))
    skin_color = db.Column(db.String (250))
    species = db.Column(db.String (250))
    favoritos = db.relationship('Favoritos', backref='personajes', lazy=True)

def __repr__(self):
        return '<Personajes %r>' % self.id

def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }

class Planetas(db.Model):
   
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    climate = db.Column(db.String (250))
    created = db.Column(db.String (250))
    diameter = db.Column(db.String (250))
    favoritos = db.relationship('Favoritos', backref='planetas', lazy=True)

    def __repr__(self):
        return '<Planetas %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "climate": self.climate,
            # do not serialize the password, its a security breach
        }

class Vehiculos(db.Model):
   
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    cargo_capacity = db.Column(db.String (250))
    consumables = db.Column(db.String (250))
    cost_in_credits = db.Column(db.String (250))
    favoritos = db.relationship('Favoritos', backref='vehiculos', lazy=True)

    def __repr__(self):
        return '<Vehiculos %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "cargo_capacity": self.cargo_capacity,
            # do not serialize the password, its a security breach
        }

class Favoritos(db.Model):
   
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    personajes_id = db.Column(db.Integer, db.ForeignKey('personajes.id'))
    vehiculos_id = db.Column(db.Integer, db.ForeignKey('vehiculos.id'))
    planetas_id = db.Column(db.Integer, db.ForeignKey('planetas.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Favoritos %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "personajes_id": self.personajes_id,
            "vehiculos_id": self.vehiculos_id,
            "planetas_id": self.planetas_id,
            "user_id": self.user_id,
            # do not serialize the password, its a security breach
        }