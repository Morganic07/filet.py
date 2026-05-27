import pygame
import math

pygame.init()

s = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
W, H = s.get_width(), s.get_height()
clock = pygame.time.Clock()

#creation des points P
P = []
for y in range(30):
    for x in range(50):
        pos_x = x * 20 + W / 4
        pos_y = y * 20 + 100
        # Le dernier élément (y==0) fixe la rangée du haut
        P.append([pos_x, pos_y, pos_x, pos_y, y == 0])

#creation des segments S
S = []
for i in range(len(P)):
    # Liens horizontaux
    if (i + 1) % 50 != 0:
        S.append([i, i + 1, 1])
    # Liens verticaux
    if i + 50 < len(P):
        S.append([i, i + 50, 1])

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False
    
    s.fill((0, 5, 10)) 
    
    mx, my = pygame.mouse.get_pos()
    md = pygame.mouse.get_pressed()
    
#physique des points
    for p in P:
        if not p[4]: 
            if md[0] and math.hypot(p[0] - mx, p[1] - my) < 30:
                p[0], p[1] = mx, my
            
            vx = (p[0] - p[2]) * 0.99
            vy = (p[1] - p[3]) * 0.99
            p[2], p[3] = p[0], p[1]
            p[0] += vx
            p[1] += vy + 0.4 # Gravité

    for _ in range(6):
        for sk in S:
            if sk[2]: 
                p1, p2 = P[sk[0]], P[sk[1]]
                dx, dy = p2[0] - p1[0], p2[1] - p1[1]
                d = math.hypot(dx, dy) or 0.1
                
                if d > 100 or (md[2] and math.hypot((p1[0]+p2[0])/2 - mx, (p1[1]+p2[1])/2 - my) < 15):
                    sk[2] = 0
                    continue
                
                f = (20 - d) / d * 0.5
                if not p1[4]:
                    p1[0] -= dx * f
                    p1[1] -= dy * f
                if not p2[4]:
                    p2[0] += dx * f
                    p2[1] += dy * f

#pygame draw
    for sk in S:
        if sk[2]:
            p1, p2 = P[sk[0]], P[sk[1]]
            pygame.draw.line(s, (0, 255, 150), (p1[0], p1[1]), (p2[0], p2[1]), 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
