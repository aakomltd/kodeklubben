import random

TITLE = 'Skatemaster'
WIDTH = 1024
HEIGHT = 500

# Her kan du justere vanskelighetsgraden i spillet
GAP = 40
SPEED = 6

skateboarder = Actor('stand', midbottom=(100, 369))
skateboarder.dead = False
skateboarder.score = 0
skateboarder.vy = 0
skateboarder.jumping = False
obstacle = Actor('obstacle', anchor=('left', 'top'), pos=(-100, 23))
sounds.bgmusic.play()

#DETTE RESETTER OBJEKTENE SOM I DETTE TILFELLET ER HINDRENE
def reset_objects():
    pipe_gap_y = random.randint(200, HEIGHT - 200)
    obstacle.pos = (WIDTH, 690 // 2)

#HER DEFINERER VI HINDRENE OG VALGENE VI HAR
def update_obstacle():
    obstacle.left -= SPEED
    if obstacle.right < 0:
        reset_objects()
        skateboarder.score += 1

#HER STYRER VI HVA SKATEBOARDEREN GJØR GITT VISSE KRITERIER
def update_skateboarder():
    uy = skateboarder.vy
    skateboarder.y += (uy + skateboarder.vy)
    if not skateboarder.dead:
        if skateboarder.jumping:
            skateboarder.image = 'jump'
        else:
            skateboarder.image = 'stand'

    if skateboarder.colliderect(obstacle):
        skateboarder.dead = True
        skateboarder.image = 'fall'

    if not 0 < skateboarder.y < 720:
        skateboarder.y = 369
        skateboarder.dead = False
        skateboarder.score = 0
        skateboarder.vy = 0
        reset_objects()


def update():
    update_obstacle()
    update_skateboarder()
    
#HER DEFINERER VI LANDINGEN
def land():
    animate(skateboarder, tween="accelerate", duration=0.4, pos=(100, 345))
    skateboarder.jumping = False
#HER DEFINERER VI HOPPET    
def jump():
    the_animation = animate(skateboarder, tween="decelerate", duration=0.4, pos=(100, 300))
    the_animation.on_finished = land 
    skateboarder.jumping = True
#HER BESTEMMER VI HVA SOM SKAL SKJE NÅR VI TRYKKER PÅ SPACE
def on_key_down(key):
    if key==keys.SPACE:
        if not skateboarder.dead:
            sounds.jump.play()
            jump()

#HER STARTER VI ALLE FUNKSJONENE SOM UTGJØR SPILLET
def draw():
    screen.blit('bg', (0, 0))
    obstacle.draw()
    skateboarder.draw()
    screen.draw.text(
        str(skateboarder.score),
        color='white',
        midtop=(WIDTH // 2, 10),
        fontsize=70,
        shadow=(1, 1)
    )
