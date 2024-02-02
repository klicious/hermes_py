from dataclasses import dataclass, field

from jinja2 import Template as JTemplate

from .type import Type


@dataclass
class Template:
    entity: str
    type: Type
    header: str
    body: str
    tail: str
    _header: JTemplate = field(init=False)
    _body: JTemplate = field(init=False)
    _tail: JTemplate = field(init=False)

    def __post_init__(self):
        self._header = JTemplate(self.header)
        self._body = JTemplate(self.body)
        if self.tail:
            self._tail = JTemplate(self.tail)

    def render_header(self, **kwargs):
        return self._header.render(**kwargs)

    def render_body(self, **kwargs):
        return self._body.render(**kwargs)

    def render_tail(self, **kwargs):
        if not self.tail:
            return ""
        return self._tail.render(**kwargs)

    def is_empty(self) -> bool:
        return not self.body
