from typing import Annotated, Literal

import tyro

from managetemplates import constants


TyroOptionalTemplateNameArgType = Annotated[
    Literal[*constants.ALL_PACKAGES] | None,
    tyro.conf.arg(
        default=None,
        help='Select the project template by name.',
    ),
]
