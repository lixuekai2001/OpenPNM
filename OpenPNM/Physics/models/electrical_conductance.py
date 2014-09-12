r"""
===============================================================================
Submodule -- electrical_conductance
===============================================================================

"""

import scipy as _sp

def series_resistors(physics,
                     phase,
                     network,
                     pore_conductivity='pore.electrical_conductivity',
                     pore_area='pore.area',
                     pore_diameter='pore.diameter',
                     throat_area='throat.area',
                     throat_length='throat.length',
                     **kwargs):
    r"""
    Calculates the electrical conductance of throat assuming cylindrical geometry

    Parameters
    ----------
    network : OpenPNM Network Object

    phase : OpenPNM Phase Object
    """
    throats = phase.throats(physics.name)
    sigmap = phase[pore_conductivity]
    sigmat = phase.interpolate_data(sigmap)
    #Get Nt-by-2 list of pores connected to each throat
    pores = network.find_connected_pores(throats=network.throats(),flatten=0)
    #Find g for half of pore 1
    parea = network[pore_area]
    pdia = network[pore_diameter]
    pdia1 = pdia[pores[:,0]]
    pdia2 = pdia[pores[:,1]]
    #remove any non-positive lengths
    pdia1[pdia1<=0] = 1e-12
    pdia2[pdia2<=0] = 1e-12
    gp1 = sigmat*parea[pores[:,0]]/(0.5*pdia1)
    gp1[~(gp1>0)] = _sp.inf #Set 0 conductance pores (boundaries) to inf
    #Find g for half of pore 2
    gp2 = sigmat*parea[pores[:,1]]/(0.5*pdia2)
    gp2[~(gp2>0)] = _sp.inf #Set 0 conductance pores (boundaries) to inf
    #Find g for full throat
    tarea = network[throat_area]
    tlen = network[throat_length]
    #remove any non-positive lengths
    tlen[tlen<=0] = 1e-12
    gt = sigmat*tarea/tlen
    value = (1/gt + 1/gp1 + 1/gp2)**(-1)
    value = value[throats]
    return value
