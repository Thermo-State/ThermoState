import inspect
import math
from contextlib import suppress
from json import JSONEncoder, JSONDecoder
from typing import Type, Any, Optional, Union, Final, List, Tuple, Dict

from Model.BaseProperty import BaseProperty
from Model.CoolPropInterface import list_props_for_var
from Model.PureSubstances import PureState

MATH_FUNC_NAMES: List[str] = ["log", "log10", "log2", "sqrt", "exp"]
MATH_NS = {fn: math.__dict__[fn] for fn in MATH_FUNC_NAMES}
NULL: Any = object()


def resolveDependency(vs: 'VarState') -> List['VarState']:
    result: List[VarState] = []
    first = vs.getDependency()
    result.extend(first)
    for vs_i in first:
        result.extend(resolveDependency(vs_i))

    result_filtered: List[VarState] = []
    for vs_i in result:
        if vs_i not in result_filtered:
            result_filtered.append(vs_i)
    return result_filtered


def whichDependsOnIt(vs: 'VarState', var_states: List['VarState']) -> Optional['VarState']:
    for vs_i in var_states:
        if vs in resolveDependency(vs_i):
            return vs_i
    return None


def get_subClasses(cls: Type) -> List[Type]:
    subclasses = cls.__subclasses__()
    for sc in subclasses:
        ssc = get_subClasses(sc)
        if ssc:
            subclasses.extend(ssc)
    return subclasses


class IDGen:
    def __init__(self, init: int = 0):
        self.count: int = init

    def nextID(self) -> int:
        self.count = self.count + 1
        return self.count


class JsonInitiable:
    TYPE_KEY: Final = "type"
    TYPE_REF: Final = "ref"
    BP_KEY: Final = "class_property"

    @classmethod
    def getInitArgs(cls) -> List[str]:
        args = inspect.getfullargspec(cls.__init__).args
        del args[0]
        return args

    def getInitDict(self) -> Dict[str, Any]:
        args: List[str] = self.getInitArgs()
        init_dict: Dict[str, Any] = {self.TYPE_KEY: self.__class__.__name__}
        init_dict.update({kw: getattr(self, kw) for kw in args})
        return init_dict


JI: Type[JsonInitiable] = JsonInitiable


class MetaFlow(JsonInitiable):
    def __init__(self, build: int):
        self.build = build


class Value(JsonInitiable):
    def __init__(self, **kwargs):
        self.value: float = math.nan

    @property
    def definition(self):
        return ""

    def get(self) -> float:
        return self.value

    def update(self):
        """ (re)fetch value from dependent upstream variable. (re)calculate inner vars_dependency as well"""
        pass

    def dependency(self) -> List['VarState']:
        return []


class VarState(JsonInitiable):
    def __init__(self, **kwargs):
        self.desc: str = ""
        self.uid: int = 0
        self._name: str = ""

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def definition(self) -> str:
        return ""

    def calculate(self):
        pass

    def getDependency(self) -> List['VarState']:
        pass

    def getIdentifier(self) -> str:
        return "uid" + str(self.uid)


class Variable(VarState):
    """ An object that wraps one of 4 types of value and assigns a unique uid"""

    def __init__(self, name: str, uid: int, inp: Value, desc: str = None):
        super().__init__()

        self.name = name
        self.uid = uid
        self.inp = inp
        self.desc: str = desc

        self.value: float = math.nan

    @property
    def definition(self) -> str:
        return self.inp.definition

    def calculate(self):
        self.inp.update()
        self.value = self.inp.get()

    def hasRange(self) -> bool:
        if getattr(self.inp, "value_range", None) is None:
            return False
        else:
            self.inp: 'IndValue'
            if self.inp.value_range is None:
                return False
            else:
                return True

    def getRange(self) -> Optional[Tuple[float]]:
        if self.hasRange():
            self.inp: 'IndValue'
            return self.inp.value_range
        else:
            return None

    def edit(self, name: str, inp: Value, desc: str = None):
        self.name = name
        self.desc = desc
        self.inp = inp

    def getDependency(self) -> List[VarState]:
        return self.inp.dependency()


