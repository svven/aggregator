"""
Loads lua script from current folder.
Current script list: pick, unpick, set_fellows, set_edition.
"""
import jinja2
import os.path as path

from .. import r, keys

_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(searchpath=path.dirname(__file__)))
def _load(template):
    "Load script from specified jinja2 template."
    temp = _env.get_template(template)
    return temp.render(**keys.DICT)

# def _load(script):
#     "Load script from specified file name."
#     with open(path.join(path.dirname(__file__), script), 'r') as file:
#         return file.read()

pick = r.register_script(_load('pick.lua'))
unpick = r.register_script(_load('unpick.lua'))
rem_link_picks = r.register_script(_load('rem_link_picks.lua'))
rem_reader_picks = r.register_script(_load('rem_reader_picks.lua'))
set_fellows = r.register_script(_load('set_fellows.lua'))
set_edition = r.register_script(_load('set_edition.lua'))
