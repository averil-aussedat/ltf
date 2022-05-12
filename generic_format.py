##################################################################################
# format file 
# keep a generic version of this file for later use
#  
# Syntax : 
# columns = [
#     "column name 1", tablecolumn (n° in datafile, "format"),
#     "column name 2", [
#         "subcolumn name a" : tablecolumn (n° in datafile, "format"),
#         "subcolumn name b" : tablecolumn (n° in datafile, "format"),
#     ],
#     "column name 3", tablecolumn (n° in datafile, "format"),
#     ...
#     "column name n", [
#         "subcolumn name a" : tablecolumn (n° in datafile, "format"),
#         ...
#         "subcolumn name z" : tablecolumn (n° in datafile, "format"),
#     ],
# ]
#
# datarows : one of the following
# - ":", "a:", ":b", "a:b" : all / starting from a / skipping last b / starting from a and skipping last b
# - [a,b,...,o] : list of elements e, with e being
#       either a number n : pick the corresponding row
#       or a tuple (a,b)  : pick rows between a and b, both included (can be reversed, like (5,3), or equal, like (42,42))
# Remarks :
# - line numbering starts from 0.
# - the order in the table will follow the order in datarows.
# - '0:0' is the same as ':'.
#
#   The datafile may contain any number of rows, 
#   as soon as the columns appearing in [columns] exist and share the same data type
#   1 row = 1 set of different datas (meant to be added during an algo run)
#
#   Any code in this file will be executed once, on loading (building datarows for instance)
#
##################################################################################

# do not modify if you don't do it in the main script as well
def tablecolumn (datacol, format):
    """
    Inputs : 
        * datacol   : un entier dans 0, ..., infty, donne le numéro de la colonne de data.txt où sont rangés les données.
        * format    : chaîne de caractère type "%.3f". 
    """
    col = {"datacol" : datacol, "format" : format}
    return col

###################################
# Parameters
###################################

caption     = "hello world" # Optional (ignore the warning if commented)
label       = "fig:hw"      # Optional (ignore the warning if commented)

# columns = [
#     "$K_0$", tablecolumn (0, "%s"),
#     "$TT(s)$", tablecolumn (1, "%.3f"),
#     "error $\mathcal{L}_1$", [
#         "absolute", tablecolumn (2, "%.3e"),
#         "relative", tablecolumn (3, "%.3e"),
#     ],
#     "error $\mathcal{L}_2$", [
#         "absolute", tablecolumn (4, "%.3e"),
#         "relative", tablecolumn (5, "%.3e"),
#     ],
#     "error $\mathcal{L}_{\infty}$", [
#         "absolute", tablecolumn (6, "%.3e"),
#         "relative", tablecolumn (7, "%.3e"),
#     ], 
# ]

columns = [
    "this", tablecolumn(0,"%s"), 
    "is", [
        "a", tablecolumn(1,"%d"), 
        "recursive", [
            "example", tablecolumn(2,"%.2e"),
            "of", [
                "a", tablecolumn(5, "%s"),
                "table", tablecolumn(5, "%.4f"),
            ]
        ]
    ]
]

# datarows = "2:2" 
datarows = [0, 4, 2, (3,3)]
sep = "\t" # data file separator

##################################################################################
#                                                                            End #
##################################################################################