# braille characters have different width than most characters
from . import raster_utils
from . import render_utils


braille_dict = {
    ((0, 0), (0, 0), (0, 0), (0, 0)): '⠀',
    ((1, 0), (0, 0), (0, 0), (0, 0)): '⠁',
    ((1, 0), (1, 0), (0, 0), (0, 0)): '⠃',
    ((1, 0), (1, 0), (1, 0), (0, 0)): '⠇',
    ((1, 1), (1, 0), (1, 0), (0, 0)): '⠏',
    ((1, 1), (1, 1), (1, 0), (0, 0)): '⠟',
    ((1, 1), (1, 1), (1, 1), (0, 0)): '⠿',
    ((1, 1), (1, 1), (1, 1), (1, 0)): '⡿',
    ((1, 1), (1, 1), (1, 1), (1, 1)): '⣿',
    ((1, 1), (1, 1), (1, 1), (0, 1)): '⢿',
    ((1, 1), (1, 1), (1, 0), (1, 0)): '⡟',
    ((1, 1), (1, 1), (1, 0), (1, 1)): '⣟',
    ((1, 1), (1, 1), (1, 0), (0, 1)): '⢟',
    ((1, 1), (1, 0), (1, 1), (0, 0)): '⠯',
    ((1, 1), (1, 0), (1, 1), (1, 0)): '⡯',
    ((1, 1), (1, 0), (1, 1), (1, 1)): '⣯',
    ((1, 1), (1, 0), (1, 1), (0, 1)): '⢯',
    ((1, 1), (1, 0), (1, 0), (1, 0)): '⡏',
    ((1, 1), (1, 0), (1, 0), (1, 1)): '⣏',
    ((1, 1), (1, 0), (1, 0), (0, 1)): '⢏',
    ((1, 0), (1, 1), (1, 0), (0, 0)): '⠗',
    ((1, 0), (1, 1), (1, 1), (0, 0)): '⠷',
    ((1, 0), (1, 1), (1, 1), (1, 0)): '⡷',
    ((1, 0), (1, 1), (1, 1), (1, 1)): '⣷',
    ((1, 0), (1, 1), (1, 1), (0, 1)): '⢷',
    ((1, 0), (1, 1), (1, 0), (1, 0)): '⡗',
    ((1, 0), (1, 1), (1, 0), (1, 1)): '⣗',
    ((1, 0), (1, 1), (1, 0), (0, 1)): '⢗',
    ((1, 0), (1, 0), (1, 1), (0, 0)): '⠧',
    ((1, 0), (1, 0), (1, 1), (1, 0)): '⡧',
    ((1, 0), (1, 0), (1, 1), (1, 1)): '⣧',
    ((1, 0), (1, 0), (1, 1), (0, 1)): '⢧',
    ((1, 0), (1, 0), (1, 0), (1, 0)): '⡇',
    ((1, 0), (1, 0), (1, 0), (1, 1)): '⣇',
    ((1, 0), (1, 0), (1, 0), (0, 1)): '⢇',
    ((1, 1), (1, 0), (0, 0), (0, 0)): '⠋',
    ((1, 1), (1, 1), (0, 0), (0, 0)): '⠛',
    ((1, 1), (1, 1), (0, 1), (0, 0)): '⠻',
    ((1, 1), (1, 1), (0, 1), (1, 0)): '⡻',
    ((1, 1), (1, 1), (0, 1), (1, 1)): '⣻',
    ((1, 1), (1, 1), (0, 1), (0, 1)): '⢻',
    ((1, 1), (1, 1), (0, 0), (1, 0)): '⡛',
    ((1, 1), (1, 1), (0, 0), (1, 1)): '⣛',
    ((1, 1), (1, 1), (0, 0), (0, 1)): '⢛',
    ((1, 1), (1, 0), (0, 1), (0, 0)): '⠫',
    ((1, 1), (1, 0), (0, 1), (1, 0)): '⡫',
    ((1, 1), (1, 0), (0, 1), (1, 1)): '⣫',
    ((1, 1), (1, 0), (0, 1), (0, 1)): '⢫',
    ((1, 1), (1, 0), (0, 0), (1, 0)): '⡋',
    ((1, 1), (1, 0), (0, 0), (1, 1)): '⣋',
    ((1, 1), (1, 0), (0, 0), (0, 1)): '⢋',
    ((1, 0), (1, 1), (0, 0), (0, 0)): '⠓',
    ((1, 0), (1, 1), (0, 1), (0, 0)): '⠳',
    ((1, 0), (1, 1), (0, 1), (1, 0)): '⡳',
    ((1, 0), (1, 1), (0, 1), (1, 1)): '⣳',
    ((1, 0), (1, 1), (0, 1), (0, 1)): '⢳',
    ((1, 0), (1, 1), (0, 0), (1, 0)): '⡓',
    ((1, 0), (1, 1), (0, 0), (1, 1)): '⣓',
    ((1, 0), (1, 1), (0, 0), (0, 1)): '⢓',
    ((1, 0), (1, 0), (0, 1), (0, 0)): '⠣',
    ((1, 0), (1, 0), (0, 1), (1, 0)): '⡣',
    ((1, 0), (1, 0), (0, 1), (1, 1)): '⣣',
    ((1, 0), (1, 0), (0, 1), (0, 1)): '⢣',
    ((1, 0), (1, 0), (0, 0), (1, 0)): '⡃',
    ((1, 0), (1, 0), (0, 0), (1, 1)): '⣃',
    ((1, 0), (1, 0), (0, 0), (0, 1)): '⢃',
    ((1, 0), (0, 0), (1, 0), (0, 0)): '⠅',
    ((1, 1), (0, 0), (1, 0), (0, 0)): '⠍',
    ((1, 1), (0, 1), (1, 0), (0, 0)): '⠝',
    ((1, 1), (0, 1), (1, 1), (0, 0)): '⠽',
    ((1, 1), (0, 1), (1, 1), (1, 0)): '⡽',
    ((1, 1), (0, 1), (1, 1), (1, 1)): '⣽',
    ((1, 1), (0, 1), (1, 1), (0, 1)): '⢽',
    ((1, 1), (0, 1), (1, 0), (1, 0)): '⡝',
    ((1, 1), (0, 1), (1, 0), (1, 1)): '⣝',
    ((1, 1), (0, 1), (1, 0), (0, 1)): '⢝',
    ((1, 1), (0, 0), (1, 1), (0, 0)): '⠭',
    ((1, 1), (0, 0), (1, 1), (1, 0)): '⡭',
    ((1, 1), (0, 0), (1, 1), (1, 1)): '⣭',
    ((1, 1), (0, 0), (1, 1), (0, 1)): '⢭',
    ((1, 1), (0, 0), (1, 0), (1, 0)): '⡍',
    ((1, 1), (0, 0), (1, 0), (1, 1)): '⣍',
    ((1, 1), (0, 0), (1, 0), (0, 1)): '⢍',
    ((1, 0), (0, 1), (1, 0), (0, 0)): '⠕',
    ((1, 0), (0, 1), (1, 1), (0, 0)): '⠵',
    ((1, 0), (0, 1), (1, 1), (1, 0)): '⡵',
    ((1, 0), (0, 1), (1, 1), (1, 1)): '⣵',
    ((1, 0), (0, 1), (1, 1), (0, 1)): '⢵',
    ((1, 0), (0, 1), (1, 0), (1, 0)): '⡕',
    ((1, 0), (0, 1), (1, 0), (1, 1)): '⣕',
    ((1, 0), (0, 1), (1, 0), (0, 1)): '⢕',
    ((1, 0), (0, 0), (1, 1), (0, 0)): '⠥',
    ((1, 0), (0, 0), (1, 1), (1, 0)): '⡥',
    ((1, 0), (0, 0), (1, 1), (1, 1)): '⣥',
    ((1, 0), (0, 0), (1, 1), (0, 1)): '⢥',
    ((1, 0), (0, 0), (1, 0), (1, 0)): '⡅',
    ((1, 0), (0, 0), (1, 0), (1, 1)): '⣅',
    ((1, 0), (0, 0), (1, 0), (0, 1)): '⢅',
    ((1, 1), (0, 0), (0, 0), (0, 0)): '⠉',
    ((1, 1), (0, 1), (0, 0), (0, 0)): '⠙',
    ((1, 1), (0, 1), (0, 1), (0, 0)): '⠹',
    ((1, 1), (0, 1), (0, 1), (1, 0)): '⡹',
    ((1, 1), (0, 1), (0, 1), (1, 1)): '⣹',
    ((1, 1), (0, 1), (0, 1), (0, 1)): '⢹',
    ((1, 1), (0, 1), (0, 0), (1, 0)): '⡙',
    ((1, 1), (0, 1), (0, 0), (1, 1)): '⣙',
    ((1, 1), (0, 1), (0, 0), (0, 1)): '⢙',
    ((1, 1), (0, 0), (0, 1), (0, 0)): '⠩',
    ((1, 1), (0, 0), (0, 1), (1, 0)): '⡩',
    ((1, 1), (0, 0), (0, 1), (1, 1)): '⣩',
    ((1, 1), (0, 0), (0, 1), (0, 1)): '⢩',
    ((1, 1), (0, 0), (0, 0), (1, 0)): '⡉',
    ((1, 1), (0, 0), (0, 0), (1, 1)): '⣉',
    ((1, 1), (0, 0), (0, 0), (0, 1)): '⢉',
    ((1, 0), (0, 1), (0, 0), (0, 0)): '⠑',
    ((1, 0), (0, 1), (0, 1), (0, 0)): '⠱',
    ((1, 0), (0, 1), (0, 1), (1, 0)): '⡱',
    ((1, 0), (0, 1), (0, 1), (1, 1)): '⣱',
    ((1, 0), (0, 1), (0, 1), (0, 1)): '⢱',
    ((1, 0), (0, 1), (0, 0), (1, 0)): '⡑',
    ((1, 0), (0, 1), (0, 0), (1, 1)): '⣑',
    ((1, 0), (0, 1), (0, 0), (0, 1)): '⢑',
    ((1, 0), (0, 0), (0, 1), (0, 0)): '⠡',
    ((1, 0), (0, 0), (0, 1), (1, 0)): '⡡',
    ((1, 0), (0, 0), (0, 1), (1, 1)): '⣡',
    ((1, 0), (0, 0), (0, 1), (0, 1)): '⢡',
    ((1, 0), (0, 0), (0, 0), (1, 0)): '⡁',
    ((1, 0), (0, 0), (0, 0), (1, 1)): '⣁',
    ((1, 0), (0, 0), (0, 0), (0, 1)): '⢁',
    ((0, 0), (1, 0), (0, 0), (0, 0)): '⠂',
    ((0, 0), (1, 0), (1, 0), (0, 0)): '⠆',
    ((0, 1), (1, 0), (1, 0), (0, 0)): '⠎',
    ((0, 1), (1, 1), (1, 0), (0, 0)): '⠞',
    ((0, 1), (1, 1), (1, 1), (0, 0)): '⠾',
    ((0, 1), (1, 1), (1, 1), (1, 0)): '⡾',
    ((0, 1), (1, 1), (1, 1), (1, 1)): '⣾',
    ((0, 1), (1, 1), (1, 1), (0, 1)): '⢾',
    ((0, 1), (1, 1), (1, 0), (1, 0)): '⡞',
    ((0, 1), (1, 1), (1, 0), (1, 1)): '⣞',
    ((0, 1), (1, 1), (1, 0), (0, 1)): '⢞',
    ((0, 1), (1, 0), (1, 1), (0, 0)): '⠮',
    ((0, 1), (1, 0), (1, 1), (1, 0)): '⡮',
    ((0, 1), (1, 0), (1, 1), (1, 1)): '⣮',
    ((0, 1), (1, 0), (1, 1), (0, 1)): '⢮',
    ((0, 1), (1, 0), (1, 0), (1, 0)): '⡎',
    ((0, 1), (1, 0), (1, 0), (1, 1)): '⣎',
    ((0, 1), (1, 0), (1, 0), (0, 1)): '⢎',
    ((0, 0), (1, 1), (1, 0), (0, 0)): '⠖',
    ((0, 0), (1, 1), (1, 1), (0, 0)): '⠶',
    ((0, 0), (1, 1), (1, 1), (1, 0)): '⡶',
    ((0, 0), (1, 1), (1, 1), (1, 1)): '⣶',
    ((0, 0), (1, 1), (1, 1), (0, 1)): '⢶',
    ((0, 0), (1, 1), (1, 0), (1, 0)): '⡖',
    ((0, 0), (1, 1), (1, 0), (1, 1)): '⣖',
    ((0, 0), (1, 1), (1, 0), (0, 1)): '⢖',
    ((0, 0), (1, 0), (1, 1), (0, 0)): '⠦',
    ((0, 0), (1, 0), (1, 1), (1, 0)): '⡦',
    ((0, 0), (1, 0), (1, 1), (1, 1)): '⣦',
    ((0, 0), (1, 0), (1, 1), (0, 1)): '⢦',
    ((0, 0), (1, 0), (1, 0), (1, 0)): '⡆',
    ((0, 0), (1, 0), (1, 0), (1, 1)): '⣆',
    ((0, 0), (1, 0), (1, 0), (0, 1)): '⢆',
    ((0, 1), (1, 0), (0, 0), (0, 0)): '⠊',
    ((0, 1), (1, 1), (0, 0), (0, 0)): '⠚',
    ((0, 1), (1, 1), (0, 1), (0, 0)): '⠺',
    ((0, 1), (1, 1), (0, 1), (1, 0)): '⡺',
    ((0, 1), (1, 1), (0, 1), (1, 1)): '⣺',
    ((0, 1), (1, 1), (0, 1), (0, 1)): '⢺',
    ((0, 1), (1, 1), (0, 0), (1, 0)): '⡚',
    ((0, 1), (1, 1), (0, 0), (1, 1)): '⣚',
    ((0, 1), (1, 1), (0, 0), (0, 1)): '⢚',
    ((0, 1), (1, 0), (0, 1), (0, 0)): '⠪',
    ((0, 1), (1, 0), (0, 1), (1, 0)): '⡪',
    ((0, 1), (1, 0), (0, 1), (1, 1)): '⣪',
    ((0, 1), (1, 0), (0, 1), (0, 1)): '⢪',
    ((0, 1), (1, 0), (0, 0), (1, 0)): '⡊',
    ((0, 1), (1, 0), (0, 0), (1, 1)): '⣊',
    ((0, 1), (1, 0), (0, 0), (0, 1)): '⢊',
    ((0, 0), (1, 1), (0, 0), (0, 0)): '⠒',
    ((0, 0), (1, 1), (0, 1), (0, 0)): '⠲',
    ((0, 0), (1, 1), (0, 1), (1, 0)): '⡲',
    ((0, 0), (1, 1), (0, 1), (1, 1)): '⣲',
    ((0, 0), (1, 1), (0, 1), (0, 1)): '⢲',
    ((0, 0), (1, 1), (0, 0), (1, 0)): '⡒',
    ((0, 0), (1, 1), (0, 0), (1, 1)): '⣒',
    ((0, 0), (1, 1), (0, 0), (0, 1)): '⢒',
    ((0, 0), (1, 0), (0, 1), (0, 0)): '⠢',
    ((0, 0), (1, 0), (0, 1), (1, 0)): '⡢',
    ((0, 0), (1, 0), (0, 1), (1, 1)): '⣢',
    ((0, 0), (1, 0), (0, 1), (0, 1)): '⢢',
    ((0, 0), (1, 0), (0, 0), (1, 0)): '⡂',
    ((0, 0), (1, 0), (0, 0), (1, 1)): '⣂',
    ((0, 0), (1, 0), (0, 0), (0, 1)): '⢂',
    ((0, 0), (0, 0), (1, 0), (0, 0)): '⠄',
    ((0, 1), (0, 0), (1, 0), (0, 0)): '⠌',
    ((0, 1), (0, 1), (1, 0), (0, 0)): '⠜',
    ((0, 1), (0, 1), (1, 1), (0, 0)): '⠼',
    ((0, 1), (0, 1), (1, 1), (1, 0)): '⡼',
    ((0, 1), (0, 1), (1, 1), (1, 1)): '⣼',
    ((0, 1), (0, 1), (1, 1), (0, 1)): '⢼',
    ((0, 1), (0, 1), (1, 0), (1, 0)): '⡜',
    ((0, 1), (0, 1), (1, 0), (1, 1)): '⣜',
    ((0, 1), (0, 1), (1, 0), (0, 1)): '⢜',
    ((0, 1), (0, 0), (1, 1), (0, 0)): '⠬',
    ((0, 1), (0, 0), (1, 1), (1, 0)): '⡬',
    ((0, 1), (0, 0), (1, 1), (1, 1)): '⣬',
    ((0, 1), (0, 0), (1, 1), (0, 1)): '⢬',
    ((0, 1), (0, 0), (1, 0), (1, 0)): '⡌',
    ((0, 1), (0, 0), (1, 0), (1, 1)): '⣌',
    ((0, 1), (0, 0), (1, 0), (0, 1)): '⢌',
    ((0, 0), (0, 1), (1, 0), (0, 0)): '⠔',
    ((0, 0), (0, 1), (1, 1), (0, 0)): '⠴',
    ((0, 0), (0, 1), (1, 1), (1, 0)): '⡴',
    ((0, 0), (0, 1), (1, 1), (1, 1)): '⣴',
    ((0, 0), (0, 1), (1, 1), (0, 1)): '⢴',
    ((0, 0), (0, 1), (1, 0), (1, 0)): '⡔',
    ((0, 0), (0, 1), (1, 0), (1, 1)): '⣔',
    ((0, 0), (0, 1), (1, 0), (0, 1)): '⢔',
    ((0, 0), (0, 0), (1, 1), (0, 0)): '⠤',
    ((0, 0), (0, 0), (1, 1), (1, 0)): '⡤',
    ((0, 0), (0, 0), (1, 1), (1, 1)): '⣤',
    ((0, 0), (0, 0), (1, 1), (0, 1)): '⢤',
    ((0, 0), (0, 0), (1, 0), (1, 0)): '⡄',
    ((0, 0), (0, 0), (1, 0), (1, 1)): '⣄',
    ((0, 0), (0, 0), (1, 0), (0, 1)): '⢄',
    ((0, 1), (0, 0), (0, 0), (0, 0)): '⠈',
    ((0, 1), (0, 1), (0, 0), (0, 0)): '⠘',
    ((0, 1), (0, 1), (0, 1), (0, 0)): '⠸',
    ((0, 1), (0, 1), (0, 1), (1, 0)): '⡸',
    ((0, 1), (0, 1), (0, 1), (1, 1)): '⣸',
    ((0, 1), (0, 1), (0, 1), (0, 1)): '⢸',
    ((0, 1), (0, 1), (0, 0), (1, 0)): '⡘',
    ((0, 1), (0, 1), (0, 0), (1, 1)): '⣘',
    ((0, 1), (0, 1), (0, 0), (0, 1)): '⢘',
    ((0, 1), (0, 0), (0, 1), (0, 0)): '⠨',
    ((0, 1), (0, 0), (0, 1), (1, 0)): '⡨',
    ((0, 1), (0, 0), (0, 1), (1, 1)): '⣨',
    ((0, 1), (0, 0), (0, 1), (0, 1)): '⢨',
    ((0, 1), (0, 0), (0, 0), (1, 0)): '⡈',
    ((0, 1), (0, 0), (0, 0), (1, 1)): '⣈',
    ((0, 1), (0, 0), (0, 0), (0, 1)): '⢈',
    ((0, 0), (0, 1), (0, 0), (0, 0)): '⠐',
    ((0, 0), (0, 1), (0, 1), (0, 0)): '⠰',
    ((0, 0), (0, 1), (0, 1), (1, 0)): '⡰',
    ((0, 0), (0, 1), (0, 1), (1, 1)): '⣰',
    ((0, 0), (0, 1), (0, 1), (0, 1)): '⢰',
    ((0, 0), (0, 1), (0, 0), (1, 0)): '⡐',
    ((0, 0), (0, 1), (0, 0), (1, 1)): '⣐',
    ((0, 0), (0, 1), (0, 0), (0, 1)): '⢐',
    ((0, 0), (0, 0), (0, 1), (0, 0)): '⠠',
    ((0, 0), (0, 0), (0, 1), (1, 0)): '⡠',
    ((0, 0), (0, 0), (0, 1), (1, 1)): '⣠',
    ((0, 0), (0, 0), (0, 1), (0, 1)): '⢠',
    ((0, 0), (0, 0), (0, 0), (1, 0)): '⡀',
    ((0, 0), (0, 0), (0, 0), (1, 1)): '⣀',
    ((0, 0), (0, 0), (0, 0), (0, 1)): '⢀',
}


def create_braille_sparkline(data, width):
    import numpy as np

    indices = np.linspace(0, len(data) - 1, 2 * width, dtype=int)
    samples = [data[index] for index in indices]
    samples = np.array(samples)

    ymin = samples.min()
    ymax = samples.max()
    dy = ymax - ymin

    grid = {
        'n_rows': 4,
        'n_columns': 2 * width,
        'xmin': 0,
        'xmax': 2 * width,
        'ymin': ymin - 0.1 * dy,
        'ymax': ymax + 0.1 * dy,
    }
    raster = raster_utils.rasterize_by_lines(yvals=samples, grid=grid)

    return render_utils.render_supergrid(
        raster,
        rows_per_cell=4,
        columns_per_cell=2,
        char_dict=braille_dict,
    )

