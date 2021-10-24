from typing import Type, List, Dict
from contextlib import suppress
from CoolProp import CoolProp, AbstractState
import numpy as np

from Model.BaseProperty import BaseProperty, BaseSpEnergy, BaseSpHeat, InvalidProperty
from Model.OtherProperties import Cp, Cv, Conductivity, Prandtl, Viscosity, CompFactor, SurfaceTension, GibbsEnergy, \
    Helmholtz, MolarMass, TCritical, TTriple, PCritical, Phase, PTriple, DensityCritical
from Model.StateProperties import Temperature, Pressure, SpVolume, Density, SpEntropy, SpEnthalpy, SpIntEnergy, Quality

cp_input_combinations: List[List] = [[{"T", "P"}, CoolProp.PT_INPUTS],
                                     [{"T", "ρ"}, CoolProp.DmassT_INPUTS],
                                     [{"T", "s"}, CoolProp.SmassT_INPUTS],
                                     [{"T", "h"}, CoolProp.HmassT_INPUTS],
                                     [{"T", "u"}, CoolProp.TUmass_INPUTS],
                                     [{"T", "x"}, CoolProp.QT_INPUTS],
                                     [{"P", "ρ"}, CoolProp.DmassP_INPUTS],
                                     [{"P", "s"}, CoolProp.PSmass_INPUTS],
                                     [{"P", "h"}, CoolProp.HmassP_INPUTS],
                                     [{"P", "u"}, CoolProp.PUmass_INPUTS],
                                     [{"P", "x"}, CoolProp.PQ_INPUTS],
                                     [{"ρ", "s"}, CoolProp.DmassSmass_INPUTS],
                                     [{"ρ", "h"}, CoolProp.DmassHmass_INPUTS],
                                     [{"ρ", "u"}, CoolProp.DmassUmass_INPUTS],
                                     [{"ρ", "x"}, CoolProp.DmassQ_INPUTS],
                                     [{"s", "h"}, CoolProp.HmassSmass_INPUTS],
                                     [{"s", "u"}, CoolProp.SmassUmass_INPUTS],
                                     [{"h", "x"}, CoolProp.HmassQ_INPUTS]]

input_order: List[Type[BaseProperty]] = [Density, SpEnthalpy, Pressure, Quality, SpEntropy, Temperature, SpIntEnergy]

list_state_properties: List[Type[BaseProperty]] = [Temperature, Pressure, Density, SpEntropy, SpEnthalpy,
                                                   SpIntEnergy, Quality]
list_other_properties: List[Type[BaseProperty]] = [Phase, SpVolume, Cp, Cv, Conductivity, Prandtl, Viscosity,
                                                   CompFactor, SurfaceTension, GibbsEnergy, Helmholtz]
list_general_properties: List[Type[BaseProperty]] = [MolarMass, TCritical, TTriple, PCritical, PTriple,
                                                     DensityCritical]
list_props_for_var: List[Type[BaseProperty]] = list_state_properties + [SpVolume, Cp, Cv, Conductivity, Prandtl,
                                                                        Viscosity, CompFactor]

list_properties_unit: List[Type[BaseProperty]] = [BaseSpEnergy, BaseSpHeat, Temperature, Pressure, SpVolume, Density,
                                                  SpEntropy, Conductivity, Viscosity, SurfaceTension, MolarMass]
list_graph_properties: List[Type[BaseProperty]] = [Temperature, Pressure, SpVolume, SpEntropy, SpEnthalpy]

list_diagrams: List[List[Type[BaseProperty]]] = [[Temperature, SpEntropy],
                                                 [SpEnthalpy, SpEntropy],
                                                 [Pressure, SpEnthalpy]]


class Fluids:
    all: List[str] = CoolProp.FluidsList()
    default: List[str] = ["Water", "Air", "R134a", "CarbonDioxide"]


def get_combination(symbol_1: str, symbol_2: str):
    given: set = {symbol_1, symbol_2}

    for combination in cp_input_combinations:
        if given == combination[0]:
            return combination[1]

    raise Exception("This line should not get to be executed in get_combination")


def get_inputs_in_order(input_1: BaseProperty, input_2: BaseProperty):
    if input_order.index(type(input_1)) < input_order.index(type(input_2)):
        return input_1, input_2
    else:
        return input_2, input_1


def not_in_CoolProp(class_property: Type[BaseProperty], st: AbstractState):
    if class_property == SpVolume:
        return 1 / st.rhomass()
    elif class_property == PTriple:
        return CoolProp.PropsSI(PTriple.kw, st.name())
    else:
        raise Exception("not_in_CoolProp This line should not get to be executed" + str(class_property))


def get_property_valueSI_frm_st(class_property: Type[BaseProperty], st: AbstractState):
    att = getattr(st, class_property.kw, None)
    if att is not None:
        return att()
    else:
        return not_in_CoolProp(class_property, st)


def get_property_frm_st(class_property: Type[BaseProperty], st: AbstractState) -> BaseProperty:
    return class_property(value=get_property_valueSI_frm_st(class_property, st))


