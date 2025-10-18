from flask import Flask, render_template

app = Flask(__name__)

@app.route('/index')
def index():
  titulo="Pagina de inicio"
  listado=['Python', 'Flask', 'Jinja2', 'HTML', 'CSS']
  return render_template('index.html', titulo=titulo, listado=listado)

@app.route('/calculos')
def about():
  return render_template('calculos.html')

@app.route('/distancia')
def distancia():
  return render_template('distancia.html')

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



