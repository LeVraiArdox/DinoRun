import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GROUND_HEIGHT = 300 

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKYBLUE = (135, 206, 235)
GROUND = (160, 82, 45)
RED = (255, 0, 0)
CACTUSGREEN = (0, 128, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Dino Game')
clock = pygame.time.Clock()

# Dino class
class Dino:
    def __init__(self):
        # Load multiple dino images
        self.run_images = pygame.image.load('dino_run.png')
        self.jump_image = pygame.image.load('dino.png')
        self.crouch_image = pygame.image.load('dino_crouch.png')
        
        # Scale images to consistent size
        self.run_images = pygame.transform.scale(self.run_images, (100, 100))
        self.jump_image = pygame.transform.scale(self.jump_image, (100, 100))
        self.crouch_image = pygame.transform.scale(self.crouch_image, (100, 50))
        
        self.current_image = self.run_images
        
        # Position and physics
        self.rect = self.current_image.get_rect()
        self.rect.x = 50
        self.rect.bottom = GROUND_HEIGHT
        self.velocity = 0
        self.gravity = 0.5
        self.jump_strength = -15
        self.is_jumping = False
        self.is_crouching = False

    def jump(self):
        if not self.is_jumping:
            self.velocity = self.jump_strength
            self.is_jumping = True
            
    def crouch(self):
        self.current_image = self.crouch_image
        self.rect.height = 50
        self.rect.width = 100
        self.rect.y = GROUND_HEIGHT + 50
        self.is_crouching = True

    def update(self):
        if self.is_jumping:
            self.current_image = self.jump_image
        elif self.is_crouching:
            self.current_image = self.crouch_image
        elif not self.is_jumping and not self.is_crouching:
            self.current_image = self.run_images

        # Apply gravity
        self.velocity += self.gravity
        self.rect.y += self.velocity

        # Ground collision
        if self.rect.bottom >= GROUND_HEIGHT:
            self.rect.bottom = GROUND_HEIGHT
            self.velocity = 0
            self.is_jumping = False
        
        # Use jump image when in air
        if self.is_jumping:
            self.current_image = self.jump_image

    def draw(self, screen):
        screen.blit(self.current_image, self.rect)

# Obstacle class
class Obstacle:
    def __init__(self):
        self.image = pygame.image.load('tower.png')
        self.image = pygame.transform.scale(self.image, (50, 125))
        self.rect = self.image.get_rect()
        self.rect.width -= 25
        self.rect.x = SCREEN_WIDTH
        self.rect.bottom = GROUND_HEIGHT
        self.speed = 5

    def update(self):
        self.rect.x -= self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
        
class Bird:
    def __init__(self):
        self.image = pygame.image.load('plane.png')
        self.image = pygame.transform.scale(self.image, (150, 50))
        self.rect = self.image.get_rect()
        self.rect.width -= 25
        self.rect.x = SCREEN_WIDTH
        self.rect.bottom = GROUND_HEIGHT
        self.speed = 5

    def update(self):
        self.rect.x -= self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.rect.y = 175
        
class DinoGame:
    def __init__(self):
        self.dino = Dino()
        self.obstacles = []
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.game_over = False
        self.ground_pos_x = 0


    def spawn_obstacle(self):
        if len(self.obstacles) == 0 or self.obstacles[-1].rect.x < SCREEN_WIDTH - random.randint(300, 2000):
            self.obstacles.append(Obstacle())
            
    def spawn_bird(self):
        if len(self.obstacles) == 0 or self.obstacles[-1].rect.x < SCREEN_WIDTH - random.randint(300, 2000):
            self.obstacles.append(Bird())
                    
    def check_collision(self):
        for obstacle in self.obstacles:
            if self.dino.rect.colliderect(obstacle.rect):
                self.game_over = True

    def update(self):
        if not self.game_over:
            self.dino.update()
            self.ground_pos_x -= 5
            
            if self.ground_pos_x <= -SCREEN_WIDTH:
                self.ground_pos_x = 0
                
            
            # Update and remove off-screen obstacles
            for obstacle in self.obstacles[:]:
                obstacle.update()
                if obstacle.rect.right < 0:
                    self.obstacles.remove(obstacle)
                    self.score += 1

            self.spawn_obstacle()
            self.spawn_bird()
            self.check_collision()

    def draw(self):
        self.sky_texture = pygame.image.load('sky.png')
        screen.fill(SKYBLUE)
        sky_tex = pygame.transform.scale(self.sky_texture, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(sky_tex, (0, 0))
        
        
        # Draw ground
        self.ground_texture = pygame.image.load('sand.png')
        
        ground_tex = pygame.transform.scale(self.ground_texture, (SCREEN_WIDTH*3, SCREEN_HEIGHT - GROUND_HEIGHT))
        pygame.draw.rect(screen, GROUND, pygame.Rect(0, GROUND_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT))
        screen.blit(ground_tex, (self.ground_pos_x, GROUND_HEIGHT))
        
        self.dino.draw(screen)
        
        for obstacle in self.obstacles:
            obstacle.draw(screen)
        
        # Draw score
        score_text = self.font.render(f'Score: {self.score}', True, BLACK)
        screen.blit(score_text, (10, 10))

        if self.game_over:
            game_over_text = self.font.render('Game Over! Press R to Restart', True, RED)
            screen.blit(game_over_text, (SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 - 50))

# Main game loop
def main():
    game = DinoGame()
    running = True

    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.dino.jump()
                    
                if event.key == pygame.K_DOWN:
                    game.dino.crouch()
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    game.dino.rect.height = 100
                    game.dino.rect.width = 100
                    game.dino.rect.y = GROUND_HEIGHT - 100
                    game.dino.is_crouching = False
                    
                                    
                if game.game_over and event.key == pygame.K_r:
                    # Restart the game
                    game = DinoGame()

        game.update()
        game.draw()
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# Run the game
if __name__ == "__main__":
    main()