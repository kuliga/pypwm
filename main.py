from pwm_tb import PwmControl_tb
from myhdl import *


def main():
    tb = PwmControl_tb()
    tb.config_sim(trace=True)
    tb.run_sim(40000 * 10)


if __name__ == '__main__':
    main()
