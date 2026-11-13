import os
import datetime as dt

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from IntroToCompSci.finance.helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    db.execute("CREATE TABLE if NOT EXISTS purchases ( user_id INTEGER NOT NULL, stock TEXT NOT NULL, price INTEGER NOT NULL, date INTEGER NOT NULL, shares INTEGER NOT NULL, action TEXT NOT NULL )")
    db.execute("CREATE TABLE if NOT EXISTS sales ( user_id INTEGER NOT NULL, stock TEXT NOT NULL, price INTEGER NOT NULL, date INTEGER NOT NULL, shares INTEGER NOT NULL, action TEXT NOT NULL )")

    id = session["user_id"]

    symbols = []
    stocks = {}
    count = 0
    owned = db.execute("SELECT stock FROM purchases WHERE user_id = ?", id)

    for stk in owned:
        stk = stk["stock"]
        if stk not in symbols:
            info = lookup(stk)

            total = 0
            shares = db.execute("SELECT shares FROM purchases WHERE stock = ? AND user_id = ?", stk, id)
            for share in shares:
                total += share["shares"]
            sold = db.execute("SELECT shares FROM sales WHERE stock = ? AND user_id = ?", stk, id)
            for sale in sold:
                total -= sale["shares"]

            count += 1
            symbols.append(stk)
            stocks[count] = {}
            stocks[count]["name"] = info["name"]
            stocks[count]["price"] = info["price"]
            stocks[count]["shares"] = total
            stocks[count]["value"] = info["price"] * total
    cash = db.execute("SELECT cash FROM users WHERE id = ?", id)[0]["cash"]

    if stocks.get(1) == None:
        return render_template("index.html", cash=cash)

    return render_template("index.html", stocks=stocks, cash=cash)


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
    if request.method == "POST":
        if not request.form.get("amount"):
            return apology("Please Input Funds to be Added")
        if int(request.form.get("amount")) < 1:
            return apology("Please Input Non-Negtive Number", 403)

        add = int(request.form.get("amount"))

        newCash = cash + add

        db.execute("UPDATE users SET cash = ? WHERE id = ?", newCash, session["user_id"])

        return redirect("/")
    else:
        return render_template("add.html", cash=cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("Please Input Symbol", 400)
        if not request.form.get("shares"):
            return apology("Please Input an Amount of Shares", 400)
        if not request.form.get("shares").isdigit():
            return apology("Please Provide a Number", 400)
        if int(request.form.get("shares")) < 1:
            return apology("Amount Must be Positive", 400)

        info = lookup(request.form.get("symbol"))
        if info == None:
            return apology("Invalid Symbol", 400)

        shares = int(request.form.get("shares"))

        cost = info["price"] * shares
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

        if cash < cost:
            return apology("Insufficient Funds", 400)

        db.execute("INSERT INTO purchases (user_id, stock, price, date, shares, action) VALUES(?,?,?,?,?,?)", session["user_id"], info["symbol"], cost, dt.datetime.today(), shares, "purchase")

        newCash = cash - cost
        db.execute("UPDATE users SET cash = ? WHERE id = ?", newCash, session["user_id"])

        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    transactions = db.execute("SELECT stock, price, date, shares, action FROM purchases UNION SELECT stock, price, date, shares, action FROM sales WHERE user_id = ? ORDER BY date", session["user_id"])

    return render_template("history.html", stocks=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("Must Provide Valid Symbol", 400)

        info = lookup(request.form.get("symbol"))
        if info == None:
            return apology("Quote Cannot be Found", 400)

        name = info["name"]
        price = info["price"]
        symbol = info["symbol"]

        return render_template("quoted.html", name=name, price=price, symbol=symbol)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("Must Provide Username", 400)
        if not request.form.get("password"):
            return apology("Must Provide Password", 400)
        if not request.form.get("confirmation"):
            return apology("Must Confirm Password", 400)
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords Must Match", 400)

        username = request.form.get("username")
        hash = generate_password_hash(request.form.get("password"))

        try:
            db.execute("INSERT INTO users (username, hash) VALUES(?,?)", username, hash)
        except ValueError:
            return apology("Username Already Exists", 400)

        session["user_id"] = db.execute("SELECT id FROM users WHERE username = ?", username)[0]["id"]

        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("Please Select a Valid Symbol", 400)
        if not request.form.get("shares"):
            return apology("Please Input an Amount of Shares", 400)
        if not request.form.get("shares").isdigit():
            return apology("Please Provide a Number", 400)
        if int(request.form.get("shares")) < 1:
            return apology("Amount Must be Positive", 400)

        owned = db.execute("SELECT stock FROM purchases WHERE user_id = ?", session["user_id"])
        stocks = {}
        symbol = []

        for stock in owned:
            stock = stock["stock"]
            if stock not in symbol:
                total = 0
                shares = db.execute("SELECT shares FROM purchases WHERE stock = ? AND user_id = ?", stock, session["user_id"])
                for share in shares:
                    total += share["shares"]
                sold = db.execute("SELECT shares FROM sales WHERE stock = ? AND user_id = ?", stock, session["user_id"])
                for sale in sold:
                    total -= sale["shares"]
                symbol.append(stock)
                stocks[stock] = {}
                stocks[stock]["symbol"] = stock
                stocks[stock]["shares"] = total

        shares = int(request.form.get("shares"))

        if request.form.get("symbol") not in symbol:
            return apology("No Stocks Found", 400)
        if shares > stocks[request.form.get("symbol")]["shares"]:
            return apology("Insufficient Shares", 400)

        info = lookup(request.form.get("symbol"))
        if info == None:
            return apology("Stock not Found", 400)

        value = shares * info["price"]
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

        newCash = cash + value
        db.execute("UPDATE users SET cash = ? WHERE id = ?", newCash, session["user_id"])

        db.execute("INSERT INTO sales (user_id, stock, price, date, shares, action) VALUES(?,?,?,?,?,?)", session["user_id"], request.form.get("symbol"), value, dt.datetime.today(), shares, "sale")

        return redirect("/")
    else:
        stocks = []

        owned = db.execute("SELECT stock FROM purchases WHERE user_id = ?", session["user_id"])
        for stock in owned:
            stock = stock["stock"]
            if stock not in stocks:
                total = 0
                shares = db.execute("SELECT shares FROM purchases WHERE stock = ? AND user_id = ?", stock, session["user_id"])
                for share in shares:
                    total += share["shares"]
                sold = db.execute("SELECT shares FROM sales WHERE stock = ? AND user_id = ?", stock, session["user_id"])
                for sale in sold:
                    total -= sale["shares"]
            if total > 0:
                stocks.append(stock)

        return render_template("sell.html", symbols=stocks)
