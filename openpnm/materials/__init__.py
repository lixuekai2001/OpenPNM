r"""
Collection of preconfigured Network-Geometry combinations
=========================================================

This module provides a library of preconfigured Network-Geometry combinations.

In most case the topology and geometry cannot be considered in isolation.
This module provides recipes that create both the Network and Geometry objects
simultaneously to ensure sensible correspondance between things like lattice
spacing and pore sizes.  Some of the classes in this module have a signficant
amount of custom code (e.g. ``VoronoiFibers``), while others are simple
recipes that combine existing models in OpenPNM (e.g. ``BereaCubic``).

"""

from ._voronoi_fibers import VoronoiFibers
from ._bundle_of_tubes import BundleOfTubes
