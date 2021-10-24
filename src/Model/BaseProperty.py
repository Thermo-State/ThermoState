from typing import Type, Final, List, Dict


class UNIT:
    SI: Final = "SI"
    ENG: Final = "English"
    DEFAULT: Final = "Default"
    CUSTOM: Final = "Customize"
    NONE: Final = "--"


class BaseProperty:
    """ Must implement these variables."""
    label: str = ""
    kw: str = ""
    symbol: str = ""
    units: List[str] = [UNIT.NONE]
    factors_list: List[float] = [1.0]
    unit_alias: Dict[str, str] = {UNIT.SI: units[0],
                                  UNIT.ENG: "",
                                  UNIT.DEFAULT: units[0]}

    curr_unit: str = "Default"

    def __init__(self, value: float, unit: str = "SI"):
        self.values: dict = {}
        self.factors: Dict[str, float] = {}
        self.round_digit: Dict[str, int] = {}

        if unit in self.unit_alias:
            unit = self.unit_alias[unit]

        for i, unit_i in enumerate(self.units):
            self.factors[unit_i] = self.factors_list[i]

        self.base_unit: str = self.units[self.factors_list.index(1.0)]

        if unit not in self.units:
            raise Exception("Not valid unit: " + unit)

        self.values[unit] = value
        if unit != self.base_unit:
            self.values[self.base_unit] = value / self.factors_list[self.units.index(unit)]

    def in_unit(self, unit: str = "SI"):
        if unit in self.unit_alias:
            unit = self.unit_alias[unit]
        if unit not in self.units:
            raise Exception("Not valid unit: " + unit + str(type(self)))

        if unit in self.values:
            return self.values[unit]
        else:
            self.values[unit] = self.values[self.base_unit] * self.factors_list[self.units.index(unit)]
            return self.values[unit]

    def in_curr_unit(self) -> float:
        return self.in_unit(self.get_curr_unit())

    def in_curr_unit_str(self):
        unit: str = self.get_curr_unit()
        value: float = self.in_unit(unit)

        return "{:.5g}".format(value)

    @classmethod
    def get_curr_unit(cls):
        unit: str = cls.curr_unit
        if unit in cls.unit_alias:
            unit = cls.unit_alias[unit]
        return unit

    @classmethod
    def set_curr_unit(cls, unit: str):
        if unit in cls.unit_alias or unit in cls.units:
            cls.curr_unit = unit
        else:
            cls.curr_unit = "Default"


class BaseSpEnergy(BaseProperty):
    label: str = "Energy"
    kw: str = ""
    symbol: str = ""
    units: List[str] = ["J/kg", "kJ/kg", "J/g", "BTU/lbm", "Cal/g"]
    factors_list: List[float] = [1.0, 1e-3, 0.001, 4.299226e-4, 2.388459e-4]
    unit_alias: Dict[str, str] = {"SI": units[0],
                                  "Default": units[1],
                                  "English": units[3]}


class BaseNumProperty(BaseProperty):
    label: str = ""
    kw: str = ""
    symbol: str = ""
    units: List[str] = ["--"]
    factors_list: List[float] = [1.0]
    unit_alias: Dict[str, str] = {"SI": units[0],
                                  "Default": units[0]}


class BaseSpHeat(BaseProperty):
    label: str = "Specific Heat"
    kw: str = ""
    symbol: str = ""
    units: list = ["J/kg⋅K", "kJ/kg⋅K", "BTU/lbm⋅R"]
    factors_list: List[float] = [1.0, 1e-3, 2.388459e-4]
    unit_alias: Dict[str, str] = {"SI": units[0],
                                  "Default": units[1],
                                  "English": units[2]}


class InvalidProperty(BaseProperty):
    """THis class should not be used itself to register anything. Only object of class should be used"""

    def __init__(self, class_property: Type[BaseProperty], error: str):
        self.label = class_property.label
        self.kw = class_property.kw
        self.symbol = class_property.symbol
        self.units = class_property.units
        self.factors_list = class_property.factors_list
        self.unit_alias = class_property.unit_alias
        self.class_property = class_property
        self.error = error
        super().__init__(0.0, "SI")

    def in_unit(self, unit: str = "SI"):
        return 0

    def in_curr_unit_str(self):
        return "?"

    def get_curr_unit(self):
        return self.class_property.get_curr_unit()

    def set_curr_unit(self, unit: str):
        self.class_property.set_curr_unit(unit)

    def error_info(self):
        return self.error
