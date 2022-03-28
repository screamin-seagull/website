import os
from flask import Flask, render_template, request, Blueprint, flash, g, redirect, url_for
from sqlalchemy import create_engine, MetaData
from guess_ai import *
from bird_scraper import *
from mtg_cube import *
import pandas as pd
import json
import git
import scrython as scry
import asyncio

app = Flask(__name__)
app.config["SECRET_KEY"] = "k137p!t4"
bp = Blueprint('blog', __name__)
engine = create_engine('sqlite:////tmp/blog.db')

cube_dir = "venv/static/Cubes"
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
    return render_template("home.html.j2", bird_image=bird_pic,
                           bird_name=bird, bird_url=bird_url)


@app.route("/comics")
def comic_list():
    return render_template("all_comics.html.j2", comics=comic_folder)


@app.route("/comics/<id>")
def comic_page():
    return render_template("comic_page.html.j2", id=id)


@app.route("/guesser", methods=["GET", "POST"])
def guesser():
    if request.method == "GET":
        return render_template("number_guesser.html.j2")
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
            return render_template("number_guesser.html.j2", output=output, guess_ai=guess_ai)
        else:
            output = "Something went wrong. Please try again"
            return render_template("number_guesser.html.j2", output=output)


@app.route("/gang_info")
def gang_info():
    return render_template("gang_info.html.j2")


@app.route("/cube_tool")
def cube_tool():
    return render_template("cube_tool.html.j2")


@app.route("/cube_tool/create", methods=["GET", "POST"])
def create_cube():
    if request.method == "GET":
        return render_template("create_cube.html.j2")
    elif request.method == "POST" and request.form["btn"] == "Create Cube":
        name = request.form.get("cube_name")
        desc = request.form.get("cube_desc")
        cmdr = request.form.get("cmdr")
        strats = request.form.get("cube_strats")
        pwd = request.form.get("password")
        Cube(name, desc, cmdr, strats, pwd)
        return redirect("/cube_tool/view/" + name)


@app.route("/cube_tool/view")
def cube_list():
    cubes = get_cubes()
    return render_template("cube_list.html.j2", cubes=cubes)


@app.route("/cube_tool/view/<cube_name>", methods=["GET", "POST"])
def cube_view(cube_name):
    if request.method == "GET":
        view_cube = get_cube(cube_dir, cube_name)
        return render_template("display_cube.html.j2", view_cube=view_cube,
                               cube_name=cube_name)
    elif request.method == "POST":
        return render_template("display_cube.html.j2")


@app.route("/cube_tool/edit/<cube_name>", methods=["GET", "POST"])
def cube_edit(cube_name):
    edit_cube = get_cube(cube_dir, cube_name)
    if request.method == "GET":
        return render_template("edit_cube.html.j2", edit_cube=edit_cube,
                               cube_name=cube_name)
    elif request.method == "POS T":
        asyncio.set_event_loop(asyncio.new_event_loop())  # Check to see if I need to terminate this or anything
        add_input = request.form.get("card")
        try:
            add = scry.cards.Named(fuzzy=add_input).name()
            edit_cube.add_card(add, 'UR', "Arf, Meow", "Commander")
        except scry.ScryfallError:
            error_msg = "Sorry, no cards were found matching the name " + add_input
            return render_template("edit_cube.html.j2", edit_cube=edit_cube,
                                   cube_name=cube_name, message=error_msg)
        return render_template("edit_cube.html.j2", edit_cube=edit_cube,
                               cube_name=cube_name, add_card=add)


@app.route("/bird_scraper", methods=["GET", "POST"])
def bird_scraper():
    return render_template("bird_scraper.html.j2")


@app.route("/skyehaven", methods=["GET", "POST"])
def skyehaven():
    if request.method == "GET":
        mode = "default"
        return render_template("skyehaven.html.j2", mode=mode)


@app.route("/skyehaven/concept_art")
def concept_art():
    return render_template("concept_art.html.j2", concepts=get_concepts())


if __name__ == "__main__":
    app.run()
