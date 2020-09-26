# Age of Empires 2 - Image generator
Generates images of units, buildings and terrain from Age of Empires 2 HD by using pyautogui to click through the map editor. Needs the base game available in steam to run.


## Getting started
Make sure you're logged into steam and have AoE2 HD in the library. To see if AoE2 starts correctly try running `bash -c "steam steam://rungameid/221380"`.

```fish
git clone https://github.com/joalon/aoe2-ml-image-generator
cd aoe2-ml-image-generator
python3 -m venv venv
. venv/bin/activate
pip3 install -r requirements.txt
python3 -m aoe2_image_gen multi_label -n 5 --visible
```

The result should end up in `results/` with either a labels.csv and a `train/` sub dir or several directories under `results/train/`.

## TODO:
* The villager/no-villager generator
* Building generator for images segmentation
