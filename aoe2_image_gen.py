#!/usr/bin/python
import subprocess
import time
import random
import traceback
import sys
import os
import pyautogui

from aoe2_units import units_dict, terrain_dict

def start_aoe2():
    subprocess.Popen(["bash", "-c", "steam steam://rungameid/221380"])
    wait_for_image('images/main-menu/aoe2-main-menu.png')

def open_map_editor():
    map_editor_location_center = pyautogui.locateCenterOnScreen('images/main-menu/aoe2-map-editor-button.png')
    pyautogui.click(map_editor_location_center)

    create_scenario_button_center = pyautogui.locateCenterOnScreen('images/main-menu/aoe2-main-menu-create-scenario-button.png')
    pyautogui.click(create_scenario_button_center)

    create_button_center = pyautogui.locateCenterOnScreen('images/main-menu/aoe2-main-menu-create-button.png')
    pyautogui.click(create_button_center)

    wait_for_image('images/map-editor/aoe2-map-editor-main-starting-view.png')

def generate_random_map():
    try:
        map_button_center = pyautogui.locateCenterOnScreen('images/map-editor/aoe2-map-editor-map-button-unclicked.png')
        pyautogui.click(map_button_center)
    except:
        pass

    default_terrain_dropdown= pyautogui.locateCenterOnScreen('images/map-editor/aoe2-map-editor-default-terrain-text.png')
    default_terrain_dropdown_clickable = pyautogui.Point(default_terrain_dropdown.x + 195, default_terrain_dropdown.y + 20)
    pyautogui.click(default_terrain_dropdown_clickable)

    terrain_index = round(random.uniform(0,len(terrain_dict)) - 1)
    pyautogui.typewrite(list(terrain_dict[terrain_index].values())[0], interval=0.2)

    generate_map_button_center = pyautogui.locateCenterOnScreen('images/map-editor/aoe2-map-editor-generate-map-button.png')
    pyautogui.click(generate_map_button_center)

def take_screenshot(n):
    pyautogui.moveRel(xOffset=200, yOffset=200)
    pyautogui.screenshot('result/train/' + str(n) + '.png', region=(848, 428, 224, 224))

def wait_for_image(image):
    while pyautogui.locateOnScreen(image) == None:
        time.sleep(0.5)

def open_unit_editor():
    try:
        units_button_center = pyautogui.locateCenterOnScreen('images/map-editor/aoe2-map-editor-units-button.png')
        pyautogui.click(units_button_center)
    except:
        pass

def place_unit(unit, location):
    pyautogui.typewrite(units_dict[unit]['place_command'], interval=0.15)
    pyautogui.click(location)

def point_is_near_other_locations(location, list_of_locations):
    if not list_of_locations:
        return False

    for i in range(len(list_of_locations)):
        if abs(list_of_locations[i].x - location.x) < 50 and abs(list_of_locations[i].y - location.y) < 50:
            return True
    return False

def generate_random_point():
    random_x = random.uniform(0, 144) + 898 
    random_y = random.uniform(0, 144) + 488
    return pyautogui.Point(random_x, random_y)

time.sleep(3)

csv_filename = 'result/labels.csv'

if os.stat(csv_filename).st_size == 0:
    with open(csv_filename, 'a') as csv_file:
        csv_file.write("image_name, tags\n")

start_aoe2()
open_map_editor()

for i in range(0, 30000):
    generate_random_map()
    open_unit_editor()

    labels = []
    already_used_locations = []
    number_of_units = round(random.uniform(1,6))

    print('placing ' + str(number_of_units) + ' units')
    for j in range(number_of_units):
        try:
            random_unit_int = round(random.uniform(0, len(units_dict)) - 1)
            unit = list(units_dict.keys())[random_unit_int]
            print('placing unit: ' + unit)

            location_tries = 0
            location = generate_random_point()
            while point_is_near_other_locations(location, already_used_locations):
                location = generate_random_point()
                location_tries += 1
                if location_tries > 10:
                    raise Exception('tried generating a random position too many times, giving up!')
            already_used_locations.append(location)

            place_unit(unit, location)
            if unit not in labels:
                labels.append(unit)
        except:
            print("Skipping...")
            pass

    with open(csv_filename, 'a') as csv_file:
        csv_file.write(str(i) + ', ' + " ".join(labels) + "\n")

    # Move mouse out of the way of the screenshot
    pyautogui.moveRel(xOffset=200)
    take_screenshot(i)

    print('labels is: ' + " ".join(labels))
    print('already_used_locations is: ' + str(already_used_locations))
    print('''
        
    ''')

print('''


Ran until the end!


''')
