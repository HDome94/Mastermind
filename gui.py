import locale
import os
import tkinter as tk
from tkinter import ttk, messagebox
import gettext
from mastermind import Game, GAMECOLORS, MOVE, GAMEROUND

GAME = Game()
WINDOWWIDTH = 940
WINDOWHEIGHT = 340
OUTERPADDING = 15


# TODO
# Codecleanup
# Typings
# Dokumentation


def loadTheme(wnd: tk.Tk, path: str):
    wnd.tk.call('source', path)


def centerWindow(wnd: tk.Tk):
    MWidth = wnd.winfo_screenwidth()
    MHeight = wnd.winfo_screenheight()
    x = int(MWidth / 2 - WINDOWWIDTH / 2)
    y = int(MHeight / 2 - WINDOWHEIGHT / 2)
    wnd.geometry(f"{WINDOWWIDTH}x{WINDOWHEIGHT}+{x}+{y}")


def SetupWindow(wnd: tk.Tk):
    wnd.title('Mastermind')
    wnd.iconbitmap("mastermind.ico")
    wnd.resizable(False, False)
    centerWindow(wnd)

    try:
        loadTheme(wnd, r'themes\azure_dark\azure dark.tcl')
        loadTheme(wnd, r'themes\azure\azure.tcl')
        azureLoaded.set(True)
    except tk.TclError:
        azureLoaded.set(False)

    wnd.style.configure(style="Header.TLabel", font=("Arial", 12))
    wnd.style.configure(style="Won.TLabel", font=("Arial", 11))
    wnd.style.configure(style="TLabel", font=("Arial", 11))
    wnd.style.configure(style="TButton", font=("Arial", 10))
    wnd.style.configure(style="TMenubutton", height=1, font=("Arial", 10))


def init():
    menu_DarkModeEnabled.set(False)
    menu_PlayerCount.set(1)
    lbl_GameCountIntVar.set(GAME.GAMECOUNT)
    lbl_RoundIntVar.set(GAME.Round)
    LANG.set("de")

    setLanguage()
    setTheme()
    setPlayersToLB()
    setActivePlayerLB()
    setTVHeader()
    addPlayersToTV()
    lb_Players.bindtags((lb_Players, window, "all"))
    treeview.bindtags((treeview, window, "all"))


def initNewRound(dissolved=False):
    if not dissolved:
        GAME.newRound()
    addPlayersToTV()
    addGameRoundToTV()
    showHideResult(state="hide")
    reloadGUI()


def getTkColor(color: GAMECOLORS) -> str:
    col = ""
    match color:
        case GAMECOLORS.RED:
            col = "Red"
        case GAMECOLORS.WHITE:
            col = "White"
        case GAMECOLORS.BLUE:
            col = "Blue"
        case GAMECOLORS.ORANGE:
            col = "Orange"
        case GAMECOLORS.GREY:
            col = "Grey"
        case GAMECOLORS.GREEN:
            col = "Green"
    return col


def getColorName(color: GAMECOLORS) -> str:
    """

    :param color: The Color to Translate
    :return: The Name of the Color in the specific Language
    """
    col = ""
    match color:
        case GAMECOLORS.RED:
            col = redTxtVar.get()
        case GAMECOLORS.WHITE:
            col = whiteTxtVar.get()
        case GAMECOLORS.BLUE:
            col = blueTxtVar.get()
        case GAMECOLORS.ORANGE:
            col = orangeTxtVar.get()
        case GAMECOLORS.GREY:
            col = greyTxtVar.get()
        case GAMECOLORS.GREEN:
            col = greenTxtVar.get()
    return col


def getBtnDefBG():
    return "silver" if menu_DarkModeEnabled.get() else "SystemButtonFace"


def getCodeString(code: list[GAMECOLORS]) -> str:
    movestr = ""
    for col in code:
        movestr += getColorName(col) + " , "
    return movestr[:-2]


def setTVHeader():
    treeview.heading("#0", text=tvHeaderPlayerTxtVar.get(), anchor='center')
    treeview.heading(1, text=tvHeaderGuessTxtVar.get(), anchor='center')
    treeview.heading(2, text=lbl_ResTxt1Var.get()[:-1], anchor='center')
    treeview.heading(3, text=lbl_ResTxt2Var.get()[:-1], anchor='center')

    tvGames.heading("#0", text=tvGamesGameRoundTxtVar.get(), anchor="center")
    tvGames.heading(1, text=tvGamesWinnerTxtVar.get(), anchor='center')
    tvGames.heading(2, text=f"{tvGamesCodeTxtVar.get()} / {tvHeaderGuessTxtVar.get()}", anchor='center')
    tvGames.heading(3, text=lbl_ResTxt1Var.get()[:-1], anchor='center')
    tvGames.heading(4, text=lbl_ResTxt2Var.get()[:-1], anchor='center')


