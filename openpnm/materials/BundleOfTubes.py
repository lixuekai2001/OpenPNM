import scipy as sp
import scipy.stats as spst
from openpnm.utils import logging, Project
from openpnm.network import Cubic
from openpnm.geometry import GenericGeometry
from openpnm.topotools import trim
import openpnm.models as mods
logger = logging.getLogger(__name__)


class BundleOfTubes(Project):
    r"""
    A basic 'bundle-of-tubes' model.

    Parameters
    ----------
    shape : array_like or int
        The number of pores in the X and Y direction of the domain.  It will
        be 2 pores thick in the Z direction, as required to be a bundle of
        tubes model.  If an ``int`` is given it will be applied to both the
        X and Y directions.

    spacing : array_like or float
        The spacing between the tubes in the X and Y direction.  If a ``float``
        is given it will be applied to both the X and Y directions.

    length : float
        The length of the tubes or thickness of the domain in the z-direction.

    psd_params : dictionary
        The parameters of the statistical distribution of the pore sizes.
        The dictionary must contain the type of distribution to use (specified
        as 'distribution'), selected from the ``scipy.stats`` module, and the
        parameters corresponding to the chosen distribution.
        The default is: ``{'distribution': 'norm', 'loc': 0.5, 'scale': 0.11}.
        Note that ``scipy.stats`` uses *loc* and *scale* to be consistent
        between different distribution types, instead of things like *mean*
        and *stddev*.

    name : string, optional
        The name to give the Project

    Examples
    --------

    """

    def __init__(self, shape, spacing=[1.0, 1.0], length=1.0,
                 psd_params={'distribution': 'norm', 'loc': 0.5, 'scale': 0.1},
                 name=None, **kwargs):
        super().__init__(name=name)

        if isinstance(shape, int):
            shape = sp.array([shape, shape, 2])
        elif len(shape) == 2:
            shape = sp.concatenate((sp.array(shape), [2]))
        else:
            raise Exception('shape not understood, must be int ' +
                            ' or list of 2 ints')
        if isinstance(spacing, float):
            spacing = sp.array([spacing, spacing, length])
        elif len(spacing) == 2:
            spacing = sp.concatenate((sp.array(spacing), [length]))
        else:
            raise Exception('spacing not understood, must be float ' +
                            'or list of 2 floats')

        net = Cubic(shape=shape, spacing=spacing, project=self, **kwargs)
        Ps_top = net.pores('top')
        Ps_bot = net.pores('bottom')
        Ts = net.find_connecting_throat(P1=Ps_top, P2=Ps_bot)
        Ts = net.tomask(throats=Ts)
        trim(network=net, throats=~Ts)

        geom = GenericGeometry(network=net, pores=net.Ps, throats=net.Ts)

        geom.add_model(propname='throat.seed',
                       model=mods.geometry.throat_seed.random)
        if psd_params['distribution'] in ['norm', 'normal', 'gaussian']:
            geom.add_model(propname='throat.diameter',
                           seeds='throat.seed',
                           model=mods.geometry.throat_size.normal,
                           loc=psd_params['loc'], scale=psd_params['scale'])
        elif psd_params['distribution'] in ['weibull']:
            geom.add_model(propname='throat.diameter',
                           seeds='throat.seed',
                           model=mods.geometry.throat_size.weibull,
                           loc=psd_params['loc'], scale=psd_params['scale'])
        else:
            func = getattr(spst, psd_params['distribution'])
            psd = func.freeze(loc=psd_params['loc'], scale=psd_params['scale'])
            geom.add_model(propname='throat.diameter',
                           seeds='throat.seed',
                           model=mods.geometry.throat_size.generic_distribution,
                           func=psd)
        geom.add_model(propname='pore.diameter',
                       model=mods.geometry.pore_size.from_neighbor_throats,
                       throat_prop='throat.diameter', mode='max')
        geom.add_model(propname='throat.length',
                       model=mods.geometry.throat_length.classic)
        geom.add_model(propname='pore.volume',
                       model=mods.misc.constant, value=0.0)
        geom.add_model(propname='throat.volume',
                       model=mods.geometry.throat_volume.cylinder)

        geom.regenerate_models()
