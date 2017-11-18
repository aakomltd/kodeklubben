# -*- coding: utf-8 -*-

# Sett opp vinduet
TITLE = 'StarBlaster'
WIDTH = 1024
HEIGHT = 500

# Plassering av Actors i forhold til bakgrunnen
GROUND = 350
SKATER_GROUND = GROUND-20
SKATER_XPOS = 100

# Variabler som setter vanskelighetsgraden i spillet
OBSTACLE_RATE = 200
OBSTACLE_PAUSE = 20
SPEED = 500
JUMP_DISTANCE = 150
SCORE_PER_OBSTACLE = 1000
JUMP_TIME = 0.3
HANG_TIME = 0.1
LAND_TIME = 0.4
SCROLL_SPEED = 3.5
SHIP_SPEED = 10

def move_up(speed):
    global ship
    x = ship.pos[0]
    y = ship.pos[1]
    ship.pos = (x, y - speed)

def move_down(speed):
    global ship
    x = ship.pos[0]
    y = ship.pos[1]
    ship.pos = (x, y + speed)

# Spilleren styrer objektet ship - som er en Actor
ship = Actor('warrior3_128x48', anchor=('left', 'top'), pos=(SKATER_XPOS, SKATER_GROUND))    # Bruk bildet 'images/stand.png' og plasser oss på rett sted
ship.score = 0
ship.hasExploded = False
ship.distance_travelled = 0
ship.move_up = move_up
ship.move_down = move_down
ship.blasts = []
ship.weaponsCooling = False
ship.isOk = True

# Her legger vi hindre etterhvert som de blir oppretta
obstacles = []
previous_obstacle = OBSTACLE_PAUSE
obstacle_animations = []

# Denne holder styr på bakgrunnen
scroll = WIDTH

# Funksjonen update() blir kjørt før hver eneste bildeoppdatering
def update():
    update_background();
    #update_obstacle()
    update_ship()

# Funsjonen on_key_down() blir kjørt hver gang du trykker på en tast
def on_key_down(key):
    if key==keys.SPACE:
        if ship.isOk:
            shoot()
        else:
            spawn_ship()

    if key==keys.UP:
            ship.move_up(SHIP_SPEED)

    if key==keys.DOWN:
            ship.move_down(SHIP_SPEED)

    if key==keys.ESCAPE:
        quit()

# Funksjonen draw() tegner grafikken på skjermen
def draw():
    screen.blit('bg', (-scroll, 0))         # tegn venstre side av bakgrunnen
    screen.blit('bg', (WIDTH-scroll, 0))    # tegn høyre side av bakgrunnen

    for obstacle in obstacles:
        obstacle.draw()                     # tegn hindre

    ship.draw()                           # tegn skipet

    screen.draw.text(                       # skriv poengene
        str(ship.score),
        color='white',
        midtop=(WIDTH // 2, 10),
        fontsize=70,
        shadow=(1, 1)
    )


# Opprett et nytt hinder på utsiden av skjermen helt til høyre - på bakken
#def create_obstacle_rampe_h():
#    actor = Actor('rampe_hoyre', anchor=('left', 'top'), pos=(WIDTH, GROUND-25))
#    actor.collision_type = 'jump'
#    return actor

#def create_obstacle_bom():
#     actor = Actor('obstacle', anchor=('left', 'top'), pos=(WIDTH, GROUND))
#     actor.collision_type = 'bail'
#     return actor

#def remove_obstacle_anim(anim):
#    if obstacle_animations.count(anim) > 0:
#        obstacle_animations.remove(anim)

# Her oppdateres hindrene
#def update_obstacle():
#    global previous_obstacle

#    if skater.hasBailed:
#        for anim in obstacle_animations:
#            if(anim.running):
#                anim.stop(complete=False)
#                remove_obstacle_anim(anim)


    # Gå igjennom hvert hinder som finnes akkurat nå
#    for obstacle in obstacles:

#        if ship.hasBailed:
#            return
#        anim = animate(obstacle, pos=(obstacle.left-SPEED, obstacle.top)) 
#        obstacle_animations.append(anim) # Flytt dette hinderet mot venstre med avstanden SPEED
#        anim.on_finished = remove_obstacle_anim(anim)

#        if obstacle.left < SKATER_XPOS:
#            skater.score += SCORE_PER_OBSTACLE  # Hvis vi har passert hinderet uten å falle, får vi poeng

#        if obstacle.left < 0:                   # Hvis hindret har passert kanten av skjermen, fjerner vi det
#            obstacles.remove(obstacle)

#    previous_obstacle -= 1
#    if(previous_obstacle > 0):
#        return;


    # Etter at vi har vært igjennom alle hindrene, er det en sjanse for at vi legger til et nytt
#    random_obstacle = random.randint(0, OBSTACLE_RATE);

#    if random_obstacle == 0:   # (Litt) tilfeldig om det blir noe nytt hinder eller ikke
#        obstacles.append( create_obstacle_bom() )
#        previous_obstacle = OBSTACLE_PAUSE
#    if random_obstacle == 1:
#        no_obstacles = len(obstacles) - 1;
#        if(no_obstacles >= 0):
#            if obstacles[len(obstacles)-1].collision_type == 'jump':
#                return
#        previous_obstacle = OBSTACLE_PAUSE
#        obstacles.append( create_obstacle_rampe_h() )

# Skatern'n prøver på nytt
def spawn_ship():
    global obstacles
    global obstacle_animations

    ship.score = 0
    ship.y = GROUND
    ship.hasBailed = False
    #for obstacle in obstacles:
    #    obstacles.remove(obstacle)
    #obstacles = []
    #for anim in obstacle_animations:
    #    if anim.running:
    #        anim.stop()
    #    obstacle_animations.remove(anim)
    #obstacle_animations = []

# Her oppdateres 'n

def update_ship():
    if ship.hasExploded:
        return                              # da er det ikke mer å gjøre her...

    ship.distance_travelled += 1

#    for obstacle in obstacles:              # sjekk om vi kolliderer med noen av hindrene
#        if skater.colliderect(obstacle):

#            if obstacle.collision_type == 'jump':
#                obstacle_left = obstacle.left+30
#                if obstacle_left < SKATER_XPOS:
#                    bail()
#                else:
#                    jump(2)
#                return

#            if obstacle.collision_type == 'bail':
#                bail()
#                return

def explode():
    ship.hasExploded = True         # jepp, vi tryna :/
    #skater.image = 'fall'               # hvis vi har tryna, vis bildet av fall

# Skyt
def shoot():
    global ship

    if ship.weaponsCooling or ship.hasExploded:
        return

    x = ship.pos[0]
    y = ship.pos[1]
    ship.blasts.append((x,y))
    




#    jump_animation = animate(skater, tween="decelerate", duration=JUMP_TIME, pos=(SKATER_XPOS, SKATER_GROUND-JUMP_DISTANCE * height))
#    jump_animation.on_finished = hang    # Når hoppet er på toppen vil vi gjerne sveve litt fordi det ser tøft ut ;)

# Heng litt i lufta
#def hang():
#    global skater
#    global hang_animation
#    hang_animation = animate(skater, tween="linear", duration=HANG_TIME, pos=(SKATER_XPOS, SKATER_GROUND-JUMP_DISTANCE), on_finished=land)

# Scrolling av bakgrunnen skyver bildet hele tiden mot venstre
def update_background():
    global scroll
    if ship.hasExploded:
        return

    scroll += SCROLL_SPEED
    if(scroll > WIDTH ):    # når vi kommer til kanten av bildet, begynner vi på nytt
        scroll = 0

