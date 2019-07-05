import os

print ""
print " Pytube Downloader "
ans=True
while ans:
    print("""
    1. Download Youtube URL and convert to MP3
    2. Download Youtube URL to MP4
    3. Exit/Quit
    """)
    ans=raw_input("What would you like to do? ")
    if ans=="1":

      print("\n Option 1 choosed...")
      str1=raw_input("type the Youtube video url and type enter: ")
      
      if str1 != "":
	os.system('youtube-dl --restrict-filenames --ignore-errors -x --audio-format mp3  "'+ str1 +'" ');
	os.system('tput clear')
	print ""
	print("\033[1;32;40m        -----:: Download done! ::------  \n")
	print "" 
	print("\033[0;37;40m ;-) t\n")

    elif ans=="2":
   
      print("\n Option 2 choosed...")

    elif ans=="3":
      print("\n Exit choosed... Goodbye") 
      ans = None
    else:
       print("\n Not Valid Choice Try again")
