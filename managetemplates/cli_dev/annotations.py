from typing import Annotated, Literal

import tyro

from managetemplates import constants


TyroOptionalTemplateNameArgType = Annotated[
    Literal[*constants.ALL_TEMPLATES] | None,
    tyro.conf.arg(
        default=None,
        help='Select the project template by name. Leave empty to select all templates.',
    ),
]
