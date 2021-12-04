from pwm import PwmControl
from clk_driver import ClkDriver
from myhdl import *
import random
MAX_PWM_PERIOD = 2 ** 32 - 1


@block
def PwmControl_tb():
    clk = Signal(bool(0))
    rst_n = ResetSignal(0, active=0, isasync=True)
    pwm0, pwm1 = Signal(0), Signal(0)
    fixed_duty_cycle, randomized_duty_cycle = Signal(
        intbv(20)), Signal(intbv(13))
    period = Signal(intbv(100))
    PwmControl_inst0 = PwmControl(clk, rst_n, fixed_duty_cycle, period, pwm0)
    PwmControl_inst1 = PwmControl(
        clk, rst_n, randomized_duty_cycle, period, pwm1)

    @always(delay(int(10)))
    def clk_signal():
        clk.next = not clk

    @instance
    def drive_reset():
        rst_n.next = 0
        yield delay(10)
        rst_n.next = 1

    @instance
    def randomize_duty_cycle():
        yield delay(10)
        while True:
            randomized_duty_cycle.next = random.randrange(period / 2)
            yield delay(2 * 100)

    return clk_signal, drive_reset, randomize_duty_cycle, PwmControl_inst0, PwmControl_inst1
