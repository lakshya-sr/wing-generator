import cadquery as cq
from cadquery.vis import show

def import_airfoil(filename):
    with open(filename) as f:
        coords = []
        chord = 1
        reading_coords = False
        for line in f:
            match line:
                case "Airfoil surface,\n":
                    print("Hello")
                    next(f)
                    reading_coords = True
                case ",\n":
                    if reading_coords:
                        reading_coords = False
                case _:
                    if reading_coords:
                        print(line)
                        coords.append(tuple(map(lambda x: float(x)/chord, line.split(","))))
                    elif line.startswith("Chord("):
                        print(line)
                        chord = float(line.split(",")[1])

        return coords        


def rectangle(span, chord, airfoil):
    airfoil = list(map(lambda x: (x[0]*chord, x[1]*chord), airfoil))
    wing = cq.Workplane("XY").polyline(airfoil).close().toPending().extrude(span)
    return wing

if __name__ == "__main__":
    show(rectangle(70*2.54, 30, import_airfoil("n63412-il.csv"))) 
