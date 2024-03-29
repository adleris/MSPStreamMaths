# Stream Maths
This package contains functions to process an input stream and take it's 
derivative. Computing the derivative numerically is sensitive to noise, so two 
low-pass filters are implemented to remove some of that noise

# Usage
As each new data point comes in, call derivative() on the data point and then
one of the low pass filters on the derivative. A publisher-subscriber model of
this could look like:

def update(val, timestep):
    return StreamMaths.lpf_smoothing(StreamMaths.derivative(val, timestep), 10)

Of the two LPFs, I think the smoothing one works best, but they're both subject
to tuning of the smoothing/length variable.

For processing bearing data, use the `derivative_bearing` function which handles
the wrap-arounds from pi to -pi that FastSLAM outputs.

Import the package into your python virtual environment as follows:
`pip install distfile.whl`
and then import into your python scrips with
`from MSPStreamMaths.StreamClass import StreamMathsClass`


## IMPORTANT NOTE
Use a different instanceof `streamClass()` for each variable you're tracking!
The classes keep internal memory of the past inputs so you don't have to worry
about passing data around, but it means trying to use multiple will make the
numbers collide.


# Building
Run `python setup.py bdist_wheel`, which will put the executable into dists/. You can then use that .whl file in a `pip install` statement as described in usage.
The most recent distribution is in dists/, but this isn't the best way to do this.

# Testing

## test_symbolic
Take the derivative of a symbolic expression (sepcified in `f(x)`) and compare its
numerical and symbolic derivates.

When you're trying to test things with the test_symbolic.py script, if you change
the START, END, or NUM, you might have to change the noise value as well.

## test_graph
Works with FastSLAM data and creates a graphical reporesentation of the data

If you run fastslam and use the test_graph.py test script, paste in the values of
dxdt,dydt,dthetadt,x,y,theta obtained to get a visualisation of the derivative and
original values, with LPF applied. You can get the necessary fastslam values with:
````
# at the start of the run
sm_x = StreamMathsClass(lpf_avg_length=16)
sm_y = StreamMathsClass(lpf_avg_length=16)
sm_T = StreamMathsClass(lpf_avg_length=16)

dxdt = []
dydt = []
dTdt = []
x_out = []
y_out = []
T_out = []

# in the update loop
global dxdt
global dydt
global dTdt
dxdt.append(sm_x.derivative(x_new, 0.1))
dydt.append(sm_y.derivative(y_new, 0.1))
dTdt.append(sm_T.derivative(theta_new, 0.1))
global x_out
global y_out
global z_out
x_out.append(x_new)
y_out.append(y_new)
T_out.append(theta_new)

# at the end
print('ddt={\'x\':', dxdt, ',\'y\':', dydt, ',\'theta\':', dTdt, '}')
print('fs2_out={\'x\':', x_out, ',\'y\':', y_out, ',\'theta\':', T_out, '}')
````
Paste the output of this into the `fs_data.txt` file in the tests directory.
