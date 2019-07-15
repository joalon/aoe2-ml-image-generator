#!/usr/bin/python
import subprocess
import time
import random

from aoe2_units import units_dict

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

def take_screenshot(n):
    pyautogui.moveRel(xOffset=200, yOffset=200)
    pyautogui.screenshot('result/' + str(n) + '.png', region=(848, 428, 224, 224))

def wait_for_image(image):
    while pyautogui.locateOnScreen(image) == None:
        time.sleep(0.5)

def goto_units_screen():
    units_button_center = pyautogui.locateCenterOnScreen('images/map-editor/aoe2-map-editor-units-button.png')
    pyautogui.click(units_button_center)

def place_unit(unit, location):
    pyautogui.typewrite(units_dict[unit]['place_command'], interval=0.15)
    pyautogui.click(location)

def point_is_near_other_locations(location, list_of_locations):
    if not list_of_locations:
        return False

    for i in range(len(list_of_locations) - 1):
        if abs(list_of_locations[i].x - location.x) < 40:
            return True
        elif abs(list_of_locations[i].y - location.y) < 40:
            return True
    return False

def generate_random_point():
    random_x = random.uniform(0, 224) + 848
    random_y = random.uniform(0, 224) + 428
    return pyautogui.Point(random_x, random_y)


csv_filename = 'labels.csv'
with open(csv_filename, 'a') as csv_file:
    csv_file.write("file, labels\n")

for i in range(3):
    time.sleep(3)
    labels = []
    already_used_locations = []
    number_of_units = round(random.uniform(1, 5))

    print('placing ' + str(number_of_units) + ' units')
    for j in range(number_of_units):
        random_unit_int = round(random.uniform(0, len(units_dict) - 1))
        unit = list(units_dict.keys())[random_unit_int]
        print('placing unit: ' + unit)

        location = generate_random_point()
        while point_is_near_other_locations(location, already_used_locations):
            location = generate_random_point() 
            print('new location is: ' + str(location))
        already_used_locations.append(location)

        place_unit(unit, location)
        if unit not in labels:
            labels.append(unit)

    pyautogui.moveRel(xOffset=200)

    with open(csv_filename, 'a') as csv_file:
        csv_file.write(str(i) + ', ' + " ".join(labels) + "\n")
    #take_screenshot(i)
    #write_labels()
    print('labels is: ' + " ".join(labels))
    print('already_used_locations is: ' + str(already_used_locations))
    print('''
        
    ''')




#start_aoe2()
#open_map_editor()
#
#num_villagers = 0
#num_no_villagers = 0
#
#for i in range(0, 2000):
#    generate_random_map()
#    
#    n = round(random.uniform(0,1))
#    if n == 0:
#        num_villagers += 1
#        place_villager()
#        take_screenshot('villager', num_villagers) 
#    else:
#        num_no_villagers += 1
#        take_screenshot('no-villager', num_no_villagers)

print('''


Ran until the end!


''')