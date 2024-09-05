from tkinter import *
import random

GAME_WIDTH = 1100
GAME_HEIGHT = 850
SPEED = 50
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "green"
FOOD_COLOR = "red"
BACKGROUND_COLOR = "black"

class Snake:
    def __init__(self):
        self.bodySize = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0,0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, int(GAME_WIDTH/SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, int(GAME_HEIGHT/SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x,y]

        canvas.create_oval(x,y,x+SPACE_SIZE, y+SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def nextTurn(snake, food):

    if game_over:
        return

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE
    snake.coordinates.insert(0, (x,y))
    square = canvas.create_rectangle(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score

        score += 1

        label.config(text="Score:{}".format(score))

        canvas.delete("food")

        food = Food()

    else:
        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if checkCollision(snake):
        gameOver()

    window.after(SPEED, nextTurn, snake, food)

def changeDirection(newDirection):
    global direction

    if newDirection == 'left':
        if direction != 'right':
            direction = newDirection
    elif newDirection == 'right':
        if direction != 'left':
            direction = newDirection
    elif newDirection == 'up':
        if direction != 'down':
            direction = newDirection
    elif newDirection == 'down':
        if direction != 'up':
            direction = newDirection

def checkCollision(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for bodyPart in snake.coordinates[1:]:
        if x == bodyPart[0] and y == bodyPart[1]:
            return True

    return False

def gameOver():
    global game_over
    game_over = True
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas', 70), text="GAME OVER", fill="red", tag="gameOver")
def restartGame():
    global snake, food, score, direction, game_over

    canvas.delete(ALL)
    snake = Snake()
    food = Food()
    score = 0
    direction = 'down'
    game_over = False
    label.config(text="Score:{}".format(score))
    nextTurn(snake, food)

window = Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0
direction = 'down'
game_over = False

label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()

restartButton = Button(window, text="Restart", command=restartGame, font=('consolas', 20))
restartButton.place(x=0,y=0)

canvas = Canvas(window, bg = BACKGROUND_COLOR, height= GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_width/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Up>', lambda event: changeDirection('up'))
window.bind('<Down>', lambda event: changeDirection('down'))
window.bind('<Left>', lambda event: changeDirection('left'))
window.bind('<Right>', lambda event: changeDirection('right'))
window.bind('<space>', lambda event: restartGame())
snake = Snake()
food = Food()

nextTurn(snake, food)

window.mainloop()