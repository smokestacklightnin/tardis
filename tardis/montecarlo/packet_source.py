import abc

import numpy as np
import numexpr as ne
from tardis import constants as const
from tardis.montecarlo import (
    montecarlo_configuration as montecarlo_configuration,
)

from astropy import units as u


class BasePacketSource(abc.ABC):
    """
    Abstract base packet source

    Parameters
    ----------
    base_seed : int
        Base Seed for random number generator
    legacy_secondary_seed : int
        Secondary seed for global numpy rng (Deprecated: Legacy reasons only)
    """

    # MAX_SEED_VAL must be multiple orders of magnitude larger than no_of_packets;
    # otherwise, each packet would not have its own seed. Here, we set the max
    # seed val to the maximum allowed by numpy.
    MAX_SEED_VAL = 2**32 - 1

    def __init__(self, base_seed=None, legacy_second_seed=None):
        self.base_seed = base_seed
        if (
            montecarlo_configuration.LEGACY_MODE_ENABLED
            and legacy_second_seed is not None
        ):
            np.random.seed(legacy_second_seed)
        else:
            np.random.seed(self.base_seed)

    def _reseed(self, seed):
        self.rng = np.random.default_rng(seed=seed)

    def create_packet_seeds(self, no_of_packets, seed_offset):
        # the iteration (passed as seed_offset) is added each time to preserve randomness
        # across different simulations with the same temperature,
        # for example. We seed the random module instead of the numpy module
        # because we call random.sample, which references a different internal
        # state than in the numpy.random module.
        self._reseed(self.base_seed + seed_offset)
        seeds = self.rng.choice(self.MAX_SEED_VAL, no_of_packets, replace=True)
        return seeds

    @abc.abstractmethod
    def set_state_from_model(self, model):
        pass

    @abc.abstractmethod
    def create_packet_radii(self, no_of_packets, *args, **kwargs):
        pass

    @abc.abstractmethod
    def create_packet_nus(self, no_of_packets, *args, **kwargs):
        pass

    @abc.abstractmethod
    def create_packet_mus(self, no_of_packets, *args, **kwargs):
        pass

    @abc.abstractmethod
    def create_packet_energies(self, no_of_packets, *args, **kwargs):
        pass

    def create_packets(self, no_of_packets, *args, **kwargs):
        """Generate packet properties as arrays

        Parameters
        ----------
        no_of_packets : int
            Number of packets

        Returns
        -------
        array
            Packet radii
        array
            Packet frequencies
        array
            Packet directions
        array
            Packet energies
        """
        radii = self.create_packet_radii(no_of_packets, *args, **kwargs)
        nus = self.create_packet_nus(no_of_packets, *args, **kwargs)
        mus = self.create_packet_mus(no_of_packets, *args, **kwargs)
        energies = self.create_packet_energies(no_of_packets, *args, **kwargs)

        return radii, nus, mus, energies


class BlackBodySimpleSource(BasePacketSource):
    """
    Simple packet source that generates Blackbody packets for the Montecarlo
    part.

    Parameters
    ----------
    radius : float64
        Initial packet radius
    temperature : float
        Absolute Temperature.
    base_seed : int
        Base Seed for random number generator
    legacy_secondary_seed : int
        Secondary seed for global numpy rng (Deprecated: Legacy reasons only)
    """

    @classmethod
    def from_model(cls, model, *args, **kwargs):
        return cls(model.r_inner[0], model.t_inner.value, *args, **kwargs)

    def __init__(self, radius=None, temperature=None, **kwargs):
        self.radius = radius
        self.temperature = temperature
        super().__init__(**kwargs)

    def set_state_from_model(self, model):
        """
        Set state of packet source (correct state should be ensured before creating packets)
        """
        self.radius = model.r_inner[0]
        self.temperature = model.t_inner.value

    def create_packets(self, no_of_packets, *args, **kwargs):
        if self.radius is None or self.temperature is None:
            raise ValueError("Black body Radius or Temperature isn't set")
        return super().create_packets(no_of_packets, *args, **kwargs)

    def create_packet_radii(self, no_of_packets):
        """
        Create packet radii

        Parameters
        ----------
        no_of_packets : int
            number of packets to be created

        Returns
        -------
        Radii for packets
            numpy.ndarray
        """
        return np.ones(no_of_packets) * self.radius

    def create_packet_nus(self, no_of_packets, l_samples=1000):
        """
        Create packet :math:`\\nu` distributed using the algorithm described in
        Bjorkman & Wood 2001 (page 4) which references
        Carter & Cashwell 1975:
        First, generate a uniform random number, :math:`\\xi_0 \\in [0, 1]` and
        determine the minimum value of
        :math:`l, l_{\\rm min}`, that satisfies the condition
        .. math::
            \\sum_{i=1}^{l} i^{-4} \\ge {{\\pi^4}\\over{90}} m_0 \\;.
        Next obtain four additional uniform random numbers (in the range 0
        to 1) :math:`\\xi_1, \\xi_2, \\xi_3, {\\rm and } \\xi_4`.
        Finally, the packet frequency is given by
        .. math::
            x = -\\ln{(\\xi_1\\xi_2\\xi_3\\xi_4)}/l_{\\rm min}\\;.
        where :math:`x=h\\nu/kT`

        Parameters
        ----------
        no_of_packets : int
        l_samples : int
            number of l_samples needed in the algorithm

        Returns
        -------
        array of frequencies
            numpy.ndarray
        """
        l_array = np.cumsum(np.arange(1, l_samples, dtype=np.float64) ** -4)
        l_coef = np.pi**4 / 90.0

        # For testing purposes
        if montecarlo_configuration.LEGACY_MODE_ENABLED:
            xis = np.random.random((5, no_of_packets))
        else:
            xis = self.rng.random((5, no_of_packets))

        l = l_array.searchsorted(xis[0] * l_coef) + 1.0
        xis_prod = np.prod(xis[1:], 0)
        x = ne.evaluate("-log(xis_prod)/l")

        return x * (const.k_B.cgs.value * self.temperature) / const.h.cgs.value

    def create_packet_mus(self, no_of_packets):
        """
        Create zero-limb-darkening packet :math:`\mu` distributed
        according to :math:`\\mu=\\sqrt{z}, z \isin [0, 1]`

        Parameters
        ----------
        no_of_packets : int
            number of packets to be created

        Returns
        -------
        Directions for packets
            numpy.ndarray
        """

        # For testing purposes
        if montecarlo_configuration.LEGACY_MODE_ENABLED:
            return np.sqrt(np.random.random(no_of_packets))
        else:
            return np.sqrt(self.rng.random(no_of_packets))

    def create_packet_energies(self, no_of_packets):
        """
        Uniformly distribute energy in arbitrary units where the ensemble of
        packets has energy of 1.

        Parameters
        ----------
        no_of_packets : int
            number of packets

        Returns
        -------
        energies for packets
            numpy.ndarray
        """
        return np.ones(no_of_packets) / no_of_packets

    def set_temperature_from_luminosity(self, luminosity: u.Quantity):
        """
        Set blackbody packet source temperature from luminosity

        Parameters
        ----------

        luminosity : u.Quantity

        """
        self.temperature = (
            (luminosity / (4 * np.pi * self.radius**2 * const.sigma_sb))
            ** 0.25
        ).to("K")


