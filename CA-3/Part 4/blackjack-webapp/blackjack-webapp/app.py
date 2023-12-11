import random

from flask import Flask, render_template, session

from model.data import make_deck, init_deck_values
from calcs import calc_total

import DBcm


app = Flask(__name__)


app.secret_key = (
    "kfke hrt'oerj erterutv'rtjv 'oieqrut0345uv 0'34qutv0rutv 'eqrutv equeqtr' u"
)

##############
creds = {
    "host": "localhost",
    "database": "BlackjackDB",
    "user": "root",
    "password": "setu2023",
}
##############

deck_values = init_deck_values()  # Global data (which is OK, as this never changes).


def draw():
    """Return a random card from the deck.

    The deck shrinks by 1 and the session updates.
    """
    selection = random.choice(session["deck"])
    session["deck"].remove(selection)
    session.modified = True
    return selection, deck_values[selection]


def generate_dealer_snippet(msg):
    """This nested function returns the snippet of HTML to update the Dealer's cards."""
    return render_template(
        "dealers.html",
        dealer_cards=session["dealer"],
        dealer_message=msg,
    )


@app.get("/")
@app.get("/start")
def display_opening_state():
    """(Re)start the game.

    Reset everything, dealing 2 cards each the Dealer and Player.
    """
    session["deck"] = make_deck()

    ######## My saving data code #########
    if "attempts" not in session:
    session["attempts"] = 0

    if "wins" not in session:
        session["wins"] = 0

    if "outcome" not in session:
        session["outcome"] = "null"

    ####

    session["attempts"] += 1

    session["save"] = save_game_data("frodo", session["outcome"], session["attempts"], session["wins"])
    ######################################

    session["player"] = []
    session["dealer"] = []
    session["can-hit"] = True
    session["can-stand"] = True
    session["player-blackjack"] = False

    session["player"].append(draw())
    session["dealer"].append(draw())
    session["player"].append(draw())
    session["dealer"].append(draw())

    player_opening_score = calc_total(session["player"])

    if player_opening_score == 21:
        session["can-hit"] = False
        session["player-blackjack"] = True
        player_opening_score = f"{player_opening_score}: Blackjack!"
        outcome = process_stand()
        session["can-stand"] = False
        return render_template(
            "alt_start.html",
            player_cards=session["player"],
            player_total=player_opening_score,
            dealer_cards=session["dealer"],
            title="Blackjack for the Web",
            header="Welcome to Blackjack for the Web",
            dealer_outcome=outcome,
        )

    return render_template(
        "start.html",
        player_cards=session["player"],
        player_total=player_opening_score,
        dealer_cards=session["dealer"],
        title="Blackjack for the Web",
        header="Welcome to Blackjack for the Web",
    )


@app.post("/hit")
def process_hit():
    """Process the hit.

    Returning only the snippet of HTML required to update the Player's section of the
    webpage.  Update the can-hit and can-stand booleans as necessary.
    """
    if session["can-hit"]:
        session["player"].append(draw())
        player_calc = calc_total(session["player"])
        if player_calc > 21:
            dealer_calc = calc_total(session["dealer"])
            session["can-hit"] = False
            session["can-stand"] = False
            snippet = render_template(
                "bust.html",
                player_cards=session["player"],
                player_total=player_calc,
                dealer_total=dealer_calc,
            )
            msg = f"Dealer wins with a score of {dealer_calc}. Player bust!"
            session["outcome"] = "loss"
            return (
                snippet
                + f"""
                    <div id="dealercards" hx-swap-oob="innerHTML">
                        { generate_dealer_snippet(msg) }
                    </div>
                """
            )
        elif player_calc == 21:
            session["can-hit"] = False
            snippet = render_template(
                "player21.html",
                player_cards=session["player"],
                player_total=player_calc,
            )
            return (
                snippet
                + f"""
                    <div id="dealercards" hx-swap-oob="innerHTML">
                        { process_stand() }
                    </div>
                """
            )
    return render_template(
        "hit.html",
        player_cards=session["player"],
        player_total=calc_total(session["player"]),
    )


@app.post("/stand")
def process_stand():
    """Process the stand.

    The Player is done (for whatever reason). It's over to the Dealer to do their thing.
    This gets a little complex due the number of "edge-case" possibilities.
    """

    if session["can-stand"]:
        session["can-hit"] = False
        session["can-stand"] = False
        dealer_calc = calc_total(session["dealer"])
        player_calc = calc_total(session["player"])

        if dealer_calc == 21 and session["player-blackjack"]:
            msg = "Both the Player and Dealer have Blackjack. It's a draw."
            session["outcome"] = "draw"
            return generate_dealer_snippet(msg)

        if dealer_calc == 21:
            msg = "The Dealer has Blackjack. The Dealer wins..."
            session["outcome"] = "loss"
            return generate_dealer_snippet(msg)

        if session["player-blackjack"]:
            msg = f"The Player has Blackjack (Dealer on {dealer_calc}), so the Player wins..."
            session["wins"] += 1 ##
            session["outcome"] = "win"
            return generate_dealer_snippet(msg)

        while True:  # Gulp...
            if player_calc > 21:
                session["outcome"] = "loss"
                return generate_dealer_snippet(
                    f"The Player is bust ({player_calc})! The Dealer wins..."
                )
            if dealer_calc > 21:
                session["wins"] += 1 ##
                session["outcome"] = "win"
                return generate_dealer_snippet(
                    f"The Dealer is bust ({dealer_calc})! The Player wins..."
                )
            if dealer_calc > player_calc:
                session["outcome"] = "loss"
                return generate_dealer_snippet(
                    f"The Dealer wins with a score of {dealer_calc}."
                )
            if (dealer_calc == player_calc) and (dealer_calc > 16):
                session["outcome"] = "draw"
                return generate_dealer_snippet("It's a draw (nobody wins).")
            if dealer_calc < 17:
                session["dealer"].append(draw())
                dealer_calc = calc_total(session["dealer"])
            else:
                session["wins"] += 1 ##
                session["outcome"] = "win"
                return generate_dealer_snippet(
                    f"The Player wins (against the Dealer's score of {dealer_calc})."
                )

    return generate_dealer_snippet("The game is over. Please start again...")

def save_game_data(gamertag, outcome, attempts, wins):
    """Save game data to the database."""
    SQL = """
        INSERT INTO games
        (gamertag, outcome, attempts, wins)
        VALUES (%s, %s, %s, %s)
    """

    with DBcm.UseDatabase(creds) as db:
        db.execute(SQL, (gamertag, outcome, attempts, wins))



if __name__ == "__main__":
    app.run(debug=True)


#####################################################################################################################################