def get_property_objects(fluid: str, input_a: BaseProperty, input_b: BaseProperty) \
        -> (List[BaseProperty], List[BaseProperty]):
    input_1, input_2 = get_inputs_in_order(input_a, input_b)
    input_combination = get_combination(input_1.symbol, input_2.symbol)
    st = AbstractState("HEOS", fluid)
    st.update(input_combination, input_1.in_unit("SI"), input_2.in_unit("SI"))
    state_properties = []
    other_properties = []

    for class_property in list_state_properties:
        try:
            valueSI: float = get_property_valueSI_frm_st(class_property, st)
            state_properties.append(class_property(value=valueSI, unit="SI"))
        except Exception as e:
            state_properties.append(InvalidProperty(class_property, str(e)))

    for class_property in list_other_properties:
        try:
            valueSI: float = get_property_valueSI_frm_st(class_property, st)
            other_properties.append(class_property(value=valueSI, unit="SI"))
        except Exception as e:
            other_properties.append(InvalidProperty(class_property, str(e)))

    return state_properties, other_properties


class LiteState:
    def __init__(self, st: AbstractState):
        self.state: Dict[str, BaseProperty] = {}
        for class_property in list_graph_properties:
            self.state[class_property.kw] = get_property_frm_st(class_property, st)

    def get_tuple_curr_unit(self, class_property_1: Type[BaseProperty], class_property_2: Type[BaseProperty]):
        return self.state[class_property_1.kw].in_curr_unit(), self.state[class_property_2.kw].in_curr_unit()

    def get_property(self, class_property: Type[BaseProperty]):
        return self.state[class_property.kw]


available_input_properties: Dict[str, List[Type[BaseProperty]]] = {}
available_input_combinations: Dict[str, Dict[str, List[Type[BaseProperty]]]] = {}
general_property_objects: Dict[str, List[BaseProperty]] = {}
saturation_points: Dict[str, List[LiteState]] = {}
completed_setup: set = set()


def get_x_y(fluid: str, class_property_1: Type[BaseProperty] = SpEntropy,
            class_property_2: Type[BaseProperty] = Temperature):
    setup_fluid(fluid)
    x_data: List[float] = []
    y_data: List[float] = []

    for lst in saturation_points[fluid]:
        x, y = lst.get_tuple_curr_unit(class_property_1, class_property_2)
        x_data.append(x)
        y_data.append(y)

    return x_data, y_data


def get_available_input_properties(fluid: str) -> List[Type[BaseProperty]]:
    setup_fluid(fluid)
    return available_input_properties[fluid]


def get_other_input_properties(fluid: str, class_property: Type[BaseProperty]) -> List[Type[BaseProperty]]:
    setup_fluid(fluid)
    return available_input_combinations[fluid][class_property.symbol]


def get_general_property_objects(fluid: str) -> List[BaseProperty]:
    setup_fluid(fluid)
    return general_property_objects[fluid]


def setup_fluid(fluid: str):
    if fluid in completed_setup:
        return

    input_combinations_sym: List[set] = []
    st = AbstractState("HEOS", fluid)
    for item in cp_input_combinations:
        try:
            st.update(item[1], 0, 0)
        except ValueError as e:
            error: str = str(e)
            i = error.find("This pair of inputs")
            if i == -1:
                input_combinations_sym.append(item[0])

    input_properties: List[Type[BaseProperty]] = []
    input_properties_sym: List[str] = []
    unordered_result: set = set()
    for combination in input_combinations_sym:
        unordered_result.update(combination)
    for class_property in list_state_properties:
        if class_property.symbol in unordered_result:
            input_properties.append(class_property)
            input_properties_sym.append(class_property.symbol)

    input_combinations_dict: Dict[str, List[Type[BaseProperty]]] = {}
    for first_input in input_properties_sym:
        input_combinations_dict[first_input] = []
        for combination in input_combinations_sym:
            if first_input in combination:
                other_input: str = combination.difference({first_input}).pop()
                other_inp_class: Type[BaseProperty] = input_properties[input_properties_sym.index(other_input)]
                input_combinations_dict[first_input].append(other_inp_class)

    list_general_property_objects: List[BaseProperty] = []
    for class_property in list_general_properties:
        # noinspection PyBroadException
        try:
            valueSI: float = get_property_valueSI_frm_st(class_property, st)
            list_general_property_objects.append(class_property(value=valueSI, unit="SI"))
        except Exception:
            pass

    list_liteState: List[LiteState] = []

    st = AbstractState("HEOS", fluid)
    Tcr = st.T_critical()
    Ttr = st.Ttriple()
    diff = round(Tcr - Ttr)
    total_points = diff if diff % 100 == 0 else diff + 100 - diff % 100

    T_sat_liq = np.linspace(Ttr, Tcr, total_points)
    T_sat_liq[1:-1] = np.round(T_sat_liq[1:-1], 2)
    T_sat_vap = np.flip(T_sat_liq)

    for Ti in T_sat_liq:
        with suppress(Exception):
            st.update(CoolProp.QT_INPUTS, 0, Ti)
            list_liteState.append(LiteState(st))

    for Ti in T_sat_vap:
        with suppress(Exception):
            st.update(CoolProp.QT_INPUTS, 1, Ti)
            list_liteState.append(LiteState(st))

    saturation_points[fluid] = list_liteState
    available_input_properties[fluid] = input_properties
    available_input_combinations[fluid] = input_combinations_dict
    general_property_objects[fluid] = list_general_property_objects
    completed_setup.add(fluid)
