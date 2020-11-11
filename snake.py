# 1) Making the necessary imports.
import random
import pygame

# 2) Gameplay object creation.
class Gameplay():

    # 3) Constructor for snake and board.
    def __init__(self):
        # 3.1) Defining a board of 20 per 20.
        self.board = []

        for x in range(20):
            myArray = []
            for y in range(20):
                myArray.append(0)
            self.board.append(myArray)

        # 3.2) Some state variables for our snake.
        self.food = ()
        self.snakeBody = [(8,8)]
        self.direction = ""
        self.alive = True
    
    # 4) This function will handle input from the user.
    def controls(self):
        # 4.1) We need to make sure that the snake can not go back on itself. So if the snake is going in a direction, 
        #      his only options are to turn right or left based on the direction.
        if self.direction == "L" or self.direction == "R":
            if pygame.key.get_pressed()[pygame.K_UP]:
                self.direction = "U"
            elif pygame.key.get_pressed()[pygame.K_DOWN]:
                self.direction = "D"

        elif self.direction == "U" or self.direction == "D":
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                self.direction = "L"
            elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                self.direction = "R"
        
        # 4.2) At the begining of the game, the user will press the right key to get started.
        else:
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                self.direction = "R"

    # 5) This function will handle our snake.
    def snake(self):
        # 6) This function will generate food for our snake.
        def generateFood():
            # 6.1) The code will be executed only if there is no food available for our snake.
            # We will call two loops that will go through the board and see if the board square is empty.
            # We will add the square position to the emptyBoardSquares.
            if len(self.food) == 0:
                emptyBoardSquares = []
                for x in range(20):
                    for y in range(20):
                        if self.board[x][y] == 0:
                            emptyBoardSquares.append((x,y))
                # 6.2) Randomly pick a square to generate food on.
                self.food = emptyBoardSquares[random.randint(0, len(emptyBoardSquares) - 1)]
        
        # 7) This function will handle the snake's body
        def updateSnakeBody():
            # 7.1) This fitst part of code is to update the snake's body based on the direction he takes.
            #      To be more precise, we only need to update the head's position and make the rest follow.
            A = 0
            B = 0
            if  self.direction == "U":
                A = 0
                B = -1
            elif  self.direction == "D":
                A = 0
                B = 1
            if  self.direction == "R":
               A = 1
               B = 0
            elif  self.direction == "L":
                A = -1
                B = 0
            
            # 7.2) This second part of code is to make sure we end the game if the head's position is beyond the
            #      boundries we set upé
            X, Y = self.snakeBody[0]
            if X + A < 0 or X + A > 19 or Y + B < 0 or Y + B > 19:
                self.alive = False
            
            # 7.3) We execute this part of the code if the snake is in our boundries
            else:
                # 7.4) We are going to make a loop that goes through the snake's body and updates it based
                #      on the direction he takes.
                copiedSnakeBody = self.snakeBody
                snakeLength = len(self.snakeBody)
                for bodyPartNumber in range(snakeLength):
                    bodyPartNumber = -bodyPartNumber -1
                    # 7.5) If the bodypart is not the head, we start by the end of the list. After each turn, 
                    #      a body part's position will be equal to the body part that comes before it.
                    if bodyPartNumber != -snakeLength:
                        self.snakeBody[bodyPartNumber] = copiedSnakeBody[bodyPartNumber - 1]
                    # 7.6) The head will be updated based on the direction the user gives as input.
                    else:
                        X += A
                        Y += B
                        self.snakeBody[0] = (X,Y)
                # 7.7) Make sure that we end the game if the head is in colision with a body part.
                if self.snakeBody[0] in self.snakeBody[1:]:
                    self.alive = False
                # 7.8) If the head is currently at the position where the food is, we are going to duplicate the
                #      last point of the snake's body and erase the food.
                if (X, Y) == self.food:
                    self.snakeBody.append(self.snakeBody[-1])
                    self.food = ()

        # 8) This is the function than handles the board
        def updateBoard():
            # 8.1) We are going to recreate an empty board.
            emptyBoard = []
            for x in range(20):
                myArray = []
                for y in range(20):
                    myArray.append(0)
                emptyBoard.append(myArray)
            
            # 8.2) Adding the food to the board.
            emptyBoard[self.food[0]][self.food[1]] = "f"
            
            # 8.3) Adding the snake to the board and updating the board parameter of our object.
            for snakeBodyPart in self.snakeBody:
                emptyBoard[snakeBodyPart[0]][snakeBodyPart[1]] = "s"

            self.board = emptyBoard
        
        # 9) Calling all our functions in logical order.
        updateSnakeBody()
        generateFood()
        updateBoard()
    
    # 10) This function will update our screen with the updated snake's body.
    #     We have a different color for empty board cases, snake cases and food cases.
    def displayScreen(self):
        for x in range(20):
            for y in range(20):
                if self.board[x][y] == 0:
                    pygame.draw.rect(screen, (255, 143, 148), [x*20, y*20, 19,19])
                elif self.board[x][y] == "s":
                    pygame.draw.rect(screen, (12, 148, 0), [x*20, y*20, 19,19])
                elif self.board[x][y] == "f":
                    pygame.draw.rect(screen, (74, 101, 255), [x*20, y*20, 19,19])

# 11) Initializing the game and screen and controling the frame rate.
pygame.init()
screen = pygame.display.set_mode((400,400))
clock = pygame.time.Clock()

# 12) Instantiating the gameplay object.
game = Gameplay()


print("Start the game by pressing the right key. May god be with you!")

# 13) Setting up the main loop.
while game.alive:
    # 14) Closing the game if the user clicks "X".
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            game.alive = False 
    
    # 15) Calling all the functions we defined above.
    game.controls()
    game.snake()
    game.displayScreen()
    pygame.display.update()
    clock.tick(10)

# 16) Displaying the score (length of snake) and quitting the game proprely.
print("You are now absolutely dead, your score is : {}".format(len(game.snakeBody)))
pygame.quit()