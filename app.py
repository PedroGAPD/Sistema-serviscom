from flask import Flask, render_template, request, jsonify
from pyswip import Prolog

app = Flask(__name__)
prolog = Prolog()
# Cargamos tu archivo oficial de Prolog
prolog.consult("serviscom.pl")

@app.route('/')
def inicio():
    # Mantenemos una vista web sencilla para probar la interfaz visual si se desea
    return render_template('index.html')

@app.route('/api/diagnosticar', methods=['POST'])
def api_diagnosticar():
    # Recibimos los datos en formato JSON (o de un formulario tradicional si se prefiere)
    data = request.get_json() if request.is_json else request.form
    
    usuario = data.get('nombre', 'invitado').lower()
    sistemas = data.get('sistemas', [])
    problemas = data.get('problemas', [])
    
    # Si vienen como string separado por comas o listas desde un form
    if isinstance(sistemas, str):
        sistemas = [s.strip() for s in sistemas.split(',') if s.strip()]
    if isinstance(problemas, str):
        problemas = [p.strip() for p in problemas.split(',') if p.strip()]

    num_problemas = len(problemas)
    num_peligro = 0
    
    # 1. Contar los peligros con Prolog
    for p in problemas:
        if list(prolog.query(f"peligro({p})")):
            num_peligro += 1

    # 2. Inyectar el entorno para Prolog (Sistemas combinados)
    list(prolog.query(f"retractall(tiene_sistema({usuario}, _))"))
    for s in sistemas:
        prolog.assertz(f"tiene_sistema({usuario}, {s})")

    diagnosticos_lista = []

    # 3. Procesar cada problema mediante la inferencia lógica de Prolog
    for problema in problemas:
        detalle_problema = {
            "problema": problema,
            "estado_critico": False,
            "solucion": None,
            "complejidad": "normal",
            "causa_probable": None,
            "hardware": False,
            "veredicto_reparacion": False,
            "motivos": []
        }
        
        # A) Evaluar si no tiene solución (crítico)
        if list(prolog.query(f"sin_solucion({problema}, {num_peligro}, {num_problemas})")):
            detalle_problema["estado_critico"] = True
            detalle_problema["motivos"].append("El sistema determinó que es un daño catastrófico o se excedió el límite de fallas.")
            diagnosticos_lista.append(detalle_problema)
            continue

        # B) Extraer la solución general mediante backtracking
        solucion_query = list(prolog.query(f"solucion_general(Solucion, {problema})"))
        if solucion_query:
            detalle_problema["solucion"] = solucion_query[0]["Solucion"]
            
            # C) Evaluar complejidad (trivial vs grave)
            if list(prolog.query(f"problema_trivial({detalle_problema['solucion']}, {problema})")):
                detalle_problema["complejidad"] = "trivial"
            elif list(prolog.query(f"problema_grave({detalle_problema['solucion']}, {problema})")):
                detalle_problema["complejidad"] = "grave"
        
        # D) Evaluar riesgos (Virus)
        if list(prolog.query(f"posible_virus(_, {problema})")):
            detalle_problema["causa_probable"] = "posible_virus"

        # E) Evaluar si requiere cambio de pieza
        if list(prolog.query(f"cambiar_pieza({problema})")):
            detalle_problema["hardware"] = True

        # F) Veredicto final de reparación
        if list(prolog.query(f"llevala_a_reparar({problema}, {num_problemas})")):
            detalle_problema["veredicto_reparacion"] = True
            if list(prolog.query(f"peligro({problema})")):
                detalle_problema["motivos"].append("Representa un peligro inminente para el equipo.")
            elif list(prolog.query(f"problema_grave(_, {problema})")):
                detalle_problema["motivos"].append("La gravedad técnica es muy alta.")
            else:
                detalle_problema["motivos"].append(f"Acumulación de fallas ({num_problemas} problemas en total).")
        else:
            detalle_problema["motivos"].append("Puede resolverse en casa sin técnico.")

        diagnosticos_lista.append(detalle_problema)

    # Limpieza final en la base de conocimientos de Prolog
    list(prolog.query(f"retractall(tiene_sistema({usuario}, _))"))

    # Estructura final del JSON de respuesta
    respuesta_json = {
        "usuario": usuario,
        "total_problemas": num_problemas,
        "total_peligros": num_peligro,
        "diagnosticos": diagnosticos_lista
    }

    return jsonify(respuesta_json)

if __name__ == '__main__':
    app.run(debug=True)