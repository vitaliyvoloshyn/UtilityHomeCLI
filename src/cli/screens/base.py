from loguru import logger

from ..context import AppContext
from .components import BaseComponent


class Screen:
    def __init__(self):
        self.context = None
        self.components: list = []

    def _set_context(self, context: AppContext):
        self.context = context

    def add(self, component: BaseComponent):
        if not isinstance(component, BaseComponent):
            raise TypeError("Компонент не являється нащадком BaseComponent")
        self.components.append(component)

    def show(self) -> dict:
        out_dict: dict = {}
        for c in self.components:
            res = c.render()
            if res:
                out_dict.update(res)
        logger.debug(out_dict)
        return out_dict
