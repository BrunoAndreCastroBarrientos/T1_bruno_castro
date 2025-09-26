import random

class Entrenador:
    def __init__(self, nombre):
        self.nombre = nombre

class Pokemon:
    def __init__(self, nombre):
        self.nombre = nombre
        self.max_ataque = random.randint(20, 100)  
        self.vida_max = random.randint(150, 400)   
        self.vida_actual = self.vida_max           

entrenador1 = None
entrenador2 = None
pokemon1 = None
pokemon2 = None
ganadas = 0
perdidas = 0

def crearEntrenadorPokemon(numero):
    """
    Crea un entrenador y su pokemon.
    numero: 1 (usted) o 2 (rival)
    Pide por teclado: nombre de entrenador y nombre de pokemon,
    y guarda en las variables globales correspondientes.
    """
    global entrenador1, entrenador2, pokemon1, pokemon2

    if numero == 1:
        print("=== Creación de su entrenador y Pokémon ===")
    else:
        print("=== Creación del entrenador rival y su Pokémon ===")

    nombre_ent = input("Nombre del entrenador: ").strip()
    while nombre_ent == "":
        nombre_ent = input("Nombre del entrenador (no vacío): ").strip()

    nombre_pok = input("Nombre del Pokémon: ").strip()
    while nombre_pok == "":
        nombre_pok = input("Nombre del Pokémon (no vacío): ").strip()

    nuevo_entrenador = Entrenador(nombre_ent)
    nuevo_pokemon = Pokemon(nombre_pok)

    if numero == 1:
        entrenador1 = nuevo_entrenador
        pokemon1 = nuevo_pokemon
    else:
        entrenador2 = nuevo_entrenador
        pokemon2 = nuevo_pokemon

    print("-> Pokémon creado: {0} | Ataque máx: {1} | Vida máx: {2}".format(
        nuevo_pokemon.nombre, nuevo_pokemon.max_ataque, nuevo_pokemon.vida_max))
    print("")

def valorDeAtaque(numero):
    """
    Calcula si un pokemon ataca total o parcialmente.
    Devuelve un entero entre 0 y el ataque máx del pokémon indicado.
    - Si numero == 1 (usted), se le permite elegir:
        T = ataque total (entre max_ataque//2 y max_ataque)
        P = ataque parcial (entre 0 y max_ataque//2)
        A = al azar (elige T o P al azar)
    - Si numero == 2 (rival), decide al azar entre T y P.
    """
    global pokemon1, pokemon2

    if numero == 1:
        max_a = pokemon1.max_ataque
        eleccion = input("Elija ataque Total (T), Parcial (P) o Azar (A): ").strip().upper()
        if eleccion not in ("T", "P", "A"):
            eleccion = "P"

        if eleccion == "A":
            eleccion = random.choice(["T", "P"])

        if eleccion == "T":
            minimo = max_a // 2
            if minimo < 0:
                minimo = 0
            danio = random.randint(minimo, max_a)
            print("  - Ataque TOTAL elegido. Potencia calculada:", danio)
            return danio
        else:
            tope = max_a // 2
            danio = random.randint(0, tope)
            print("  - Ataque PARCIAL elegido. Potencia calculada:", danio)
            return danio

    else:
        max_a = pokemon2.max_ataque
        tipo = random.choice(["T", "P"])
        if tipo == "T":
            minimo = max_a // 2
            if minimo < 0:
                minimo = 0
            danio = random.randint(minimo, max_a)
            print("  - (Rival) Ataque TOTAL. Potencia:", danio)
            return danio
        else:
            tope = max_a // 2
            danio = random.randint(0, tope)
            print("  - (Rival) Ataque PARCIAL. Potencia:", danio)
            return danio

