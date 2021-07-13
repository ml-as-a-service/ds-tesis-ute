import os
import shutil
import glob 

dir = os.path.dirname(os.path.realpath(__file__))

outfilename = dir+'/dist/extract_hierarchical_structure.js'

# ------------------------------------------------------------
with open(outfilename, 'wb') as outfile:
    with open(dir+'/config.js', 'rb') as readfile:
        shutil.copyfileobj(readfile, outfile)

    for filename in sorted(glob.glob(dir+'/classes/*.class.js')):
        print(filename)
        if filename == outfilename:
            # don't want to copy the output into the output
            continue
        with open(filename, 'rb') as readfile:
            shutil.copyfileobj(readfile, outfile)

    with open(dir+'/init.js', 'rb') as readfile:
        shutil.copyfileobj(readfile, outfile)




