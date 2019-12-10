import turtle
import time
import re

file = open("turtle", "r")
contenu = file.read()
contenu = contenu.split('\n')

turtle.setup( width = 20000, height = 20000, startx = 0, starty = 0)
turtle.degrees()

for s in contenu:
    if not s:
        continue
    nu = int(re.search(r'\d+', s).group())
    if "gauche" in s:
        turtle.lt(nu)
    elif "droite" in s:
        turtle.rt(nu)
    elif "Avance" in s:
        turtle.fd(nu)
    elif "Recule" in s:
        turtle.bk(nu)

time.sleep(10)
