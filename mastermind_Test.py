import mastermind

COLORS = mastermind.GAMECOLORS


class Game(mastermind.Game):
    def __init__(self, playercount=1):
        super().__init__(playercount)
        self.__Code = (COLORS.RED, COLORS.BLUE, COLORS.RED, COLORS.GREEN)


# AUWERTUNGSTESTS

# 1,2 Richtig + 1 richtige Farbe
def Test1():
    game = Game()
    game.Color1 = COLORS.RED
    game.Color2 = COLORS.BLUE
    game.Color3 = COLORS.GREEN
    game.Color4 = COLORS.GREY
    res1, res2 = game.guessing()
    print("Test1: ", res1 == 2, res2 == 1)


# 3,4 Richtig + 1 richtige Farbe
def Test2():
    game = Game()
    game.Color1 = COLORS.BLUE
    game.Color2 = COLORS.GREY
    game.Color3 = COLORS.RED
    game.Color4 = COLORS.GREEN
    res1, res2 = game.guessing()
    print("Test2: ", res1 == 2, res2 == 1)


# Farbe mehrmals aber nur 1-mal an richtiger Pos
def Test3():
    game = Game()
    game.Color1 = COLORS.RED
    game.Color2 = COLORS.GREY
    game.Color3 = COLORS.GREY
    game.Color4 = COLORS.RED
    res1, res2 = game.guessing()
    print("Test3: ", res1 == 1, res2 == 1)


# Keine richtigen
def Test4():
    game = Game()
    game.Color1 = COLORS.ORANGE
    game.Color2 = COLORS.ORANGE
    game.Color3 = COLORS.GREY
    game.Color4 = COLORS.GREY
    res1, res2 = game.guessing()
    print("Test4: ", res1 == 0, res2 == 0)


# Alle Farben enthalten aber falsche Pos
def Test5():
    game = Game()
    game.Color1 = COLORS.BLUE
    game.Color2 = COLORS.RED
    game.Color3 = COLORS.GREEN
    game.Color4 = COLORS.RED
    res1, res2 = game.guessing()
    print("Test5: ", res1 == 0, res2 == 4)


# Alle Richtig
def Test6():
    game = Game()
    game.Color1 = COLORS.RED
    game.Color2 = COLORS.BLUE
    game.Color3 = COLORS.RED
    game.Color4 = COLORS.GREEN
    res1, res2 = game.guessing()
    print("Test6: ", res1 == 4, res2 == 0)


# Allgemeine Tests

# Neue Runde
def Test11():
    game = Game()
    gamecount = game.GAMECOUNT
    game.Color1 = COLORS.BLUE
    game.Color2 = COLORS.RED
    game.Color3 = COLORS.GREEN
    game.Color4 = COLORS.RED
    game.guessing()
    game.newRound()
    print("Test11: ", gamecount != game.GAMECOUNT, game.Round == 1)


# Mehrspieler Tests

# Spielerzahl wird gesetzt (Konstruktor)
def Test7():
    game = Game(2)
    print("Test7: ", game.PlayerCount == 2)


# Spielerzahl nachträglich ändern => Neues Spiel
def Test8():
    game = Game()
    game.Color1 = COLORS.BLUE
    game.Color2 = COLORS.RED
    game.Color3 = COLORS.GREEN
    game.Color4 = COLORS.RED
    game.guessing()
    game.PlayerCount = 2
    print("Test8: ", game.PlayerCount == 2, game.Round == 1)


# Rundenzahl erhöht sich erst, wenn alle Spieler dran waren
def Test9():
    game = Game(2)
    rndStart = game.Round

    game.setColors([COLORS.BLUE, COLORS.RED, COLORS.GREEN, COLORS.RED])
    game.guessing()
    rnd1 = game.Round

    game.setColors([COLORS.GREY, COLORS.ORANGE, COLORS.WHITE, COLORS.RED])
    game.guessing()
    rnd2 = game.Round

    print("Test9:", rndStart == rnd1 and rnd1 != rnd2)


# Letzten Move von Spieler bekommen
def Test10():
    game = Game(2)
    game.Color1 = COLORS.BLUE
    game.Color2 = COLORS.RED
    game.Color3 = COLORS.GREEN
    game.Color4 = COLORS.RED
    game.guessing()
    game.Color1 = COLORS.GREY
    game.Color2 = COLORS.ORANGE
    game.Color3 = COLORS.WHITE
    game.Color4 = COLORS.RED
    game.guessing()
    guessp1 = [COLORS.BLUE, COLORS.RED, COLORS.GREEN, COLORS.RED]
    movep1 = game.getLastMoveFromPlayer(1)
    guessp2 = [COLORS.GREY, COLORS.ORANGE, COLORS.WHITE, COLORS.RED]
    movep2 = game.getLastMoveFromPlayer(2)
    print("Test10:", movep1[1] == guessp1, movep2[1] == guessp2)


def Teste():
    Test1()
    Test2()
    Test3()
    Test4()
    Test5()
    Test6()
    Test7()
    Test8()
    Test9()
    Test10()
    Test11()


Teste()
