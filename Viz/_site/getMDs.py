import os
from tqdm import tqdm
import numpy as np
from wasabi import msg

#-----------------------------------------------

files = []

for r, _, f in os.walk("assets/images/fulls/"):
    for file in f:
        if '.jpg' in file:
            files.append([os.path.join(r, file),file.replace(".jpg","")])
print("")
files.sort()

#-----------------------------------------------

for file in tqdm(range(len(files))):

    name,description = files[file][1].split("-")

    string = "---"+"\n"+"title: "+name+"\n"+"caption: "+description+"\n"+"---"

    print(string)

    with open("_images/"+name+"-"+description+".md", 'w') as f:
        f.write(string)
    f.close()