def defender(defensor, valor_ataque):
    """
    Calcula y graba la vida restante del Pokémon defensor (1 o 2).
    Tira un dado (1..6); si sale 6, el ataque se reduce a 0 (bloquea).
    Retorna la vida_actual del Pokémon defensor.
    También imprime un resumen tras el ataque.
    """
    global pokemon1, pokemon2, entrenador1, entrenador2

    dado = random.randint(1, 6)
    if dado == 6:
        valor_ataque = 0
        print("  - Dado de defensa: 6 -> ¡Bloqueo perfecto! Daño reducido a 0.")
    else:
        print("  - Dado de defensa:", dado)

    if defensor == 1:
        poke_def = pokemon1
        ent_def = entrenador1
    else:
        poke_def = pokemon2
        ent_def = entrenador2

    poke_def.vida_actual = poke_def.vida_actual - valor_ataque

    vida_mostrar = poke_def.vida_actual
    if vida_mostrar < 0:
        vida_mostrar = 0

    print("  - Daño recibido:", valor_ataque)
    print("  - {0} de {1} ahora tiene {2}/{3} de vida.\n".format(
        poke_def.nombre, ent_def.nombre, vida_mostrar, poke_def.vida_max))

    return poke_def.vida_actual

def recuperar():
    """
    Llena la vida actual de los Pokémon antes de una batalla.
    No recibe parámetros (usa las variables globales).
    """
    global pokemon1, pokemon2
    if pokemon1 is not None:
        pokemon1.vida_actual = pokemon1.vida_max
    if pokemon2 is not None:
        pokemon2.vida_actual = pokemon2.vida_max

print("======================================")
print("        ¡BATALLA POKÉMON (Consola)    ")
print("======================================\n")

crearEntrenadorPokemon(1)

opcion = ""
while opcion != "F":
    print("Menú: [P] Pelear   |   [F] Finalizar")
    opcion = input("Elija una opción: ").strip().upper()
    print("")

    if opcion == "P":
        crearEntrenadorPokemon(2)

        recuperar()

        print(">>> Entra al campo el Pokémon rival:")
        print("Nombre: {0} | Ataque máx: {1} | Vida: {2}".format(
            pokemon2.nombre, pokemon2.max_ataque, pokemon2.vida_max))
        print("")

        turno = 1
        terminado = False
        while not terminado:
            if turno == 1:
                print("Turno de {0} ({1})".format(entrenador1.nombre, pokemon1.nombre))
                input("  (Presione ENTER para lanzar su ataque) ")
                danio = valorDeAtaque(1)
                vida_restante = defender(2, danio)
                if vida_restante <= 0:
                    print("¡¡{0} de {1} ha caído!!".format(pokemon2.nombre, entrenador2.nombre))
                    print(">>> GANADOR: {0} con {1}\n".format(entrenador1.nombre, pokemon1.nombre))
                    ganadas += 1
                    terminado = True
                else:
                    turno = 2
            else:
                print("Turno de {0} ({1})".format(entrenador2.nombre, pokemon2.nombre))
                input("  (Presione ENTER para continuar el ataque del rival) ")
                danio = valorDeAtaque(2)
                vida_restante = defender(1, danio)
                if vida_restante <= 0:
                    print("¡¡{0} de {1} ha caído!!".format(pokemon1.nombre, entrenador1.nombre))
                    print(">>> GANADOR: {0} con {1}\n".format(entrenador2.nombre, pokemon2.nombre))
                    perdidas += 1
                    terminado = True
                else:
                    turno = 1

    elif opcion == "F":
        print("======================================")
        print("              RESUMEN FINAL           ")
        print("======================================")
        print("Su Pokémon:")
        print("  - Nombre: {0}".format(pokemon1.nombre))
        print("  - Ataque máximo: {0}".format(pokemon1.max_ataque))
        print("  - Vida máxima: {0}".format(pokemon1.vida_max))
        print("  - Vida actual: {0}".format(pokemon1.vida_actual))
        print("")
        print("Encuentros ganados: {0}".format(ganadas))
        print("Encuentros perdidos: {0}".format(perdidas))
        print("¡Gracias por jugar!")
    else:
        print("Opción no válida. Escriba P para pelear o F para finalizar.\n")
