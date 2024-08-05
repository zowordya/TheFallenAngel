import pygame

clock = pygame.time.Clock()
pygame.init()
running = True
screen = pygame.display.set_mode((564, 376))
pygame.display.set_caption("The Fallen Angel")
bg = pygame.image.load('images/bg.png').convert()
player_speed = 10
player_x = 50
player_y = 250
is_jump = False
jump_cont = 8
gameplay = True
walk_right = [
    pygame.image.load('images/right/1.png').convert_alpha(),
    pygame.image.load('images/right/2.png').convert_alpha(),
    pygame.image.load('images/right/3.png').convert_alpha(),
    pygame.image.load('images/right/4.png').convert_alpha(),
]
walk_left = [
    pygame.image.load('images/left/1.png').convert_alpha(),
    pygame.image.load('images/left/2.png').convert_alpha(),
    pygame.image.load('images/left/3.png').convert_alpha(),
    pygame.image.load('images/left/4.png').convert_alpha(),
]
ghost = pygame.image.load("images/gost.png").convert_alpha()


label = pygame.font.Font('fonts/PixelifySans-VariableFont_wght.ttf', 40)
lose_label = label.render('You Lose', False, (189, 0, 0))
restart_label = label.render('Try again', False, (189, 0, 0))

restart_label_rect = restart_label.get_rect(topleft=(200, 200))

bullet = pygame.image.load('images/ball.png').convert_alpha()
bullets = []

ghost_list = []
player_anim_count = 0
bgx = 0
bg_sound = pygame.mixer.Sound("sounds/bg.mp3")
bg_sound.play()

ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 3000)
while running:

    clock.tick(13) #замедляем анимацию
    #Делаем перемещение фона
    screen.blit(bg, (bgx, 0))
    screen.blit(bg, (bgx + 564, 0))

    if gameplay:

        keys = pygame.key.get_pressed()
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

        if ghost_list:
            for (i, el) in enumerate(ghost_list):
                screen.blit(ghost, el)
                el.x -= 10

                if el.x < -50:
                    ghost_list.pop(i)


                if player_rect.colliderect(el):
                    gameplay = False



        # делаем перемещение
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))
    # Пишем прыжки
        if not is_jump:
            if keys[pygame.K_UP]:
                is_jump = True
        else:
            if jump_cont >= -8:
                if jump_cont > 0:

                    player_y -= (jump_cont ** 2) / 2
                else:
                    player_y += (jump_cont ** 2) / 2
                jump_cont -= 1
            else:
                is_jump = False
                jump_cont = 8



        if keys[pygame.K_LEFT] and player_x > 20:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 470:
            player_x += player_speed

        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1

        bgx -= 2
        if bgx == -564:
            bgx = 0

        if bullets:
            for (i, el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x += 20
                if el.x > 564:
                    bullets.pop(i)
                if ghost_list:
                    for (index, ghost_el) in enumerate(ghost_list):
                        if el.colliderect(ghost_el):
                            ghost_list.pop(index)
                            bullets.pop(i)
    else:
        screen.fill((18, 23, 20))
        screen.blit(lose_label, (200, 100))
        screen.blit(restart_label, restart_label_rect)
        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 50
            ghost_list.clear()
            bullets.clear()

    pygame.display.update()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == ghost_timer:
            ghost_list.append(ghost.get_rect(topleft=(564, 280)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            bullets.append(bullet.get_rect(topleft=(player_x + 65, player_y + 40)))
