#!/bin/bash
source .env

Help()
{
	echo "Get input data from Advent of Code"
	echo "DO NOT RUN THIS ON LOOP; ONLY RUN ONCE"
	echo
	echo "Syntax: get_input_data y d [-h]"
	echo "Argumments:"
	echo "y    year"
	echo "d    day"
	echo
}

while getopts ":h" option; do
	case $option in 
		h) # display help
			Help
			exit;;
		/?) # Invalid option
			echo "Error: Invalid option"
			exit;;
	esac
done

mkdir -p $1/day$2/data

curl https://adventofcode.com/$1/day/$2/input --cookie "session=$SESSION" > $1/day$2/data/input.txt
