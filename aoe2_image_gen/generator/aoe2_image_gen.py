#!/usr/bin/python
import time
import random
import pyautogui
from pynput.mouse import Listener
import os
import Xlib
import argparse

from aoe2_image_gen.generator.aoe2_units import units_dict, terrain_dict

from easyprocess import EasyProcess
from pyvirtualdisplay import Display



def steam_login():
    steam_password = os.environ["STEAM_PASSWORD"]

    wait_for_image(f"{IMAGE_PATH}/steam/steam-login-screen.png")

    steam_password_box_center = pyautogui.locateCenterOnScreen(
        f"{IMAGE_PATH}/steam/steam-password-box.png"
    )
    pyautogui.click(steam_password_box_center)
    pyautogui.typewrite(steam_password + "\n")


def open_map_editor():
    map_editor_location_center = pyautogui.locateCenterOnScreen(
        f"{IMAGE_PATH}/main-menu/aoe2-map-editor-button.png"
    )
    pyautogui.click(map_editor_location_center)

    create_scenario_button_center = pyautogui.locateCenterOnScreen(
        f"{IMAGE_PATH}/main-menu/aoe2-create-scenario-button.png"
    )
    pyautogui.click(create_scenario_button_center)

    create_button_center = pyautogui.locateCenterOnScreen(
        f"{IMAGE_PATH}/main-menu/aoe2-create-button.png"
    )
    pyautogui.click(create_button_center)

    wait_for_image(f"{IMAGE_PATH}/map-editor/aoe2-map-editor-main-starting-view.png")


def generate_random_map():
    # try:
    #    map_button_center = pyautogui.locateCenterOnScreen('images/map-editor/aoe2-map-editor-map-button-unclicked.png')
    #    pyautogui.click(map_button_center)
    # except:
    #    print("Couldn't find the map editor button")

    pyautogui.click(x=25, y=18)

    default_terrain_dropdown = pyautogui.locateCenterOnScreen(
        f"{IMAGE_PATH}/map-editor/aoe2-map-editor-default-terrain-text.png"
    )
    default_terrain_dropdown_clickable = pyautogui.Point(
        default_terrain_dropdown.x + 195, default_terrain_dropdown.y + 20
    )
    pyautogui.click(default_terrain_dropdown_clickable)

    terrain_index = round(random.uniform(0, len(terrain_dict)) - 1)
    pyautogui.typewrite(list(terrain_dict[terrain_index].values())[0], interval=0.2)

    generate_map_button_center = pyautogui.locateCenterOnScreen(
        f"{IMAGE_PATH}/map-editor/aoe2-generate-map-button.png"
    )
    pyautogui.click(generate_map_button_center)


def take_screenshot(n):
    pyautogui.screenshot(
        "results/train/" + str(n) + ".png", region=(400, 272, 224, 224)
    )


def wait_for_image(image, timeout=30):
    seconds_waited = 0
    wait_time = 0.5
    while pyautogui.locateOnScreen(image) == None:
        time.sleep(wait_time)
        seconds_waited += wait_time
        if seconds_waited > timeout:
            raise TimeoutError("wait_for_image timeout expired")
    time.sleep(0.01)


def open_unit_editor():
    try:
        units_button_center = pyautogui.locateCenterOnScreen(
            f"{IMAGE_PATH}/map-editor/aoe2-map-editor-units-button.png"
        )
        pyautogui.click(units_button_center)
    except:
        pass


def place_unit(unit, location):
    pyautogui.typewrite(units_dict[unit]["place_command"], interval=0.15)
    pyautogui.click(location)


def point_is_near_other_locations(location, list_of_locations):
    if not list_of_locations:
        return False

    for i in range(len(list_of_locations)):
        if (
            abs(list_of_locations[i].x - location.x) < 50
            and abs(list_of_locations[i].y - location.y) < 50
        ):
            return True
    return False


