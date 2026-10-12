# Balloon Shooting Game - Processing (Python Mode)
# Based on assignment A1 outline

import random

score = 0
start_time = 0
GAME_DURATION = 30  # 30 seconds
balloons = []
game_over = False


def create_balloon():
    r = random.uniform(15, 45)  # radius, smaller = more points
    return {
        "x": random.uniform(30, 570),
        "y": height + random.uniform(0, 200),
        "r": r,
        "speed": random.uniform(1.5, 4),
        "color": color(random.uniform(0, 255),
                        random.uniform(0, 255),
                        random.uniform(0, 255))
    }


def update_balloon(b):
    b["y"] -= b["speed"]


def display_balloon(b):
    w = b["r"] * 1.6      # balloon width
    h = b["r"] * 2.2      # balloon height (taller than wide, like a real balloon)

    # balloon body (tall ellipse shape)
    noStroke()
    fill(b["color"])
    ellipse(b["x"], b["y"], w, h)

    # small highlight for a 3D glossy look
    fill(255, 255, 255, 90)
    ellipse(b["x"] - w * 0.2, b["y"] - h * 0.3, w * 0.25, h * 0.15)

    # string (straight line)
    stroke(80)
    strokeWeight(1.5)
    line(b["x"], b["y"] + h * 0.48, b["x"], b["y"] + h * 0.48 + 35)


def is_out_of_bounds(b):
    return b["y"] + b["r"] < 0


def is_hit(b, mx, my):
    return dist(mx, my, b["x"], b["y"]) < b["r"]


def get_points(b):
    # smaller balloon = more points, larger balloon = fewer points
    # r ranges 15-45 -> points range roughly 5-1
    return int(map(b["r"], 15, 45, 5, 1))


def setup():
    size(600, 700)
    noCursor()
    reset_game()


def reset_game():
    global score, start_time, balloons, game_over
    score = 0
    start_time = millis()
    balloons = []
    game_over = False


def draw():
    global balloons, game_over

    background(30, 30, 40)

    elapsed = (millis() - start_time) / 1000.0
    time_left = GAME_DURATION - elapsed

    if time_left > 0:
        # spawn a new balloon occasionally
        if random.uniform(0, 1) < 0.03:
            balloons.append(create_balloon())

        # update and draw balloons, remove ones off screen
        for b in balloons[:]:
            update_balloon(b)
            display_balloon(b)
            if is_out_of_bounds(b):
                balloons.remove(b)

        # draw red crosshair
        draw_crosshair()

        # show score and remaining time
        fill(255)
        textSize(22)
        textAlign(LEFT, TOP)
        text("Score: " + str(score), 15, 15)
        textAlign(RIGHT, TOP)
        text("Time: " + str(int(max(time_left, 0))), width - 15, 15)
    else:
        game_over = True
        display_game_over()


def draw_crosshair():
    mx, my = mouseX, mouseY
    stroke(255, 0, 0)
    strokeWeight(3)
    line(mx - 8, my, mx + 8, my)
    line(mx, my - 8, mx, my + 8)


def display_game_over():
    fill(255)
    textAlign(CENTER, CENTER)
    textSize(48)
    text("GAME OVER", width / 2, height / 2 - 40)
    textSize(28)
    text("Final Score: " + str(score), width / 2, height / 2 + 10)
    textSize(18)
    text("Click to Restart", width / 2, height / 2 + 50)


def mousePressed():
    global score
    if game_over:
        reset_game()
        return

    for b in balloons[:]:
        if is_hit(b, mouseX, mouseY):
            score += get_points(b)
            balloons.remove(b)
            break
