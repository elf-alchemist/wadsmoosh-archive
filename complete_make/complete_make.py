
import os
import omg

"""
TODO:
- initial pre-pass that determines which WADs are available
- copy master levels to appropriate filenames + split teeth.wad
- parse & extract lists of lumps for each IWAD (lumpname : optional filename)
  - (how to distinguish between different kinds?)
- special cases:
  - apply tnt map31 fix
  - extract DPHOOF from doom.wad
- zip up pk3 (import zipfile module)
"""

SRC_WAD_DIR = 'source_wads/'
RES_DIR = 'res/'
MAPS_DIR = RES_DIR + 'maps/'
WAD_EXT = 'wad'

IWADS = ['doom', 'doom2', 'tnt', 'plutonia', 'nerve']

# prefixes for filenames of maps extracted from IWADs
WAD_MAP_PREFIXES = {
    'doom': '',
    'doom2': '',
    'tnt': 'tnt_',
    'plutonia': 'plut_',
    'nerve': 'nerve_'
}

# lists of lumps to extract from each IWAD
WAD_LUMP_LISTS = {
    'doom': 'doom1_lumps.txt',
    'doom2': 'doom2_lumps.txt',
    'tnt': 'tnt_lumps.txt',
    'plutonia': 'plutonia_lumps.txt'
}

CORE_LUMPS = [
    'playpal', 'colormap', 'endoom', 'genmidi', 'dmxgus'
]

MASTER_LEVELS_MAP_ORDER = [
    'attack', 'canyon', 'catwalk', 'combine', 'fistula', 'garrison', 'manor',
    'paradox', 'subspace', 'subterra', 'ttrap', 'virgil', 'minos', 'bloodsea',
    'mephisto', 'nessus', 'geryon', 'vesperas', 'blacktwr', 'teeth'
]

MASTER_LEVELS_MAP_PREFIX = 'ml_'

def get_iwad_path(base_name):
    return SRC_WAD_DIR + base_name + '.' + WAD_EXT

def extract_map(in_wad, map_name, out_filename):
    out_wad = omg.WAD()
    ed = omg.MapEditor(in_wad.maps[map_name])
    out_wad.maps[map_name] = ed.to_lumps()
    out_wad.to_file(out_filename)

def extract_iwad_maps(wad_name, map_prefix):
    in_wad_filename = get_iwad_path(wad_name)
    if not os.path.exists(in_wad_filename):
        print('IWAD %s not found' % in_wad_filename)
        return
    in_wad = omg.WAD()
    in_wad.from_file(in_wad_filename)
    for map_name in in_wad.maps.find('*'):
        print('  processing map %s...' % map_name)
        out_wad_filename = MAPS_DIR + map_prefix + map_name + '.' + WAD_EXT
        extract_map(in_wad, map_name, out_wad_filename)
        print('  saved map %s' % out_wad_filename)

for iwad_name in IWADS:
    print('processing IWAD %s...' % iwad_name)
    extract_iwad_maps(iwad_name, WAD_MAP_PREFIXES[iwad_name])

# i = omg.WAD()
# i.from_file('source_wads/doom.wad')
# i.data['PLAYPAL'].to_file('playpal')
# if image:
# i.data['SKY1'].to_Image().save()
