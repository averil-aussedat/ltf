# Latex table formatter

Small script to convert data files into vertical latex tables. 
Needed : python3, package multirow in latex.

### Use
Python command line script :
```
python3 latex_table_formatter.py format_file data_file output_file
```

Arguments are
  - __format file__ : modification of generic_format, gives the structure of the table (heading, columns, format of columns, selected lines), name, label.
  - __data file__ : probably output of some algorithm. Anything that can be open with python3 'open' and read with 'readlines'. Each line is a collection of different datas (for instance, L1 error in column 0, L2 in column 3).
  - __output file__ : optional, name of the output file where the table will be placed. Default 'latex_table_output.txt'.

Latex code is printed in terminal and stored in output file.

### Format file structure

Variables ``caption``, ``label`` and ``sep`` (column separator in datafile) are strings. 
``datarows`` indicates which rows of datafile appear in the table. Can be
  - ":", "a:", ":b", "a:b" : all / starting from a / skipping last b / starting from a and skipping last b lines. Here a and b are integers, with "0:0" equivalent to ":".
  - [a,b,...,o] : list of elements e, with e being either an integer, or a tuple (a,b). Picks rows between a and b, both included. Can be equal or reversed.
The order in the table is the order in datarows.

``columns`` is a list of elements going two-by-two, namely [name1, data1, ..., nameN, dataN], with name a string (name of the column) and data being 
  - the output of ``tablecolumn(n,fmt)`` : n is the number of the corresponding column in datafile (starts from 0), and fmt a string format (ex. "%.3f").
  - a list of [subname1, subdata1, ..., subnameM, subdataM], splitting the column in subcolumns. 

### Example 

In format file called ``fmt.py`` : 
```
caption = "hello world"
label = "tab:hw"
datarows = [1,(5,2)]
sep = "\t"
columns = columns = [
    "this", tablecolumn(0,"%s"), 
    "is", [
        "a", tablecolumn(1,"%d"), 
        "recursive", [
            "example", tablecolumn(4,"%.2e"),
            "of", [
                "a", tablecolumn(2, "%s"),
                "table", tablecolumn(1, "%.4f"),
            ]
        ]
    ]
]
```

In datafile called ``data.txt`` :
```
10puissance2	0.0	1.0	2.0	3.0	4.0	5.0	6.0	7.0	8.0	9.0	aaaa
ceciestunestring	0.0	1.0	2.0	3.0	4.0	5.0	6.0	7.0	8.0	9.0	aaaa
ceci aussi	0.0	1.0	2.0	3.0	4.0	5.0	6.0	7.0	8.0	9.0	aaaa
ceci a	0.0	1.0	2.0	3.0	4.0	5.0	6.0	7.0	8.0	9.0	aaaa
ceci ab	0.0	1.0	2.0	3.0	4.0	5.0	6.0	7.0	8.0	9.0	aaaa
ceci abc	0.0	1.0	2.0	3.0	4.0	5.0	6.0	7.0	8.0	9.0	aaaa
et encore ceci	0.0	1.0	2.0	3.0	4.0	5.0	6.0	7.0	8.0	9.0	aaaa
```

Output of ``python3 latex_table_formatter.py fmt data out.txt`` :
```
\begin{table}
	\centering
	\begin{tabular}{|c|c|c|c|c|} \hline
	\multirow{4}*{this} & \multicolumn{4}{c|}{is} \\ 
	\cline{2-5} & \multirow{3}*{a} & \multicolumn{3}{c|}{recursive} \\ 
	\cline{3-5} & & \multirow{2}*{example} & \multicolumn{2}{c|}{of} \\ 
	\cline{4-5} & & & a & table \\ 
	\hline \hline 
	10puissance2 & 0 & 1.00e+00 & 4.0 & 4.0000 \\ \hline 
	ceci ab & 0 & 1.00e+00 & 4.0 & 4.0000 \\ \hline 
	ceci aussi & 0 & 1.00e+00 & 4.0 & 4.0000 \\ \hline 
	ceci a & 0 & 1.00e+00 & 4.0 & 4.0000 \\ \hline 
	\end{tabular}
	\caption{hello world}
	\label{fig:hw}
\end{table}
```
