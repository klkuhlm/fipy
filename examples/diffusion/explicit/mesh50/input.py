#!/usr/bin/env python

## 
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "input.py"
 #                                    created: 12/29/03 {3:23:47 PM}
 #                                last update: 10/6/04 {12:53:44 PM} 
 #  Author: Jonathan Guyer
 #  E-mail: guyer@nist.gov
 #  Author: Daniel Wheeler
 #  E-mail: daniel.wheeler@nist.gov
 #    mail: NIST
 #     www: http://ctcms.nist.gov
 #  
 # ========================================================================
 # This software was developed at the National Institute of Standards
 # and Technology by employees of the Federal Government in the course
 # of their official duties.  Pursuant to title 17 Section 105 of the
 # United States Code this software is not subject to copyright
 # protection and is in the public domain.  FiPy is an experimental
 # system.  NIST assumes no responsibility whatsoever for its use by
 # other parties, and makes no guarantees, expressed or implied, about
 # its quality, reliability, or any other characteristic.  We would
 # appreciate acknowledgement if the software is used.
 # 
 # This software can be redistributed and/or modified freely
 # provided that any derivative works bear some notice that they are
 # derived from it, and any modified versions bear some notice that
 # they have been modified.
 # ========================================================================
 #  
 #  Description: 
 # 
 #  History
 # 
 #  modified   by  rev reason
 #  ---------- --- --- -----------
 #  2003-11-10 JEG 1.0 original
 # ###################################################################
 ##

"""

This input file again solves a 1D diffusion problem as in::
    
    $ examples/diffusion/steadyState/mesh1D/input.py
    
The difference in this example is that the solution method is explicit.
The equation used is the `ExplicitDiffusionEquation`.  In this case many
steps have to be taken to reach equilibrium.  The `timeStepDuration`
parameter specifies the size of each time step and `steps` is the number of
time steps.

    >>> dx = 1.
    >>> dy = 1.
    >>> nx = 50
    >>> ny = 1
    >>> valueLeft = 0.
    >>> valueRight = 1.
    >>> timeStepDuration = 0.2
    >>> steps = 10

A loop is required to execute the necessary time steps:

    >>> for step in range(steps):
    ...     it.timestep()

The result is again tested in the same way:

    >>> Lx = nx * dx
    >>> x = mesh.getCellCenters()[:,0]
    >>> analyticalArray = valueLeft + (valueRight - valueLeft) * x / Lx
    >>> import Numeric
    >>> Numeric.allclose(var, answer, rtol = 1e-3, atol = 1e-3)
    1

"""

__docformat__ = 'restructuredtext'

import Numeric

from fipy.meshes.grid2D import Grid2D
from fipy.equations.explicitDiffusionEquation import ExplicitDiffusionEquation
from fipy.solvers.linearPCGSolver import LinearPCGSolver
from fipy.boundaryConditions.fixedValue import FixedValue
from fipy.boundaryConditions.fixedFlux import FixedFlux
from fipy.iterators.iterator import Iterator
from fipy.variables.cellVariable import CellVariable
from fipy.viewers.grid2DGistViewer import Grid2DGistViewer

dx = 1.
dy = 1.
nx = 50
ny = 1
valueLeft = 0.
valueRight = 1.
timeStepDuration = 0.2
steps = 10

mesh = Grid2D(dx, dy, nx, ny)

var = CellVariable(
    name = "concentration",
    mesh = mesh,
    value = valueLeft)

eq = ExplicitDiffusionEquation(
    var,
    transientCoeff = 1. / timeStepDuration, 
    diffusionCoeff = 1.,
    solver = LinearPCGSolver(
    tolerance = 1.e-15, 
    steps = 1000
    ),
    boundaryConditions=(
    FixedValue(mesh.getFacesLeft(),valueLeft),
    FixedValue(mesh.getFacesRight(),valueRight),
    FixedFlux(mesh.getFacesTop(),0.),
    FixedFlux(mesh.getFacesBottom(),0.)
    )
    )

it = Iterator((eq,))

answer = Numeric.array([  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
        2.04800000e-07,  6.34880000e-06,  9.13408000e-05,  8.10188800e-04,
        4.96660480e-03,  2.23737856e-02,  7.69755136e-02,  2.07879578e-01,
        4.50699674e-01,  8.01663386e-01])

if __name__ == '__main__':
    for step in range(steps):
        it.timestep()
##     print var
    viewer = Grid2DGistViewer(var)
    viewer.plot()
    raw_input('finished')

