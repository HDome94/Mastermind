import random
from typing import Union, Optional
from enum import Enum, auto
from collections import namedtuple

# TODO
# Codecleanup
# Guessing aufdrößeln
# Typings
# Dokumentation


class GAMECOLORS(Enum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()
    WHITE = auto()
    ORANGE = auto()
    GREY = auto()


MOVE = namedtuple("Move", ["Round", "Guess", "Res1", "Res2"])
GAMEROUND = namedtuple("Gameround", ["GameNo", "Rounds", "Winner", "Players", "Code"])


class Game:
    COLORS = (GAMECOLORS.RED, GAMECOLORS.GREEN, GAMECOLORS.BLUE, GAMECOLORS.WHITE, GAMECOLORS.ORANGE, GAMECOLORS.GREY)
    GAMECOUNT = 0
    __GAMES = {}

    def __init__(self, playercount: int = 1, editRound: bool = False):
        self.__Code = random.choices(Game.COLORS, k=4)
        self.__Color1 = None
        self.__Color2 = None
        self.__Color3 = None
        self.__Color4 = None
        self.__playercount = playercount
        self.__players = {p: Player(p) for p in range(1, playercount + 1)}
        self.__activePlayer = 1
        self.__Round = 1
        self.__won = False
        self.__winner = None
        self.__started = False
        if not editRound:
            Game.GAMECOUNT += 1

    @property
    def Round(self) -> int:
        return self.__Round

    @property
    def Color1(self) -> GAMECOLORS:
        return self.__Color1

    @Color1.setter
    def Color1(self, color: Union[GAMECOLORS, None]):
        if isinstance(color, GAMECOLORS) or color is None:
            self.__Color1 = color
        else:
            raise TypeError("Use the Color Enums")

    @property
    def Color2(self) -> GAMECOLORS:
        return self.__Color2

    @Color2.setter
    def Color2(self, color: Union[GAMECOLORS, None]):
        if isinstance(color, GAMECOLORS) or color is None:
            self.__Color2 = color

    @property
    def Color3(self) -> GAMECOLORS:
        return self.__Color3

    @Color3.setter
    def Color3(self, color: Union[GAMECOLORS, None]):
        if isinstance(color, GAMECOLORS) or color is None:
            self.__Color3 = color

    @property
    def Color4(self) -> GAMECOLORS:
        return self.__Color4

    @Color4.setter
    def Color4(self, color: Union[GAMECOLORS, None]):
        if isinstance(color, GAMECOLORS) or color is None:
            self.__Color4 = color

    @property
    def PlayerCount(self):
        return self.__playercount

    @PlayerCount.setter
    def PlayerCount(self, count: int):
        if count >= 1:
            if self.__started:
                self.__init__(count)
            else:
                self.__init__(count, editRound=True)

    @property
    def ActivePlayer(self) -> int:
        return self.__activePlayer

    @property
    def LastPlayer(self) -> int:
        return self.ActivePlayer - 1 if self.ActivePlayer != 1 else self.PlayerCount

    @property
    def Won(self) -> bool:
        return self.__won

    @property
    def Winner(self) -> int:
        return self.__winner

    def setColors(self, colors: list[GAMECOLORS]):
        self.Color1 = colors[0]
        self.Color2 = colors[1]
        self.Color3 = colors[2]
        self.Color4 = colors[3]

    def __resetColors(self):
        self.__Color1 = None
        self.__Color2 = None
        self.__Color3 = None
        self.__Color4 = None

    def __checkGuess(self, guess: list[GAMECOLORS]):
        """
        Checks the guess
        :param guess:
        :return:
        """
        _code = list(self.__Code)
        _guess = list(guess)
        _correct = 0
        i = 0
        while i < 4:
            if _guess[i - _correct] == _code[i - _correct]:
                _code.pop(i - _correct)
                _guess.pop(i - _correct)
                _correct += 1
            i += 1

        _correctColors = 0
        for color in _guess:
            if color in _code:
                _correctColors += 1

        return _correct, _correctColors

    def guessing(self) -> tuple[int, int]:
        """

        :return: The count
        """
        if self.Color1 and self.Color2 and self.Color3 and self.Color4 and not self.__won:
            self.__started = True
            guess = [self.Color1, self.Color2, self.Color3, self.Color4]
            self.__resetColors()

            correct, correctColor = self.__checkGuess(guess)
            if correct == 4 and correctColor == 0:
                self.__won = True
                self.__winner = self.__activePlayer

            _move = MOVE(Round=self.Round, Guess=guess, Res1=correct, Res2=correctColor)
            self.__players[self.__activePlayer].setPlayMove(_move)

            if self.__activePlayer == self.PlayerCount and not self.__won:
                self.__Round += 1
                self.__activePlayer = 1
            elif not self.__won:
                self.__activePlayer += 1

            return correct, correctColor

    def newRound(self):
        Game.__addRoundToStatistic(GAMEROUND(Game.GAMECOUNT, self.Round, self.__winner, dict(self.__players.items()), self.__Code))
        self.__init__(self.__playercount)

    def getLastMoveFromPlayer(self, playernr: int) -> MOVE:
        return self.__players[playernr].getLastPlayMove()

    def getAllPlayMoves(self) -> dict[int, tuple[MOVE]]:
        return {playernr: player.getPlayMoves() for playernr, player in self.__players.items()}

    def dissolve(self) -> list[GAMECOLORS]:
        code = self.__Code
        self.newRound()
        return code

    @staticmethod
    def __addRoundToStatistic(gameround: GAMEROUND):
        if isinstance(gameround, GAMEROUND):
            Game.__GAMES.setdefault(gameround.GameNo, gameround)

    @staticmethod
    def getLastGameRound() -> GAMEROUND:
        return Game.__GAMES[Game.GAMECOUNT-1]

    @staticmethod
    def getAllGameRounds() -> list[GAMEROUND]:
        return list(Game.__GAMES.values())


class Player:
    def __init__(self, nr: int):
        self.__nr = nr
        self.__plays = {}
        self.__moves = 0

    @property
    def PlayerNr(self) -> int:
        return self.__nr

    @property
    def MoveCount(self) -> int:
        return self.__moves

    def setPlayMove(self, move: MOVE):
        self.__plays.setdefault(move.Round, move)
        self.__moves += 1

    def getLastPlayMove(self) -> MOVE:
        return self.__plays[self.__moves]

    def getPlayMove(self, _round: int) -> MOVE:
        if _round in self.__plays:
            return self.__plays[_round]

    def getPlayMoves(self) -> tuple[MOVE]:
        return tuple(*self.__plays.values())

    def __str__(self):
        return str(self.__nr)

    def __repr__(self):
        return self.__str__()
