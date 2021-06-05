import random

from discord.ext import commands


bot = commands.Bot(command_prefix='&')

board = [[1,2,3],[4,5,6],[7,8,9]]
tturn = [0]
ongoing = [False]
difficulty = [0]
def show_board():
    tore = ""
    for a in board:
        for b in a:
            tore += str(b)
            tore += " "
        tore += '\n'
    return tore

def player_move(a):
    a = int(a)
    board[int((a - 1) / 3)][int((a - 1) % 3)] = "X"
    tturn[0] = tturn[0] + 1

def valid_move(a):
    a = int(a)
    return (board[int((a - 1) / 3)][int((a - 1) % 3)] != "X"
    and board[int((a - 1) / 3)][int((a - 1) % 3)] != "O"
    and int(a) <= 9
    and int(a) >= 1)

def reset():
    for a in range(1, 10):
        board[int((a - 1) / 3)][int((a - 1) % 3)] = str(a)
    tturn[0] = 0

def result(a):
    if a == "1":
        return "Draw!"
    return a + " won!"

def bot_move(a):
    board[int((a - 1) / 3)][int((a - 1) % 3)] = "O"
    tturn[0] = tturn[0] + 1
    return show_board() + "Bot moved " + str(a)

def check_win():
    for x in range(3):
        if board[x][0] == board[x][1] and board[x][1] == board[x][2]:
            return board[x][0]
    for x in range(3):
        if board[0][x] == board[1][x] and board[1][x] == board[2][x]:
            return board[0][x]
    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        return board[1][1]
    if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        return board[1][1]
    if tturn[0] == 9:
        return "1"
    return "0"

def basic_win_and_block():
    available_moves = []
    for x in range(1, 10):
        if valid_move(x):
            available_moves.append(x)
    for x in available_moves:
        board[int((x - 1) / 3)][int((x - 1) % 3)] = "O"
        if check_win() == "O":
            board[int((x - 1) / 3)][int((x - 1) % 3)] = str(x)
            return x
        board[int((x - 1) / 3)][int((x - 1) % 3)] = str(x)
    for x in available_moves:
        board[int((x - 1) / 3)][int((x - 1) % 3)] = "X"
        if check_win() == "X":
            board[int((x - 1) / 3)][int((x - 1) % 3)] = str(x)
            return x
        board[int((x - 1) / 3)][int((x - 1) % 3)] = str(x)
    return -1

def random_move():
    available_moves = []
    for x in range(1, 10):
        if valid_move(x):
            available_moves.append(x)
    return random.choice(available_moves)

def attackable(a):
    count = 0
    for b in a:
        if board[int((b - 1) / 3)][int((b - 1) % 3)] == "O":
            count = count + 1
        if board[int((b - 1) / 3)][int((b - 1) % 3)] == "X":
            return False
    if count == 1:
        return True
    return False

def vulnerable(a):
    count = 0
    for b in a:
        if board[int((b - 1) / 3)][int((b - 1) % 3)] == "X":
            count = count + 1
        if board[int((b - 1) / 3)][int((b - 1) % 3)] == "O":
            return False
    if count == 1:
        return True
    return False

def advance_thinking():
    corner = [1, 3, 7, 9]
    non_diag = [[1,2,3],[4,5,6],[7,8,9],[1,4,7],[2,5,8],[3,6,9]]
    all_line = [[1,2,3],[4,5,6],[7,8,9],[1,4,7],[2,5,8],[3,6,9],[1,5,9],[3,5,7]]
    
    if valid_move(5):
        return 5
    if tturn[0] == 1 and board[1][1] == "X":
        return random.choice(corner)
    
    if (board[1][1] == "X" or tturn[0] == 3):
        move_list = []
        for a in non_diag:
            if (attackable(a)):
                move_list.append(a)
        if (move_list != []):
            tore = random.choice(random.choice(move_list))
            while not valid_move(tore):
                tore = random.choice(random.choice(move_list))
            return tore
    k = []
    possible_moves = []
    for a in all_line:
        if (vulnerable(a)):
            for kk in k:
                if list(set(kk).intersection(a)) != []:
                    possible_moves.append(list(set(kk).intersection(a)))
            k.append(a)
    return random.choice(random.choice(possible_moves))

def bot_calculate():
    if difficulty[0] > 0 and basic_win_and_block() != -1:
        return basic_win_and_block()
    if difficulty[0] > 1 and advance_thinking() != -1:
        return advance_thinking()
    return random_move()

@bot.command(name="start", help="Start a match; level: <0 - random move; 1 - have basic attack and block; 2 - unbeatable>")
async def start(ctx, level: int):
    reset()
    ongoing[0] = True
    difficulty[0] = level
    await ctx.send(show_board())
    await ctx.send("Game start! Level = " + str(level) + "! You(X) go first!")

@bot.command(name="showboard", help="Show current game")
async def showboard(ctx):
    if ongoing[0]:
        await ctx.send(show_board())
    else:
        await ctx.send("Start a game before you move! Use &start")

@bot.command(name="move", help="Make your move; place_at is your move <1-9>")
async def move(ctx, place_at: int):
    if ongoing[0]:
        if valid_move(place_at):
            player_move(place_at)
            await ctx.send(show_board())
            await ctx.send("You moved " + str(place_at))
            if check_win() == "0":
                await ctx.send(bot_move(bot_calculate()))
                if check_win() != "0":
                    await ctx.send(result(check_win()))
                    reset()
                    ongoing[0] = False
            else:
                await ctx.send(result(check_win()))
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
