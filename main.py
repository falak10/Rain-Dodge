import pygame
import time
import random
pygame.font.init()
#----------------------------------------------------------------------------------------
# Window properties
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rain Dodge")
#----------------------------------------------------------------------------------------
# Load the images and scale them to the desired sizes
bg_image = pygame.transform.scale(pygame.image.load("backgroundcat.jpg"), (WIDTH, HEIGHT))
player_image = pygame.transform.scale(pygame.image.load("player_image.png"), (60, 60))
rain_image = pygame.transform.scale(pygame.image.load("rain_image.png"), (30, 30))
player_velo = 5
rain_velo = 3
font = pygame.font.SysFont("san-serief", 30)
#----------------------------------------------------------------------------------------
# Add the images on the screen - player, rain, and text
def draw(player, elapsed_time, rains):
    WIN.blit(bg_image, (0, 0))
    time_text = font.render(f"time:{round(elapsed_time)}s", 1, "black")
    WIN.blit(time_text, (10, 10))
    WIN.blit(player_image, (player.x, player.y))

    for rain in rains:
        WIN.blit(rain_image, (rain.x, rain.y))

    pygame.display.update()
#----------------------------------------------------------------------------------------
# Window main loop
def main():
    run = True
    # Moving character
    player = pygame.Rect(200, HEIGHT - player_image.get_height(), player_image.get_width(), player_image.get_height())

    # adding timer on the screen
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    # adding rain
    rain_add_increment = 2000
    rain_count = 0

    rains = []
    hit = False

    move_left = False
    move_right = False
#----------------------------------------------------------------------------------------
    while run:
        # movement for frame and the rain generation
        rain_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if rain_count > rain_add_increment:
            for _ in range(4):
                rain_x = random.randint(0, WIDTH - rain_image.get_width())  # randomly generate the rain in the screen coordinate
                rain = pygame.Rect(rain_x, -rain_image.get_height(), rain_image.get_width(), rain_image.get_height())  # will make the rain come from above the screen
                rains.append(rain)

            rain_add_increment = max(200, rain_add_increment - 50)  # ensures that rain_add_increment is always at least 200
            rain_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_LEFT:
                    move_left = True
                elif event.key == pygame.K_RIGHT:
                    move_right = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    move_left = False
                elif event.key == pygame.K_RIGHT:
                    move_right = False

        # Update player position based on the key states
        if move_left and player.x - player_velo >= 0:
            player.x -= player_velo
        if move_right and player.x + player_velo + player_image.get_width() <= WIDTH:
            player.x += player_velo

        # move the rain independently
        for rain in rains[:]:  # making copy of the list to remove the rain that is no longer needed
            rain.y += rain_velo
            if rain.y > HEIGHT:
                rains.remove(rain)
            elif rain.colliderect(player):  # remove the rain if it hits the player
                rains.remove(rain)
                hit = True
                break
            
        if hit: #when the player get hit stop and display the following text
            lost_text = font.render("YOU LOST!", 1,"black")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2)) # to make the text appear in the center of the screen
            pygame.display.update()
            pygame.time.delay(4000)
            break   

        draw(player, elapsed_time, rains)

    pygame.quit()

# To run the file directly
if __name__ == "__main__":
    main()