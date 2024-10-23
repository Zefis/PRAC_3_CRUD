from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)

# Necesario para poder usar sesiones
app.secret_key = 'unaclavesecreta'

# Función para generar el ID de los contactos
def generar_id():
    # Corregido: Cambié 'contacto' por 'contactos' para acceder correctamente a la lista de contactos.
    if 'contactos' in session and len(session['contactos']) > 0:
        return max(item['id'] for item in session['contactos']) + 1
    else:
        return 1

@app.route("/")
def index():
    # Corregido: Verificación correcta de si 'contactos' no está en la sesión
    if 'contactos' not in session:
        session['contactos'] = []  # Inicializa la lista de contactos en la sesión si no existe
    
    # Obtiene los contactos de la sesión
    contactos = session.get('contactos', [])
    return render_template('index.html', contactos=contactos)

# Ruta para agregar un nuevo contacto
@app.route("/nuevo", methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        # Se capturan los datos del formulario
        fecha = request.form['fecha']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        turno = request.form['turno']
        seminarios = request.form.getlist('seminarios')
        
        # Se crea un diccionario para el nuevo contacto
        nuevo_contacto = {
            'id': generar_id(),
            'fecha': fecha,
            'nombre': nombre,
            'apellido': apellido,
            'turno': turno,
            'seminarios': seminarios
        }
        
        # Verifica si 'contactos' no está en la sesión, lo inicializa si es necesario
        if 'contactos' not in session:
            session['contactos'] = []
        
        # Se agrega el nuevo contacto a la lista de la sesión
        session['contactos'].append(nuevo_contacto)
        session.modified = True  # Marca la sesión como modificada
        return redirect(url_for('index'))
    
    return render_template('nuevo.html')

# Ruta para editar un contacto existente
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    # Obtiene la lista de contactos de la sesión
    lista_contactos = session.get('contactos', [])
    # Busca el contacto a editar según su ID
    contacto = next((c for c in lista_contactos if c['id'] == id), None)  # Corregido: Eliminé el espacio extra
    
    # Si no se encuentra el contacto, redirige al index
    if not contacto:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        # Actualiza los valores del contacto
        contacto['fecha'] = request.form['fecha']
        contacto['nombre'] = request.form['nombre']
        contacto['apellido'] = request.form['apellido']
        contacto['turno'] = request.form['turno']
        contacto['seminarios'] = request.form.getlist('seminarios')
        session.modified = True  # Marca la sesión como modificada
        return redirect(url_for('index'))
    
    return render_template('editar.html', contacto=contacto)

# Ruta para eliminar un contacto
@app.route("/eliminar/<int:id>", methods=["POST"])  # Corregido: Cambié "/elminar" a "/eliminar"
def eliminar(id):
    # Obtiene la lista de contactos de la sesión
    lista_contactos = session.get('contactos', [])
    # Busca el contacto a eliminar según su ID
    contacto = next((c for c in lista_contactos if c['id'] == id), None)  # Corregido: Eliminé el espacio extra
    
    # Si se encuentra el contacto, se elimina de la lista
    if contacto:
        session['contactos'].remove(contacto)
        session.modified = True  # Marca la sesión como modificada
    
    return redirect(url_for('index'))

# Corre la aplicación en modo debug
if __name__ == "__main__":
    app.run(debug=True)
