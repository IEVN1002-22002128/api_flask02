from flask import Flask, render_template, request, make_response, redirect, flash
from forms_pipsas import ClienteForm, PizzaForm
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = "pizzeria_secret"

# funciones aux
def leer_cookie(nombre, tipo='lista'):
    data = request.cookies.get(nombre)
    return json.loads(data) if data else ([] if tipo=='lista' else {})

def guardar_cookie(resp, nombre, data):
    resp.set_cookie(nombre, json.dumps(data))

def calcular_precio(tamaño, ingredientes, cantidad):
    precios = {'chica':40,'mediana':80,'grande':120}
    return (precios[tamaño] + 10*len(ingredientes)) * cantidad

def ventas_por_cliente(ventas):
    totales = {}
    for v in ventas:
        totales[v["cliente"]] = totales.get(v["cliente"], 0) + v["total"]
    return totales

# ruta p
@app.route('/', methods=['GET', 'POST'])
def index():
    cliente = ClienteForm(request.form)
    pizza = PizzaForm(request.form)

    pizzas = leer_cookie('pizzas')
    ventas = leer_cookie('ventas')

    if request.method == 'POST':

        # agregar picsa
        if 'agregar' in request.form:
            nueva = dict(
                tamaño=pizza.tamaño.data,
                ingredientes=request.form.getlist('ingredientes'),
                cantidad=pizza.cantidad.data,
            )
            nueva["subtotal"] = calcular_precio(**nueva)
            pizzas.append(nueva)

        # quitar picsa
        elif 'quitar' in request.form:
            idx = int(request.form.get("pizza_id", -1))
            if 0 <= idx < len(pizzas): pizzas.pop(idx)

        # terminar pedido
        elif 'terminar' in request.form:
            if not cliente.nombre.data:
                flash("ponle nombre", "danger")
            elif not pizzas:
                flash("ponle picsas", "danger")
            else:
                total = sum(p["subtotal"] for p in pizzas)
                nueva_venta = {
                    "cliente": cliente.nombre.data,
                    "direccion": cliente.direccion.data,
                    "telefono": cliente.telefono.data,
                    "fecha": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                    "total": total
                }
                ventas.append(nueva_venta)
                pizzas.clear()
                flash(f" ya quedó: ${total}", "success")

        resp = make_response(redirect('/'))
        guardar_cookie(resp, 'pizzas', pizzas)
        guardar_cookie(resp, 'ventas', ventas)
        return resp

    # mostrar pagina
    hoy = datetime.now().strftime("%d-%m-%Y")
    ventas_dia = [v for v in ventas if v["fecha"].startswith(hoy)]
    total_dia = sum(v["total"] for v in ventas_dia)
    total_hist = sum(v["total"] for v in ventas)

    return render_template("pizzeria.html",
        cliente_data=cliente,
        pizzas_actuales=pizzas,
        pizza_form=pizza,
        total_pedido=sum(p["subtotal"] for p in pizzas),
        ventas_dia=ventas_dia,
        total_ventas_dia=total_dia,
        ventas_por_cliente=ventas_por_cliente(ventas),
        total_ventas_totales=total_hist
    )

# limpiar cukis
@app.route("/limpiar_ventas")
def limpiar_ventas():
    resp = make_response(redirect('/'))
    ventas = [v for v in leer_cookie('ventas') if not v["fecha"].startswith(datetime.now().strftime("%d-%m-%Y"))]
    guardar_cookie(resp, 'ventas', ventas)
    return resp

@app.route("/limpiar_todo")
def limpiar_todo():
    resp = make_response(redirect('/'))
    guardar_cookie(resp, 'pizzas', [])
    guardar_cookie(resp, 'ventas', [])
    return resp

if __name__ == "__main__":
    app.run(debug=True)