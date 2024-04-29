from settings import *
from classes import *


# for building an .exe version with pyinstaller include the config file within the .exe file


def get_ai_settings():

    """ Finds the config file with the settings of the AI, searches in the same folder this file is places in """

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
    
def run(config_file, generations=500):

    # Load NEAT config
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    population = neat.Population(config)

    # Add reporters for progress and statistics
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())

    _ = population.run(game, generations)

def show_main_menu():
        
        """ Draws the elements of the main menu to the screen """

        window.blit(BACKGROUND, (0,0))

        # Titel

        main_menu_title = FONT_MAIN_MENU.render("Falcon", 1, BLACK)

        title_x = (window.get_width() - main_menu_title.get_width()) // 2
        window.blit(main_menu_title, (title_x, 80))

        # Menu Buttons

        pygame.draw.rect(window, (RED), MAIN_MENU_BUTTON_PLAY)
        main_menu_limited_text = FONT_MAIN_MENU.render("Start", 1, (WHITE)) 
        main_menu_limited_text_x = (window.get_width() - main_menu_limited_text.get_width()) // 2
        window.blit(main_menu_limited_text, (main_menu_limited_text_x,215))

        pygame.draw.rect(window, (RED), MAIN_MENU_BUTTON_HELP)
        main_menu_help_text = FONT_MAIN_MENU.render("Mehr Informationen", 1, (WHITE)) 
        main_menu_help_text_x = (window.get_width() - main_menu_help_text.get_width()) // 2
        window.blit(main_menu_help_text, (main_menu_help_text_x,340))

        pygame.draw.rect(window, (RED), MAIN_MENU_BUTTON_STOP)
        main_menu_stop_text = FONT_MAIN_MENU.render("Beenden", 1, (WHITE))
        main_menu_unlimited_text_x = (window.get_width() - main_menu_stop_text.get_width()) // 2
        window.blit(main_menu_stop_text, (main_menu_unlimited_text_x,465))
                    
        pygame.display.flip()

def main_menu():

    """ Contains the logic for the main menu """

    run_main_menu = True
    click = False

    while run_main_menu:

        mx, my = pygame.mouse.get_pos() 

        if MAIN_MENU_BUTTON_PLAY.collidepoint((mx, my)): 
            if click:
                global window
                window = pygame.display.set_mode((WIDTH,HEIGHT))
                get_ai_settings()
                run_main_menu = False  

        if MAIN_MENU_BUTTON_HELP.collidepoint((mx, my)):
            if click:
                help_menu() 

        if MAIN_MENU_BUTTON_STOP.collidepoint((mx, my)):
            if click:
                run_main_menu = False
                pygame.quit()
                sys.exit()

        click = False
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                    
        show_main_menu()

def render_multiline_text(surface, text, pos, font, color):

    """ Calculate the width for line breaks in the help menu text """

    words = textwrap.wrap(text, width=50) 
    x, y = pos
    for word in words:
        rendered_text = font.render(word, True, color)
        surface.blit(rendered_text, (x, y))
        y += font.get_height()

