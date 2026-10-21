%Hechos
sin_solucion(perdida_de_documentos_o_archivos).
sin_solucion(liquido_derramado).
sin_solucion(corrosion_dentro_del_equipo).
sin_solucion(equipo_quemado).
sin_solucion(placa_madre_danada).

peligro(equipo_con_virus).
peligro(equipo_totalmente_sobrecalentado).
peligro(equipo_sigue_sin_encender).
peligro(equipo_hackeado).
peligro(no_reconoce_puertos).
peligro(se_apaga_constantemente).

causa_de_virus(instalacion_insegura_de_aplicacion).
causa_de_virus(mal_funcionamiento_antivirus).
causa_de_virus(abrir_enlaces_desconocidos).
causa_de_virus(sobrecarga_de_recursos).
causa_de_virus(usb_de_dudosa_procedencia).

pieza_rota(faltan_teclas).
pieza_rota(pantalla_estrellada).
pieza_rota(bisagra_rota).
pieza_rota(cargador_en_mal_estado).
pieza_rota(fuente_quemada).
pieza_rota(pasta_termica_sobrecalentada).

solucion(limpiar_memoria, poca_memoria, windows).
solucion(reiniciar_equipo, error_de_instalacion, windows).
solucion(limpieza_de_sistema, disco_lleno, windows).
solucion(revisar_consumo_cpu, sistema_lento, windows).
solucion(revisar_consumo_memoria, sistema_lento, windows).
solucion(cerrar_programas, sistema_lento, windows).
solucion(restaurar_sistema, pantalla_azul, windows).
solucion(reparar_inicio, no_inicia_sistema, windows).
solucion(realizar_diagnostico_de_hardware, enciende_pero_no_muestra_imagen, windows).
solucion(revisar_consumo_memoria, elementos_no_guardados, windows).
solucion(vaciar_cache_dns, sin_internet, windows).
solucion(limpiar_ram, pitidos_sin_video, windows).

solucion(realizar_diagnostico_de_hardware, enciende_pero_no_muestra_imagen, macos).
solucion(revisar_consumo_memoria, elementos_no_guardados,macos).
solucion(limpiar_memoria, poca_memoria, macos).
solucion(reiniciar_equipo, error_de_instalacion, macos).
solucion(revisar_consumo_cpu, sistema_lento ,macos).
solucion(revisar_consumo_memoria, sistema_lento, macos).
solucion(limpiar_ram, pitidos_sin_video, macos).

solucion(abrir_htop, linux_lento, linux).
solucion(limpiar_cache_apt, disco_lleno, linux).
solucion(reiniciar_network_manager, sin_internet, linux).
solucion(reparar_grub, no_inicia_linux, linux).
solucion(revisar_systemctl, servicio_caido, linux).
solucion(revisar_consumo_memoria, elementos_no_guardados, linux).
solucion(limpiar_memoria, poca_memoria, linux).
solucion(realizar_diagnostico_de_hardware, enciende_pero_no_muestra_imagen, linux).
solucion(reiniciar_equipo, error_de_instalacion, linux).

%Reglas
solucion_para_windows(Solucion, Problema) :-
    solucion(Solucion, Problema, windows).

solucion_para_macos(Solucion, Problema) :-
    solucion(Solucion, Problema, macos).

solucion_para_linux(Solucion, Problema) :-
    solucion(Solucion, Problema, linux).

solucion_general(Solucion, Problema):-
    solucion(Solucion, Problema, Sistema),
    (
        Sistema=macos;
        Sistema=windows;
        Sistema=linux
    ).

combinado(Usuario):-
    tiene_sistema(Usuario, windows),
    tiene_sistema(Usuario, linux).

problema_combinado(Solucion1, Problema1, Solucion2, Problema2):-
    solucion(Solucion1, Problema1, windows),
    solucion(Solucion2, Problema2, linux),
    Solucion1=Solucion2,
    Problema1=Problema2.

problema_trivial(Solucion, poca_memoria):- 
    solucion(Solucion, poca_memoria, _).

problema_trivial(cerrar_programas, sistema_lento):- 
    solucion(cerrar_programas, sistema_lento, _).

problema_grave(Solucion1, enciende_pero_no_muestra_imagen):- 
    problema_combinado(Solucion1, enciende_pero_no_muestra_imagen, Solucion1, enciende_pero_no_muestra_imagen).

problema_grave(Solucion1, elementos_no_guardados):- 
    problema_combinado(Solucion1, elementos_no_guardados, Solucion1, elementos_no_guardados).

problema_grave(abrir_htop, linux_lento):- 
    solucion(abrir_htop, linux_lento, linux).

posible_virus(_, Problema):-
    causa_de_virus(Problema).

posible_virus(Solucion1, elementos_no_guardados):-
    problema_combinado(Solucion1, elementos_no_guardados, Solucion1, elementos_no_guardados).

llevala_a_reparar(Problema, Num_problemas):-
    problema_grave(_, Problema);
    Num_problemas > 3;
    peligro(Problema).

sin_solucion(_, Num_peligro, Num_problemas):-
    Num_peligro>5;
    Num_problemas>5.

comprar_nuevo_equipo(Problema):-
    sin_solucion(Problema).

cambiar_pieza(Pieza):-
    pieza_rota(Pieza).