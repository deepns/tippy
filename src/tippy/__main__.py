import os

os.chdir(os.path.dirname(__file__))
import tippy

config = tippy.get_config("config.json")
tips = tippy.get_tips(config)
for tip in tips:
    tippy.show_tip(tip)
