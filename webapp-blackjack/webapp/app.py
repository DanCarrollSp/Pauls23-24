import random

from model.data import make_deck, init_deck_values
from calcs import calc_total #, determine_ace_value

from flask import Flask, render_template, request, session, render_template

app = Flask(__name__)


deck_values = init_deck_values()
deck = make_deck()


##Global Variables##
canHit = True
playerOver21 = False
stood = False

playerWon = False
dealerWon = False
drawGame = False
gameOver = False


def draw():
    """Select a random card from the deck. The deck shrinks by 1."""
    selection = random.choice(session["deck"])
    session["deck"].remove(selection)
    session.modified = True
    return selection, deck_values[selection]

def decide_winner():

    ##Global variables
    global playerWon
    global dealerWon
    global drawGame
    
    ##Gets card value totals
    player_value = calc_total(session["player"])
    dealer_value = calc_total(session["dealer"])

    ##decide who wins here with if statements
    if(player_value > dealer_value): 
        playerWon = True
        dealerWon = False
        drawGame = False
    if(player_value < dealer_value):
        playerWon = False
        dealerWon = True
        drawGame = False

    if(player_value > 21 and dealer_value <= 21):
        playerWon = False
        dealerWon = True
        drawGame = False
    if(player_value <= 21 and dealer_value > 21):
        playerWon = True
        dealerWon = False
        drawGame = False

    if(player_value > 21 and dealer_value > 21):
        playerWon = False
        dealerWon = False
        drawGame = True
    if(player_value == dealer_value):
        playerWon = False
        dealerWon = False
        drawGame = True



##########################################################################################################################################
@app.get("/")
@app.get("/start")
def display_opening_state():

    global stood 
    stood = False

    session["deck"] = make_deck()
    session["player"] = []
    session["dealer"] = []

    session["player"].append(draw())
    session["dealer"].append(draw())
    session["player"].append(draw())
    session["dealer"].append(draw())

    return render_template(
        "start.html",
        player_cards=session["player"],
        player_total=calc_total(session["player"]),
        dealer_cards=session["dealer"],
        dealer_total=calc_total(session["dealer"]),
        title="",
        header="",
        footer="",
    )

##########################################################################################################################################
@app.post("/stand")
def over_to_the_dealer():

    #variables
    global canHit
    global stood

    global playerWon
    global dealerWon
    global drawGame
    global gameOver


    ##Player cant hit after standing
    canHit = False
    stood = True
    gameOver = True

    ##Dealer hits until value is 17 or more
    while (calc_total(session["dealer"]) <= 17):
        session["dealer"].append(draw())
        

    ##Decide if player won, lost or drawed
    decide_winner()
    

    ##Return correct info
    common_data = {
        "player_cards": session["player"],
        "player_total": calc_total(session["player"]),
        "dealer_cards": session["dealer"],
        "dealer_total": calc_total(session["dealer"]),
        "dealer_total_text": calc_total(session["dealer"]),
        "title": "",
        "header": "",
        "footer": "",
    }

    if playerWon:
        common_data["player_won"] = playerWon

    if dealerWon:
        common_data["dealer_won"] = dealerWon

    if drawGame:
        common_data["draw_game"] = drawGame

    return render_template("start.html", **common_data)




##########################################################################################################################################
@app.post("/hit")
def select_another_card():

    ##Global variables
    global stood
    
    ##Gets card value totals
    player_value = calc_total(session["player"])

    
    ##Add a card to the player hand if they havent gone over 21
    if(player_value <= 21 and stood == False): session["player"].append(draw())


    ##With dealer calc total
    if(stood == False):
        return render_template(
        "start.html",
        player_cards=session["player"],
        player_total=calc_total(session["player"]),
        dealer_cards=session["dealer"],
        dealer_total=calc_total(session["dealer"]),
        title="",
        header="",
        footer=""
    ) 
    else:##Without dealer calc total
        return render_template(
        "start.html",
        player_cards=session["player"],
        player_total=calc_total(session["player"]),
        dealer_cards=session["dealer"],
        dealer_total=calc_total(session["dealer"]),
        dealer_total_text=calc_total(session["dealer"]),
        title="",
        header="",
        footer="",
    )
##########################################################################################################################################



app.secret_key = "ufbesufbseubfrhf87guw2833gf833fyhncsiunnnnn0000001390284509o54"

if __name__ == "__main__":
    app.run(debug=True)