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
    cnt = Signal(intbv(0, 0, MAX_PWM_PERIOD))
    duty_cycle_reg = Signal(intbv(0))
    cycle_completed = Signal(bool(0))

    @always_seq(clk.posedge, reset=rst_n)
    def set_pwm():
        if rst_n == 0:
            pwm.next = 0
            cnt.next = 0
            cycle_completed.next = 1
        else:
            if cnt < period:
                cnt.next = cnt + 1
                cycle_completed.next = 0
                if cnt < duty_cycle_reg:
                    pwm.next = 1
                else:
                    pwm.next = 0
            else:
                cnt.next = 0
                pwm.next = 0
                cycle_completed.next = 1

    @always_seq(clk.posedge, reset=rst_n)
    def set_duty_cycle():
        if rst_n == 0:
            duty_cycle_reg.next = 0
        else:
            if cycle_completed == 1:
                duty_cycle_reg.next = duty_cycle
            else:
                duty_cycle_reg.next = duty_cycle_reg

    return set_pwm, set_duty_cycle