class BlackBodySimpleSourceRelativistic(BlackBodySimpleSource):
    """
    Simple packet source that generates Blackbody packets for the Montecarlo
    part.

    Parameters
    ----------
    time_explosion : float 64
        Time elapsed since explosion
    radius : float64
        Initial packet radius
    temperature : float
        Absolute Temperature.
    base_seed : int
        Base Seed for random number generator
    legacy_secondary_seed : int
        Secondary seed for global numpy rng (Deprecated: Legacy reasons only)
    """

    @classmethod
    def from_model(cls, model, *args, **kwargs):
        return cls(
            model.time_explosion,
            model.r_inner[0],
            model.t_inner.value,
            *args,
            **kwargs,
        )

    def __init__(self, time_explosion=None, **kwargs):
        self.time_explosion = time_explosion
        super().__init__(**kwargs)

    def set_state_from_model(self, model):
        """
        Set state of packet source (correct state should be ensured before creating packets)
        """
        self.time_explosion = model.time_explosion
        super().set_state_from_model(model)

    def create_packets(self, no_of_packets):
        """Generate relativistic black-body packet properties as arrays

        Parameters
        ----------
        no_of_packets : int
            Number of packets

        Returns
        -------
        array
            Packet radii
        array
            Packet frequencies
        array
            Packet directions
        array
            Packet energies
        """
        if self.radius is None or self.time_explosion is None:
            raise ValueError("Black body Radius or Time of Explosion isn't set")
        self.beta = ((self.radius / self.time_explosion) / const.c).to("")
        return super().create_packets(no_of_packets)

    def create_packet_nus(self, no_of_packets):
        """
        Create zero-limb-darkening packet :math:`\mu^\prime` distributed
        according to :math:`\\mu^\\prime=2 \\frac{\\mu^\\prime + \\beta}{2 \\beta + 1}`.
        The complicated distribution is due to the fact that the inner boundary
        on which the packets are initialized is not comoving with the material.

        Parameters
        ----------
        no_of_packets : int
            number of packets to be created

        Returns
        -------
        array of frequencies
            numpy.ndarray
        """
        z = self.rng.random(no_of_packets)
        beta = self.beta
        return -beta + np.sqrt(beta**2 + 2 * beta * z + z)

    def create_packet_energies(self, no_of_packets):
        """
        Uniformly distribute energy in arbitrary units where the ensemble of
        packets has energy of 1 multiplied by relativistic correction factors.

        Parameters
        ----------
        no_of_packets : int
            number of packets

        Returns
        -------
        energies for packets
            numpy.ndarray
        """
        beta = self.beta
        gamma = 1.0 / np.sqrt(1 - beta**2)
        static_inner_boundary2cmf_factor = (2 * beta + 1) / (1 - beta**2)
        energies = np.ones(no_of_packets) / no_of_packets
        # In principle, the factor gamma should be applied to the time of
        # simulation to account for time dilation between the lab and comoving
        # frame. However, all relevant quantities (luminosities, estimators, ...)
        # are calculated as ratios of packet energies and the time of simulation.
        # Thus, we can absorb the factor gamma in the packet energies, which is
        # more convenient.
        return energies * static_inner_boundary2cmf_factor / gamma
