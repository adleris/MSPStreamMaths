import matplotlib.pyplot as plt
import numpy as np

# I have no idea why this import doesnt't work but figure this out and the script will work
from MSPStreamMaths.StreamMaths import StreamMaths

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


def test_symbolic():
    sm = StreamMaths(lpf_smoothing=10, lpf_avg_length=3)
    
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
        numerical.append(sm.derivative(f(t_i) + noise, ts))
        
        # LPF the numerical derivative
        lpf_smooth_list.append(sm.lpf_smooth(numerical[-1]))
        lpf_moving_avg_list.append(sm.lpf_moving_avg(numerical[-1]))


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


if __name__ == "__main__":
    test_symbolic()