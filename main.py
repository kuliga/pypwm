from pwm_tb import PwmControl_tb
from pwm import PwmControl
from myhdl import *
MAX_PWM_PERIOD = 2 ** 32 - 1


def main():
    clk = Signal(bool(0))
    rst_n = ResetSignal(0, active=0, isasync=True)
    period = Signal(intbv(100, 0, MAX_PWM_PERIOD, 32))
    pwm = Signal(bool(0))
    duty_cycle = Signal(intbv(20, 0, MAX_PWM_PERIOD, 32))

    PwmControl_inst = PwmControl(clk, rst_n, duty_cycle, period, pwm)
    PwmControl_inst.convert(hdl='VHDL', initial_values=True)

    tb = PwmControl_tb()
    tb.config_sim(trace=True)
    tb.run_sim(40000 * 10)


if __name__ == '__main__':
    main()
