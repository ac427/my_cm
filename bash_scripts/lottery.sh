#!/bin/bash -l 
#
expressions=(" 123 " " 124 " " 125 " " 126 " " 127 " " 128 " " 129 " " 130 " " 131 " " 132 " " 133 " " 134-1 " " 134-2 " " 134-3 " " 134-4 " " 134-5 " " 134-6 ")

# Seed random generator
RANDOM=$$$(date +%s)

    # Get random expression...
    selectedexpression=${expressions[$RANDOM % ${#expressions[@]} ]}

    # Write to Shell
    echo $selectedexpression