def reloadGamesTV():
    tvGames.delete(*tvGames.get_children())
    for r in GAME.getAllGameRounds():
        addGameRoundToTV(r)


def addGameRoundToTV(_round: GAMEROUND = None):
    if _round is None:
        _round = GAME.getLastGameRound()
    _winner = f"{playerTxtVar.get()} {_round.Winner}" if _round.Winner is not None else noneTxtVar.get()

    tvGames.insert(parent='', index='end', iid=_round.GameNo, text=f"{lbl_GameCountTxtVar.get()} {_round.GameNo}",
                   values=(_winner, getCodeString(_round.Code)))

    for r in range(1, _round.Rounds + 1):
        if _round.Players[1].getPlayMove(r):
            tvGames.insert(parent=_round.GameNo, index='end', iid=f"{_round.GameNo}R{r}", text=f"{tvRoundTxtVar.get()} {r}")
            for p in _round.Players.values():
                move = p.getPlayMove(r)
                if move:
                    tvGames.insert(parent=f"{_round.GameNo}R{r}", index='end', iid=f"{_round.GameNo}R{r}P{p}",
                                   text=f"{playerTxtVar.get()} {p}",
                                   values=("", getCodeString(move.Guess), move.Res1, move.Res2))


def addPlayersToTV():
    treeview.delete(*treeview.get_children())
    for p in range(1, GAME.PlayerCount + 1):
        treeview.insert(parent='', index='end', iid=p, text=f"{playerTxtVar.get()} {p}")


def addMoveToTV(player: int = None, move: MOVE = None):
    if player is None:
        player = GAME.LastPlayer
    if move is None:
        move = GAME.getLastMoveFromPlayer(player)
    movestr = getCodeString(move.Guess)
    treeview.insert(parent=str(player), index='end', iid=f"P{player}R{move.Round}",
                    text=f"{tvRoundTxtVar.get()} {move.Round}",
                    values=(movestr, move.Res1, move.Res2))


def reloadTV():
    addPlayersToTV()
    for p, moves in GAME.getAllPlayMoves().items():
        for move in moves:
            addMoveToTV(p, move)


def expandActivePlayerTV():
    for e in treeview.get_children():
        treeview.item(e, open=False)
    treeview.item(GAME.ActivePlayer, open=True)


def setPlayersToLB():
    lb_Players.delete(0, tk.END)
    for p in range(1, GAME.PlayerCount + 1):
        lb_Players.insert(tk.END, f"{playerTxtVar.get()} {p}")
    setActivePlayerLB()


def setActivePlayerLB():
    for p in range(0, GAME.PlayerCount):
        if menu_DarkModeEnabled.get():
            lb_Players.itemconfig(p, bg='#333333', fg="white")
        else:
            lb_Players.itemconfig(p, bg='SystemButtonFace', fg="black")
    lb_Players.itemconfig(GAME.ActivePlayer - 1, bg='blue', fg="white")


