Website Cloud Provider Lookup

This script reads a list of website names from an input Excel file, and writes the following information to an output Excel file:

    Website name
    IP address of the website
    Organization that owns the IP address
    Whether the website is using a cloud provider

The script also creates a separate Excel file with a list of websites that were not found in the output file.
Prerequisites

    Python 3
    Shodan API key - obtain one at https://www.shodan.io/
    Required Python libraries: configparser, pandas, openpyxl, socket, shodan

Setup

    Place the input Excel file in the same directory as the script.
    Rename the input file to input.xlsx.
    Create a file called config.ini in the same directory as the script.
    In config.ini, add a section called SHODAN and a key called api_key, and set its value to your Shodan API key.

    [SHODAN]
    api_key = YOUR_SHODAN_API_KEY

Running the script

    Run the script using the command python script.py.
    When prompted, enter the names of the input and output Excel files, and the name of the column in the input file that contains the website names.
    The output Excel files will be created in the same directory as the script.

Example

Input file (input.xlsx):
Website
google.com
example.com
notawebsite

Output file (output.xlsx):
Website    	IP Address	    Organization	    Using Cloud Provider
google.com	172.217.16.110	Google LLC	      Yes
example.com	93.184.216.34	  Cloudflare, Inc.	No

Output file with websites not found in the first output file (not_found.xlsx):
Website
notawebsite
