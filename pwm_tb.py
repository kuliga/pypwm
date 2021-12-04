from pwm import PwmControl
from myhdl import *
import random


@block
def PwmControl_tb():
    """ Test bench for the PwmControl block.
    Author: Jan Kuliga (4EiT)
    Date: 04.12.2021
    ###############
    There are two instances of this block. They share clk, rst_n and period signals.
    In order to check correctness of block's behavior, value of duty_cycle 
    parameter is changed over the time.
    """
    clk = Signal(bool(0))
    rst_n = ResetSignal(0, active=0, isasync=True)
    period = Signal(intbv(100))
    pwm0, pwm1 = Signal(0), Signal(0)
    fixed_duty_cycle, randomized_duty_cycle = Signal(
        intbv(20)), Signal(intbv(13))
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
            randomized_duty_cycle.next = random.randrange(period)
            yield delay(2 * 100)

    return clk_signal, drive_reset, randomize_duty_cycle, PwmControl_inst0, PwmControl_inst1