def setLanguage():
    locale.setlocale(locale.LC_ALL, '')
    lang = LANG.get()
    locale_path = os.path.join(os.path.dirname(__file__), 'locale')
    gettext.bindtextdomain('messages', locale_path)
    gettext.textdomain('messages')
    language = gettext.translation('messages', localedir=locale_path, languages=[lang], fallback=True)
    language.install()
    _ = language.gettext

    langMenueTxtVar.set(_("Language"))
    langmenue.entryconfigure(0, label=_("German"))
    langmenue.entryconfigure(1, label=_("English"))
    langmenue.entryconfigure(2, label=_("Spanish"))
    langmenue.entryconfigure(3, label=_("French"))
    langmenue.entryconfigure(4, label=_("Italian"))
    langmenue.entryconfigure(5, label=_("Chinese"))

    playermenuetbn.config(text=_("Player"))
    playerTxtVar.set(_("Player"))
    playermenue.entryconfigure(0, label=f"1 {_('Player')}")
    playermenue.entryconfigure(1, label=f"2 {_('Player')}")
    playermenue.entryconfigure(2, label=f"3 {_('Player')}")
    playermenue.entryconfigure(3, label=f"4 {_('Player')}")
    playermenue.entryconfigure(4, label=f"5 {_('Player')}")

    thememenuebtn.config(text=_("Theme"))
    thememenue.entryconfigure(0, label=_("Light"))
    thememenue.entryconfigure(1, label=_("Dark"))

    lbl_GameCountTxtVar.set(_("Game No")+":")
    lbl_RoundTxtVar.set(_("Current Round")+":")
    lbl_ResTxt1Var.set(_("Correct")+":")
    lbl_ResTxt2Var.set(_("Correct Color")+":")
    lbl_GuessTxtVar.set(_("Current Guess")+":")
    lbl_LastGuessTxtVar.set(_("Last Guess")+":")
    btn_NewRoundTxtVar.set(_("New Round"))
    btn_GuessingTxtVar.set(_("Guess"))
    lbl_Won1Var.set(_("Won"))
    lbl_Won2Var.set(_("Won2"))

    tabView.tab(movesFrame, text=_("Moves"))
    tabView.tab(gameStatsFrame, text=_("Gamehistory"))

    tvHeaderPlayerTxtVar.set(f"{_('Player')} / {_('Round')}")
    tvHeaderGuessTxtVar.set(_("GuessTV"))
    tvRoundTxtVar.set(_("Round"))

    tvGamesGameRoundTxtVar.set(f"{_('Game No')} / {_('Round')}")
    tvGamesWinnerTxtVar.set(_("Winner"))
    tvGamesCodeTxtVar.set(_("Code"))

    redTxtVar.set(_("Red"))
    greenTxtVar.set(_("Green"))
    blueTxtVar.set(_("Blue"))
    whiteTxtVar.set(_("White"))
    orangeTxtVar.set(_("Orange"))
    greyTxtVar.set(_("Grey"))

    btn_dissolveTxtVar.set(_("Dissolve"))
    dissolveTxtVar.set(_("Dissolve Text"))

    noneTxtVar.set(_("Nobody"))

    setTVHeader()
    setPlayersToLB()
    reloadTV()
    reloadGamesTV()
    expandActivePlayerTV()


def setTheme():
    if azureLoaded.get():
        if menu_DarkModeEnabled.get():
            window.config(background="#2d2d30")
            window.style.theme_use('azuredark')
        else:
            window.config(background="SystemButtonFace")
            window.style.theme_use('azure')
            window.style.configure(style="TFrame", background="SystemButtonFace", foreground="black")
            window.style.configure(style="TLabel", background="SystemButtonFace", foreground="black")
            window.style.configure(style="Treeview", background="SystemButtonFace",
                                   fieldbackground="SystemButtonFace", foreground="black")
            window.style.configure(style="TNotebook", background="SystemButtonFace",
                                   fieldbackground="SystemButtonFace", foreground="black")

    setActivePlayerLB()
    refreshGuessBtns()


def setPlayerCount():
    count = menu_PlayerCount.get()
    if count > 1:
        showHidePlayers("show")
    else:
        showHidePlayers("hide")
    GAME.PlayerCount = count
    setPlayersToLB()
    addPlayersToTV()

    lb_Players.place_forget()
    lb_Players.place(x=0, y=0, height=(16 * count) + 1)
    showHideResult(state="hide")
    reloadGUI()


def setColBtnStates(state: str):
    btn_red.config(state=state)
    btn_green.config(state=state)
    btn_blue.config(state=state)
    btn_white.config(state=state)
    btn_orange.config(state=state)
    btn_grey.config(state=state)


def checkAllColSet():
    if GAME.Color1 and GAME.Color2 and GAME.Color3 and GAME.Color4:
        setColBtnStates(state="disabled")
        btn_guess.config(state="normal")
    else:
        setColBtnStates(state="normal")
        btn_guess.config(state="disabled")


def setGuessColors(color: GAMECOLORS):
    col = getTkColor(color)
    if GAME.Color1 is None:
        btn_guess1.config(bg=col, state="normal")
        GAME.Color1 = color
    elif GAME.Color2 is None:
        btn_guess2.config(bg=col, state="normal")
        GAME.Color2 = color
    elif GAME.Color3 is None:
        btn_guess3.config(bg=col, state="normal")
        GAME.Color3 = color
    elif GAME.Color4 is None:
        btn_guess4.config(bg=col, state="normal")
        GAME.Color4 = color

    checkAllColSet()


