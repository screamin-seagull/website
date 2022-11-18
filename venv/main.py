import os
from flask import Flask, render_template, request, Blueprint, redirect
from sqlalchemy import create_engine
from guess_ai import *
from bird_scraper import *
from mtg_cube import *
import scrython as scry
import asyncio
import pandas as pd
import json
import plotly
import plotly.express as px
from venv import SpotifyToybox as st

app = Flask(__name__)
app.config["SECRET_KEY"] = "k137p!t4"
bp = Blueprint('blog', __name__)
engine = create_engine('sqlite:////tmp/blog.db')

comic_folder = os.listdir(os.path.join(app.static_folder, "Comics"))


def get_cubes():
    cube_folder = os.listdir(os.path.join(app.static_folder, "Cubes"))
    cubes = []
    for cube in cube_folder:
        cubes.append(cube[: - 5])
    return cubes


def get_concepts():
    concept_folder = os.listdir(os.path.join(app.static_folder, "Concept Art"))
    return concept_folder


@app.route("/")
def default_route():
    return redirect("/home")


@app.route("/home")
def homepage():
    home_bird = RandomBird()
    bird_pic = home_bird.main_image
    bird_url = home_bird.bird_url
    bird = home_bird.bird_name
    return render_template("home.html", bird_image=bird_pic,
                           bird_name=bird, bird_url=bird_url)


@app.route("/guesser", methods=["GET", "POST"])
def guesser():
    if request.method == "GET":
        return render_template("number_guesser.html")
    elif request.method == "POST":
        if request.form["btn"] == "Run":
            target = request.form.get("target_num")
            guess_ai = Guesser(target, 5, 20, 5)
            output = []
            while guess_ai.best_guess[0] != int(target):
                output.extend([str(guess_ai.get_gen()), str(guess_ai.get_best()),
                               "Best Guess: " + str(guess_ai.best_guess[0])])
                guess_ai.next_gen()

            output.extend([str(guess_ai.get_gen()), str(guess_ai.get_best()),
                          "Best Guess: " + str(guess_ai.best_guess[0])])
            output.append("You number was guessed in " + str(guess_ai.current_gen) + " generations")
            return render_template("number_guesser.html", output=output, guess_ai=guess_ai)
        else:
            output = "Something went wrong. Please try again"
            return render_template("number_guesser.html", output=output)


@app.route("/info")
def project_info():
    return render_template("info.html", active_project="guesser")


@app.route("/cube_tool")
def cube_tool():
    return render_template("cube_tool.html")


@app.route("/cube_tool/create", methods=["GET", "POST"])
def create_cube():
    if request.method == "GET":
        return render_template("create_cube.html")
    elif request.method == "POST" and request.form["btn"] == "Create Cube":
        folder = os.path.join(app.static_folder, 'Cubes/')
        name = request.form.get("cube_name")
        desc = request.form.get("cube_desc")
        cmdr = request.form.get("cmdr")
        strats = request.form.get("cube_strats")
        pwd = request.form.get("password")
        Cube(folder, name, desc, cmdr, strats, pwd, True)
        return redirect("/cube_tool/view/" + name)


@app.route("/cube_tool/view")
def cube_list():
    cubes = get_cubes()
    return render_template("cube_list.html", cubes=cubes)


@app.route("/cube_tool/view/<cube_name>")
def cube_view(cube_name):
    cube_dir = os.path.join(app.static_folder, 'Cubes/') + cube_name + ".xlsx"
    view_cube = load(cube_dir)
    return render_template("display_cube.html", view_cube=view_cube,
                           cube_name=cube_name)


@app.route("/cube_tool/edit/<cube_name>", methods=["GET", "POST"])
def cube_edit(cube_name):
    cube_dir = os.path.join(app.static_folder, 'Cubes/') + cube_name + ".xlsx"
    edit_cube = load(cube_dir)
    strats = edit_cube.strats
    if request.method == "GET":
        return render_template("edit_cube.html", edit_cube=edit_cube,
                               cube_name=cube_name, strats=strats)
    elif request.method == "POST":
        asyncio.set_event_loop(asyncio.new_event_loop())  # Check to see if I need to terminate this or anything
        add_input = request.form.get("card")
        try:
            add = scry.cards.Named(fuzzy=add_input).name()
            print(add)
            edit_cube.add_card(add, 'UR', "Arf, Meow", "Commander")
        except scry.ScryfallError:
            error_msg = "Sorry, no cards were found matching the name " + add_input
            return render_template("edit_cube.html", edit_cube=edit_cube,
                                   cube_name=cube_name, message=error_msg,
                                   strats=strats)
        return render_template("edit_cube.html", edit_cube=edit_cube,
                               cube_name=cube_name, add_card=add,
                               strats=strats)


@app.route("/bird_scraper", methods=["GET", "POST"])
def bird_scraper():
    bird = RandomBird()
    bird_pic = bird.main_image
    bird_url = bird.bird_url
    bird_name = bird.bird_name
    return render_template("bird_scraper.html", bird_image=bird_pic,
                           bird_name=bird_name, bird_url=bird_url)


@app.route("/skyehaven", methods=["GET", "POST"])
def skyehaven():
    if request.method == "GET":
        mode = "default"
        return render_template("skyehaven.html", mode=mode)


@app.route("/skyehaven/stories")
def short_stories():
    return render_template("WIP.html")


@app.route("/skyehaven/concept_art")
def concept_art():
    return render_template("concept_art.html", concepts=get_concepts())


@app.route("/spotify_toybox", methods=["GET", "POST"])
def toybox():
    test_file = "static/jordan_data.json"
    testbox = st.SpotifyToybox(test_file)
    artists, times = [], []
    if request.method == 'GET':
        test_times = testbox.top_artists_time(False, 8)
        for time in test_times:
            print(time, test_times[time])
            artists.append(time)
            times.append(test_times[time] / 60000)
        print(artists, times)
    elif request.method == 'POST':
        toy_file = request.form.get('filename')
        toybox = st.SpotifyToybox(toy_file)
        toybox_times = toybox.top_artists_time(False, 8)
        for time in toybox_times:
            print(time, toybox_times[time])
            artists.append(time)
            times.append(toybox_times[time] / 60000)
        print(artists, times)
    df = pd.DataFrame({
        'Artist': artists,
        'Time': times
    })
    fig = px.bar(df, x='Artist', y='Time', color='Artist', width=len(artists) * 100, height=600)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("toybox.html", graphJSON=graphJSON)


if __name__ == "__main__":
    app.run()
