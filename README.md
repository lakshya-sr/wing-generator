# Wing Generator

This script generates wing models from airfoil data, wing type and wing parameters.

# Usage

## 1. Setup

Run in command line:

```
pip install -r requirements.txt
```

## 2. Run

```
python generate.py <wing_type> <airfoil> -w <wingspan> -c <chord> -o <output>
```

Replace <wing_type> with type of wing (Currently only "rectangle" is supported), &lt;airfoil> with name of csv file of airfoil data download from airfoiltools.com, &lt;output> with output filename.

