from loguru import logger

from ..cli.context import AppContext
from .schema import ComponentDTO
from .screen_components import BaseComponent


class BaseScreen:
    def __init__(self, context: AppContext) -> None:
        self.context = context
        self.components: list = []

    def _set_context(self, context: AppContext):
        self.context = context

    def add(self, component: BaseComponent):
        if not isinstance(component, BaseComponent):
            raise TypeError("Компонент не являється нащадком BaseComponent")
        self.components.append(component)

    def show(self) -> ComponentDTO:
        out_dict: dict = {}
        for c in self.components:
            res = c.render()
            if res:
                for k, v in res.items():
                    if (
                        k in out_dict
                        and isinstance(out_dict[k], dict)
                        and isinstance(v, dict)
                    ):
                        out_dict[k] = (
                            out_dict[k] | v
                        )  # Об'єднуємо два вкладені словники
                    else:
                        out_dict[k] = v
        dto = ComponentDTO.model_validate(out_dict)
        return dto
