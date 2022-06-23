# MaxCutCodes
Some Python/Sage code for computing Max Cut problems.


A number of codes are given for computing Max Cut of some graphs.
One should first create the directory DATA_MaxCut.

SAGE
----

Sage has a command for computing the max cut. The data can be
computed with

```sh
$ sage TestCanonicalCut.sage
```


MaxSAT
------

The MaxCut can be computed via the Maximum satisfiability.
We use the EvalMaxSAT code (see https://github.com/FlorentAvellaneda/EvalMaxSAT)
which has to be compiled and available in the PATH.

The command is then:

```sh
$ python3 TestCanonicalCut_MaxSat.py
```

GUROBI
------

The gurobi solver is available in python via the package gurobipy.
The command is then:

```sh
$ python3 TestCanonicalCut_MaxSat.py
```

OR-TOOLS
-------

The OR-tools is available in python. The command is then:

```sh
$ python3 TestCanonicalCut_ortools.py
```

