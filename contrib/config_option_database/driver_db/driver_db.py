from __future__ import annotations

from typing import Dict, KeysView, ValuesView

from .driver import Driver


class DriverDB:
    def __init__(self) -> None:
        self.__drivers: Dict[str, Dict[str, Driver]] = dict()

    @property
    def contexts(self) -> KeysView[str]:
        return self.__drivers.keys()

    def add_driver(self, driver: Driver) -> DriverDB:
        context = self.__drivers.setdefault(driver.context, {})

        if driver.name in context.keys():
            context[driver.name].merge(driver)
        else:
            context[driver.name] = driver.copy()

        return self

    def get_driver(self, context: str, driver_name: str) -> Driver:
        return self.__drivers[context][driver_name]

    def get_drivers_in_context(self, context: str) -> ValuesView[Driver]:
        return self.__drivers[context].values()

    def merge(self, other: DriverDB) -> DriverDB:
        for context in other.contexts:
            for driver in other.get_drivers_in_context(context):
                self.add_driver(driver)

        return self

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DriverDB):
            return False

        return self.__drivers == other.__drivers

    def __repr__(self) -> str:
        return "DriverDB({})".format(repr(self.__drivers))
