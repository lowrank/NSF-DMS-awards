import os
from nsf_query import get_awards_csv
from datetime import datetime

default = 1976
current = datetime.now().year # grep all awards till current year

# Program list to be downloaded.
programs = {
    "Applied Mathematics" : default,
    "Computational Mathematics" : 1984,
    "Analysis" : 1991,
    "Probability" : default,
    "Statistics" : default,
    "Algebra and Number Theory" : default,
    "Topology" : default,
    "Mathematical Biology" : 2001,
    "Geometric Analysis" : default,
    "Combinatorics" : 2006,
    "Foundations" : default
}


for program, start_year in programs.items():
    for year in range(start_year, current + 1):
        print( "downloading " + program + " " + str(year) )

        cur_dir = os.path.dirname(__file__)
        prog_dir = program.replace(" ", "-")
        
        target_file = os.path.join(os.path.join(cur_dir, prog_dir), "Awards-" + program.replace(" ", "-") +"-" + str(year) + ".csv")

        if os.path.exists(target_file) and year < current:
            print( "file exists for " + program + " " + str(year) +"\n" )
        else:
            out = get_awards_csv(program, year)
            if out == 0:
                print( "update needed, the download is completed for " + program + " " + str(year) +"\n" )
            elif out == 1:
                print( "update is not needed, the download is completed for " + program + " " + str(year) +"\n")
            elif out == 2:
                print(" creating new file, the download is completed for " + program + " " + str(year) +"\n")
            else:
                print("downloading issue, awards not downloaded.")
