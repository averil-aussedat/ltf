#######################################################################################
# Latex table formatter
# Created by Averil Prost, may 2022
# 
# Input : 
#   - a format file (.py) containing objects (see generic_format.py)
#   - a data file (.txt or readable as)
# 
# The data file contains raw data from simulation
# The format file describes how the table must be constructed from the data
# 
# Output : latex, in form of a terminal output & a .txt file 
#
#######################################################################################

import numpy as np
import sys
import importlib

verbose = False

print("Welcome in latex table formatter.")
print("Call this script with the following arguments : format_file data_file <output_file>")
print("You may need to \\usepackage{multirow} if funny 2* appear in the head.")

####################################################################
# Récupération des infos du format file

args = sys.argv[1:]
if (len(args)<2):
    print("WARNING : Please provide a format_file and a data_file.")
    exit (1)
elif (len(args)==2):
    format_file_name = args[0].replace(".py","")
    data_file_name = args[1]
    output_file_name = "latex_table_output.txt"
    print("Output will be placed in %s" % (output_file_name))
else:
    format_file_name = args[0].replace(".py","")
    data_file_name = args[1]
    output_file_name = args[2]
    if ("." not in output_file_name):
        output_file_name += ".txt"

try:
    fmt = importlib.import_module(format_file_name)
except:
    print("WARNING : error opening format file '%s'. Abandon" % (format_file_name))
    exit (1)
####################################################################

####################################################################
# Vérification que le format file est bien conforme
try:
    fmt.columns
except:
    print("WARNING : 'columns' not found in format file. Abandon")
    exit (1)

# more format check
def recur_check (col, is_ok):
    if (np.mod(len(col),2) != 0):
        is_ok = False
        print("WARNING : uneven number of elements in a level of columns")
    else:
        for ic, c in enumerate(col[1::2]):
            if ((type(col[2*ic]) is not str) or (not ((type(c) is list) or (type(c) is dict)))):
                is_ok = False
                print("WARNING : bad type in columns. Use strings for name and dicts/lists of columns for datas")
            if (is_ok and (type(c) is list)):
                is_ok = recur_check (c, is_ok)
    return is_ok

is_ok = recur_check (fmt.columns, True)
if (not is_ok):
    print("WARNING : 'columns' is not well formatted. Abandon")
    exit (1)
if (len(fmt.columns)==0):
    print("WARNING : empty 'columns'.")

try:
    fmt.caption
except:
    print("WARNING : 'caption' not found in format file. Add 'caption = \"mycaption\"' to format file if you want one.")
    fmt.caption = ""

try:
    fmt.label
except:
    print("WARNING : 'label' not found in format file. Add 'label = \"mylabel\"' to format file if you want one.")
    fmt.label = ""

try:
    fmt.datarows
except:
    print("WARNING : 'datarows' not found in format file. Taking default datarows=\":\".")
    fmt.datarows = ":"

try:
    fmt.sep
except:
    print("WARNING : 'sep' not found in format file. Taking default sep=\":\". This may cause column discrimination error!")
    fmt.sep = "\t"
####################################################################

####################################################################
# Extraction des infos pratiques du format file
def recur_count (columns, ncols, nrows, current_row):
    for c in columns[1::2]:
        if type(c) is dict:
            ncols += 1
            nrows = np.max([nrows, current_row])              
        elif type(c) is list:
            [ncols, nrows, current_row] = recur_count (c, ncols, nrows, current_row+1)
        else: 
            print("WARNING : error in extracting infos from column. Please check format.")
    return [ncols, nrows, current_row-1]

[ncols, nrows, current_row] = recur_count (fmt.columns, 0, 1, 1)

lines_head = [[] for _ in range(nrows)]
lines_data = []

def recur_lines (columns, lines_head, lines_data, current_row, level_width, nrows):
    for ic, c in enumerate(columns[1::2]):
        if type(c) is dict:
            # remplissage jusqu'au plancher de l'en-tête
            lines_head[current_row].append([columns[2*ic], nrows-current_row, 1])
            for irow in range(nrows-current_row-1):
                lines_head[current_row+1+irow].append([]) # laisser du blanc
            lines_data.append (c)
            if (current_row > 0):
                level_width[-2] += 1 # ajouter la largeur de cette colonne à celle du dessus

        else: # si (comme ?) le boulot de vérification a bien été fait, type(c)=list ici
            [lines_head, lines_data, current_row, level_width] = recur_lines (c, lines_head, lines_data, current_row+1, level_width+[0], nrows)
            lines_head[current_row].append ([columns[2*ic], 1, level_width[-1]])
            if (current_row > 0):
                level_width[-2] += level_width[-1] # ajouter la largeur de cette colonne à celle du dessus
                level_width[-1] = 0 # passer à la colonne suivante
            else:
                level_width = [0] # passer à la colonne principale suivante : remise à 0
    return [lines_head, lines_data, current_row-1, level_width[:-1]]

[lines_head, lines_data, current_row, level_width] = recur_lines (fmt.columns, lines_head, lines_data, 0, [0], nrows)
####################################################################

####################################################################
# Récupération des données
try:
    datafile = open(data_file_name, "r")
except:
    print("WARNING : datafile %s not found. Abandon" % (data_file_name))
    exit (1)
datalines = datafile.readlines ()
datafile.close ()

datalines = [[numstr.replace("\n","") for numstr in line.split(fmt.sep)] for line in datalines]
datas = []
for rawline in datalines:
    line = []
    for f in rawline:
        try: # brutal, but very efficient
            line.append(float(f))
        except:
            line.append(f)
    datas.append(line)

