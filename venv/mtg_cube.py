import json
import csv

import pandas as pd


class Cube:
    def __init__(self, name, desc, cmdr, strats, pwd, is_new):
        self.card_info = None
        self.name = name
        self.file = "venv/static/Cubes/" + name + ".xlsx"
        self.cards_file = "venv/static/Cubes/" + name + "_cards.csv"
        self.desc = desc
        self.cmdr = cmdr
        self.strats = strats
        self.pwd = pwd
        self.is_new = is_new


    def new_cube(self):
        self.cube_info = pd.DataFrame({
            'cube_name': self.name,
            'cube_description': self.desc,
            'cube_is_cmdr': self.cmdr,
            'cube_strats': self.strats,
            'cube_pwd': self.pwd
        }, index=[0])
        self.cube_info.to_excel(self.file, sheet_name='Cube Info', index=False)

    def add_card(self, card_name, card_cid, card_strats, card_tags):
        print(self.file)
        card_info = pd.DataFrame({
            'card_name': card_name,
            'card_cid': card_cid,
            'card_strats': card_strats,
            'card_tags': card_tags
        }, index=[0])
        with pd.ExcelWriter(self.file) as writer:
            card_info.to_excel(writer, sheet_name='Cards')
            #card_info.to_excel(self.file, sheet_name='Cards', index=False)


def get_cube(folder, cube_name):
    try:
        res_path = folder + "/" + cube_name + ".xlsx"
        cube_info = pd.read_excel(res_path)
        res_name = cube_info['cube_name']
        res_desc = cube_info['cube_description']
        res_cmdr = cube_info['cube_is_cmdr']
        res_strats = cube_info['cube_strats']
        res_pwd = cube_info['cube_pwd']
        res_cube = Cube(res_name, res_desc, res_cmdr, res_strats, res_pwd)
        return res_cube
    except FileNotFoundError:
        return "No matching cube"
