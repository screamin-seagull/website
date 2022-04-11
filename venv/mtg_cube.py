import pandas as pd


class Cube:
    def __init__(self, folder, name, desc, cmdr, strats, pwd, is_new):
        self.card_info = {}
        self.cube_info = {}
        self.name = name
        self.file = str(folder) + str(name) + ".xlsx"
        self.desc = desc
        self.cmdr = cmdr
        self.strats = strats.split(", ")
        self.is_new = is_new
        if self.is_new:
            self.new_cube()
            self.pwd = pwd

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
            # card_info.to_excel(self.file, sheet_name='Cards', index=False)


def load(path):
    try:
        cube_info = pd.read_excel(path, sheet_name='Cube Info')
        res_name = cube_info['cube_name'][0]
        res_desc = cube_info['cube_description'][0]
        res_cmdr = cube_info['cube_is_cmdr'][0]
        res_strats = cube_info['cube_strats'][0]
        res_pwd = cube_info['cube_pwd'][0]
        res_cube = Cube(path, res_name, res_desc, res_cmdr, res_strats, res_pwd, False)
        return res_cube
    except FileNotFoundError:
        return "No matching cube"