def setResults(correct: int, correctColor: int):
    lbl_ResInt1Var.set(correct)
    lbl_ResInt2Var.set(correctColor)
    showHideResult(state="show")


def resetCurGuessBtns():
    bg = getBtnDefBG()
    btn_guess1.config(bg=bg, state="disabled")
    btn_guess2.config(bg=bg, state="disabled")
    btn_guess3.config(bg=bg, state="disabled")
    btn_guess4.config(bg=bg, state="disabled")


def refreshGuessBtns():
    bg = getBtnDefBG()
    if GAME.Round > 1:
        move = GAME.getLastMoveFromPlayer(GAME.ActivePlayer)
        cols = []
        for color in move.Guess:
            cols.append(getTkColor(color))
        btn_LastGuess1.config(bg=cols[0])
        btn_LastGuess2.config(bg=cols[1])
        btn_LastGuess3.config(bg=cols[2])
        btn_LastGuess4.config(bg=cols[3])
        btn_LastGuess1.place(x=115, y=0, width=25, height=25)
        btn_LastGuess2.place(x=165, y=0, width=25, height=25)
        btn_LastGuess3.place(x=215, y=0, width=25, height=25)
        btn_LastGuess4.place(x=265, y=0, width=25, height=25)
    else:
        btn_LastGuess1.config(bg=bg)
        btn_LastGuess2.config(bg=bg)
        btn_LastGuess3.config(bg=bg)
        btn_LastGuess4.config(bg=bg)
        btn_LastGuess1.place_forget()
        btn_LastGuess2.place_forget()
        btn_LastGuess4.place_forget()
        btn_LastGuess3.place_forget()

    if btn_guess1.cget("bg") in ["SystemButtonFace", "silver"]:
        btn_guess1.config(bg=bg, state="disabled")
    if btn_guess2.cget("bg") in ["SystemButtonFace", "silver"]:
        btn_guess2.config(bg=bg, state="disabled")
    if btn_guess3.cget("bg") in ["SystemButtonFace", "silver"]:
        btn_guess3.config(bg=bg, state="disabled")
    if btn_guess4.cget("bg") in ["SystemButtonFace", "silver"]:
        btn_guess4.config(bg=bg, state="disabled")


def refreshHeader():
    lbl_GameCountIntVar.set(GAME.GAMECOUNT)
    lbl_RoundIntVar.set(GAME.Round)


def reloadGUI():
    resetCurGuessBtns()
    refreshHeader()
    refreshGuessBtns()
    setActivePlayerLB()
    checkAllColSet()
    window.focus_set()
    expandActivePlayerTV()


def showHideResult(state: str):
    match state:
        case "hide":
            lbl_ResTxt1.place_forget()
            lbl_ResTxt2.place_forget()
            lbl_ResInt1.place_forget()
            lbl_ResInt2.place_forget()
        case "show":
            lbl_ResTxt1.place(x=5, y=10, width=110, height=25)
            lbl_ResInt1.place(x=120, y=10, width=10, height=25)
            lbl_ResTxt2.place(x=5, y=40, width=110, height=25)
            lbl_ResInt2.place(x=120, y=40, width=10, height=25)


def showWonMsgBox():
    if GAME.PlayerCount > 1:
        msg = f"{playerTxtVar.get()} {GAME.Winner} {lbl_Won2Var.get()}"
        messagebox.showinfo(lbl_Won1Var.get(), msg)
    else:
        messagebox.showinfo(lbl_Won1Var.get(), lbl_Won1Var.get())


def showHidePlayers(state: str):
    match state:
        case "show":
            window.geometry(f"1020x{WINDOWHEIGHT}")
            tabView.place_forget()
            sepLine.place_forget()
            playerFrame.place(x=330, y=80, width=80, height=90)
            lbl_Playerlist.place(x=330, y=0, width=55, height=25)
            tabView.place(x=420, y=15, width=600, height=313)
            sepLine.place(x=5, y=60, width=405, height=5)
        case "hide":
            window.geometry(f"{WINDOWWIDTH}x{WINDOWHEIGHT}")
            playerFrame.place_forget()
            lbl_Playerlist.place_forget()
            tabView.place_forget()
            sepLine.place_forget()
            tabView.place(x=340, y=15, width=600, height=313)
            sepLine.place(x=5, y=60, width=320, height=5)


