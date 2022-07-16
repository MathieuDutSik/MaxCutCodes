# MaxCutCodes
Some Python/Sage code for computing Max Cut problems.

A number of codes are given for computing Max Cut of some graphs.
One should first create the directory DATA_MaxCut.

Then by running the following scripts we can create files in the
directory DATA_MaxCut that will contain the result.

SAGE
----

Sage (available via https://www.sagemath.org/) has a command for
computing the max cut.
The data can be computed with the following command:

```sh
$ sage TestCanonicalCut.sage
```


MaxSAT
------

The MaxCut can be computed via the Maximum satisfiability.
We use the EvalMaxSAT code (see https://github.com/FlorentAvellaneda/EvalMaxSAT)
which has to be compiled and available in the PATH.
The data can be computed with the following command:

```sh
$ python3 TestCanonicalCut_MaxSat.py
```


GUROBI
------

The gurobi solver (available via https://www.gurobi.com/) is available in python
via the package gurobipy.
The data can be computed with the following command:

```sh
$ python3 TestCanonicalCut_gurobi.py
```


OR-TOOLS
-------

The OR-tools is available in python. This code has not been tested for
correctness due to the difficulty of installing OR-tools solver. The
command is then:

```sh
$ python3 TestCanonicalCut_ortools.py
```


CHECKING CORRECTNESS:
---------------------

```sh
$ gap.sh CheckCoherency.g
```

It checks if the obtained results by different methods are coherent.

