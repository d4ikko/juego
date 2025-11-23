import pygame, random, sys, time, math
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.init()

try:
    salto_sonido = pygame.mixer.Sound("salto.mp3")
    error_sonido = pygame.mixer.Sound("error.mp3")
    victoria_sonido = pygame.mixer.Sound("victoria.mp3")
    acierto_sonido = pygame.mixer.Sound("acierto.mp3")
except:
    salto_sonido = error_sonido = victoria_sonido = acierto_sonido = None
try:
    musica_mapas = [
        pygame.mixer.Sound("musica.mp3"),
        pygame.mixer.Sound("musica2.mp3"),
        pygame.mixer.Sound("musica3.mp3"),
        pygame.mixer.Sound("musica4.mp3")
    ]
    for m in musica_mapas:
        m.set_volume(0.45)
except:
    musica_mapas = []

def reproducir_musica_mapa(idx):
    try:
        pygame.mixer.stop()
        musica_mapas[idx].play(-1)
    except:
        pass

ANCHO, ALTO = 900, 500
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Math pug")

BLANCO = (255,255,255)
NEGRO  = (10,10,10)
AZUL   = (150,200,255)
SOMBRA = (180,180,180)

fuente = pygame.font.SysFont("Arial", 28)
fuente_grande = pygame.font.SysFont("Arial", 36)
clock = pygame.time.Clock()
def cargar_img(path, scale=None):
    try:
        img = pygame.image.load(path).convert_alpha()
        if scale:
            img = pygame.transform.scale(img, scale)
        return img
    except Exception:
        surf = pygame.Surface(scale if scale else (100,100))
        surf.fill((200,200,200))
        return surf


fondos = [
    cargar_img("fondo.jpg", (ANCHO, ALTO)),
    cargar_img("fondo2.jpg", (ANCHO, ALTO)),
    cargar_img("fondo3.jpg", (ANCHO, ALTO)),
    cargar_img("fondo4.jpg", (ANCHO, ALTO))
]


bloque_img = cargar_img("bloque.png", (120,30))
meta_img   = cargar_img("meta.png", (80,80))
pug_img    = cargar_img("pug.png", (70,70))
klohe_img = pygame.transform.scale(pygame.image.load("klohe.png"), (130,130))
klohefin = pygame.transform.scale(pygame.image.load("klohecomiendo.png"), (120,120))




mapa_actual = 0

reproducir_musica_mapa(mapa_actual)

num_bloques = 5
def generar_bloques_para_mapa(mapa_idx):
    bloques = []
    x_start = 80
    spacing = 150
    if mapa_idx == 1:
        x_start = 60; spacing = 155
    if mapa_idx == 2:
        x_start = 100; spacing = 140
    for i in range(num_bloques):
        bloques.append(pygame.Rect(x_start + i*spacing, 400, 120, 30))
    return bloques

bloques = generar_bloques_para_mapa(mapa_actual)

pug = pygame.Rect(80,330,70,70)
bloque_actual = 0
nivel = 1
puntaje = 0
saltando = False
vel_y = 0
errores = 0

tiempo_limite = 30
tiempo_restante = tiempo_limite
ultimo_tiempo = time.time()
def formatear_num(n):
    try:
        if isinstance(n, str):
            return n
        if isinstance(n, float):
          
            if abs(n - round(n)) < 1e-9:
                return str(int(round(n)))
            else:
                s = f"{n:.3f}".rstrip('0').rstrip('.')
                return s
        else:
            return str(n)
    except:
        return str(n)
