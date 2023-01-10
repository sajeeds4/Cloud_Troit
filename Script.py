'''
coding: utf-8
By Gulam Mohammed Sajeed
Twitter : @0101011011010O
Github  : https://github.com/sajeeds4
'''


import configparser
import pandas as pd
import openpyxl
import socket
import shodan

# Read the configuration file
print("Reading configuration file and getting API key...")
config = configparser.ConfigParser()
config.read('config.ini')

api_key = config.get('SHODAN', 'api_key', fallback=None)  #1

if api_key is None:
    api_key = str(input("Enter Shodan API here : "))
    config['SHODAN'] = {}
    config['SHODAN']['api_key'] = api_key

# Save the configuration file if the API key was not present in it originally
if api_key is None:
    with open('config.ini', 'w') as configfile:
        config.write(configfile)




def banner():
    print("""%s
    
 ____    _       _ _____ _____ ____  
/ ___|  / \     | | ____| ____|  _ \ 
\___ \ / _ \ _  | |  _| |  _| | | | |
 ___) / ___ \ |_| | |___| |___| |_| |
|____/_/   \_\___/|_____|_____|____/ 

        
%s%s
       # By Gulam Mohammed Sajeed
       # Twitter : S A ج D (@0101011011010O)
       
    """ % (R, W, Y))

print("Please enter the names of the input and output files.")
File_name = str(input("Enter the file name here with extension : "))
Row_name = str(input("Enter the row name here : "))
outs = str(input("Enter the desired output file name with extension : "))
bouts = str(input("Enter the desired output file name for not found websites with extension :"))


def website_to_ip(website):
  try:
    ip_address = socket.gethostbyname(website)
    return ip_address
  except socket.gaierror:
    return 'n/a'

def check_cloud_provider(ip_address):
  api = shodan.Shodan(api_key)

  try:
      host = api.host(ip_address)
  except shodan.exception.APIError:
      return None

  # Extract relevant information from the host
  ip = host["ip_str"]
  org = host.get("org", "n/a")
  cloud_providers = []
  for item in host['data']:
      product = item.get('product', '').lower()
      if 'amazon' in product:
          cloud_providers.append('Amazon Web Services')
      elif 'google' in product:
          cloud_providers.append('Google Cloud Platform')
      elif 'azure' in product:
          cloud_providers.append('Microsoft Azure')

  return ip, org, cloud_providers

# Read the input Excel file
df = pd.read_excel(File_name)

# Create a new Excel file for the output
wb = openpyxl.Workbook()
ws = wb.active
ws.title = 'Sheet1'

# Add a header row to the output sheet
ws.append(['Website', 'IP Address', 'Organization', 'Logic Error'])

# Iterate through each row in the input sheet
for index, row in df.iterrows():
  website = row[Row_name]
  ip_address = website_to_ip(website)
  print("Looking up IP address for website:", website)

  info = check_cloud_provider(ip_address)

  if info is not None:
      ip, org, cloud_providers = info
      # Determine if the website is using a cloud provider
      if len(cloud_providers) > 0:
          using_cloud = 'Yes'
      else:
          using_cloud = 'No'
      ws.append([website, ip, org, using_cloud])

# Save the output Excel file
wb.save(outs)

# Read the input and output Excel files
df_input = pd.read_excel(File_name)
df_output = pd.read_excel(outs)

websites_input = df_input[Row_name]
websites_output = df_output['Website']

# Find the unique websites in the input file
unique_websites = websites_input[~websites_input.isin(websites_output)]

# Create a new Excel file for the unique websites
wb_unique = openpyxl.Workbook()
ws_unique = wb_unique.active
ws_unique.title = 'Sheet1'

# Add a header row to the unique websites sheet
ws_unique.append(['Unique Websites'])

# Add the unique websites to the sheet
for website in unique_websites:
    ws_unique.append([website])

# Save the unique websites Excel file
wb_unique.save(bouts)