def btn_Guess1_Click():
    setColBtnStates(state="normal")
    btn_guess1.config(bg=getBtnDefBG(), state="disabled")
    btn_guess.config(state="disabled")
    GAME.Color1 = None


def btn_Guess2_Click():
    setColBtnStates(state="normal")
    btn_guess2.config(bg=getBtnDefBG(), state="disabled")
    btn_guess.config(state="disabled")
    GAME.Color2 = None


def btn_Guess3_Click():
    setColBtnStates(state="normal")
    btn_guess3.config(bg=getBtnDefBG(), state="disabled")
    btn_guess.config(state="disabled")
    GAME.Color3 = None


def btn_Guess4_Click():
    setColBtnStates(state="normal")
    btn_guess4.config(bg=getBtnDefBG(), state="disabled")
    btn_guess.config(state="disabled")
    GAME.Color4 = None


def btn_Guess_Click():
    showHideResult(state="hide")
    correct, correctColor = GAME.guessing()
    won = False
    if correct == 4:
        won = True
        showWonMsgBox()
    elif GAME.PlayerCount > 1 and GAME.Round > 1:
        lastRes = GAME.getLastMoveFromPlayer(GAME.ActivePlayer)
        setResults(lastRes.Res1, lastRes.Res2)
    elif GAME.PlayerCount == 1:
        setResults(correct, correctColor)

    if won:
        initNewRound()
    else:
        addMoveToTV()
        reloadGUI()


def btn_NewRound_Click():
    txt = f"{btn_NewRoundTxtVar.get()}?"
    if messagebox.askyesno(txt, txt):
        initNewRound()


def btn_dissolve_Click():
    code = [getColorName(col) for col in GAME.dissolve()]
    messagebox.showinfo(btn_dissolveTxtVar.get(), f"{dissolveTxtVar.get()}: \n {code}")
    initNewRound(dissolved=True)


window = tk.Tk()
window.style = ttk.Style(window)
azureLoaded = tk.BooleanVar()
SetupWindow(window)

LANG = tk.StringVar()
playerTxtVar = tk.StringVar()
langMenueTxtVar = tk.StringVar()
themeMenueTxtVar = tk.StringVar()
menu_DarkModeEnabled = tk.BooleanVar()
menu_PlayerCount = tk.IntVar()

lbl_GameCountTxtVar = tk.StringVar()
lbl_GameCountIntVar = tk.IntVar()
lbl_RoundTxtVar = tk.StringVar()
lbl_RoundIntVar = tk.IntVar()

lbl_ResTxt1Var = tk.StringVar()
lbl_ResTxt2Var = tk.StringVar()
lbl_Won1Var = tk.StringVar()
lbl_Won2Var = tk.StringVar()
lbl_ResInt1Var = tk.IntVar()
lbl_ResInt2Var = tk.IntVar()

lbl_LastGuessTxtVar = tk.StringVar()
lbl_GuessTxtVar = tk.StringVar()
btn_NewRoundTxtVar = tk.StringVar()
btn_GuessingTxtVar = tk.StringVar()

tvRoundTxtVar = tk.StringVar()
tvHeaderPlayerTxtVar = tk.StringVar()
tvHeaderGuessTxtVar = tk.StringVar()

tabGameStatsTxtVar = tk.StringVar()
tvGamesGameRoundTxtVar = tk.StringVar()
tvGamesWinnerTxtVar = tk.StringVar()
tvGamesCodeTxtVar = tk.StringVar()

redTxtVar = tk.StringVar()
greenTxtVar = tk.StringVar()
blueTxtVar = tk.StringVar()
whiteTxtVar = tk.StringVar()
orangeTxtVar = tk.StringVar()
greyTxtVar = tk.StringVar()

btn_dissolveTxtVar = tk.StringVar()
dissolveTxtVar = tk.StringVar()
btn_gameStatsTxtVar = tk.StringVar()

noneTxtVar = tk.StringVar()

langmenue = tk.Menu(master=window, tearoff=0)
langmenue.add_radiobutton(variable=LANG, value="de", command=setLanguage)
langmenue.add_radiobutton(variable=LANG, value="en", command=setLanguage)
langmenue.add_radiobutton(variable=LANG, value="es", command=setLanguage)
langmenue.add_radiobutton(variable=LANG, value="fr", command=setLanguage)
langmenue.add_radiobutton(variable=LANG, value="it", command=setLanguage)
langmenue.add_radiobutton(variable=LANG, value="zh", command=setLanguage)
langmenuebtn = ttk.Menubutton(master=window, textvariable=langMenueTxtVar, menu=langmenue, direction='below')

