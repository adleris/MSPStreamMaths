import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
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
