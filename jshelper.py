#########################################################
'''
js-helper.py: Some functions for the website

Author: Danilo Lessa Bernardineli
'''
#########################################################

#################### Dependences #########################
import csv


def write_JSON_codes(codeFilename="cod_linhas.csv", filenameOutput="codes.json"):
    ''' Translates linecode csv file to JSON format
    Keyword arguments:
    codeFilename -- path to csv file
    filenameOutput -- path to output file
    '''

    i = 0
    line = ""
    line_ida = ""
    line_volta = ""
    output = "{\"linhas\":["
    with open(codeFilename, 'r') as csvfile:	
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csvreader:
            if(i == 2):
                i = 0
                output += "{\"linha\":\"%s\",\"codigoIda\":%s,\"codigoVolta\":%s}," % (line, line_ida, line_volta)
            else:
                i += 1
                line = row[0]
                if(row[2] == '1'):
                    line_ida = row[1]
                if(row[2] == '2'):
                    line_volta = row[1]
    output = output[:-1]
    output += "]}"
    with open(filenameOutput, 'w') as outputfile:
        outputfile.write(output)


