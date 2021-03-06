r"""
Object model for storing geometrical information of the network
===============================================================

The ``geometry`` module contains the ``GenericGeometry`` class, and an
assortment of subclasses that implement specific pore-scale geometrical models.

The GenericGeometry Class
-------------------------

Geometry objects (as well as Physics objects) are ``Subdomain`` subclasses,
which allow them to be assigned to subset of the full domain (although this is
not alway necessary).  This functionality was added so that networks with
distinct regions could be modelled by giving each region its own Geometry
with unique models (e.g. to give a bi-modal pore size distribution).

Library of Preconfigured Geometry Classes
-----------------------------------------

This module contains a small selection of Geometry classes that are
pre-configured with a selection of pore-scale models.  These classes provide
a good starting point, but generally the choice of models and parameters used
will be specific to each problem and must be designed by the user.

The ``_StickAndBall`` class, as it's name suggests assumes spherical pores and
cylindrical throats.  Pore sizes are assigned by finding the largest sphere
that can fit at each site (this will be dictated by the lattice spacing used
when generating the Network), then scaling that value by a random number
between 0 and 0.1.  Throat diameters are taken as half the size of the smaller
of it's two neighbors.  All other properties are calculated using the geometry
of spheres and throats.

Customizing a Preconfigured Geometry Instance
---------------------------------------------

Perhaps the ``SpheresAndCylinders`` class is almost suitable but you wish
to decrease the pores sizes.  The following example illustrates how to
alter the ``'pore.size'`` model accordingly:

>>> import openpnm as op
>>> pn = op.network.Cubic([5, 5, 5])
>>> geo = op.geometry.SpheresAndCylinders(network=pn, pores=pn.Ps, throats=pn.Ts)

We can reach into the ``models`` attribute and change the parameters of any
model as follows:

>>> max(geo['pore.diameter']) < 1.0  # Confirm largest pore is less than 1.0
True
>>> geo.models['pore.seed']['num_range'] = [0.2, 0.7]
>>> geo.regenerate_models()  # Must regenerate all models
>>> max(geo['pore.diameter']) < 0.7  # Largest pore is now less than 0.7
True

This example illustrated that you can change one property ('pore.seed') and
that change can be cascaded to all dependent properties ('pore.diameter').

"""
from ._generic import GenericGeometry
from ._circles import CirclesAndRectangles
from ._cones import ConesAndCylinders
from ._cubes import CubesAndCuboids
from ._imported import Imported
from ._pyramids import PyramidsAndCuboids
from ._spheres import SpheresAndCylinders
from ._squares import SquaresAndRectangles
from ._trapezoids import TrapezoidsAndRectangles