def generate_random_point():
    random_x = random.uniform(12, 140) + 400
    random_y = random.uniform(60, 200) + 272
    return pyautogui.Point(random_x, random_y)


def generate_villager_dataset(numberOfImages):
    global VISIBLE
    print(numberOfImages)
    if VISIBLE:
        print("Visible!")
    raise NotImplementedError()


def show_map_editor(numberOfImages):
    global VISIBLE
    with Display(visible=1 if VISIBLE else 0, size=(res_x, res_y)) as disp:
        pyautogui._pyautogui_x11._display = Xlib.display.Display(os.environ["DISPLAY"])
        with EasyProcess(f'bash -c "steam steam://rungameid/{GAME_ID}"'):

            wait_for_image(f"{IMAGE_PATH}/main-menu/aoe2-main-menu.png")

            open_map_editor()

            def on_click(x, y, button, pressed):
                print('{0} {1} at {2}'.format(
                    'Pressed' if pressed else 'Released',
                    button,
                    (x, y)))

            with Listener(on_click=on_click) as listener:
                listener.join()



def generate_multi_label_dataset(numberOfImages, csv_filename="results/labels.csv"):
    with Display(visible=1 if VISIBLE else 0, size=(res_x, res_y), backend='xephyr') as disp:
        pyautogui._pyautogui_x11._display = Xlib.display.Display(os.environ["DISPLAY"])
        with EasyProcess(f'bash -c "steam steam://rungameid/{GAME_ID}"'):

            if not os.path.exists(csv_filename):
                with open(csv_filename, "w+") as f:
                    f.write("image_name, tags\n")

            if not os.path.exists("./results/train"):
                os.mkdir("./results/train")

            wait_for_image(f"{IMAGE_PATH}/main-menu/aoe2-main-menu.png")

            open_map_editor()

            for i in range(0, numberOfImages):
                generate_random_map()
                open_unit_editor()

                labels = []
                already_used_locations = []
                number_of_units = round(random.uniform(1, 6))

                for j in range(number_of_units):
                    try:
                        random_unit_int = round(random.uniform(0, len(units_dict)) - 1)
                        unit = list(units_dict.keys())[random_unit_int]

                        location_tries = 0
                        location = generate_random_point()
                        while point_is_near_other_locations(
                            location, already_used_locations
                        ):
                            location = generate_random_point()
                            location_tries += 1
                            if location_tries > 10:
                                raise Exception(
                                    "tried generating a random position too many times, giving up!"
                                )
                        already_used_locations.append(location)

                        place_unit(unit, location)
                        if unit not in labels:
                            labels.append(unit)
                    except:
                        pass

                with open(csv_filename, "a") as csv_file:
                    csv_file.write(str(i) + ", " + " ".join(labels) + "\n")

                # Move mouse out of the way of the screenshot
                pyautogui.moveRel(xOffset=224)
                take_screenshot(i)


def main():
    GAME_ID = None
    IMAGE_PATH = "images"

    res_x = 1024
    res_y = 768

    FUNCTION_MAP = {
        "map-editor": show_map_editor,
        "villagers": generate_villager_dataset,
        "multi_label": generate_multi_label_dataset,
    }

    parser = argparse.ArgumentParser(
        description="Generate machine learning datasets using the Age of Empires 2 map editor running under steam."
    )
    parser.add_argument("command", choices=FUNCTION_MAP.keys())
    parser.add_argument(
        "-n",
        type=int,
        nargs=1,
        default=[5],
        help="Number of images to generate in the dataset.",
    )
    parser.add_argument(
        "-v",
        "--visible",
        action="store_true",
        default=False,
        help="Start in a visible window, otherwise it runs in a virtual frame buffer.",
    )

    args = parser.parse_args()

    global VISIBLE
    VISIBLE = args.visible
    GAME_ID = '221380'
    IMAGE_PATH += '/hd'

    argument_function = FUNCTION_MAP[args.command]
    argument_function(numberOfImages=args.n[0])

if __name__ == "__main__":
    main()
