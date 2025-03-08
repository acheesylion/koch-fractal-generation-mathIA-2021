# kochfractalgeneration

Koch Fractal Generation is a Python Class to aid in the generation of general koch fractal functions

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the necessary dependancies.

```bash
pip install numpy
pip install matplotlib
```

## Usage

```python
import kochfractalgeneration.py

# create a base fractal, with the number of sides to be generated
# this is done using the KochFractal Class 
# the static method gen_reg_polygon_base(sides) is used to generate the desired polygon
sides = 3 # this will generate a regular polygon of side 3, a triangle
base_fractal = KochFractal.gen_reg_polygon_base(sides)

# from the different subclasses, choose a subclass variant 
generation = 1
points = KochTriangle(base_fractal).generate(generation)

# plot the points using matplotlib
plot_fractal(points)

```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)