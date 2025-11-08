from wtforms import Form, StringField, SelectField, SelectMultipleField, IntegerField, DateField
from wtforms import validators
from datetime import datetime

class ClienteForm(Form):
    nombre = StringField("Nombre", [
        validators.DataRequired(message='El nombre es requerido')
    ])
    direccion = StringField("Dirección", [
        validators.DataRequired(message='La dirección es requerida')
    ])
    telefono = StringField("Teléfono", [
        validators.DataRequired(message='El teléfono es requerido')
    ])
    fecha = DateField("Fecha", format='%d-%m-%Y', default=datetime.now)

class PizzaForm(Form):
    tamaño = SelectField("Tamaño Pizza", choices=[
        ('chica', 'Chica $40'),
        ('mediana', 'Mediana $80'), 
        ('grande', 'Grande $120')
    ], validators=[validators.DataRequired()])
    
    ingredientes = SelectMultipleField("Ingredientes", choices=[
        ('jamon', 'Jamón $10'),
        ('pina', 'Piña $10'),
        ('champinones', 'Champiñones $10')
    ])
    
    cantidad = IntegerField("Num. de Pizzas", [
        validators.NumberRange(min=1, message='Mínimo 1 pizza'),
        validators.DataRequired(message='La cantidad es requerida')
    ], default=1)