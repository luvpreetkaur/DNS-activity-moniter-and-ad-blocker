First extract doamin and time from the dns log file (regex expressions are used to do so) and added to a dictionary
Then checking within a time frame of 60-90 seconds printing the main domain name and sub domain names in the report file
Lastly deleted the keys and values after writing in the report to avoid reiteration 