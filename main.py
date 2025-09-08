import pygame
import random
import asyncio

pygame.font.init()

WIDTH,HEIGHT = 1000,750
WIN = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption("Pong 2")
FPS = 60

WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (128,128,128)
BLUE = (55,155,255)
RED = (255,55,55)

TIMER_FONT = pygame.font.SysFont("comicsans", 30)
EVENT_FONT = pygame.font.SysFont("comicsans", 55)

radius = 15

paddle_width, paddle_height = 18, 150
left_paddle_x, right_paddle_x = 85 - paddle_width//2, WIDTH - 85 - paddle_width//2

# time stuff
NEW_EVENT_TIME = 15
TIMER_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIMER_EVENT, NEW_EVENT_TIME*1000)

def draw_window(ball_x, ball_y, left_paddle_y, right_paddle_y, fog, remaining_seconds, event_name, BALL_COLOUR, ball2_x, ball2_y, left_score, right_score):
    WIN.fill(BLUE)

    pygame.draw.rect(WIN, BLACK, pygame.Rect(0, 117.5, WIDTH, 8))

    pygame.draw.circle(WIN, BALL_COLOUR, (ball_x, ball_y), radius)
    if event_name == "Double Trouble":
        pygame.draw.circle(WIN, BALL_COLOUR, (ball2_x, ball2_y), radius)

    pygame.draw.rect(WIN, BLACK, pygame.Rect(left_paddle_x, left_paddle_y, paddle_width, paddle_height))
    pygame.draw.rect(WIN, BLACK, pygame.Rect(right_paddle_x, right_paddle_y, paddle_width, paddle_height))

    if fog:
        pygame.draw.rect(WIN, GREY, pygame.Rect(WIDTH//4, 125, WIDTH//2, HEIGHT - 125))

    text = TIMER_FONT.render(f"New Event In: {remaining_seconds}", 1, WHITE)
    WIN.blit(text, (WIDTH - text.get_width() - 10, 10))
    event_text = EVENT_FONT.render(f"Current Event: {event_name}", 1, WHITE)
    WIN.blit(event_text, (20, 20))

    left_score_text = TIMER_FONT.render(f"Left Score: {left_score}", 1, WHITE)
    WIN.blit(left_score_text, (20, 130))
    right_score_text = TIMER_FONT.render(f"Right Score: {right_score}", 1, WHITE)
    WIN.blit(right_score_text, (WIDTH - right_score_text.get_width() - 20, 130))

    pygame.display.update()
    

async def main():
    run = True
    direction = [0, 1]
    angle = [0, 1, 2]
    special_event = [0, 1,1,1, 2,2,2, 3,3, 4,4, 5,5,5, 6,6,6, 7,7,7, 8,8,8] # 0 none, 1 fast paddles, 2 slow paddles, 3 fog, 4 fire ball,
                                                                              # 5 fast mode, 6 double trouble, 7 invisible wall, 8 random ball
    #special_event = [5] # for testing
    clock = pygame.time.Clock()
    ball_x, ball_y = WIDTH//2 - radius, HEIGHT//2 - radius
    ball_vel_x, ball_vel_y = 8, 8
    ball2_x, ball2_y = WIDTH//2 - radius, HEIGHT//2 - radius
    ball2_vel_x, ball2_vel_y = 8, 8
    left_paddle_y = right_paddle_y = HEIGHT//2 - paddle_height//2 + 62
    left_paddle_vel = right_paddle_vel = 0
    paddle_speed = 9
    fog = False
    countdown_seconds = NEW_EVENT_TIME  # Initial countdown duration
    start_ticks = pygame.time.get_ticks()
    event_name = "None"
    BALL_COLOUR = WHITE
    left_score = 0
    right_score = 0
    event_choice = 0
    past_event = 0

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    left_paddle_vel = -paddle_speed
                if event.key == pygame.K_s:
                    left_paddle_vel = paddle_speed
                if event.key == pygame.K_UP:
                    right_paddle_vel = -paddle_speed
                if event.key == pygame.K_DOWN:
                    right_paddle_vel = paddle_speed

            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_w, pygame.K_s):
                    left_paddle_vel = 0
                if event.key in (pygame.K_UP, pygame.K_DOWN):
                    right_paddle_vel = 0

            if event.type == TIMER_EVENT:
                countdown_seconds = NEW_EVENT_TIME  # Initial countdown duration
                start_ticks = pygame.time.get_ticks()
                paddle_speed = 9
                fog = False
                BALL_COLOUR = WHITE
                ball_vel_x = 8 if ball_vel_x > 0 else -8
                ball_vel_y = 8 if ball_vel_y > 0 else -8
                past_event = event_choice
                while event_choice == past_event:
                    event_choice = random.choice(special_event)
                    print("retry")
                if event_choice == 0:
                    event_name = "None"
                elif event_choice == 1:
                    paddle_speed = 24
                    event_name = "Fast Paddles"
                elif event_choice == 2:
                    paddle_speed = 6
                    event_name = "Slow Paddles"
                elif event_choice == 3:
                    fog = True
                    paddle_speed = 11
                    event_name = "Fog"
                elif event_choice == 4:
                    paddle_speed = 11
                    ball_vel_x *= 1.7
                    ball_vel_y *= 1.7
                    BALL_COLOUR = RED
                    event_name = "Fire Ball"
                elif event_choice == 5:
                    paddle_speed = 18
                    ball_vel_x *= 1.4
                    ball_vel_y *= 1.4
                    event_name = "Fast Mode"
                elif event_choice == 6:
                    paddle_speed = 10
                    event_name = "Double Trouble"
                elif event_choice == 7:
                    event_name = "Invisible Wall"
                elif event_choice == 8:
                    event_name = "Random Ball"

        current_ticks = pygame.time.get_ticks()
        elapsed_seconds = (current_ticks - start_ticks) / 1000
        remaining_seconds = max(0, countdown_seconds - int(elapsed_seconds))

        if event_name == "Random Ball" and ball_x > 325 and ball_x < WIDTH - 325:
            if random.randint(1, 125) == 1:
                ball_vel_x *= -1
            if random.randint(1, 125) == 2:
                ball_vel_y *= -1

        # paddle movement
        if left_paddle_y < 125:
            left_paddle_y = 125
        if left_paddle_y >= HEIGHT - paddle_height:
            left_paddle_y = HEIGHT - paddle_height
        if right_paddle_y < 125:
            right_paddle_y = 125
        if right_paddle_y >= HEIGHT - paddle_height:
            right_paddle_y = HEIGHT - paddle_height

        # ball movement
        if ball_y - radius <= 125 or ball_y + radius >= HEIGHT:
            ball_vel_y *= -1
        if ball_x - radius <= 0:
            ball_x, ball_y = WIDTH//2 - radius, HEIGHT//2 - radius
            print("SCORE RIGHT")
            right_score += 1
            dir = random.choice(direction)
            ang = random.choice(angle)
            if dir == 0:
                if ang == 0:
                    ball_vel_x, ball_vel_y = 7.5, -9
                elif ang == 1:
                    ball_vel_x, ball_vel_y = 7.5, -7.5
                elif ang == 2:
                    ball_vel_x, ball_vel_y = 9, -7.5
            elif dir == 1:
                if ang == 0:
                    ball_vel_x, ball_vel_y = 7.5, 9
                elif ang == 1:
                    ball_vel_x, ball_vel_y = 7.5, 7.5
                elif ang == 2:
                    ball_vel_x, ball_vel_y = 9, 7.5
            if event_name == "Fast Mode":
                ball_vel_x *= 1.5
                ball_vel_y *= 1.5
            if event_name == "Fire Ball":
                ball_vel_x *= 1.7
                ball_vel_y *= 1.7

        if ball_x + radius >= WIDTH:
            ball_x, ball_y = WIDTH//2 - radius, HEIGHT//2 - radius
            print("SCORE LEFT")
            left_score += 1
            dir = random.choice(direction)
            ang = random.choice(angle)
            if dir == 0:
                if ang == 0:
                    ball_vel_x, ball_vel_y = 7.5, -9
                elif ang == 1:
                    ball_vel_x, ball_vel_y = 7.5, -7.5
                elif ang == 2:
                    ball_vel_x, ball_vel_y = 9, -7.5
            elif dir == 1:
                if ang == 0:
                    ball_vel_x, ball_vel_y = 7.5, 9
                elif ang == 1:
                    ball_vel_x, ball_vel_y = 7.5, 7.5
                elif ang == 2:
                    ball_vel_x, ball_vel_y = 9, 7.5
            ball_vel_x *= -1
            if event_name == "Fast Mode":
                ball_vel_x *= 1.5
                ball_vel_y *= 1.5
            if event_name == "Fire Ball":
                ball_vel_x *= 1.7
                ball_vel_y *= 1.7


        # second ball for double trouble
        if event_name == "Double Trouble":
            if ball2_y - radius <= 125 or ball2_y + radius >= HEIGHT:
                ball2_vel_y *= -1
            if ball2_x - radius <= 0:
                ball2_x, ball2_y = WIDTH//2 - radius, HEIGHT//2 - radius
                print("SCORE RIGHT")
                right_score += 1
                dir = random.choice(direction)
                ang = random.choice(angle)
                if dir == 0:
                    if ang == 0:
                        ball2_vel_x, ball2_vel_y = 5, -6
                    elif ang == 1:
                        ball2_vel_x, ball2_vel_y = 5, -5
                    elif ang == 2:
                        ball2_vel_x, ball2_vel_y = 6, -5
                elif dir == 1:
                    if ang == 0:
                        ball2_vel_x, ball2_vel_y = 5, 6
                    elif ang == 1:
                        ball2_vel_x, ball2_vel_y = 5, 5
                    elif ang == 2:
                        ball2_vel_x, ball2_vel_y = 6, 5

            if ball2_x + radius >= WIDTH:
                ball2_x, ball2_y = WIDTH//2 - radius, HEIGHT//2 - radius
                print("SCORE LEFT")
                left_score += 1
                dir = random.choice(direction)
                ang = random.choice(angle)
                if dir == 0:
                    if ang == 0:
                        ball2_vel_x, ball2_vel_y = 5, -6
                    elif ang == 1:
                        ball2_vel_x, ball2_vel_y = 5, -5
                    elif ang == 2:
                        ball2_vel_x, ball2_vel_y = 6, -5
                elif dir == 1:
                    if ang == 0:
                        ball2_vel_x, ball2_vel_y = 5, 6
                    elif ang == 1:
                        ball2_vel_x, ball2_vel_y = 5, 5
                    elif ang == 2:
                        ball2_vel_x, ball2_vel_y = 6, 5
                ball2_vel_x *= -1
        else:
            ball2_x, ball2_y = WIDTH//2 - radius, HEIGHT//2 - radius

        ball_x += ball_vel_x
        ball_y += ball_vel_y
        ball2_x += ball2_vel_x
        ball2_y += ball2_vel_y
        left_paddle_y += left_paddle_vel
        right_paddle_y += right_paddle_vel

        if left_paddle_x <= ball_x <= left_paddle_x + paddle_width:
            if left_paddle_y <= ball_y <= left_paddle_y + paddle_height:
                ball_x = left_paddle_x + paddle_width
                ball_vel_x *= -1

        if right_paddle_x <= ball_x <= right_paddle_x + paddle_width:
            if right_paddle_y <= ball_y <= right_paddle_y + paddle_height:
                ball_x = right_paddle_x
                ball_vel_x *= -1

        if event_name == "Invisible Wall":
            if WIDTH//2 - 5 <= ball_x <= WIDTH//2 + 5:
                if 200 <= ball_y <= 500:
                    ball_vel_x *= -1

        if event_name == "Double Trouble":
            if left_paddle_x <= ball2_x <= left_paddle_x + paddle_width:
                if left_paddle_y <= ball2_y <= left_paddle_y + paddle_height:
                    ball2_x = left_paddle_x + paddle_width
                    ball2_vel_x *= -1

            if right_paddle_x <= ball2_x <= right_paddle_x + paddle_width:
                if right_paddle_y <= ball2_y <= right_paddle_y + paddle_height:
                    ball2_x = right_paddle_x
                    ball2_vel_x *= -1

        draw_window(ball_x, ball_y, left_paddle_y, right_paddle_y, fog, remaining_seconds, event_name, BALL_COLOUR, ball2_x, ball2_y, left_score, right_score)
        await asyncio.sleep(0)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())