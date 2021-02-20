from collections import deque

class StreamMaths():
    def __init__(self, lpf_smoothing=None, lpf_avg_length=None):
        """
        # Moving Average
        Take the moving average over the data stream. A greater length has a
        greater impact on noise reduction, but increases lag. A moving average
        of 1 has no affect on the data.

        # Smoothing
        Smooth the incoming data stream. Smoothing of 1 makes no change to
        incoming data. increased smoothing value has a greater effect on the
        data, but also increases lag.
        """
        self.ddx_prev_in = 0
        self.ddx_prev_result = 0

        # smoothing
        self.lpf_smoothing_prev = None              # previous data
        self.lpf_smoothing_value = lpf_smoothing    # configuration

        # moving avg
        self.lpf_moving_avg_length = lpf_avg_length                    # configuration
        if self.lpf_moving_avg_length is not None:
            self.lpf_moving_avg_prev = deque(maxlen=self.lpf_moving_avg_length)    # previous data
    
    def derivative(self, next_in, timestep):
        """
        take the derivative of an input stream of numbers
        @param next_in next number of the input stream
        @param timestep time since last input.
        """
        dydt = (next_in - self.ddx_prev_in) / timestep
        self.ddx_prev_in = next_in
        return dydt

    def derivative_bearing(self, next_in, timestep):
        """
        take the derivative of a bearing input stream of numbers.
        Takes into account the loop around from pi to -pi.
        @param next_in next number of the input stream
        @param timestep time since last input.
        """
        MAX_TURN = 2 # radians: The maximum turn we're assuming can happen per timestep
        PI = 3.1415926535
        dydt = (next_in - self.ddx_prev_in) / timestep
        if abs(abs(dydt) - abs(self.ddx_prev_result)) > MAX_TURN:                 # we've had a jump in the derivative

            # recompute derivative but subtract 2pi: clockwise motion and crossed the x-axis
            dydt = (next_in - self.ddx_prev_in - 2*PI) / timestep
            if abs(abs(dydt) - abs(self.ddx_prev_result)) > MAX_TURN:
            
                # recompute derivative but add 2pi: anticlockwise motion and crossed the x-axis
                dydt = (next_in - self.ddx_prev_in + 2*PI) / timestep
                # if abs(abs(dydt) - abs(self.ddx_prev_result)) > MAX_TURN:
                    # at this point we haven't found anything, I don't think we should reach this point?

        # whatever value we had for dydt here, it should work!

        self.ddx_prev_in = next_in
        self.ddx_prev_result = dydt
        return dydt

    def lpf_smooth(self, next_in):
        """
        source: http://phrogz.net/js/framerate-independent-low-pass-filter.html
        If an lpf_smoothing value was not given on initialisation, raises a
        UserWarning

        This can be modified to include varying timesteps, but it didn't work when 
        I tried it. The formula would change to: 
        
        lpf_smoothing.prev += timestep * (next_in - lpf_smoothing.prev) / smoothing
        """
        if self.lpf_smoothing_prev is not None:
            # normal operation
            self.lpf_smoothing_prev += (next_in - self.lpf_smoothing_prev) / self.lpf_smoothing_value
            return self.lpf_smoothing_prev
        else:
            # smoothing not initialised, abort
            if self.lpf_smoothing_value is None:
                raise UserWarning("lpf_smoothing not initialised")
                return 0.0

            # initialise with first input
            self.lpf_smoothing_prev = next_in
            return 0.0
    
    def lpf_moving_avg(self, next_in):
        """
        Take the moving average of the data stream
        """
        if self.lpf_moving_avg_length is not None:
            # normal operation
            self.lpf_moving_avg_prev.append(next_in)
            return sum(self.lpf_moving_avg_prev)/len(self.lpf_moving_avg_prev)
        else:
            raise UserWarning("lpf_moving_avg not initialised")
            return 0.0
