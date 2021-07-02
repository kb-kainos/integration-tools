# Author: Kane Bash
# Version: 0.1
# Place in directory with CSV files to generate fileDefs text files. Format matches fileDefs-FILE_NAME

import pandas as pd
from dateutil.parser import parse
import os
import glob

os.chdir('./')
csvlist = glob.glob('*.{}'.format('csv'))

for file in csvlist:
    filename = os.path.splitext(file)[0]
    text = '/***************************\n' \
           '*\n * File Definitions\n*\n ***************************/\n\n' \
           '/*******************************************************************************\n* adaptive staging table model/structure\n' \
           '*******************************************************************************/\nExternalSystem = {\n    ' \
           'Tables: [\n        {\n' \
           '            name: "' + filename + '",\n            displayName: "' + filename + '",\n            columns: [\n'

    df = pd.read_csv(filename + '.csv')

# Add more types.
    def parsetype(dtype, col):
        if dtype == 'int64':
            return 'int" }'
        if dtype == 'float64':
            return 'float" }'
        if dtype == 'object':
            return parsedates(col)

# Update to check more rows?
    def parsedates(cols):
        try:
            parse(cols[1])
            return 'datetime" }'
        except:
            return 'text", length: 200 }'


    for items in df:
        datatype = str(df[items].dtype)
        text += '                { name: "' + items + '", displayName: "' + items + '", type: "' + parsetype(
            datatype, df[items]) + '\n'

    text += "\n            ]\n        }\n    ]\n};"

    defsfile = open('fileDefs-' + filename + '.txt', 'x')
    defsfile.write(text)