def generar_pregunta_AB(mapa_idx, nivel_actual):

    if mapa_idx == 0:
        modo = random.choice(["mult", "raiz"])
        if modo == "mult":
            a = random.randint(2,15)
            b = random.randint(2,15)
            resultado = a * b
            texto = f"{a} × {b}"
        else:
            base = random.randint(2,15)
            resultado = base
            texto = f"√({base*base})"

        deltas = [-2,-1,1,2,3,-3]
        candidatos = [resultado + d for d in deltas if resultado + d >= 0 and resultado + d != resultado]
        if not candidatos:
            candidatos = [resultado + 1]
        falsa = random.choice(candidatos)

        if random.choice([True, False]):
            return texto, resultado, falsa, "A", resultado
        else:
            return texto, falsa, resultado, "B", resultado

   
    elif mapa_idx == 1:
        a = random.randint(1,6)
        b = random.randint(-6,6)
        c = random.randint(-6,6)
        x0 = random.randint(-5,5)
        texto = f"Si f(x) = {a}x² + {b}x + {c}, ¿f({x0}) = ?"
        resultado = a*x0*x0 + b*x0 + c

        candidatos = [resultado + d for d in (-7,-5,-3,3,5,7)]
        falsa = random.choice(candidatos)

        if random.choice([True, False]):
            return texto, resultado, falsa, "A", resultado
        else:
            return texto, falsa, resultado, "B", resultado

    elif mapa_idx == 2:
        tipo = random.choice(["log10", "sin", "cos", "tan"])

        if tipo == "log10":
            exp = random.randint(1,4)
            n = 10**exp
            texto = f"log₁₀({n})"
            resultado = exp
            falsa = resultado + random.choice([-1,1])
            if falsa < 0:
                falsa = resultado + 1

            if random.choice([True, False]):
                return texto, resultado, falsa, "A", resultado
            else:
                return texto, falsa, resultado, "B", resultado

      
        ang = random.choice([0,30,45,60,90])
        rad = math.radians(ang)

        if tipo == "sin":
            val = math.sin(rad)
            texto = f"sin({ang}°)"
        elif tipo == "cos":
            val = math.cos(rad)
            texto = f"cos({ang}°)"
        else:
            if ang == 90:
                ang = random.choice([0,30,45,60])
                rad = math.radians(ang)
            val = math.tan(rad)
            texto = f"tan({ang}°)"

        resultado = round(val, 3)
        offset = (abs(resultado) + 0.2) * random.uniform(0.06, 0.25)
        falsa = round(resultado + random.choice([-1,1]) * offset, 3)
        if falsa == resultado:
            falsa = round(resultado + 0.07, 3)

        if random.choice([True, False]):
            return texto, resultado, falsa, "A", resultado
        else:
            return texto, falsa, resultado, "B", resultado

    elif mapa_idx == 3:
        tipo = random.choice(["log", "trigo", "expon", "mixta"])

 
        if tipo == "log":
            base = random.choice([2, 3, 5, 10])
            exp = random.randint(2, 6)
            resultado = exp
            valor = base ** exp
            texto = f"log_{base}({valor})"

        elif tipo == "trigo":
            ang = random.choice([0,30,45,60,90])
            func = random.choice(["sin", "cos", "tan"])
            rad = math.radians(ang)

            if func == "sin":
                resultado = round(math.sin(rad), 3)
                texto = f"sin({ang}°)"
            elif func == "cos":
                resultado = round(math.cos(rad), 3)
                texto = f"cos({ang}°)"
            else:
                if ang == 90:
                    ang = random.choice([0,30,45,60])
                    rad = math.radians(ang)
                resultado = round(math.tan(rad), 3)
                texto = f"tan({ang}°)"

        elif tipo == "expon":
            base = random.randint(2, 8)
            exp = random.randint(2, 6)
            resultado = base ** exp
            texto = f"{base}^{exp}"

      
        else:
            a = random.randint(2, 9)
            b = random.randint(2, 9)
            c = random.randint(2, 5)
            texto = f"√({a*b*c}) + log_{a}({a**c})"
            resultado = round(((a*b*c)**0.5) + c, 3)

      
        falsa = round(resultado + random.uniform(-5, 5), 3)
        if falsa == resultado:
            falsa += 0.1

        if random.choice([True, False]):
            return texto, resultado, falsa, "A", resultado
        else:
            return texto, falsa, resultado, "B", resultado


pregunta_texto, opcionA, opcionB, correcta_letra, resultado_real = generar_pregunta_AB(mapa_actual, nivel)


