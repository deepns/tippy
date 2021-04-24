import os
import tippy

os.chdir(os.path.dirname(__file__))

def main():
    config = tippy.get_config("config.json")
    tips = tippy.get_tips(config)
    for tip in tips:
        tippy.show_tip(tip)

if __name__ == "__main__":
    main()
