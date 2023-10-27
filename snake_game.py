import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE
SNAKE_SPEED = 10

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# Direction
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Initialize the clock
clock = pygame.time.Clock()

# Initialize the snake
snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
snake_direction = RIGHT

# Initialize scoring
score = 0

# Initialize game over flag and trials
game_over = False
trials = 3

# Function to generate random food color and position
def generate_food():
    food_color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    food_position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    return food_color, food_position

# Initialize the first food
food_color, food_position = generate_food()

# Function to display text with center alignment
def draw_centered_text(text, y_offset, font_size=36, color=BLACK):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(text_surface, text_rect)

# Main game loop
while trials > 0:
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_direction != DOWN:
                    snake_direction = UP
                elif event.key == pygame.K_DOWN and snake_direction != UP:
                    snake_direction = DOWN
                elif event.key == pygame.K_LEFT and snake_direction != RIGHT:
                    snake_direction = LEFT
                elif event.key == pygame.K_RIGHT and snake_direction != LEFT:
                    snake_direction = RIGHT

        # Move the snake
        new_head = (snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1])

        # Check for collisions with the walls
        if (
            new_head[0] < 0
            or new_head[0] >= GRID_WIDTH
            or new_head[1] < 0
            or new_head[1] >= GRID_HEIGHT
        ):
            trials -= 1
            game_over = True

        # Check for collisions with itself
        if new_head in snake:
            trials -= 1
            game_over = True

        # Check for collisions with food
        if new_head == food_position:
            score += 1
            snake.insert(0, food_position)
            food_color, food_position = generate_food()
        else:
            snake.insert(0, new_head)
            snake.pop()

        # Draw the background
        screen.fill(WHITE)

        # Draw the snake
        for segment in snake:
            pygame.draw.circle(screen, GREEN, (segment[0] * GRID_SIZE + GRID_SIZE // 2, segment[1] * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE // 2)

        # Draw the snake's head with eyes
        head_x, head_y = snake[0]
        pygame.draw.circle(screen, BLACK, (head_x * GRID_SIZE + 0.3 * GRID_SIZE, head_y * GRID_SIZE + 0.3 * GRID_SIZE), 2)
        pygame.draw.circle(screen, BLACK, (head_x * GRID_SIZE + 0.7 * GRID_SIZE, head_y * GRID_SIZE + 0.3 * GRID_SIZE), 2)

        # Draw the food
        food_x, food_y = food_position
        pygame.draw.circle(screen, food_color, (food_x * GRID_SIZE + GRID_SIZE // 2, food_y * GRID_SIZE + GRID_SIZE // 2), 7)

        # Update the display
        pygame.display.update()

        # Control the snake's speed
        clock.tick(SNAKE_SPEED)

    # Game over screen
    screen.fill(WHITE)

    if trials > 0:
        draw_centered_text("Game Over", -50)
        draw_centered_text(f"Trials Remaining: {trials}", 50, color=GREEN)
        draw_centered_text("Press SPACE to Play Again", 100, font_size=24, color=GRAY)
    else:
        no_more_trials_text = font.render("No more trials", True, BLACK)
        no_more_trials_rect = no_more_trials_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        screen.blit(no_more_trials_text, no_more_trials_rect)

    # Display the score on top
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.update()

    # Wait for a key press to start a new game
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and trials > 0:
                snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
                snake_direction = RIGHT
                food_color, food_position = generate_food()
                game_over = False
                score = 0

# Quit Pygame when all trials are exhausted
pygame.quit()
sys.exit()
