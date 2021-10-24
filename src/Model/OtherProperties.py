from typing import Dict, List

from CoolProp import (iphase_liquid,
                      iphase_supercritical,
                      iphase_supercritical_gas,
                      iphase_supercritical_liquid,
                      iphase_critical_point,
                      iphase_gas,
                      iphase_twophase,
                      iphase_unknown)

from .BaseProperty import BaseProperty, BaseSpEnergy, BaseSpHeat, BaseNumProperty
from .StateProperties import Pressure, Temperature, Density


class CompFactor(BaseNumProperty):
    label: str = "Compressibility Factor"
    kw: str = "compressibility_factor"
    symbol: str = "Z"


class Conductivity(BaseProperty):
    label: str = "Conductivity"
    kw: str = "conductivity"
    symbol: str = "κ"
    units: List[str] = ["W/m⋅K", "kW/m⋅K", "BTU/h⋅ft⋅°F"]
    factors_list: List[float] = [1.0, 1e-3, 0.577789317]
    unit_alias: Dict[str, str] = {"SI": units[0],
                                  "Default": units[0],
                                  "English": units[2]}


class Cp(BaseSpHeat):
    label: str = "Constant Pressure Heat Capacity"
    kw: str = "cpmass"
    symbol: str = "Cp"


class Cv(BaseSpHeat):
    label: str = "Constant Volume Heat Capacity"
    kw: str = "cvmass"
    symbol: str = "Cv"


class GasConstant(BaseProperty):
    label: str = "Gas Constant"
    kw: str = "gas_constant"
    symbol: str = "R"
    units: List[str] = ["J/mol⋅K", "kJ/mol⋅K"]
    factors_list: List[float] = [1.0, 1e-3]
    unit_alias: Dict[str, str] = {"SI": units[0],
                                  "Default": units[1]}


class GibbsEnergy(BaseSpEnergy):
    label: str = "Gibbs Energy"
    kw: str = "gibbsmass"
    symbol: str = "G"


class Helmholtz(BaseSpEnergy):
    label: str = "Helmholtz Energy"
    kw: str = "helmholtzmass"
    symbol: str = "F"


class MolarMass(BaseProperty):
    label: str = "Molar Mass"
    kw: str = "molar_mass"
    symbol: str = "M"
    units: List[str] = ["kg/mol", "g/mol"]
    factors_list: List[float] = [1.0, 1e3]
    unit_alias: Dict[str, str] = {"SI": units[0],
                                  "Default": units[0]}


class DensityCritical(Density):
    label: str = "Critical Density"
    kw: str = "rhomass_critical"
    symbol: str = "ρcr"


class PCritical(Pressure):
    label: str = "Critical Pressure"
    kw: str = "p_critical"
    symbol: str = "Pcr"


class PTriple(Pressure):
    label: str = "Triple Point Pressure"
    kw: str = "p_triple"
    symbol: str = "Ptr"


class TCritical(Temperature):
    label: str = "Critical Temperature"
    kw: str = "T_critical"
    symbol: str = "Tcr"


class TTriple(Temperature):
    label: str = "Triple Point Temperature"
    kw: str = "TTriple"
    symbol: str = "Ttr"


class TReducing(Temperature):
    label: str = "Reducing Temp"
    kw: str = "T_reducing"
    symbol: str = "Tr"


class Prandtl(BaseNumProperty):
    label: str = "Prandtl Number"
    kw: str = "Prandtl"
    symbol: str = "Pr"


class SoundSpeed(BaseProperty):
    label: str = "Speed of Sound"
    kw: str = "speed_sound"
    symbol: str = "Vs"
    units: List[str] = ["m/s", "km/s", "km/h", "MPH", "ft/s"]
    factors_list: List[float] = [1.0, 1e-3, 3.6, 2.236936, 3.28084]
    unit_alias: Dict[str, str] = {"SI": units[0],
                                  "Default": units[0],
                                  "English": units[3]}


class SurfaceTension(BaseProperty):
    label: str = "Surface Tension"
    kw: str = "surface_tension"
    symbol: str = "σ"
    units: List[str] = ["mN/m", "N/m", "dyn/cm", "lb/ft"]
    factors_list: List[float] = [1e3, 1.0, 1e3, 0.0685]
    unit_alias: Dict[str, str] = {"SI": units[1],
                                  "Default": units[0],
                                  "English": units[3]}


class Viscosity(BaseProperty):
    label: str = "Viscosity"
    kw: str = "viscosity"
    symbol: str = "μ"
    units: List[str] = ["Pa⋅s", "P", "cP", "kgf⋅s/m²", "lbf⋅s/ft²"]
    factors_list: List[float] = [1.0, 10, 1000, 0.1019716, 0.02088543]
    unit_alias: Dict[str, str] = {"SI": units[0],
                                  "Default": units[2],
                                  "English": units[4]}


class Phase(BaseNumProperty):
    label: str = "Phase"
    kw: str = "phase"
    symbol: str = "phase"
    phase_dict: Dict[int, str] = {iphase_liquid: 'Sub-critical liquid',
                                  iphase_supercritical: 'Supercritical',
                                  iphase_supercritical_gas: 'Supercritical gas',
                                  iphase_supercritical_liquid: 'Supercritical liquid',
                                  iphase_critical_point: 'critical point',
                                  iphase_gas: 'Sub-critical gas',
                                  iphase_twophase: 'Two-phase',
                                  iphase_unknown: 'Unknown phase'}

    def in_curr_unit_str(self):
        return self.phase_dict.get(self.in_unit())
