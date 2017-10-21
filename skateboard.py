import random

# Sett opp vinduet
TITLE = 'SkateMaster 9000'
WIDTH = 1024
HEIGHT = 500

# Plassering av Actors i forhold til bakgrunnen
GROUND = 350
SKATER_GROUND = GROUND-20
SKATER_XPOS = 100

# Variabler som setter vanskelighetsgraden i spillet
OBSTACLE_RATE = 300
SPEED = 500
JUMP_DISTANCE = 150
SCORE_PER_OBSTACLE = 1000
JUMP_TIME = 0.3
HANG_TIME = 0.1
LAND_TIME = 0.4
SCROLL_SPEED = 3.5

# Spilleren styrer objektet skater - som er en Actor
skater = Actor('stand', anchor=('left', 'top'), pos=(SKATER_XPOS, SKATER_GROUND))    # Bruk bildet 'images/stand.png' og plasser oss på rett sted
skater.score = 0
skater.isJumping = False
skater.hasBailed = False

# Her legger vi hindre etterhvert som de blir oppretta
obstacles = []

# Denne holder styr på bakgrunnen
scroll = WIDTH

# Funksjonen update() blir kjørt før hver eneste bildeoppdatering
def update():
    update_background();
    update_obstacle()
    update_skater()

# Funsjonen on_key_down() blir kjørt hver gang du trykker på en tast
def on_key_down(key):
    if key==keys.SPACE:
        if skater.hasBailed:
            spawn_skater()
        else:
            jump()

    if key==keys.ESCAPE:
        quit()

# Funksjonen draw() tegner grafikken på skjermen
def draw():
    screen.blit('bg', (-scroll, 0))         # tegn venstre side av bakgrunnen
    screen.blit('bg', (WIDTH-scroll, 0))    # tegn høyre side av bakgrunnen

    for obstacle in obstacles:
        obstacle.draw()                     # tegn hindre

    skater.draw()                           # tegn skater'n

    screen.draw.text(                       # skriv poengene
        str(skater.score),
        color='white',
        midtop=(WIDTH // 2, 10),
        fontsize=70,
        shadow=(1, 1)
    )

# Opprett et nytt hinder på utsiden av skjermen helt til høyre - på bakken
def create_obstacle():
    return Actor('obstacle', anchor=('left', 'top'), pos=(WIDTH, GROUND))

# Her oppdateres hindrene
def update_obstacle():

    # Gå igjennom hvert hinder som finnes akkurat nå
    for obstacle in obstacles:

        animate(obstacle, pos=(obstacle.left-SPEED, obstacle.top)) # Flytt dette hinderet mot venstre med avstanden SPEED

        if obstacle.left < SKATER_XPOS and not skater.hasBailed:
            skater.score += SCORE_PER_OBSTACLE  # Hvis vi har passert hinderet uten å falle, får vi poeng

        if obstacle.left < 0:                   # Hvis hindret har passert kanten av skjermen, fjerner vi det
            obstacles.remove(obstacle)

    # Etter at vi har vært igjennom alle hindrene, er det en sjanse for at vi legger til et nytt
    if random.randint(0, OBSTACLE_RATE) == 0:   # (Litt) tilfeldig om det blir noe nytt hinder eller ikke
        obstacles.append(create_obstacle())

# Skatern'n prøver på nytt
def spawn_skater():
    skater.score = 0
    skater.y = GROUND
    skater.isJumping = False
    skater.hasBailed = False
    obstacles = []

# Her oppdateres skater'n
def update_skater():

    if skater.hasBailed:
        return                              # da er det ikke mer å gjøre her...

    skater.score += 1

    if skater.isJumping:                    # hvis vi er i et hopp, vis hoppebildet
        skater.image = 'jump'
    else:                                   # ellers, vis det vanlige bildet
        skater.image = 'stand'

    for obstacle in obstacles:              # sjekk om vi kolliderer med noen av hindrene
        if skater.colliderect(obstacle):
            skater.hasBailed = True         # jepp, vi tryna :/
            skater.image = 'fall'               # hvis vi har tryna, vis bildet av fall
            return


# Sett igang et hopp
def jump():
    if skater.isJumping:
        return

    skater.isJumping = True
    sounds.jump.play()
    jump_animation = animate(skater, tween="decelerate", duration=JUMP_TIME, pos=(SKATER_XPOS, SKATER_GROUND-JUMP_DISTANCE))
    jump_animation.on_finished = hang    # Når hoppet er på toppen vil vi gjerne sveve litt fordi det ser tøft ut ;)

# Heng litt i lufta
def hang():
    global skater
    global hang_animation
    hang_animation = animate(skater, tween="linear", duration=HANG_TIME, pos=(SKATER_XPOS, SKATER_GROUND-JUMP_DISTANCE), on_finished=land)

# Begynn på landingen
def land():
    global land_animation
    global skater
    land_animation = animate(skater, tween="accelerate", duration=LAND_TIME, pos=(SKATER_XPOS, SKATER_GROUND), on_finished=jump_landed)


# Når vi har landet kan vi ta nye hopp
def jump_landed():
    skater.isJumping = False

# Scrolling av bakgrunnen skyver bildet hele tiden mot venstre
def update_background():
    global scroll
    scroll += SCROLL_SPEED
    if(scroll > WIDTH ):    # når vi kommer til kanten av bildet, begynner vi på nytt
        scroll = 0

