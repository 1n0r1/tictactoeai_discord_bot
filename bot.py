from discord.ext import commands
import random

bot = commands.Bot(command_prefix='&')

board = [[1,2,3],[4,5,6],[7,8,9]]
tturn = [0]
ongoing = [False]

def showBoard():
    tore = ""
    for a in board:
        for b in a:
            tore += str(b)
            tore += " "
        tore += '\n'
    return tore

def playerMove(a):
    a = int(a)
    board[int((a - 1) / 3)][int((a - 1) % 3)] = "X"
    tturn[0] = tturn[0] + 1

def validMove(a):
    a = int(a)
    if (board[int((a - 1) / 3)][int((a - 1) % 3)] != "X" and board[int((a - 1) / 3)][int((a - 1) % 3)] != "O" and int(a) <= 9 and 1 <= int(a)):
        return True
    else:
        return False

def reset():
    for a in range(1, 10):
        board[int((a - 1) / 3)][int((a - 1) % 3)] = str(a)
    tturn[0] = 0

def result(a):
    if (a == "1"):
        return "Draw!"
    else:
        return a + " won!"

def botMove(a):
    board[int((a - 1) / 3)][int((a - 1) % 3)] = "O"
    tturn[0] = tturn[0] + 1
    return showBoard() + "Bot moved " + str(a)

def checkWin():
    for x in range(3):
        if (board[x][0] == board[x][1] and board[x][1] == board[x][2]):
            return board[x][0]
    for x in range(3):
        if (board[0][x] == board[1][x] and board[1][x] == board[2][x]):
            return board[0][x]
    if (board[0][0] == board[1][1] and board[1][1] == board[2][2]):
        return board[1][1]
    if (board[0][2] == board[1][1] and board[1][1] == board[2][0]):
        return board[1][1]
    if (tturn[0] == 9):
        return "1"
    return "0"

def botCalculate():
    availableMoves = []
    for x in range(1, 10):
        if (validMove(x)):
            availableMoves.append(x)
    return random.choice(availableMoves)

@bot.command(name="start", help="Start a match")
async def start(ctx):
    reset()
    ongoing[0] = True
    await ctx.send(showBoard())
    await ctx.send("Game start!")


@bot.command(name="move", help="Make your move; a is your move <1-9>")
async def move(ctx, a):
    if (ongoing[0]):
        if (validMove(a)):
            playerMove(a)
            await ctx.send(showBoard())
            await ctx.send("You moved " + str(a))
            if (checkWin() == "0"):
                await ctx.send(botMove(botCalculate()))
                if (checkWin() != "0"):
                    await ctx.send(result(checkWin()))
                    reset()
                    ongoing[0] = False
            else:
                await ctx.send(result(checkWin()))
                reset()
                ongoing[0] = False
        else:
            await ctx.send("Invalid move")
    else:
        await ctx.send("Start a game before you move! Use &start")


with open("BOT_TOKEN.txt", "r") as token_file:
    TOKEN = token_file.read()
    print("Token file read")
    bot.run(TOKEN)