def pasar_siguiente_mapa():
    global mapa_actual, bloques, bloque_actual, pug, nivel, pregunta_texto, opcionA, opcionB, correcta_letra, resultado_real
    mapa_actual += 1
    if mapa_actual >= len(fondos):
       
        pantalla.fill(BLANCO)
        fin = fuente_grande.render("¡Felicidades! Klohe llegó a su comida!", True, NEGRO)
        pantalla.blit(fin, (ANCHO//2 - fin.get_width()//2, ALTO//2 - 140))

# --- Imagen final centrada ---
        img_x = ANCHO//2 - klohefin.get_width()//2
        img_y = ALTO//2 - klohefin.get_height()//2 + 20
        pantalla.blit(klohefin, (img_x, img_y))

# --- Texto a la izquierda ---
        txt_puntaje = fuente.render(f"Puntaje final: {puntaje}", True, NEGRO)
        pantalla.blit(txt_puntaje, (img_x - txt_puntaje.get_width() - 40, img_y + 20))

# --- Texto a la derecha ---
        txt_errores = fuente.render(f"Errores: {errores}", True, (200, 0, 0))
        pantalla.blit(txt_errores, (img_x + klohefin.get_width() + 40, img_y + 20))
        if victoria_sonido: victoria_sonido.play()
        pygame.display.flip()
        pygame.time.wait(3000)
        reiniciar_todo()
        return

    reproducir_musica_mapa(mapa_actual)
    bloques[:] = generar_bloques_para_mapa(mapa_actual)
    bloque_actual = 0
    pug.x, pug.y = 80,330
    nivel = 1
    pregunta_texto, opcionA, opcionB, correcta_letra, resultado_real = generar_pregunta_AB(mapa_actual, nivel)

def reiniciar_todo():
    global mapa_actual, nivel, puntaje, bloque_actual, pug, tiempo_restante, ultimo_tiempo, pregunta_texto, opcionA, opcionB, correcta_letra, resultado_real
    mapa_actual = 0
    reproducir_musica_mapa(mapa_actual)
    nivel = 1
    puntaje = 0
    bloque_actual = 0
    pug.x, pug.y = 80,330
    tiempo_restante = tiempo_limite
    ultimo_tiempo = time.time()
    bloques[:] = generar_bloques_para_mapa(mapa_actual)
    pregunta_texto, opcionA, opcionB, correcta_letra, resultado_real = generar_pregunta_AB(mapa_actual, nivel)


def dibujar_caja_con_sombra(surface, rect, color_bg, sombra_color, texto_surf=None, border_radius=12):
    
    sombra_rect = rect.copy()
    sombra_rect.x += 4; sombra_rect.y += 4
    pygame.draw.rect(surface, sombra_color, sombra_rect, border_radius=border_radius)
    
    pygame.draw.rect(surface, color_bg, rect, border_radius=border_radius)
   
    if texto_surf:
        tx = rect.x + 20
        ty = rect.y + (rect.height - texto_surf.get_height())//2
        surface.blit(texto_surf, (tx, ty))


running = True
while running:
    pantalla.blit(fondos[mapa_actual], (0,0))

  
    for i, b in enumerate(bloques):
        pantalla.blit(bloque_img, (b.x, b.y))
        if i == len(bloques) - 1:
            pantalla.blit(meta_img, (b.x + 20, b.y - 70))

    pantalla.blit(pug_img, (pug.x, pug.y))

    caja_q = pygame.Rect(ANCHO//2 - 200, 20, 400, 56)
    texto_surface = fuente.render(pregunta_texto, True, NEGRO)
    dibujar_caja_con_sombra(pantalla, caja_q, BLANCO, SOMBRA, texto_surface, border_radius=14)
    texto_igual_surface = fuente.render("es igual a", True, NEGRO)


    texto_igual_surface = fuente.render("= ?", True, NEGRO)


    pantalla.blit(
    texto_igual_surface,
    (caja_q.right + 10, caja_q.y + caja_q.height//2 - texto_igual_surface.get_height()//2)
)
    rectA = pygame.Rect(ANCHO//2 - 300, 100, 260, 80)
    rectB = pygame.Rect(ANCHO//2 + 40, 100, 260, 80)

 
    displayA = formatear_num(opcionA)
    displayB = formatear_num(opcionB)
    txtA_surf = fuente.render(f"A: {displayA}", True, NEGRO)
    txtB_surf = fuente.render(f"B: {displayB}", True, NEGRO)

    dibujar_caja_con_sombra(pantalla, rectA, BLANCO, SOMBRA, txtA_surf, border_radius=12)
    dibujar_caja_con_sombra(pantalla, rectB, BLANCO, SOMBRA, txtB_surf, border_radius=12)

    pantalla.blit(fuente.render(f"Mapa: {mapa_actual+1}/{len(fondos)}", True, NEGRO), (20, 20))
    pantalla.blit(fuente.render(f"Puntaje: {puntaje}", True, NEGRO), (20, 52))
    pantalla.blit(fuente.render(f"Errores: {errores}", True, NEGRO), (20, 84)
)
    ahora = time.time()
    tiempo_restante -= (ahora - ultimo_tiempo)
    ultimo_tiempo = ahora
    pantalla.blit(fuente.render(f"Tiempo: {int(tiempo_restante)}s", True, NEGRO), (ANCHO - 180, 20))

    if tiempo_restante <= 0:
        if error_sonido: error_sonido.play()
        for i_anim in range(20):
            pug.y += 6
            pantalla.blit(fondos[mapa_actual], (0,0))
            for b in bloques: pantalla.blit(bloque_img, (b.x,b.y))
            pantalla.blit(pug_img, (pug.x,pug.y))
            pygame.display.flip()
            clock.tick(60)
        pug.x, pug.y = 80,330
        bloque_actual = 0
        tiempo_restante = tiempo_limite
        pregunta_texto, opcionA, opcionB, correcta_letra, resultado_real = generar_pregunta_AB(mapa_actual, nivel)

  
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
            break
        if e.type == pygame.KEYDOWN:
            eleccion = None
            if e.key == pygame.K_a:
                eleccion = "A"
            elif e.key == pygame.K_b:
                eleccion = "B"

            if eleccion:
                if eleccion == correcta_letra:
                    
                    if acierto_sonido: acierto_sonido.play()
                    puntaje += 10
                    nivel += 1
                    bloque_actual += 1
                    saltando = True
                    vel_y = -18
                    if salto_sonido: salto_sonido.play()
                    tiempo_restante = tiempo_limite
                    if bloque_actual < len(bloques):
                        pregunta_texto, opcionA, opcionB, correcta_letra, resultado_real = generar_pregunta_AB(mapa_actual, nivel)
                else:
                  
                    if error_sonido: error_sonido.play()
                    errores += 1
                    for i_anim in range(40):
                        pug.y += 10
                        
                        pantalla.blit(fondos[mapa_actual], (0,0))
                        for b in bloques: pantalla.blit(bloque_img, (b.x,b.y))
                        pantalla.blit(pug_img, (pug.x,pug.y))
                        pygame.display.flip()
                        clock.tick(60)
                    pug.x, pug.y = 80,330
                    bloque_actual = 0
                    tiempo_restante = tiempo_limite
                    pregunta_texto, opcionA, opcionB, correcta_letra, resultado_real = generar_pregunta_AB(mapa_actual, nivel)

    if saltando:
        pug.y += vel_y
        vel_y += 1
        if pug.y >= 330:
            pug.y = 330
            saltando = False
            if bloque_actual >= len(bloques):

                         
                pantalla.fill(BLANCO)
                ganar = fuente_grande.render("¡completaste el mapa !", True, NEGRO)
                pantalla.blit(ganar, (ANCHO//2 - ganar.get_width()//2, ALTO//2 - 60))
                pantalla.blit(klohe_img, (ANCHO//2 - 60, ALTO//2 - 20))
                if victoria_sonido: victoria_sonido.play()
                pygame.display.flip()
                pygame.time.wait(1200)
                pasar_siguiente_mapa()
            else:
                pug.x = bloques[bloque_actual].x
                tiempo_restante = tiempo_limite

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
