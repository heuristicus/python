#!/usr/bin/python
import sys
import math

global light_speed

def time_taken(metres):
    """
    """
    time_strings = ['seconds','minutes','hours','days','years']
    time = float(metres)/light_speed
    desc_string = ''
    if time > 31556926:
        years = float(time)/31556926
        print 'years %d'%(years)
        print 'time left: %f'%(time-(years*31556926))
    if time < 1:
        desc_string += time + time_strings[0]
    print 'Time to travel %d metres is %s'%(float(metres), desc_string)


if __name__ == '__main__':
    global light_speed
    light_speed = 299792458
    time_taken(sys.argv[1])
