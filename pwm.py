from myhdl import *

MAX_PWM_PERIOD = 2 ** 32 - 1


@block
def PwmControl(clk, rst_n, duty_cycle, period, pwm):
    """ PWM module
    clk - clock input
    rst - reset input
    duty_cycle - input, requested duty cycle (in number of clock cycles)
    period - period of a time between continuous pwm cycles (in number of clock cycles)
    pwm - output
    """
    cnt = Signal(intbv(1, 0, MAX_PWM_PERIOD))

    @always_seq(clk.posedge, reset=rst_n)
    def set_pwm():
        if rst_n == 0:
            pwm.next = 0
            cnt.next = 0
        else:
            if cnt < period:
                cnt.next = cnt + 1
                if cnt < duty_cycle:
                    pwm.next = 1
                else:
                    pwm.next = 0
            else:
                cnt.next = 0
                pwm.next = 1

    return set_pwm
