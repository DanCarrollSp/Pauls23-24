import random

from model.data import make_deck, init_deck_values
from calcs import calc_total #, determine_ace_value

from flask import Flask, render_template, request, session, render_template

app = Flask(__name__)


deck_values = init_deck_values()
deck = make_deck()

def draw():
    """Select a random card from the deck. The deck shrinks by 1."""
    selection = random.choice(session["deck"])
    session["deck"].remove(selection)
    session.modified = True
    return selection, deck_values[selection]


##Global Variables##
canHit = True
playerOver21 = False
stood = False






@app.get("/")
@app.get("/start")
def display_opening_state():

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


@app.post("/stand")
def over_to_the_dealer():

    #variables
    global canHit
    global stood

    ####Player can no longer hit
    ####Reveal dealers cards
    ##The dealer will hit unitl they have a sum of 17 or higher
    ##If the dealer goes over 21 dealer BUSTS
    ##If the dealer has less than player the dealer BUSTS
    canHit = False
    stood = True

    while (calc_total(session["dealer"]) <= 17):
        session["dealer"].append(draw())
        


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

@app.post("/hit")
def select_another_card():

    #variables
    global canHit
    global playerOver21
    
    ####If player hasnt stood
    #### add a card to players hand
    ##If player goes over 21 its the dealers turn
    ##Dealer reveals card and hits until they reach 17 or more
    ##If the dealer doesnt go over 21 player BUSTS

    if(calc_total(session["player"]) > 21):
        playerOver21 = True


    if(playerOver21 == False):##If player hasnt stood
        use_player_total = calc_total(session["player"])##Add card to player hand


        if(use_player_total <= 21):
            ##Player hasnt busted
            session["player"].append(draw())
        else:
            ##Player busted
            temp = 1



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

    if(stood == True):
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




app.secret_key = "ufbesufbseubfrhf87guw2833gf833fyhncsiunnnnn0000001390284509o54"

if __name__ == "__main__":
    app.run(debug=True)