# supprimer les éventuelles lignes vides
datas = [line for line in datas if ((len(line)>0) and (line!=[""]))]
lendatas = len(datas)

if verbose:
    print("datas : ", datas)
####################################################################

####################################################################
########## Coeur du script : construction de la table latex

output = "\\begin{table}\n"
output += "\t\\centering\n"
output += "\t\\begin{tabular}{|" + "c|"*ncols + "} \\hline\n"

########## placement de l'en-tête
for iline, line in enumerate(lines_head):
    output += "\t"
    # si pas la première ligne : remplissage des lignes brisées (\cline)

    if (iline > 0):
        coldep = 1
        cline_open = False
        for iele, ele in enumerate(line):
            if (len(ele)>0): # pas vide
                if (cline_open):
                    colarr += ele[2] # continuation d'une cline ouverte : somme des largeurs
                else:
                    cline_open = True # ouverture d'une cline
                    colarr = coldep + 1
            else: # ele vide
                if (cline_open):
                    cline_open = False # fermeture d'une cline
                    output += "\\cline{%d-%d} " % (coldep, colarr-1)
                    coldep = colarr+1
                else:
                    coldep += 1 # recherche d'une future cline
        # fermeture d'une éventuelle cline laissée ouverte
        if (cline_open):
            output += "\\cline{%d-%d} " % (coldep, colarr-1)

    # remplissage des noms
    for ic, c in enumerate(line): # soit [], donc remplissage, soit [nom, lignes, colonnes]
        if (len(c)>1): 
            if (c[2] > 1): # multicolonnes
                if (ic==0):
                    output += "\\multicolumn{%d}{|c|}{%s} " % (c[2], c[0])
                else:
                    output += "\\multicolumn{%d}{c|}{%s} " % (c[2], c[0])
            elif (c[1] > 1): # multilignes
                output += "\\multirow{%s}*{%s} " % (c[1], c[0])
            else: # single output
                output += c[0] + " "
        if (ic < len(line)-1):
            output += "& "
        else:
            output += "\\\\ \n"
output += "\t\\hline \\hline \n" 

########## placement des données
if (type(fmt.datarows) is str):
    try:
        rows_bounds = fmt.datarows.split(":")
        if (len(rows_bounds) != 2):
            print("WARNING : could not cast %s as valid datarows. Taking datarows=\":\" by default")
            list_of_rows = range(lendatas)
        else:
            for irb in [0,1]:
                if (rows_bounds[irb]==""):
                    rows_bounds[irb] = 0
                else:
                    try:
                        rows_bounds[irb] = int(rows_bounds[irb])
                    except:
                        print("WARNING : datarow[%d] = unknown thing %s. Taking 0 by default" % (irb, rows_bounds[irb]))
                        rows_bounds[irb] = 0
            list_of_rows = np.arange(rows_bounds[0], lendatas-rows_bounds[1], 1)
            if (len(list_of_rows)==0):
                print("WARNING : empty datarows.")
    except:
        print("WARNING : could not cast %s as valid datarows. Taking datarows=\":\" by default")
        list_of_rows = range(lendatas)

elif (type(fmt.datarows) is list):
    list_of_rows = []
    for i in fmt.datarows:
        if type(i) is tuple:
            if (np.min(i) < 0):
                print("WARNING : datarows ask for line %d. May the user start line numbering from 0, please ?" % np.min(i))
            elif (np.max(i) >= lendatas):
                print("WARNING : datarows ask for line %d. Line numbering starts from 0 : clipping at %d by default" % (np.max(i), lendatas-1))
            dalist = list(np.arange(np.max([0,np.min(i)]), np.min([np.max(i)+1, lendatas])))
            if (i[0] <= i[1]):
                list_of_rows += dalist
            else:
                list_of_rows += dalist[::-1]
                
        elif type(i) is int:
            if (i < 0):
                print("WARNING : datarows ask for line %d. May the user start line numbering from 0, please ?" % (i))
            elif (i >= lendatas):
                print("WARNING : datarows ask for line %d : clipping at %d by default (line numbering starts from 0)" % (i, lendatas-1))
            list_of_rows.append(np.max([0,np.min([lendatas-1, i])]))
        else:
            print("WARNING : Unknown element ", i, " in datarows, ignored")
else:
    print("WARNING : unknown datarows type : ", type(fmt.datarows), "Please use list or 'a:b' string.")
    list_of_rows = []

for row in list_of_rows:
    output += "\t"
    for ic, c in enumerate (lines_data):
        if (c["datacol"] >= len(datas[row])):
            print("WARNING : format ask for column %d but datafile only have %d columns. Ignored" % (c["datacol"], len(datas[row])))
        else:
            try:
                output += c["format"] % (datas[row][c["datacol"]])
            except:
                print("WARNING : format error. Expected was %s, received data " % (c["format"]), datas[row][c["datacol"]], " of type", type(datas[row][c["datacol"]]))
        if (ic < ncols-1):
            output += " & "
        else:
            output += " \\\\ \\hline \n"

########## end of table
output += "\t\\end{tabular}\n"
if (len(fmt.caption)>0):
    output += "\t\\caption{" + fmt.caption + "}\n"
if (len(fmt.label)>0):
    output += "\t\\label{" + fmt.label + "}\n"
output += "\\end{table}"
####################################################################

print("\n")
print(output)
print("\n")

output_file = open (output_file_name, "w")
output_file.write (output)
output_file.close ()

print("Bye")
#######################################################################################
#                                                                                 Fin #
#######################################################################################
