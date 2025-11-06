from flask import Flask, render_template, request
import forms
import math

class CalculadoraDistancia:
    def __init__(self, xa=0, ya=0, xb=0, yb=0):
        self.coordXA = xa
        self.coordYA = ya
        self.coordXB = xb
        self.coordYB = yb
        self.distanciaCalculada = 0

    def ejecutar_calculo(self):
        self.distanciaCalculada = math.sqrt(
            (self.coordXB - self.coordXA) ** 2 +
            (self.coordYB - self.coordYA) ** 2
        )

    def mostrar_resultado(self):
        return f"Distancia calculada: {self.distanciaCalculada:.2f} unidades"


app = Flask(__name__)

@app.route('/index')
def index():
  titulo="Pagina de inicio"
  listado=['Python', 'Flask', 'Jinja2', 'HTML', 'CSS']
  return render_template('index.html', titulo=titulo, listado=listado)

@app.route('/calculos', methods=['GET', 'POST'])
def calculos():

    if request.method == 'POST':
        numero1 = request.form.get('numero1', '')
        numero2 = request.form.get('numero2', '')
        operacion = request.form.get('operacion', '')

        try:
            n1, n2 = int(numero1), int(numero2)
            if operacion == 'suma':
                resultado = n1 + n2
            elif operacion == 'resta':
                resultado = n1 - n2
            elif operacion == 'multiplicacion':
                resultado = n1 * n2
            elif operacion == 'division':
                resultado = n1 / n2 if n2 != 0 else "Div entre cero"
        except ValueError:
            resultado = "Error: Ingresa números válidos"

    return render_template('calculos.html',
                           resultado=resultado,
                           numero1=numero1,
                           numero2=numero2)

@app.route('/distancia', methods=['GET', 'POST'])
def distancia():
    resultado = None
    puntoA_X = puntoA_Y = puntoB_X = puntoB_Y = ''

    if request.method == 'POST':
        try:
            puntoA_X = float(request.form.get('puntoA_X', 0))
            puntoA_Y = float(request.form.get('puntoA_Y', 0))
            puntoB_X = float(request.form.get('puntoB_X', 0))
            puntoB_Y = float(request.form.get('puntoB_Y', 0))

            calc = CalculadoraDistancia(puntoA_X, puntoA_Y, puntoB_X, puntoB_Y)
            calc.ejecutar_calculo()
            resultado = calc.mostrar_resultado()

        except ValueError:
            resultado = "Error: Ingresa valores numéricos válidos"

    return render_template('distancia.html',
                           resultado=resultado,
                           puntoA_X=puntoA_X,
                           puntoA_Y=puntoA_Y,
                           puntoB_X=puntoB_X,
                           puntoB_Y=puntoB_Y)

@app.route("/Alumnos",methods=['GET','POST'])
def alumnos():
  mat=0
  nom=""
  ape=""
  email=""
  alumno_clas=forms.UserForm(request.form)
  if request.method == 'POST' and alumno_clas.validate():
    mat=alumno_clas.matricula.data
    nom=alumno_clas.nombre.data
    ape=alumno_clas.apellido.data
    email=alumno_clas.correo.data
  return render_template('alumnos.html',form=alumno_clas, mat=mat,nom=nom,ape=ape,email=email)

@app.route('/user/<string:user>')
def user(user):
  return f"Hello, {user}!"

@app.route('/numero/<int:num>')
def func(num):
  return f"El numero es: {num}!"

@app.route('/sum/<int:num1>/<int:num2>')
def suma(num1, num2):
  return f"La suma es: {num1 + num2}!"

@app.route('/user/<int:id>/<string:username>')
def username(id, username):
  return "ID: {} nombre: {}".format(id,username)

@app.route('/suma/<float:n1>/<float:n2>')
def func1(n1,n2):
  return "la suma es: {}".format(n1+n2)

@app.route('/default/')
@app.route('/default/')
def func2(dft="sss"):
  return "el valor dft es:" + dft

@app.route('/prueba/<int:num>')
def func3():
  return '''

<html>
<head>
  <link></link>
    <title> Página de prueba </title>
  </head>
  <body>
    <h1>HOLA SOY EL ANTICRISTO</h1>
    <p>PAGINA DE PROEBA XD</p>
  </body>
</html>

'''

if __name__ == '__main__':
  app.run(debug=True)