from flask import Flask, render_template, request
from pyswip import Prolog

app = Flask(__name__)
prolog = Prolog()
# Cargamos tu archivo oficial
prolog.consult("serviscom.pl")

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/diagnosticar', methods=['POST'])
def diagnosticar():
    usuario = request.form['nombre'].lower()
    sistemas = request.form.getlist('sistemas')
    problemas = request.form.getlist('problemas')
    
    num_problemas = len(problemas)
    num_peligro = 0
    
    # 1. Dejar que Prolog cuente los peligros
    for p in problemas:
        if list(prolog.query(f"peligro({p})")):
            num_peligro += 1

    # 2. Inyectar el entorno para Prolog (El sistema combinado)
    list(prolog.query(f"retractall(tiene_sistema({usuario}, _))"))
    for s in sistemas:
        prolog.assertz(f"tiene_sistema({usuario}, {s})")

    diagnosticos = []

    # 3. Extraer el diagnóstico profundo de Prolog
    for problema in problemas:
        detalle_html = f"<strong>Reporte para '{problema.replace('_', ' ')}':</strong><ul>"
        
        # A) Evaluar si hay solución o si el equipo está perdido
        # Pasamos los números reales para que Prolog evalúe sus reglas matemáticas
        es_sin_solucion = list(prolog.query(f"sin_solucion({problema}, {num_peligro}, {num_problemas})"))
        if es_sin_solucion:
            detalle_html += "<li>❌ <b>Estado Crítico:</b> El sistema no tiene solución. "
            if num_peligro > 5 or num_problemas > 5:
                detalle_html += "Prolog determinó que excediste el límite de daños lógicos soportados."
            else:
                detalle_html += "Prolog determinó que es un daño físico catastrófico."
            detalle_html += " Se recomienda comprar equipo nuevo.</li></ul><hr>"
            diagnosticos.append(detalle_html)
            continue # Si ya está quemado, no evaluamos más

        # B) Extraer la solución general mediante backtracking
        solucion_query = list(prolog.query(f"solucion_general(Solucion, {problema})"))
        if solucion_query:
            solucion = solucion_query[0]["Solucion"]
            detalle_html += f"<li>✅ <b>Solución técnica encontrada:</b> Debes {solucion.replace('_', ' ')}.</li>"
            
            # C) Prolog evalúa la naturaleza de la solución (Trivial vs Grave)
            if list(prolog.query(f"problema_trivial({solucion}, {problema})")):
                detalle_html += "<li>🟢 <b>Complejidad:</b> Es un problema trivial, puedes resolverlo tú mismo.</li>"
                
            if list(prolog.query(f"problema_grave({solucion}, {problema})")):
                detalle_html += "<li>🔴 <b>Complejidad:</b> Prolog lo clasifica como un PROBLEMA GRAVE.</li>"
        
        # D) Prolog evalúa riesgos colaterales (Virus)
        if list(prolog.query(f"posible_virus(_, {problema})")):
            detalle_html += "<li>🦠 <b>Causa probable:</b> Esto se debe a un posible VIRUS o comportamiento inseguro.</li>"

        # E) Prolog evalúa daños de hardware (Piezas)
        if list(prolog.query(f"cambiar_pieza({problema})")):
            detalle_html += "<li>🔧 <b>Hardware:</b> Es una pieza rota, la solución es reemplazarla por una nueva.</li>"

        # F) Veredicto final de acción (Usando la regla unificada)
        es_reparacion = list(prolog.query(f"llevala_a_reparar({problema}, {num_problemas})"))
        if es_reparacion:
            detalle_html += "<li>🚨 <b>Veredicto del Sistema:</b> LLÉVALA A REPARAR INMEDIATAMENTE. "
            if list(prolog.query(f"peligro({problema})")):
                detalle_html += "(Motivo: Representa un peligro inminente para la computadora).</li>"
            elif list(prolog.query(f"problema_grave(_, {problema})")):
                detalle_html += "(Motivo: La gravedad técnica es muy alta).</li>"
            else:
                detalle_html += f"(Motivo: Acumulación de fallas. Tienes {num_problemas} problemas en total).</li>"
        else:
            detalle_html += "<li>ℹ️ <b>Veredicto del Sistema:</b> Puedes aplicar la solución en casa, no requiere técnico por ahora.</li>"

        detalle_html += "</ul><hr>"
        diagnosticos.append(detalle_html)

    # Limpieza final
    list(prolog.query(f"retractall(tiene_sistema({usuario}, _))"))

    # Render simple para ver el resultado
    html_respuesta = f"<h2>Diagnóstico Experto para: {usuario.capitalize()}</h2>"
    for d in diagnosticos:
        html_respuesta += d
    html_respuesta += "<br><a href='/'>Hacer otro diagnóstico</a>"
    
    return html_respuesta

if __name__ == '__main__':
    app.run(debug=True)