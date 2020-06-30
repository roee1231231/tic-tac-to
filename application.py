from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def value_replace(current):
    if current == "X":
        return "O"
    else:
        return "X"

def check_board(board):
    for i in board:
        if i[0] and i[0] == i[1] and i[1] == i[2]:
            return i[0]
    for i in range(len(board)):
        if board[0][i] and board[0][i] == board[1][i] and board[1][i] == board[2][i]:
            return board[0][i]
    if board[0][0] and board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        return board[0][0]
    if board[0][2] and board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        return board[0][2]
    return None

@app.route("/")
def index():

    if "board" not in session:
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        session["turn"] = "X"
        session["winner"] = None

    return render_template("game.html", game=session["board"], turn=session["turn"], winner=session['winner'])

@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    session["board"][row][col] = session["turn"]
    session["turn"] = value_replace(session["turn"])
    if check_board(session['board']):
        session["winner"] = check_board(session['board'])
    return redirect(url_for("index"))

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)