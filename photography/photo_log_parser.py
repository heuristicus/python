#!/usr/bin/python

import sys
import re

def process_log(log_file):
    """Processes the log file received in the arguments.
    
    Arguments:
    - `log_file`: A photo accept log in a specific format.
    """
    f = open(log_file)
    s = f.read()
    time_period = re.findall('\[.*\]-\[.*\]', s)
    # Replace org mode date formats with something maybe more readable
    mod_period = []
    for period in time_period:
        # Chain replace, can't be bothered to call on multiple lines.
        rep = period.replace(']-[', ' to ').replace(']', '').replace('[','')
        mod_period.append(rep)
    image_total = re.findall('Camera image total: (.*)', s)
    accepted_images = re.findall('Images accepted: (.*)', s)
    do_calculations(mod_period, image_total, accepted_images)

def do_calculations(periods, image_totals, accepted_images):
    """Calculates some stuff by looking through the lists of data.
    
    Arguments:
    - `periods`: The time periods from the log
    - `image_totals`: The image totals on the camera each time period
    - `accepted_images`: The accepted images each time period
    """
    previous_total = 0.0
    previous_accepted = 0.0
    total_accept = 0.0
    for i in range(len(periods)):
        print periods[i]
        accepted = float(accepted_images[i])
        total = float(image_totals[i])
        photos_taken = float(total - previous_total)
        print 'Photos taken: %d'%(photos_taken)
        print 'Photos accepted: %d'%(accepted)
        accept_percent = (accepted/photos_taken)*100
        print 'Accept percentage: %f'%(accept_percent)
        previous_total = total
        previous_accepted = accepted
        total_accept += accept_percent
    print 'Average accept percentage: %f'%(total_accept/9)

    
def main():
    """
    """
    default_log_location = '/home/michal/Dropbox/logs/photo_accept_log.org'
    args = sys.argv[1:]
    if len(args) == 0:
        process_log(default_log_location)
    elif len(args) == 1:
        process_log(args[0])
    else:
        print 'Require just the photo accept log.'

if __name__ == '__main__':
    main()
