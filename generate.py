import cadquery as cq
from cadquery.vis import show
import argparse
import sys

def import_airfoil(filename):
    with open(filename) as f:
        coords = []
        chord = 1
        reading_coords = False
        for line in f:
            match line:
                case "Airfoil surface,\n":
                    next(f)
                    reading_coords = True
                case ",\n":
                    if reading_coords:
                        reading_coords = False
                case _:
                    if reading_coords:
                        log(line)
                        coords.append(tuple(map(lambda x: float(x)/chord, line.split(","))))
                    elif line.startswith("Chord("):
                        log(line)
                        chord = float(line.split(",")[1])

        return coords        


def rectangle(span, chord, airfoil):
    airfoil = list(map(lambda x: (x[0]*chord, x[1]*chord), airfoil))
    wing = (cq.Workplane("XY")
            .polyline(airfoil)
            .close()
            .toPending()
            .extrude(span))
    return wing


logging = False
def log(msg):
    if logging:
        print(msg)

if __name__ == "__main__":
    #show(rectangle(70*2.54, 30, import_airfoil("n63412-il.csv"))) 
    parser = argparse.ArgumentParser(prog="WingGenerator", 
            description="Generate 3D models for wings by specifying type and parameters.")
    parser.add_argument("wing_type")
    parser.add_argument("airfoil")
    parser.add_argument("-w", "--wingspan")
    parser.add_argument("-c", "--chord")
    parser.add_argument("-o", "--output")

    args = parser.parse_args()
    wing = None
    match args.wing_type:
        case "rectangle":
            wing = rectangle(float(args.wingspan), float(args.chord), import_airfoil(args.airfoil))
        case _:
            log("Wing type not supported")
            exit()
    if wing:
        if args.output:
            filename = args.output
        else:
            filename = f"{args.airfoil.rstrip('.csv')}-{args.wing_type}.step"
        wing.export(filename)
    else:
        log("Error")

