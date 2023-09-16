import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BUBBLE_SIZE = 50
BACKGROUND_COLOR = (136, 187, 255)  # Light blue
POP_SOUND = pygame.mixer.Sound('pop.wav')
GAME_FONT = pygame.font.Font('ArchitectsDaughter-Regular.ttf', 36)

# Difficulty settings
DIFFICULTY_SETTINGS = {
    'easy': {'num_bubbles': 10, 'bubble_speed': 2, 'game_duration': 30},
    'medium': {'num_bubbles': 20, 'bubble_speed': 4, 'game_duration': 45},
    'hard': {'num_bubbles': 30, 'bubble_speed': 6, 'game_duration': 60},
    'extreme': {'num_bubbles': 40, 'bubble_speed': 8, 'game_duration': 90}
}

# Function to generate a random RGB color tuple
def generate_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Generate a list of 10 random RGB colors
BUBBLE_COLORS = [generate_random_color() for _ in range(10)]

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bubble Wrap Popping Challenge")


# Function to create a new bubble with a random color
def create_bubble():
    x = random.randint(0, SCREEN_WIDTH - BUBBLE_SIZE)
    y = random.randint(0, SCREEN_HEIGHT - BUBBLE_SIZE)
    vx = random.randint(-5, 5)
    vy = random.randint(-5, 5)
    color = random.choice(BUBBLE_COLORS)
    return pygame.Rect(x, y, BUBBLE_SIZE, BUBBLE_SIZE), (vx, vy), color


# Function to display the title screen and select difficulty
def title_screen():
    title_font = pygame.font.Font('ArchitectsDaughter-Regular.ttf', 45)
    instruction_font = pygame.font.Font('ArchitectsDaughter-Regular.ttf', 20)

    title_text = title_font.render("Bubble Wrap Popping Game", True, (0, 0, 0))
    easy_text = instruction_font.render("Press 'E' for Easy", True, (0, 0, 0))
    medium_text = instruction_font.render("Press 'M' for Medium", True, (0, 0, 0))
    hard_text = instruction_font.render("Press 'H' for Hard", True, (0, 0, 0))
    extreme_text = instruction_font.render("Press 'X' for Extreme", True, (0, 0, 0))

    screen.fill(BACKGROUND_COLOR)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - 280, 100))
    screen.blit(easy_text, (SCREEN_WIDTH // 2 - 100, 250))
    screen.blit(medium_text, (SCREEN_WIDTH // 2 - 100, 300))
    screen.blit(hard_text, (SCREEN_WIDTH // 2 - 100, 350))
    screen.blit(extreme_text, (SCREEN_WIDTH // 2 - 100, 400))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    return 'easy'
                elif event.key == pygame.K_m:
                    return 'medium'
                elif event.key == pygame.K_h:
                    return 'hard'
                elif event.key == pygame.K_x:
                    return 'extreme'


# Function to display buttons
def draw_button(screen, text, position, size, background_color, text_color):
    button_rect = pygame.Rect(position, size)
    pygame.draw.rect(screen, background_color, button_rect)

    text_surface = GAME_FONT.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=button_rect.center)

    screen.blit(text_surface, text_rect)

    return button_rect


# Game loop
while True:
    selected_difficulty = title_screen()
    difficulty_settings = DIFFICULTY_SETTINGS[selected_difficulty]
    num_bubbles = difficulty_settings['num_bubbles']
    bubble_speed = difficulty_settings['bubble_speed']
    game_duration = difficulty_settings['game_duration']

    # Create the initial bubbles
    bubbles = []
    bubble_velocities = []
    bubble_colors = []
    for _ in range(num_bubbles):
        bubble, velocity, color = create_bubble()
        bubbles.append(bubble)
        bubble_velocities.append(velocity)
        bubble_colors.append(color)

    # Game variables
    score = 0
    game_over = False
    paused = False
    retry_button_pressed = False
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not paused and not retry_button_pressed:
                for i, bubble in enumerate(bubbles):
                    if bubble.collidepoint(event.pos):
                        bubbles.pop(i)
                        bubble_velocities.pop(i)
                        bubble_colors.pop(i)
                        score += 1
                        POP_SOUND.play()
                        break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_r and game_over:
                    retry_button_pressed = True
                    break
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        if not game_over:
            screen.fill(BACKGROUND_COLOR)

            # Update bubble positions
            for i, bubble in enumerate(bubbles):
                if not paused:
                    bubble.x += bubble_velocities[i][0] * bubble_speed
                    bubble.y += bubble_velocities[i][1] * bubble_speed

                    # Bounce off screen edges
                    if bubble.left < 0 or bubble.right > SCREEN_WIDTH:
                        bubble_velocities[i] = (-bubble_velocities[i][0], bubble_velocities[i][1])
                    if bubble.top < 0 or bubble.bottom > SCREEN_HEIGHT:
                        bubble_velocities[i] = (bubble_velocities[i][0], -bubble_velocities[i][1])

                # Draw bubbles with colors
                pygame.draw.ellipse(screen, bubble_colors[i], bubble)

            # Draw score
            score_text = GAME_FONT.render(f"Score: {score}", True, (0, 0, 0))
            screen.blit(score_text, (10, 10))

            # Draw time remaining
            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
            remaining_time = max(0, game_duration - elapsed_time)
            time_text = GAME_FONT.render(f"Time: {remaining_time}", True, (0, 0, 0))
            screen.blit(time_text, (SCREEN_WIDTH - 150, 10))

            # Draw pause/resume button
            if not retry_button_pressed:
                button_color = (0, 255, 0) if paused else (255, 0, 0)
                button_text = "Resume" if paused else "Pause"
                button_rect = draw_button(screen, button_text, (10, SCREEN_HEIGHT - 40), (100, 30), button_color,
                                          (0, 0, 0))
                if button_rect.collidepoint(pygame.mouse.get_pos()):
                    if pygame.mouse.get_pressed()[0]:
                        paused = not paused

            # Check for game over
            if elapsed_time >= game_duration:
                game_over = True

            # Draw retry button
            if game_over:
                retry_button_rect = draw_button(screen, "Retry", (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 20),
                                                (100, 30), (0, 0, 255), (255, 255, 255))
                if retry_button_rect.collidepoint(pygame.mouse.get_pos()):
                    if pygame.mouse.get_pressed()[0]:
                        retry_button_pressed = True
                        break

            # Spawn a new bubble after each click (if not paused and not retrying)
            if not paused and not retry_button_pressed and not bubbles:
                bubble, velocity, color = create_bubble()
                bubbles.append(bubble)
                bubble_velocities.append(velocity)
                bubble_colors.append(color)

            pygame.display.flip()
            clock.tick(60)  # 60 frames per second

    # Game over screen
    while True:
        # Inside your game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Your existing game logic goes here

        # Update the display and maintain the music
        pygame.display.flip()
        pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
        pygame.event.set_allowed(pygame.constants.USEREVENT)
        pygame.event.set_allowed(pygame.QUIT)
        pygame.event.clear()
        clock.tick(60)  # 60 frames per second

        if retry_button_pressed:
            break

        game_over_text = GAME_FONT.render(f"Game Over! Score: {score}", True, (0, 0, 0))
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 50))
        pygame.display.flip()
