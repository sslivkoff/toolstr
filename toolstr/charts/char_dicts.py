"""see https://en.wikipedia.org/wiki/Box-drawing_character"""
from __future__ import annotations

from .. import spec


whole_dict: spec.GridCharDict = {
    ((0,),): ' ',
    ((1,),): '█',
}


quadrants_dict: spec.GridCharDict = {
    #
    # no block
    ((0, 0), (0, 0)): ' ',
    #
    # single block
    ((1, 0), (0, 0)): '▘',
    ((0, 1), (0, 0)): '▝',
    ((0, 0), (1, 0)): '▖',
    ((0, 0), (0, 1)): '▗',
    #
    # double block
    ((1, 1), (0, 0)): '▀',
    ((0, 0), (1, 1)): '▄',
    ((1, 0), (0, 1)): '▚',
    ((0, 1), (1, 0)): '▞',
    ((1, 0), (1, 0)): '▌',
    ((0, 1), (0, 1)): '▐',
    #
    # triple block
    ((0, 1), (1, 1)): '▟',
    ((1, 0), (1, 1)): '▙',
    ((1, 1), (0, 1)): '▜',
    ((1, 1), (1, 0)): '▛',
    #
    # quadruple block
    ((1, 1), (1, 1)): '█',
}

height_split_dict: spec.GridCharDict = {
    ((0,), (0,), (0,), (0,), (0,), (0,), (0,), (0,)): ' ',
    ((0,), (0,), (0,), (0,), (0,), (0,), (0,), (1,)): '▁',
    ((0,), (0,), (0,), (0,), (0,), (0,), (1,), (1,)): '▂',
    ((0,), (0,), (0,), (0,), (0,), (1,), (1,), (1,)): '▃',
    ((0,), (0,), (0,), (0,), (1,), (1,), (1,), (1,)): '▄',
    ((0,), (0,), (0,), (1,), (1,), (1,), (1,), (1,)): '▅',
    ((0,), (0,), (1,), (1,), (1,), (1,), (1,), (1,)): '▆',
    ((0,), (1,), (1,), (1,), (1,), (1,), (1,), (1,)): '▇',
    ((1,), (1,), (1,), (1,), (1,), (1,), (1,), (1,)): '█',
}

width_split_dict: spec.GridCharDict = {
    ((0, 0, 0, 0, 0, 0, 0, 0),): ' ',
    ((0, 0, 0, 0, 0, 0, 0, 1),): '▏',
    ((0, 0, 0, 0, 0, 0, 1, 1),): '▎',
    ((0, 0, 0, 0, 0, 1, 1, 1),): '▍',
    ((0, 0, 0, 0, 1, 1, 1, 1),): '▌',
    ((0, 0, 0, 1, 1, 1, 1, 1),): '▋',
    ((0, 0, 1, 1, 1, 1, 1, 1),): '▊',
    ((0, 1, 1, 1, 1, 1, 1, 1),): '▉',
    ((1, 1, 1, 1, 1, 1, 1, 1),): '█',
}


def get_char_dict(name: spec.SampleMode) -> spec.GridCharDict:
    if name == 'braille':
        from . import braille_utils

        return braille_utils.braille_dict
    elif name == 'sextants':
        from . import sextant_utils

        return sextant_utils.sextants_dict
    elif name is None or name == 'whole':
        return whole_dict
    else:
        small_char_dicts: dict[str, spec.GridCharDict] = {
            'quadrants': quadrants_dict,
            'width_split': width_split_dict,
            'height_split': height_split_dict,
        }

        return small_char_dicts[name]
