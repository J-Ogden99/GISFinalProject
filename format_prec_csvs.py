import io
import os
from glob import glob

root = r'C:\Users\polar\PycharmProjects\GISFinalProject'
files = glob(os.path.join(root, '*PREC.txt'))
print("Files to parse: ", files)

for file in files:
    with io.open(file, 'r') as f:
        with io.open(f"{file.split('.')[0]}.csv", 'w') as n:
            for line_num, line in enumerate(f):
                for el_num, el in enumerate(line.split()):
                    if line_num == 0:
                        if el_num < 2:
                            n.write(el + ',')
                        elif 14 < el_num and el_num < 18:
                            n.write(el + '_PREC,')
                    else:
                        if el_num < 2 or (14 < el_num < 18):
                            n.write(el + ',')
                n.write('\n')

        f.close()
        n.close()


