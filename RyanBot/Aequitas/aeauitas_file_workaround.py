import os


for files in os.listdir('C:\\users\\ryanm\\desktop\\Temp AT Alt\\'):
    test = int(files.replace('.xml', '')) + 119
    final_name = str(test) + '.xml'
    print final_name
    os.rename('C:\\users\\ryanm\\desktop\\Temp AT Alt\\' + files,  final_name)