playermenue = tk.Menu(master=window, tearoff=0)
playermenue.add_radiobutton(variable=menu_PlayerCount, value=1, command=setPlayerCount)
playermenue.add_radiobutton(variable=menu_PlayerCount, value=2, command=setPlayerCount)
playermenue.add_radiobutton(variable=menu_PlayerCount, value=3, command=setPlayerCount)
playermenue.add_radiobutton(variable=menu_PlayerCount, value=4, command=setPlayerCount)
playermenue.add_radiobutton(variable=menu_PlayerCount, value=5, command=setPlayerCount)
playermenuetbn = ttk.Menubutton(master=window, menu=playermenue, direction='below')

thememenue = tk.Menu(master=window, tearoff=0)
thememenue.add_radiobutton(variable=menu_DarkModeEnabled, value=False, command=setTheme)
thememenue.add_radiobutton(variable=menu_DarkModeEnabled, value=True, command=setTheme)
thememenuebtn = ttk.Menubutton(master=window, menu=thememenue, direction='below')


bgFrame = ttk.Frame(master=window)
headFrame = ttk.Frame(master=window)
resFrame = ttk.Frame(master=window)
guessFrame = ttk.Frame(master=window)
controlFrame = ttk.Frame(master=window)
playerFrame = ttk.Frame(master=window)
tabView = ttk.Notebook(master=window)
movesFrame = ttk.Frame(master=tabView, width=590, height=325)
gameStatsFrame = ttk.Frame(master=tabView, width=590, height=325)

tabView.add(movesFrame)
tabView.add(gameStatsFrame)

lbl_GameCount = ttk.Label(master=headFrame, textvariable=lbl_GameCountTxtVar, anchor='w', style="Header.TLabel")
lbl_GameCountInt = ttk.Label(master=headFrame, textvariable=lbl_GameCountIntVar, anchor='w', style="Header.TLabel")
lbl_Round = ttk.Label(master=headFrame, textvariable=lbl_RoundTxtVar, anchor='w', style="Header.TLabel")
lbl_RoundInt = ttk.Label(master=headFrame, textvariable=lbl_RoundIntVar, anchor='w', style="Header.TLabel")
lbl_Playerlist = ttk.Label(master=headFrame, textvariable=playerTxtVar, anchor='w', style="Header.TLabel")
sepLine = ttk.Separator(master=window)

lbl_ResTxt1 = ttk.Label(master=resFrame, textvariable=lbl_ResTxt1Var)
lbl_ResTxt2 = ttk.Label(master=resFrame, textvariable=lbl_ResTxt2Var)
lbl_ResInt1 = ttk.Label(master=resFrame, textvariable=lbl_ResInt1Var)
lbl_ResInt2 = ttk.Label(master=resFrame, textvariable=lbl_ResInt2Var)

lbl_LastGuess = ttk.Label(master=guessFrame, textvariable=lbl_LastGuessTxtVar)
btn_LastGuess1 = tk.Button(master=guessFrame, state="disabled", bg="SystemButtonFace")
btn_LastGuess2 = tk.Button(master=guessFrame, state="disabled", bg="SystemButtonFace")
btn_LastGuess3 = tk.Button(master=guessFrame, state="disabled", bg="SystemButtonFace")
btn_LastGuess4 = tk.Button(master=guessFrame, state="disabled", bg="SystemButtonFace")

lbl_guess = ttk.Label(master=guessFrame, textvariable=lbl_GuessTxtVar)
btn_guess1 = tk.Button(master=guessFrame, command=btn_Guess1_Click, state="disabled", bg="SystemButtonFace")
btn_guess2 = tk.Button(master=guessFrame, command=btn_Guess2_Click, state="disabled", bg="SystemButtonFace")
btn_guess3 = tk.Button(master=guessFrame, command=btn_Guess3_Click, state="disabled", bg="SystemButtonFace")
btn_guess4 = tk.Button(master=guessFrame, command=btn_Guess4_Click, state="disabled", bg="SystemButtonFace")