class State(VarState):
    def __init__(self, no: int, uid: int, fluid: str, desc: str,
                 class_property_1: Type[BaseProperty], class_property_2: Type[BaseProperty],
                 inp_1: Value, inp_2: Value, unit_1: str, unit_2: str):
        super().__init__()
        self.no = no
        self.uid = uid
        self.fluid = fluid
        self.class_property_1 = class_property_1
        self.class_property_2 = class_property_2
        self.inp_1 = inp_1
        self.inp_2 = inp_2
        self.unit_1 = unit_1
        self.unit_2 = unit_2
        self.desc = desc

        self.value: PureState = NULL
        self.properties: Dict[str, BaseProperty] = {}

    @property
    def name(self) -> str:
        return f"State {self.no}"

    def calculate(self):
        self.inp_1.update()
        self.inp_2.update()

        prop_1: BaseProperty = self.class_property_1(value=self.inp_1.get(), unit=self.unit_1)
        prop_2: BaseProperty = self.class_property_2(value=self.inp_2.get(), unit=self.unit_2)
        self.value: PureState = PureState(fluid=self.fluid, input_a=prop_1, input_b=prop_2)

        for p in self.value.state_properties:
            self.properties[p.kw] = p
        for p in self.value.other_properties:
            self.properties[p.kw] = p

    def getPropertyValue(self, class_property: Type[BaseProperty], unit: str) -> float:
        return self.properties.get(class_property.kw).in_unit(unit=unit)

    @property
    def definition(self) -> str:
        sub1_def: str = self.class_property_1.symbol + " = "
        sub2_def: str = self.class_property_2.symbol + " = "

        input_1: Value = self.inp_1
        input_2: Value = self.inp_2
        unit_1 = self.unit_1
        unit_2 = self.unit_2

        if isinstance(input_1, StateValue):
            sub1_def = sub1_def + input_1.definition_wo_unit
        else:
            input_1: 'Value'
            sub1_def = sub1_def + input_1.definition + " (" + unit_1 + ")"

        if isinstance(input_2, StateValue):
            sub2_def = sub2_def + input_2.definition_wo_unit
        else:
            input_2: 'Value'
            sub2_def = sub2_def + input_2.definition + " (" + unit_2 + ")"

        return self.fluid + " at " + sub1_def + " & " + sub2_def

    def edit(self, no: int, fluid: str, desc: str,
             class_property_1: Type[BaseProperty], class_property_2: Type[BaseProperty],
             inp_1: Value, inp_2: Value, unit_1: str, unit_2: str):
        self.no = no
        self.fluid = fluid
        self.class_property_1 = class_property_1
        self.class_property_2 = class_property_2
        self.inp_1 = inp_1
        self.inp_2 = inp_2
        self.unit_1 = unit_1
        self.unit_2 = unit_2
        self.desc = desc

    def getDependency(self) -> List['VarState']:
        return self.inp_1.dependency() + self.inp_2.dependency()


class IndValue(Value):
    """ Independent float value. may contain range information"""

    def __init__(self, value: float, value_range: Tuple[float, float] = None):
        super().__init__()
        self.value_range = value_range
        self.value = value
        self._definition: str = "{:.5g}".format(value)

    @property
    def definition(self) -> str:
        return self._definition


class DepValue(Value):
    """ alternative to ExprValue when dependent on single upstream variable. eval() overhead is avoided"""

    def __init__(self, var_ref: Variable):
        super().__init__()
        self.var_ref = var_ref

    @property
    def definition(self) -> str:
        return self.var_ref.name

    def update(self):
        self.value = self.var_ref.value

    def dependency(self) -> List['VarState']:
        return [self.var_ref]


class ExprManager:
    id_to_label: Dict[str, str] = {"*": "×", "**": "^"}

    def __init__(self, expr: List[Union[str, Variable]], ups_vars: List[Variable]):
        self.ups_vars = ups_vars

        self.__expr = expr
        self.__expr_dis = []
        self.__update_expr_dis()

    def add(self, o: Union[str, Variable]):
        self.__expr.append(o)
        if isinstance(o, Variable):
            self.__expr_dis.append(o.name)
        else:
            self.__expr_dis.append(self.getButtonLabel(bid=o))

    def pop(self):
        with suppress(Exception):
            self.__expr.pop()
            self.__expr_dis.pop()

    def clear(self):
        self.__expr.clear()
        self.__expr_dis.clear()

    def __update_expr_dis(self):
        self.__expr_dis.clear()
        for i in self.__expr:
            if isinstance(i, Variable):
                self.__expr_dis.append(i.name)
            else:
                self.__expr_dis.append(self.getButtonLabel(bid=i))

    def displayText(self):
        return "".join(self.__expr_dis)

    def getExpr(self):
        return self.__expr

    def getExprDis(self):
        return self.__expr_dis

    @classmethod
    def getButtonLabel(cls, bid: str) -> str:
        if bid in cls.id_to_label:
            return cls.id_to_label[bid]
        else:
            return bid


class ExprValue(Value):
    """ value may depends on upstream and inner variables"""

    def __init__(self, expr: List[Union[str, Variable]], inner_vars: List[Variable]):
        super().__init__()
        self.ups_dependency: List[Variable] = []
        self.inner_vars: List[Variable] = []
        self.expr = expr
        self.vars_dependency: Dict[str, Variable] = {}

        def_expr = expr.copy()
        expr_eval = expr.copy()
        for i, token in enumerate(expr):
            if isinstance(token, Variable):
                if token in inner_vars:
                    self.inner_vars.append(token)
                else:
                    self.ups_dependency.append(token)
                var_id: str = token.getIdentifier()
                self.vars_dependency[var_id] = token
                def_expr[i] = "{" + var_id + "}"
                expr_eval[i] = var_id
            else:
                token: str
                def_expr[i] = ExprManager.getButtonLabel(token)

        self.def_string: str = "".join(def_expr)
        self.eval_string: str = "".join(expr_eval)

    @property
    def definition(self):
        return self.def_string.format(**{k: v.name for k, v in self.vars_dependency.items()})

    def update(self):
        for v in self.inner_vars:
            v.calculate()

        MATH_NS["__builtins__"] = {}

        self.value = eval(self.eval_string, MATH_NS, {k: v.value for k, v in self.vars_dependency.items()})

    def dependency(self) -> List['VarState']:
        return self.ups_dependency + self.inner_vars


