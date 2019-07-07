#!/usr/bin/python
import subprocess
import time
import random

import pyautogui

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

    try:
        random_map_untoggled = pyautogui.locateCenterOnScreen('images/map-editor/aoe2-map-editor-random-map-untoggled.png')
        random_map_untoggled_clickable = pyautogui.Point(random_map_untoggled.x - 40, random_map_untoggled.y)
        pyautogui.click(random_map_untoggled_clickable)
    except:
        pass

    try:
        random_map_dropdown= pyautogui.locateCenterOnScreen('images/map-editor/aoe2-map-editor-random-map-dropdown-undropped.png')
        random_map_dropdown_clickable = pyautogui.Point(random_map_dropdown.x + 107, random_map_dropdown.y + 7)
        pyautogui.click(random_map_dropdown_clickable)
        pyautogui.typewrite('aaaa\n', interval=0.2)
    except:
        pass

    generate_map_button_center = pyautogui.locateCenterOnScreen('images/map-editor/aoe2-map-editor-generate-map-button.png')
    pyautogui.click(generate_map_button_center)

def place_villager():
    try:
        units_button_center = pyautogui.locateCenterOnScreen('images/map-editor/aoe2-map-editor-units-button.png')
        pyautogui.click(units_button_center)
    except:
        pass

    villager_place = pyautogui.Point(960, 540)

    try:
        delete_unit_button = pyautogui.locateCenterOnScreen('images/map-editor/aoe2-map-editor-delete-unit-checkbox-unchecked.png')
        delete_unit_button_clickable = pyautogui.Point(delete_unit_button.x - 10, delete_unit_button.y)
        pyautogui.click(delete_unit_button_clickable)
        for i in range(5):
            pyautogui.click(villager_place)
    except:
        pass


    n = round(random.uniform(0,1))
    if n == 0:
        pyautogui.typewrite('v')
    else:
        pyautogui.typewrite('vv')

    pyautogui.click(villager_place)

    pyautogui.moveRel(yOffset=260)

def take_screenshot(unit_name, n):
    screenshot_center_offset = round(random.uniform(0,180))
    pyautogui.screenshot('result/' + unit_name + '_' + str(n) + '.png', region=(960 - screenshot_center_offset, 540 - screenshot_center_offset, 224, 224))

def wait_for_image(image):
    while pyautogui.locateOnScreen(image) == None:
        time.sleep(0.5)

start_aoe2()
open_map_editor()

num_villagers = 0
num_no_villagers = 0

for i in range(0, 2000):
    generate_random_map()
    
    n = round(random.uniform(0,1))
    if n == 0:
        num_villagers += 1
        place_villager()
        take_screenshot('villager', num_villagers) 
    else:
        num_no_villagers += 1
        take_screenshot('no-villager', num_no_villagers)

print('''


Ran until the end!


''')