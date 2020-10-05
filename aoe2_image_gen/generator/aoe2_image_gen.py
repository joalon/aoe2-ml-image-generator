#!/usr/bin/python
import time
import random
import pyautogui
import os
import Xlib

from aoe2_image_gen.generator.aoe2_units import units_dict, terrain_dict

from easyprocess import EasyProcess
from pyvirtualdisplay import Display


def steam_login():
    steam_password = os.environ["STEAM_PASSWORD"]

    wait_for_image("images/hd/steam/steam-login-screen.png")

    steam_password_box_center = pyautogui.locateCenterOnScreen(
        "images/hd/steam/steam-password-box.png"
    )
    pyautogui.click(steam_password_box_center)
    pyautogui.typewrite(steam_password + "\n")


def open_map_editor():
    map_editor_location_center = pyautogui.locateCenterOnScreen(
        "images/hd/main-menu/aoe2-map-editor-button.png"
    )
    pyautogui.click(map_editor_location_center)

    create_scenario_button_center = pyautogui.locateCenterOnScreen(
        "images/hd/main-menu/aoe2-create-scenario-button.png"
    )
    pyautogui.click(create_scenario_button_center)

    create_button_center = pyautogui.locateCenterOnScreen(
        "images/hd/main-menu/aoe2-create-button.png"
    )
    pyautogui.click(create_button_center)

    wait_for_image("images/hd/map-editor/aoe2-map-editor-main-starting-view.png")


def generate_random_map():
    pyautogui.click(x=25, y=18)

    default_terrain_dropdown = pyautogui.locateCenterOnScreen(
        "images/hd/map-editor/aoe2-map-editor-default-terrain-text.png"
    )
    default_terrain_dropdown_clickable = pyautogui.Point(
        default_terrain_dropdown.x + 195, default_terrain_dropdown.y + 20
    )
    pyautogui.click(default_terrain_dropdown_clickable)

    terrain_index = round(random.uniform(0, len(terrain_dict)) - 1)
    pyautogui.typewrite(list(terrain_dict[terrain_index].values())[0], interval=0.2)

    generate_map_button_center = pyautogui.locateCenterOnScreen(
        "images/hd/map-editor/aoe2-generate-map-button.png"
    )
    pyautogui.click(generate_map_button_center)


def take_screenshot(name, region):
    pyautogui.screenshot(
        "results/train/" + str(name) + ".png", region=region
    )


def wait_for_image(image, timeout=30):
    seconds_waited = 0
    wait_time = 0.5
    while pyautogui.locateOnScreen(image) == None:
        time.sleep(wait_time)
        seconds_waited += wait_time
        if seconds_waited > timeout:
            raise TimeoutError(f"wait_for_image timeout expired while waiting for {image}")
    time.sleep(0.01)


def open_unit_editor():
    units_button_center = pyautogui.locateCenterOnScreen(
        "images/hd/map-editor/aoe2-map-editor-units-button.png"
    )
    pyautogui.click(units_button_center)


def place_unit(unit, location):
    pyautogui.typewrite(unit["place_command"], interval=0.15)
    pyautogui.moveTo(location.x, location.y, 0.2, pyautogui.easeInQuad)
    pyautogui.click()

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


def generate_random_point() -> pyautogui.Point:
    random_x = random.uniform(12, 140) + 400
    random_y = random.uniform(60, 200) + 272
    return pyautogui.Point(random_x, random_y)


def generate_villager_dataset(numberOfImages, csv_filepath, visible, resolution):
    with Display(visible=1 if visible else 0, size=resolution, backend='xephyr') as disp:
        pyautogui._pyautogui_x11._display = Xlib.display.Display(os.environ["DISPLAY"])
        with EasyProcess('bash -c "steam steam://rungameid/221380"'):

            if not os.path.exists(csv_filepath):
                os.makedirs(csv_parentdir)

            wait_for_image("images/hd/main-menu/aoe2-main-menu.png")

            open_map_editor()

            for i in range(0, numberOfImages):

                unit = random.choice([unit_dict['male_villager'], unit_dict['female_villager'], None])

                filename = ""
                if unit is not None:
                    point = generate_random_point()
                    place_unit(unit, point)
                    filename = "villager_" + i
                else:
                    filename = "no-villager_" + i

                # Move mouse out of the way of the screenshot. Without tweening it would leave unit artifacts on screen
                pyautogui.moveTo(900, 700, 0.5, pyautogui.easeInQuad)
                take_screenshot(name=filename, region=(350, 272, 224, 224))


def generate_multi_label_dataset(numberOfImages: int, csv_filepath="results/labels.csv", resolution=(1024,768), visible=False):
    with Display(visible=1 if visible else 0, size=resolution, backend='xephyr') as disp:
        pyautogui._pyautogui_x11._display = Xlib.display.Display(os.environ["DISPLAY"])
        with EasyProcess('bash -c "steam steam://rungameid/221380"'):

            csv_parentdir = "/".join(csv_filepath.split("/")[0:-1])
            if not os.path.exists(csv_parentdir):
                os.makedirs(csv_parentdir)

            if not os.path.exists(csv_filepath):
                with open(csv_filepath, "w+") as f:
                    f.write("image_name, tags\n")

            wait_for_image("images/hd/main-menu/aoe2-main-menu.png")

            open_map_editor()

            for i in range(0, numberOfImages):
                generate_random_map()
                open_unit_editor()

                labels = []
                already_used_locations = []
                number_of_units = round(random.uniform(1, 6))

                for j in range(number_of_units):
                    try:
                        unit = random.choice(list(units_dict.items()))[1]

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
                        # Maybe try handling it!?
                        pass

                with open(csv_filepath, "a") as csv_file:
                    csv_file.write(str(i) + ", " + " ".join(labels) + "\n")

                # Move mouse out of the way of the screenshot. Without tweening it would leave unit artifacts on screen
                pyautogui.moveTo(900, 700, 0.5, pyautogui.easeInQuad)
                take_screenshot(name=i, region=(350, 272, 224, 224))
