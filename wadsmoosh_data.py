# data tables for WadSmoosh
# every line in this file must be valid Python!

# pre-authored resources to copy
RES_FILES = [
    'mapinfo.txt', 'language.txt', 'endoom', 'smooshed.txt',
    'textures.common', 'textures.doom1', 'textures.doom2',
    'textures.tnt', 'textures.plut', 'animdefs.txt',
    'graphics/M_DOOM.png', 'graphics/TITLEPIC.png',
    'graphics/M_HELL.png', 'graphics/M_NOREST.png',
    'graphics/M_MASTER.png', 'graphics/M_TNT.png',
    'graphics/M_PLUT.png',
    'mapinfo/doom1_levels.txt', 'mapinfo/doom2_levels.txt',
    'mapinfo/masterlevels.txt', 'mapinfo/tnt_levels.txt',
    'mapinfo/plutonia_levels.txt'
]

IWADS = ['doom', 'doom2', 'tnt', 'plutonia', 'nerve']

# lists of lumps common to doom 1+2
COMMON_LUMPS = [
    'data_common', 'flats_common', 'graphics_common', 'patches_common',
    'sounds_common', 'sprites_common'
]

DOOM1_LUMPS = [
    'graphics_doom1', 'music_doom1', 'patches_doom1', 'sounds_doom1'
]

DOOM2_LUMPS = [
    'flats_doom2', 'graphics_doom2', 'music_doom2', 'patches_doom2',
    'sounds_doom2', 'sprites_doom2'
]

# lists of lumps to extract from each IWAD
WAD_LUMP_LISTS = {
    'doom': COMMON_LUMPS + DOOM1_LUMPS,
    'doom2': COMMON_LUMPS + DOOM2_LUMPS,
    'tnt': ['graphics_tnt', 'music_tnt', 'patches_tnt'],
    'plutonia': ['graphics_plutonia', 'music_plutonia', 'patches_plutonia']
}

# prefixes for filenames of maps extracted from IWADs
WAD_MAP_PREFIXES = {
    'doom': '',
    'doom2': '',
    'tnt': 'tn_',
    'plutonia': 'pl_',
    'nerve': 'nv_',
    # master levels not processed like other wads, bespoke prefix lookup
    'masterlevels': 'ml_'
}

# replacements for final doom textures that conflict with doom2 textures
TEXTURE_REPLACEMENTS = {
    'tnt': {
        'SW1GSTON': 'SW1GSTNT',
        'SW2GSTON': 'SW2GSTNT',
        'SKY1': 'TNT_SKY1',
        'SW1BRN1': 'SW1BRN1T',
        'SW2BRN1': 'SW2BRN1T',
        'SW1SKULL': 'SW1SKULT',
        'SW2SKULL': 'SW2SKULT',
        'SLADRIP1': 'SLADRPT1',
        'SLADRIP3': 'SLADRPT3',
        'BLODGR1': 'BLODGRT1',
        'BLODGR4': 'BLODGRT4'
    },
    'plutonia': {
        'DBRAIN1': 'PBRAIN1',
        'DBRAIN4': 'PBRAIN4',
        'FIREBLU1': 'FIREPLU1',
        'FIREBLU2': 'FIREPLU2',
        'SW1SKULL': 'SW1SKULP',
        'SW2SKULL': 'SW2SKULP',
        'SKY3': 'PSKY3',
        'SW1BRN1': 'SW1BRN1T',
        'SW2BRN1': 'SW2BRN1T',
        'WFALL1': 'PWFALL1',
        'WFALL2': 'PWFALL2',
        'WFALL3': 'PWFALL3',
        'WFALL4': 'PWFALL4'
    }
}

MASTER_LEVELS_MAP_ORDER = [
    'attack', 'canyon', 'catwalk', 'combine', 'fistula', 'garrison', 'manor',
    'paradox', 'subspace', 'subterra', 'ttrap', 'virgil', 'minos', 'bloodsea',
    'mephisto', 'nessus', 'geryon', 'vesperas', 'blacktwr', 'teeth'
]

# texture patches to extract from specific master levels PWADs
MASTER_LEVELS_PATCHES = {
    'combine': ('RSKY1', 'ML_SKY1'),
    'manor': ('STARS', 'ML_SKY2'),
    'virgil': ('RSKY1', 'ML_SKY3')
}