btn_red = tk.Button(master=guessFrame, bg="Red", command=lambda: setGuessColors(GAMECOLORS.RED))
btn_green = tk.Button(master=guessFrame, bg="Green", command=lambda: setGuessColors(GAMECOLORS.GREEN))
btn_blue = tk.Button(master=guessFrame, bg="Blue", command=lambda: setGuessColors(GAMECOLORS.BLUE))
btn_white = tk.Button(master=guessFrame, bg="White", command=lambda: setGuessColors(GAMECOLORS.WHITE))
btn_orange = tk.Button(master=guessFrame, bg="Orange", command=lambda: setGuessColors(GAMECOLORS.ORANGE))
btn_grey = tk.Button(master=guessFrame, bg="Grey", command=lambda: setGuessColors(GAMECOLORS.GREY))

btn_newRound = ttk.Button(master=controlFrame, textvariable=btn_NewRoundTxtVar, command=btn_NewRound_Click)
btn_dissolve = ttk.Button(master=controlFrame, textvariable=btn_dissolveTxtVar, command=btn_dissolve_Click)
btn_guess = ttk.Button(master=controlFrame, textvariable=btn_GuessingTxtVar, command=btn_Guess_Click, state="disabled")

lb_Players = tk.Listbox(master=playerFrame, width=80, height=90, background="SystemButtonFace", border=0, borderwidth=0)

treeScrollSide = ttk.Scrollbar(movesFrame)
treeScrollSide.pack(side='right', fill='y')
treeview = ttk.Treeview(master=movesFrame, yscrollcommand=treeScrollSide.set, columns=(1, 2, 3), height=12)
treeScrollSide.config(command=treeview.yview)
treeview.column("#0", anchor='center', width=120)
treeview.column(1, anchor='w', width=230)
treeview.column(2, anchor='w', width=80)
treeview.column(3, anchor='w', width=110)

tvGamesScroll = ttk.Scrollbar(gameStatsFrame)
tvGamesScroll.pack(side='right', fill='y')
tvGames = ttk.Treeview(master=gameStatsFrame, yscrollcommand=tvGamesScroll.set, columns=(1, 2, 3, 4), height=12)
tvGamesScroll.config(command=tvGames.yview)
tvGames.column("#0", anchor='w', width=120)
tvGames.column(1, anchor='w', width=70)
tvGames.column(2, anchor='w', width=200)
tvGames.column(3, anchor='w', width=70)
tvGames.column(4, anchor='w', width=110)

playermenuetbn.grid(row=0, column=0, padx=2, pady=1)
langmenuebtn.grid(row=0, column=2, padx=1, pady=1)
thememenuebtn.grid(row=0, column=3, padx=1, pady=1)

bgFrame.place(x=5, y=30, width=1080, height=350)
headFrame.place(x=10, y=30, width=1080, height=50)
sepLine.place(x=5, y=60, width=320, height=5)
resFrame.place(x=12, y=65, width=320, height=90)
guessFrame.place(x=12, y=155, width=300, height=170)
controlFrame.place(x=5, y=300, width=320, height=35)
tabView.place(x=340, y=15, width=600, height=313)

lbl_GameCount.place(x=0, y=0, width=110, height=25)
lbl_GameCountInt.place(x=60, y=0, width=55, height=25)
lbl_Round.place(x=165, y=0, width=110, height=25)
lbl_RoundInt.place(x=275, y=0, width=55, height=25)

lbl_LastGuess.place(x=5, y=0, width=110, height=20)
lbl_guess.place(x=5, y=40, width=110, height=20)
btn_guess1.place(x=115, y=40, width=25, height=25)
btn_guess2.place(x=165, y=40, width=25, height=25)
btn_guess3.place(x=215, y=40, width=25, height=25)
btn_guess4.place(x=265, y=40, width=25, height=25)

btn_red.place(x=10, y=90, width=30, height=30)
btn_green.place(x=60, y=90, width=30, height=30)
btn_blue.place(x=110, y=90, width=30, height=30)
btn_white.place(x=160, y=90, width=30, height=30)
btn_orange.place(x=210, y=90, width=30, height=30)
btn_grey.place(x=260, y=90, width=30, height=30)

btn_newRound.grid(row=0, column=0, padx=7, pady=2)
btn_dissolve.grid(row=0, column=1, padx=7, pady=2)
btn_guess.grid(row=0, column=2, padx=7, pady=2)

lb_Players.place(x=0, y=0, height=16 * GAME.PlayerCount)
treeview.place(x=0, y=0, width=580, height=290)
tvGames.place(x=0, y=0, width=580, height=290)

init()

window.mainloop()
