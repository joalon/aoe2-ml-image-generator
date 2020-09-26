import argparse
from aoe2_image_gen.generator import aoe2_image_gen

def main():

    function_map = {
        "villagers": aoe2_image_gen.generate_villager_dataset,
        "multi_label": aoe2_image_gen.generate_multi_label_dataset,
    }

    parser = argparse.ArgumentParser(
        description="Generate machine learning datasets using the Age of Empires 2 map editor running under steam."
    )
    parser.add_argument("command", choices=function_map.keys())
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
    resolution = (1024, 768)

    argument_function = function_map[args.command]
    argument_function(numberOfImages=args.n[0], resolution=resolution, visible=args.visible)

if __name__ == "__main__":
    main()
