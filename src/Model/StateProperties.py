from typing import List, Dict

from .BaseProperty import BaseProperty, BaseSpEnergy, BaseNumProperty


class Temperature(BaseProperty):
    """docstring for Temperature."""
    label: str = "Temperature"
    kw: str = "T"
    symbol: str = "T"
    units: List = ["K", "°C", "°F", "R"]
    factors_list: List[float] = [1.0, 1.0, 1.0, 1.0]
    unit_alias: Dict[str, str] = {"SI": units[0],
                                  "Default": units[0],
                                  "English": units[2]}

    def __init__(self, value: float, unit: str = "K"):
        super().__init__(value, unit)

        if unit in self.unit_alias:
            unit = self.unit_alias[unit]

        self.__K: float or None = None
        self.__C: float or None = None
        self.__F: float or None = None
        self.__R: float or None = None

        if unit == self.units[0]:
            self.__K = value
        elif unit == self.units[1]:
            self.__C = value
            self.__c_to_k()
        elif unit == self.units[2]:
            self.__F = value
            self.__f_to_k()
        elif unit == self.units[3]:
            self.__R = value
            self.__r_to_k()
        else:
            raise Exception("Units must be 'K', 'C', 'F', or 'R'")

    def in_unit(self, unit: str = "SI") -> float:
        if unit in self.unit_alias:
            unit = self.unit_alias[unit]

        if unit == self.units[0]:
            return self.__K
        elif unit == self.units[1]:
            if self.__C is None:
                self.__k_to_c()
            return self.__C
        elif unit == self.units[2]:
            if self.__F is None:
                self.__k_to_f()
            return self.__F
        elif unit == self.units[3]:
            if self.__R is None:
                self.__k_to_r()
            return self.__R
        else:
            raise Exception("Units must be 'K', 'C', 'F', or 'R' --" + unit)

    def __k_to_c(self):
        self.__C = self.__K - 273.15

    def __k_to_f(self):
        self.__F = (self.__K - 273.15) * 9 / 5 + 32

    def __k_to_r(self):
        self.__R = self.__K * 9 / 5

    def __c_to_k(self):
        self.__K = self.__C + 273.15

    def __f_to_k(self):
        self.__K = (self.__F - 32) * 5 / 9 + 273.15

    def __r_to_k(self):
        self.__K = self.__R * 5 / 9


class Pressure(BaseProperty):
    label: str = "Pressure"
    kw: str = "p"
    symbol: str = "P"
    units: List = ["Pa", "kPa", "MPa", "lbf/in²", "bar", "mmHg", "atm", "dyn/cm²", "kgf/cm²"]
    factors_list: List[float] = [1.0, 1e-3, 1e-6, 0.00014503773, 1e-5, 0.0075006149, 9.869233e-6, 10, 1.019716e-5]
    unit_alias: Dict[str, str] = {"SI": units[0],
                                  "Default": units[2],
                                  "English": units[3]}


class SpVolume(BaseProperty):
    label: str = "Specific Volume"
    kw: str = "sp_volume"
    symbol: str = "v"
    units: List = ["m³/kg", "ft³/lbm", "cm³/g"]
    factors_list: List[float] = [1.0, 16.0185, 1e3]
    unit_alias: Dict[str, str] = {"SI": units[0],
                                  "Default": units[0],
                                  "English": units[1]}


class Density(BaseProperty):
    label: str = "Density"
    kw: str = "rhomass"
    symbol: str = "ρ"
    units: List = ["kg/m³", "lbm/ft³", "g/cm³", "lbm/in³"]
    factors_list: List[float] = [1.0, 0.06242797, 1e-3, 3.61273e-5]
    unit_alias: Dict[str, str] = {"SI": units[0],
                                  "Default": units[0],
                                  "English": units[1]}


class SpEnthalpy(BaseSpEnergy):
    label: str = "Enthalpy"
    kw: str = "hmass"
    symbol: str = "h"


class SpIntEnergy(BaseSpEnergy):
    label: str = "Internal Energy"
    kw: str = "umass"
    symbol: str = "u"


class SpEntropy(BaseProperty):
    label: str = "Entropy"
    kw: str = "smass"
    symbol: str = "s"
    units: List = ["J/kg⋅K", "kJ/kg⋅K", "BTU/lbm⋅R"]
    factors_list: List[float] = [1.0, 1e-3, 0.0002388459]
    unit_alias: Dict[str, str] = {"SI": units[0],
                                  "Default": units[1],
                                  "English": units[2]}


class Quality(BaseNumProperty):
    label: str = "Quality"
    kw: str = "Q"
    symbol: str = "x"

    def in_curr_unit_str(self):
        value: float = self.in_unit(self.get_curr_unit())
        if not 0.0 <= value <= 1.0:
            return "--"
        else:
            return super().in_curr_unit_str()
