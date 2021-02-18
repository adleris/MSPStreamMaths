"""
functions to process an input stream and take it's derivative.
computing the derivative over 2 numerically is sensitive to noise, so two 
low-pass filters are implemented to remove some of that noise

usage:
As each new data point comes in, call derivative() on the data point and then
one of the low pass filters on the derivative. A publisher-subscriber model of
this could look like:

def update(val, timestep):
    return lpf_smoothing(derivative(val, timestep), 10)
    
Of the two LPFs, I think the smoothing one works best, but they're both subject
to tuning of the smoothing/length variable.

As a sidenote, I wrote the functions with a publisher-subscriber model in mind
so I wrote them as static functions, which means you can't have multiple in
parallel, but you also don't need to retain any past data when using them. 
Refactoring them into classes might be better if you want to run comparisons, 
as trying to run them in parallel means they're all modifying the same data!

Also, when you're trying to test things, if you change the START, END, or NUM, 
you might have to change the noise value as well.
"""

import numpy as np

def derivative(next_in, timestep):
    """
    take the derivative of an input stream of numbers
    the first number in the stream does not have a derivative returned and will
    always return 0.0. This is because the derivative requires 2 inputs for the
    calculation to occur.
    @param next_in next number of the input stream
    @param timestep time since last input. timestep will likely be a constant.
    """
    
    if not hasattr(derivative, "prev_in"):
        derivative.prev_in = next_in
        return 0.0
    dydt = (next_in - derivative.prev_in) / timestep
    derivative.prev_in = next_in
    return dydt
    

# LOW PASS FILTERS

def lpf_smoothing(next_in, smoothing):
    """
    http://phrogz.net/js/framerate-independent-low-pass-filter.html
    smoothing of 1 makes no change to incoming data. increased smoothing value
    has a greater effect on the data.
    This can be modified to include varying timesteps, but it didn't work when 
    I tried it. The fomrula would change to: 
    
    lpf_smoothing.prev += timestep * (next_in - lpf_smoothing.prev) / smoothing
    """
    if not hasattr(lpf_smoothing, "prev"):
        lpf_smoothing.prev = next_in
        return 0.0

    lpf_smoothing.prev += (next_in - lpf_smoothing.prev) / smoothing
    
    return lpf_smoothing.prev
    

def lpf_moving_avg(next_in, length):
    """
    LPF that takes a moving average of the data stream
    """
    from collections import deque
    
    if not hasattr(lpf_moving_avg, "prev"):    # first piece of data, initialise prev 
        lpf_moving_avg.prev = deque([next_in], length)
        return 0.0
    
    lpf_moving_avg.prev.append(next_in)
    if len(lpf_moving_avg.prev) < length:      # not enough data yet for moving average
        return 0.0
    
    return sum(lpf_moving_avg.prev)/length
    
    
# functions for testing
    
def f(x):
    """
    symbolic function under examination
    """
    return x*np.sin(x)
    
def dfdx(x):
    """
    symbolic derivative of function under examination, to also be computed numerically
    """
    return x*np.cos(x) + np.sin(x)

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    
    START=0
    END  =10
    NUM  =100

    t = [ t for t in np.linspace(START,END,NUM)]
    numerical = []
    lpf_smooth_list = []
    lpf_moving_avg_list = []
    
    
    ts = t[1] - t[0]
    for t_i in t:
        # numerically compute the derivative of the function + noise
        noise = (np.random.rand() - 0.5)/10
        #noise = 0
        numerical.append(derivative(f(t_i) + noise, ts))
        
        # LPF the numerical derivative
        lpf_smooth_list.append(lpf_smoothing(numerical[-1], 10))
        lpf_moving_avg_list.append(lpf_moving_avg(numerical[-1], 3))


    # visualise some plots
    
     # symbolic derivative in high resolution
    plt.plot(np.linspace(START,END,200), 
             [dfdx(t) for t in np.linspace(START,END,200)], 
             'k', label="actual")
    
    # numerical derivative
    plt.plot(t, numerical, 'c', label="numerical diff")
    
    # low pass filtering of numerical derivative
    plt.plot(t, lpf_smooth_list, label="LPF (smoothing)")
    plt.plot(t, lpf_moving_avg_list, label="LPF (moving avg)")
   
    plt.legend(loc="lower left")
    plt.show()


    #x,y,z
    #v = derivative((x**2+y**2+z**2)**(1/3), ts)
    #w = derivative(theta, ts)
