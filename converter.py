import os
import re
import sys
import svgutils
import pandas as pd
from cairosvg import svg2png


SIZES = [50, 100, 150, 200, 250, 300, 350, 400]
SVG_FOLDER = 'logos'


def saveAsPngs(filename, path):
    svg = svgutils.transform.fromfile(filename)
    for size in SIZES:
        svg.set_size([str(size), str(size)])
        png_file = path + "/" + str(size) + "x" + str(size) + ".png"
        svg2png(bytestring=svg.to_str(), write_to=png_file)


if __name__ == "__main__":
    assert len(sys.argv) > 1, "Need Input Csv file"
    df = pd.read_csv(sys.argv[1])
    for key, svg_file in zip(df['School Name'].tolist(), df['svg_file_path'].tolist()):
        print("=" * 50)
        print("Converting svg file for " + key)
        keyname = " ".join(re.findall("[a-zA-Z]+", key)).replace(" ", '_')
        path = SVG_FOLDER + "/" + keyname
        if (svg_file == "Fail") or not os.path.exists(svg_file):
            print("WARNING: Did not find svg file for " + key)
        try:
            saveAsPngs(svg_file, path)
            print("Successfully convert svg into pngs!")
        except:
            print("ERROR: Failed to generate pngs!")
    print("="*50)
    print("DONE")