from typing import Type, List, Dict

from Model.CoolPropInterface import get_property_objects
from .BaseProperty import BaseProperty


class PureState:
    def __init__(self, fluid: str, input_a: BaseProperty, input_b: BaseProperty, no: int = 0):
        self.no = no
        self.fluid: str = fluid

        self.state_properties: List[BaseProperty] = []
        self.other_properties: List[BaseProperty] = []

        self.state_properties, self.other_properties = get_property_objects(fluid, input_a, input_b)

        self.properties: Dict[str, BaseProperty] = \
            {prop.kw: prop for prop in self.state_properties + self.other_properties}

    def get_state_properties(self) -> List[BaseProperty]:
        return self.state_properties

    def get_other_properties(self) -> List[BaseProperty]:
        return self.other_properties

    def get_state_property(self, index: int):
        return self.state_properties[index]

    def get_state_property_count(self) -> int:
        return len(self.state_properties)

    def get_property(self, class_property: Type[BaseProperty]):
        return self.properties[class_property.kw]


class StateNoManager:
    def __init__(self, states: Dict[str, List[PureState]]):
        self.states = states
        self.count: Dict[str, int] = {}
        self.refresh()

    def get_no(self, fluid: str) -> int:
        return self.count[fluid]

    def increment(self, fluid: str):
        self.count[fluid] = self.count.get(fluid, 0) + 1

    def resetOrder(self, fluid: str):
        for i, state in enumerate(self.states[fluid]):
            state.no = i + 1
        self.count[fluid] = len(self.states[fluid]) + 1

    def refresh(self):
        self.count = {}
        for k, v in self.states.items():
            if v:
                max_no = max([s.no for s in v])
            else:
                max_no = 0

            self.count[k] = max_no + 1

    def fluidChanged(self):
        states_keys = self.states.keys()
        count_keys = tuple(self.count.keys())

        for key in count_keys:
            if key not in states_keys:
                del self.count[key]

        for key in states_keys:
            if key not in count_keys:
                self.count[key] = 1

    def refreshFluid(self, fluid: str):
        state_list = self.states[fluid]
        if state_list:
            max_no = max([s.no for s in state_list])
        else:
            max_no = 0
        self.count[fluid] = max_no + 1