class StateValue(Value):

    def __init__(self, state: State, class_property: Type[BaseProperty], unit: str):
        super().__init__()
        self.state = state
        self.class_property = class_property
        self.unit = unit

    @property
    def definition_wo_unit(self) -> str:
        return f"{self.class_property.symbol}:{self.state.no}"

    @property
    def definition(self) -> str:
        return f"{self.definition_wo_unit} ({self.unit})"

    def update(self):
        self.value = self.state.getPropertyValue(class_property=self.class_property, unit=self.unit)

    def dependency(self) -> List['VarState']:
        return [self.state]


class Flow(JsonInitiable):
    def __init__(self, name: str, fluids: List[str], ranged_vars: List[Variable], var_states: List[VarState],
                 desc: str = ""):
        self.name = name
        self.desc = desc
        self.fluids = fluids
        self.ranged_vars: List[Variable] = ranged_vars
        self.var_states: List[VarState] = var_states

    def edit(self, name: str, fluids: List[str], var_states: List[VarState], ranged_vars: List[Variable],
             desc: str = ""):
        self.name = name
        self.fluids = fluids
        self.desc = desc
        self.var_states: List[VarState] = var_states
        self.ranged_vars: List[Variable] = ranged_vars

    def getLastID(self) -> int:
        ids: List[int] = [vs.uid for vs in self.var_states + self.ranged_vars]
        if ids:
            return max(ids)
        else:
            return 0


class FlowJsonEncoder(JSONEncoder):
    def __init__(self):
        super().__init__(ensure_ascii=False)
        self.ref_obj: List[VarState] = []

    def default(self, o: Any) -> Any:
        if isinstance(o, JsonInitiable):
            if isinstance(o, VarState):
                if o in self.ref_obj:
                    return {JI.TYPE_KEY: JI.TYPE_REF,
                            "uid": o.uid}
                else:
                    self.ref_obj.append(o)
                    return o.getInitDict()
            return o.getInitDict()

        elif issubclass(o, BaseProperty):
            return {JI.TYPE_KEY: BaseProperty.__name__,
                    JI.BP_KEY: o.__name__}
        else:
            return super().default(o=o)


class FlowJsonDecoder(JSONDecoder):
    def __init__(self, build: int):
        super().__init__(object_hook=self.object_hook, strict=False)
        self.ji_classes: Dict[str, Type[JsonInitiable]] = {cls.__name__: cls for cls in get_subClasses(JsonInitiable)}
        self.ref: Dict[int, VarState] = {}
        self.build = build

    def object_hook(self, json_obj: Dict) -> Any:
        if JI.TYPE_KEY not in json_obj:
            return json_obj
        type_str: str = json_obj[JI.TYPE_KEY]
        del json_obj[JI.TYPE_KEY]
        if type_str in self.ji_classes.keys():
            cls: Type = self.ji_classes[type_str]
            cls: Type[Union[MetaFlow, Flow, VarState, Value]]
            obj = cls(**json_obj)
            if isinstance(obj, MetaFlow):
                if obj.build != self.build:
                    age: str = "newer" if obj.build > self.build else "older"
                    raise Exception("Failed to read file. The file was created with " + age + " build of ThermoState")
            if isinstance(obj, VarState):
                self.ref[obj.uid] = obj
            return obj
        elif type_str == BaseProperty.__name__:
            cls_name: str = json_obj[JI.BP_KEY]
            for cls in list_props_for_var:
                if cls_name == cls.__name__:
                    return cls
        elif type_str == JI.TYPE_REF:
            return self.ref[json_obj["uid"]]
        else:
            return json_obj


def flowImporter(json_str: str, build: int) -> Flow:
    error_str: str = "Not Valid File, Code: {}"
    try:
        flow_ls: List = FlowJsonDecoder(build=build).decode(json_str)
    except:
        raise Exception(error_str.format(0))
    if type(flow_ls) != list:
        raise Exception(error_str.format(1))
    elif len(flow_ls) == 0:
        raise Exception(error_str.format(2))
    elif not isinstance(flow_ls.pop(0), MetaFlow):
        raise Exception(error_str.format(3))
    for flow in flow_ls:
        if not isinstance(flow, Flow):
            raise Exception(error_str.format(4))
        return flow


def flowExporter(flow: Flow, build: int) -> str:
    flowPack: List = [MetaFlow(build=build), flow]
    return FlowJsonEncoder().encode(flowPack)
