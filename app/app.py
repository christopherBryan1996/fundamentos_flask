from flask import Flask, config, render_template, request, url_for, redirect, jsonify
from flask.helpers import url_for
from werkzeug.utils import redirect
from flask_mysqldb import MySQL

app=Flask(__name__) #inicializamos la aplicacion

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = ''
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='rh'

conexion = MySQL(app)

@app.before_request
def before_request():
    print('antes de la peticion ...')

@app.after_request
def after_request(response):
    print('Despues de la peticion')
    return response

#creamos una ruta 
@app.route('/')
def index():
    #return 'hola mundo'
    cursos=['PHP','Python', 'Java', 'Kotlin', 'Dart', 'JavaScript']
    data={
        'titulo': 'Index',
        'bienvenida': '¡Saludos!',
        'cursos': cursos,
        'numero_cursos': len(cursos)
    }
    return render_template('index.html', data=data)
#una ruta con params|| para poner que es un entero se pone int 
@app.route('/contacto/<nombre>/<int:edad>')
#el parametro de la funcion debe de llamarse igual que el params
def contacto(nombre,edad):
    data={
        'titulo':'Contacto',
        'nombre': nombre,
        'edad': edad
    }
    return render_template('contacto.html',data=data)

def query_strig():
    #http://127.0.0.1:3005/query_string?param1=bryan
    print(request)
    print(request.args)
    print(request.args.get('param1'))
    return 'ok'

@app.route('/empleados')
def lista_empleados():
    data={}
    try:
        cursor=conexion.connection.cursor()
        sql='select apellido,nombre,fecha from employees'
        cursor.execute(sql)
        cursos=cursor.fetchall()
        #print(cursos)
        data['cursos']=cursos
        data['mensaje']='exito'

    except Exception as ex:
        data['mensaje']='error ...'
    
    return jsonify(data)

def paguina_no_encontrada(error):
    #return render_template('404.html'),404
    #nos manda a una ruta predestinada
    return redirect(url_for('index'))

if __name__=='__main__':#vemos si estamos en el archivo inicial 
    app.add_url_rule('/query_string',view_func=query_strig)
    app.register_error_handler(404, paguina_no_encontrada)
    app.run(debug=True, port=3005)#esto nos sirve para actualizar cuando guardemos cambios cerrar el servidor y volverlo activar 