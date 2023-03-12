import os
import subprocess

for i in os.listdir("."):
    file_name = os.path.splitext(i)[0].split("_")
    
    if len(file_name) == 2:
        if file_name[1] == "crawler":
            print(i)
            subprocess.run("python {}".format(i), shell=True)