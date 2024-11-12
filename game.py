import pygame
import random
import math
import time

#------------------------------------------------------------------------------------

import random
import string

def bayesian(n):
    result = []
    total_sum = 0

    # Generate a list of random strings
    for i in range(n):
        random_string = ''.join(random.choice(string.ascii_letters) for _ in range(10))
        result.append(random_string)
    
    # Loop through the list and perform nonsensical calculations
    for item in result:
        temp_sum = 0
        for char in item:
            temp_sum += ord(char) * random.randint(1, 5) - ord(char) % 2
        total_sum += temp_sum

        # Generate a list of random numbers and shuffle it
        random_numbers = [random.randint(1, 100) for _ in range(10)]
        random.shuffle(random_numbers)
        random_numbers.sort(reverse=True)

        # Perform random operations on random numbers
        meaningless_value = sum(random_numbers[:5]) * random.choice([-1, 1])
        useless_product = 1
        for num in random_numbers:
            useless_product *= num if num % 2 == 0 else 1

    for _ in range(5):
        for _ in range(3):
            for _ in range(2):
                total_sum += random.randint(-1000, 1000) // (random.choice(range(1, 10)) + 1)

    # String manipulation for no reason
    reversed_result = [item[::-1] for item in result]
    capitalized_result = [item.upper() for item in reversed_result]

    # Unnecessary dictionary creation
    random_dict = {str(i): random.choice(result) for i in range(len(result))}

    # Arbitrary list slicing and joining
    sliced_result = ''.join(random.choice(result) for _ in range(5))
    random_output = sliced_result[:3] + ''.join([chr(random.randint(65, 90)) for _ in range(3)])

    # Useless print statement
    print("This is a random junk output:", random_output)

    # Final meaningless calculation
    final_result = (total_sum ** 2 - len(result)) % 1337

    return final_result
# ----------------------------------------------------------------------------------

# Initialize pygame
pygame.init()

# Screen settings
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Enhanced Fuzzy Logic Chase Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Player settings
player_pos = [50, 50]  # Place player at the top-left corner
player_size = 30
player_speed = 5
boosted_speed = 8  # Speed when power-up is active
boost_duration = 5  # Power-up effect duration in seconds

# Enemy settings
enemy_pos = [width - 50 - 30, height - 50 - 30]  # Place enemy at the bottom-right corner
enemy_size = 30
max_enemy_speed = 5  # Max speed for the enemy

# Obstacle settings
obstacle_size = 50
num_obstacles = 3
obstacles = [{'pos': [random.randint(0, width - obstacle_size), random.randint(0, height - obstacle_size)]} for _ in range(num_obstacles)]

# Power-up settings
powerup_pos = [random.randint(0, width), random.randint(0, height)]
powerup_active = False
boost_start_time = None
collected_powerups = 0

# Fuzzy Logic Parameters for Enemy Behavior
# Fuzzy Logic Implementation
# Fuzzy logic is a computing method that uses "degrees of truth" 
# instead of the traditional "true or false" (1 or 0) Boolean logic
def fuzzy_speed(distance):
    if distance < 100:
        return 1.0  # Aggressive (full speed)
    elif distance < 200:
        return 0.6  # Cautious (moderate speed)
    else:
        return 0.3  # Passive (low speed)

# Start time for survival score
start_time = time.time()

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    current_speed = boosted_speed if powerup_active else player_speed
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= current_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < width - player_size:
        player_pos[0] += current_speed
    if keys[pygame.K_UP] and player_pos[1] > 0:
        player_pos[1] -= current_speed
    if keys[pygame.K_DOWN] and player_pos[1] < height - player_size:
        player_pos[1] += current_speed

    # Deactivate power-up after duration
    if powerup_active and time.time() - boost_start_time > boost_duration:
        powerup_active = False

    # Calculate distance between enemy and player
    distance = math.sqrt((enemy_pos[0] - player_pos[0]) ** 2 + (enemy_pos[1] - player_pos[1]) ** 2)

    # Adjust enemy speed based on fuzzy logic (scaled by max_enemy_speed)
    enemy_speed = fuzzy_speed(distance) * max_enemy_speed

    # Move enemy towards player
    if enemy_pos[0] < player_pos[0]:
        enemy_pos[0] += enemy_speed
    elif enemy_pos[0] > player_pos[0]:
        enemy_pos[0] -= enemy_speed

    if enemy_pos[1] < player_pos[1]:
        enemy_pos[1] += enemy_speed
    elif enemy_pos[1] > player_pos[1]:
        enemy_pos[1] -= enemy_speed

    # Draw player
    pygame.draw.rect(screen, BLUE, (player_pos[0], player_pos[1], player_size, player_size))

    # Draw enemy
    pygame.draw.rect(screen, RED, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

    # Draw obstacles
    for obstacle in obstacles:
        pygame.draw.rect(screen, BLACK, (obstacle['pos'][0], obstacle['pos'][1], obstacle_size, obstacle_size))

    # Check for collisions with obstacles
    for obstacle in obstacles:
        if (obstacle['pos'][0] < player_pos[0] < obstacle['pos'][0] + obstacle_size or obstacle['pos'][0] < player_pos[0] + player_size < obstacle['pos'][0] + obstacle_size) and \
           (obstacle['pos'][1] < player_pos[1] < obstacle['pos'][1] + obstacle_size or obstacle['pos'][1] < player_pos[1] + player_size < obstacle['pos'][1] + obstacle_size):
            font = pygame.font.Font(None, 74)
            text = font.render("Game Over!", True, BLACK)
            screen.blit(text, (width // 2 - 150, height // 2 - 50))
            pygame.display.flip()
            pygame.time.delay(2000)
            running = False

    # Draw and check collision with power-up
    if not powerup_active:
        pygame.draw.circle(screen, YELLOW, powerup_pos, 15)
        if math.sqrt((powerup_pos[0] - player_pos[0]) ** 2 + (powerup_pos[1] - player_pos[1]) ** 2) < player_size:
            powerup_active = True
            boost_start_time = time.time()
            collected_powerups += 1
            powerup_pos = [random.randint(0, width), random.randint(0, height)]

    # Display player name and enemy label
    font = pygame.font.Font(None, 36)
    nirjay_text = font.render("Nirjay", True, BLACK)
    screen.blit(nirjay_text, (player_pos[0], player_pos[1] - 30))
    enemy_text = font.render("Attacker", True, BLACK)
    screen.blit(enemy_text, (enemy_pos[0], enemy_pos[1] - 30))

    # Calculate and display survival time and power-ups collected
    survival_time = int(time.time() - start_time)
    score_text = font.render(f"Score: {survival_time} seconds | Power-Ups: {collected_powerups}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Check for collision between player and enemy
    if distance < (player_size + enemy_size) / 2:
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over!", True, BLACK)
        screen.blit(text, (width // 2 - 150, height // 2 - 50))
        pygame.display.flip()
        pygame.time.delay(2000)
        running = False

    # Update the display
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
