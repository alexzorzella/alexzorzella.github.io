from typing import Any


def create_element(tag_name: str, attributes: dict[str, str | None], children: list[str] | None = None,
                   self_closing: bool = False) -> str:
    if self_closing:
        assert children is None, "Self closing tags must not have children"

    if children is None:
        child_str = ""
    else:
        child_str = "\n".join(children)

    attribute_str = ""

    for attribute, value in attributes.items():
        if value is not None:
            attribute_str += f'{attribute}="{value}" '

    tag_str = f'<{tag_name} {attribute_str}>{child_str}'

    if not self_closing:
        tag_str += f'</{tag_name}>'

    return tag_str

def create_html_dropdown(name: str, id: str, options: list[tuple[Any, Any]]):
    return create_element(
        "select",
        { "name": name, "id": id },
        [
            create_element("option", { "value": str(option[0]) }, [ option[1] ]) for option in options
        ]
    )