def show_help_menu():
    
    """ Draws the help menu to the screen """

    window.fill(WHITE)

    title_text = """In diesem Programm lernt ein Machine-Learning-Algorithmus, basierend auf Reinforcement Learning durch evolutionäres Lernen, ein einfaches Spiel zu spielen. 
                    Sie können die neuronalen Netze der verschiedenen Spieler untersuchen und nach Ablauf der ersten Runde auch mit den bisherigen Gewinnern vergleichen. 		
                    Dieses Programm ist Open Source und darf von jedem für Bildungszwecke eingesetzt werden. 
                    Mehr Informationen finden Sie unter https://github.com/Arminius-Software
                 """
    render_multiline_text(window, title_text, ((window.get_width() - 600) // 2, 80), FONT, BLACK)

    # Buttons
    pygame.draw.rect(window, RED, HELP_BACK_BUTTON)
    help_back_text = FONT_MAIN_MENU.render("Zurück", True, WHITE) 
    help_back_text_x = (window.get_width() - help_back_text.get_width()) // 2
    window.blit(help_back_text, (help_back_text_x, HEIGHT - 200 + 15))

    pygame.display.flip()

def help_menu():

    """ Contains the logic for the help menu """
    
    run_help_menu = True
    click = False

    while run_help_menu:

        mx, my = pygame.mouse.get_pos()

        if HELP_BACK_BUTTON.collidepoint((mx, my)): 
            if click:
                main_menu()
                run_help_menu = False  

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        show_help_menu()

def show_game(players, asteroids, generation, is_paused, update_neural_net_top, update_neural_net_bottom):

    """ Draws the game to the screen """

    window.blit(BACKGROUND, (0,0), (0, 0, GAME_WIDTH, HEIGHT))
    # if update_neural_net_top:
    #     pygame.draw.rect(window, WHITE, (GAME_WIDTH, 0, GAME_WIDTH, HEIGHT /2))
    # if update_neural_net_bottom:
    #     pygame.draw.rect(window, WHITE, (GAME_WIDTH, int(HEIGHT / 2), GAME_WIDTH, int(HEIGHT / 2)))

    for player in players:
        player.draw()

    for asteroid in asteroids:
        asteroid.draw()

    fps = int(clock.get_fps())
    fps_text = FONT.render("FPS: " + str(fps), 1, RED)
    fps_x_coordinate = GAME_WIDTH - fps_text.get_width() - 10
    fps_y_coordinate = 10
    window.blit(fps_text, (fps_x_coordinate, fps_y_coordinate))

    generation_text = FONT.render("Generation: " + str(generation), 1, RED)
    generation_x_coordinate = GAME_WIDTH - generation_text.get_width() - 10
    generation_y_coordinate = 50
    window.blit(generation_text, (generation_x_coordinate, generation_y_coordinate))

    score_text = FONT.render("Score: " + str(score), 1, RED)
    score_x_coordinate = GAME_WIDTH - score_text.get_width() - 10
    score_y_coordinate = 90
    window.blit(score_text, (score_x_coordinate, score_y_coordinate))

    highscore_text = FONT.render("Highscore: " + str(high_score), 1, RED)
    highscore_x_coordinate = GAME_WIDTH - highscore_text.get_width() - 10
    highscore_y_coordinate = 130
    window.blit(highscore_text, (highscore_x_coordinate, highscore_y_coordinate))

    player_text = FONT.render("Spieler: " + str(len(players)), 1, RED)
    player_x_coordinate = GAME_WIDTH - player_text.get_width() - 10
    player_y_coordinate = 170
    window.blit(player_text, (player_x_coordinate, player_y_coordinate))

    pygame.draw.rect(window, (BUTTON_GREY), PAUSE_BUTTON)
    if is_paused == False:
        pause_text = FONT.render("Pause", 1, (BLACK))
    else:
        pause_text = FONT.render("Weiter", 1, (BLACK))

    window.blit(pause_text, (740, 16))
 
def show_neural_net_top(players, ge, current_player_selected_net_top):

    pygame.draw.rect(window, WHITE, (GAME_WIDTH, 0, GAME_WIDTH, HEIGHT /2))

    # this check prevents a crash that occours when the player last in the list is selected and then dies
    if current_player_selected_net_top > len(players):
        current_player_selected_net_top = 1

    weights_top = extract_weights(str(ge[current_player_selected_net_top - 1]))

    neural_net_one = NeuralNet()
    neural_net_one.draw(NEURAL_NET_REC_TOP, weights_top)
    players[current_player_selected_net_top - 1].draw_player_at_neural_net(1280, 35)
    
    pygame.draw.rect(window, (BUTTON_GREY), NEXT_POSITIVE_BUTTON_TOP)
    next_positive_button_top_text = FONT.render("Nächster", 1, (BLACK))
    window.blit(next_positive_button_top_text, (1274,356))

    pygame.draw.rect(window, (BUTTON_GREY), NEXT_NEGATIVE_BUTTON_TOP)
    next_negative_button_top_text = FONT.render("Zurück", 1, (BLACK))
    window.blit(next_negative_button_top_text, (734,356))

    pygame.draw.line(window, BLACK, (GAME_WIDTH, HEIGHT/2), (WIDTH, HEIGHT/2), 2)

def show_neural_net_bottom(players, ge, current_player_selected_net_bottom):

    pygame.draw.rect(window, WHITE, (GAME_WIDTH, int(HEIGHT / 2), GAME_WIDTH, int(HEIGHT / 2)))

    # this check prevents a crash that occours when the player last in the list is selected and then dies
    if current_player_selected_net_bottom > len(players):
        current_player_selected_net_bottom = 1

    # select weight for bottom neural net depending on if current players are selected or winners of previous generations (+ maybe the current if only 1 agent left) 
    if mode_winner and len(winner_weights) > 0:
        weights_bottom = extract_weights(str(winner_weights[current_winner_selected]))
    else:
        weights_bottom = extract_weights(str(ge[current_player_selected_net_bottom - 1]))

    neural_net_two = NeuralNet()
    neural_net_two.draw(NEURAL_NET_REC_BOTTOM, weights_bottom)

    if not mode_winner:
        players[current_player_selected_net_bottom - 1].draw_player_at_neural_net(1280, HEIGHT/2 + 35)
    elif mode_winner and len(winner_weights) > 0:
        winner_gen_text = FONT.render(f"Generation: {current_winner_selected}", 1, (BLACK))
        window.blit(winner_gen_text, (1220, (HEIGHT / 2) + 20))
    
    pygame.draw.rect(window, (BUTTON_GREY), WINNER_CURRENT_SWITCH_BUTTON)
    if not mode_winner:
        winner_current_switch_text = FONT.render("Aktuell", 1, (BLACK))
        window.blit(winner_current_switch_text, (735, 418))
    else:
        winner_current_switch_text_winners = FONT.render("Gewinner", 1, (BLACK))
        window.blit(winner_current_switch_text_winners, (719, 418))

    pygame.draw.rect(window, (BUTTON_GREY), NEXT_POSITIVE_BUTTON_BOTTOM)
    next_positive_button_bottom_text = FONT.render("Nächster", 1, (BLACK))
    window.blit(next_positive_button_bottom_text, (1274,756))

    pygame.draw.rect(window, (BUTTON_GREY), NEXT_NEGATIVE_BUTTON_BOTTOM)
    next_negative_button_bottom_text = FONT.render("Zurück", 1, (BLACK))
    window.blit(next_negative_button_bottom_text, (734,756))

    pygame.draw.line(window, BLACK, (GAME_WIDTH, HEIGHT/2), (WIDTH, HEIGHT/2), 2)

    
def extract_weights(string):

    """ Extracts the weights out of the string containing the weights using regular expressions """

    pattern = r'weight=([-+]?\d*\.\d+|[-+]?\d+)'
    weights = re.findall(pattern, string)

    rounded_weights = []
    for weight in weights:
        rounded_weights.append(round(float(weight), 2))

    index_split = 6 * 4

    first_group = []
    for i in range(0, index_split, 4):
        first_group.append(rounded_weights[i:i+4])

    second_group = []
    for i in range(index_split, len(rounded_weights), 2):
        second_group.append(rounded_weights[i:i+2])

    structured_weights = [first_group, second_group]

    return structured_weights

def get_random_player_x(players):

    choosen_player = random.choice(players)
    
    return choosen_player.x

def create_initial_asteroids(players):

    """ Creates the asteroids at the beginning of the game """

    asteroids = []
    while len(asteroids) < MAX_ASTEROIDS:
        x = get_random_player_x(players)
        asteroids.append(Asteroid(x))

    return asteroids

def spawn_asteroids_per_frame(asteroids, players, num_asteroids):

    """ Spawns new asteroids"""

    count = 0
    for asteroid in asteroids:
        if asteroid.falling == False and count < num_asteroids:
            asteroid.x = get_random_player_x(players)
            asteroid.falling = True
            count += 1
        if count == num_asteroids:
            break

    return asteroids

def move_asteroids(asteroids):

    asteroids_to_remove = []

    for asteroid_ in asteroids:
        if asteroid_.falling:
            asteroid_.y += asteroid_.speed
            if asteroid_.y >= HEIGHT:
                asteroids_to_remove.append(asteroid_)

    for asteroid_ in asteroids_to_remove:
        asteroid_.falling = False
        asteroid_.y = random.uniform(-200, -90)
        global score
        score += 1

    return asteroids

def euclidean_distance(player, asteroid):

    dx = player.x - asteroid.x
    dy = player.y - asteroid.y

    return math.sqrt(dx**2 + dy**2)

def get_x_closest_asteroids(player, asteroids, x):

    """ Returns the x closests asteroids to a player (based on euclidean distance) """

    if x == MAX_ASTEROIDS:
        return asteroids

    # Calculate distances between player and each asteroid
    asteroid_distances = []
    for asteroid in asteroids:
        distance = euclidean_distance(player, asteroid)
        asteroid_distances.append((asteroid, distance))
    
    # Sort asteroids by distance
    sorted_asteroids = sorted(asteroid_distances, key=lambda x: x[1])

    # Return the x closest asteroids
    closest_asteroids = []
    for i in range(x):
        closest_asteroids.append(sorted_asteroids[i][0])
    
    return closest_asteroids

def get_x_y_from_asteroids(closet_asteroids):

    values = []

    for asteroid in closet_asteroids:
        values.extend([asteroid.x, asteroid.y])

    return values

def player_decision(players, asteroids, nets, ge):

    """ Sends the input vars to neat and moves the players based on the result of the output nodes"""

    for indx, player in enumerate(players):

        closest_asteroids = get_x_closest_asteroids(player, asteroids, CLOSESTS_ASTEROIDS)
        values = get_x_y_from_asteroids(closest_asteroids)
        input_data = [player.x, player.y]
        input_data.extend(values)

        # Activate the neural network with the modified input
        output = nets[indx].activate(input_data)

        if output[0] > 0.5:
            player.move_left()
        else:
            player.move_right()

        if output[1] > 0.5:
            player.move_up()
        else:
            player.move_down()

        ge[indx].fitness += 0.1

    return players, nets, ge

def detect_collision(rect1, rect2):
    return rect1.colliderect(rect2)

def collision(players, asteroids, nets, ge):

    """ Checks for collisions between a player and an asteroid, removes the player if he was hit """

    for indx, player in enumerate(players):
        player_hitbox = pygame.Rect(player.hitbox)

        player_dead = False
        # the player_dead check prevents a crash when a player is hit by two asteroids at the same time

        for asteroid in asteroids:
            asteroid_rect = pygame.Rect(asteroid.hitbox)
            if player_hitbox.colliderect(asteroid_rect):
                ge[indx].fitness -= 1  
                players.pop(indx)
                nets.pop(indx)
                ge.pop(indx)
                player_dead = True
            if player_dead:
                break

    if len(players) == 1 and len(winner_weights) < generation + 1:
        winner_weights.append(ge[0])

    return players, nets, ge

def adjust_highscore():

    global score
    global high_score

    if score > high_score:
        high_score = score

def game(genomes, config):

    """ Contains the logic for the game """

    global generation
    global current_winner_selected
    global mode_winner
    current_player_selected_net_top = 1
    current_player_selected_net_bottom = 1

    run_game = True
    click = False
    is_paused = False

    update_neural_net_top = True
    update_neural_net_bottom = True

    # Initialize lists for players, genomes, and neural networks
    players = [Player() for _ in range(len(genomes))]
    nets = [neat.nn.FeedForwardNetwork.create(g, config) for _, g in genomes]
    ge = [g for _, g in genomes]

    # give out colors
    for idx, player in enumerate(players):
        player.color = PLAYER_COLORS[idx]
        
    asteroids = create_initial_asteroids(players)

    # Set initial fitness values to zero for each genome
    for g in ge:
        g.fitness = 0

    asteroid_fps_spawn_counter = 0

    while run_game:

        if not is_paused:
            # contact neural net and move player
            players, nets, ge = player_decision(players, asteroids, nets, ge)

            asteroid_fps_spawn_counter += 1
            # spawn new asteroids every X frames (number is found in settings.py)
            if asteroid_fps_spawn_counter > FRAMES_PER_ASTEROID:
                asteroids = spawn_asteroids_per_frame(asteroids, players, 1)
                asteroid_fps_spawn_counter = 0

            # move and remove asteroids when off screen
            asteroids = move_asteroids(asteroids)

            # handle collision between players and asteroids
            players, nets, ge = collision(players, asteroids, nets, ge)

            adjust_highscore()

            if len(players) <= 0:
                global score
                score = 0
                generation += 1
                run_game = False
                break

        mx, my = pygame.mouse.get_pos() 
        if PAUSE_BUTTON.collidepoint((mx, my)):
            if click:
                is_paused = not is_paused

        if NEXT_POSITIVE_BUTTON_TOP.collidepoint((mx,my)):
            if click:
                current_player_selected_net_top += 1

                if current_player_selected_net_top > len(players):
                    current_player_selected_net_top = 1

                update_neural_net_top = True

        if NEXT_NEGATIVE_BUTTON_TOP.collidepoint((mx,my)):
            if click:
                current_player_selected_net_top -= 1

                if current_player_selected_net_top <= 1:
                    current_player_selected_net_top = len(players)

                update_neural_net_top = True

        if WINNER_CURRENT_SWITCH_BUTTON.collidepoint((mx,my)):
            if click and len(winner_weights) > 0:
                mode_winner = not mode_winner
                update_neural_net_bottom = True

        if NEXT_POSITIVE_BUTTON_BOTTOM.collidepoint((mx,my)):
            if click:
                if mode_winner and len(winner_weights) > 0:
                    current_winner_selected += 1

                    if current_winner_selected == len(winner_weights):
                        current_winner_selected = 0
                else:
                    current_player_selected_net_bottom += 1

                    if current_player_selected_net_bottom > len(players):
                        current_player_selected_net_bottom = 1

                update_neural_net_bottom = True

        if NEXT_NEGATIVE_BUTTON_BOTTOM.collidepoint((mx,my)):
            if click:

                if mode_winner and len(winner_weights) > 0:
                    current_winner_selected -= 1
                    if current_winner_selected < 0:
                        current_winner_selected = len(winner_weights) - 1 

                else:
                    current_player_selected_net_bottom -= 1

                    if current_player_selected_net_bottom <= 1:
                        current_player_selected_net_bottom = len(players)

                update_neural_net_bottom = True

        click = False

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            if event.type == pygame.QUIT:
                run_game = False
                pygame.quit()
                sys.exit()

        clock.tick(120)  # limit the FPS

        show_game(players, asteroids, generation, is_paused, update_neural_net_top, update_neural_net_bottom)
        if update_neural_net_top:
            show_neural_net_top(players, ge, current_player_selected_net_top)
        if update_neural_net_bottom:
            show_neural_net_bottom(players, ge, current_player_selected_net_bottom)
        update_neural_net_top = False
        update_neural_net_bottom = False
        pygame.display.flip()
    
if __name__ == "__main__":
    main_menu()