
import os
from shutil import copyfile
from zipfile import ZipFile

import omg

"""
TODO:
- texture error in tnt map20: "Unknown middle texture 'BLOD3' on first side of linedef 125"
- finish custom ENDOOM art
- test with various wads missing
"""

SRC_WAD_DIR = 'source_wads/'
DATA_DIR = 'data/'
DEST_DIR = 'pk3/'
DEST_FILENAME = 'complete.pk3'
RES_DIR = 'res/'
RES_FILES = [
    'mapinfo.txt', 'language.txt', 'endoom',
    'textures.txt', 'textures.tnt', 'textures.plut',
    'graphics/M_DOOM.png', 'graphics/TITLEPIC.png',
    'mapinfo/doom1_levels.txt', 'mapinfo/doom2_levels.txt',
    'mapinfo/masterlevels.txt', 'mapinfo/tnt_levels.txt',
    'mapinfo/plutonia_levels.txt'
]

IWADS = ['doom', 'doom2', 'tnt', 'plutonia', 'nerve']

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
    'tnt': 'tnt_',
    'plutonia': 'plut_',
    'nerve': 'nerve_'
}

MASTER_LEVELS_MAP_ORDER = [
    'attack', 'canyon', 'catwalk', 'combine', 'fistula', 'garrison', 'manor',
    'paradox', 'subspace', 'subterra', 'ttrap', 'virgil', 'minos', 'bloodsea',
    'mephisto', 'nessus', 'geryon', 'vesperas', 'blacktwr', 'teeth'
]

MASTER_LEVELS_MAP_PREFIX = 'ml_'

MASTER_LEVELS_PATCHES = {
    'combine': ('RSKY1', 'ML_SKY1'),
    'manor': ('STARS', 'ML_SKY2'),
    'virgil': ('RSKY1', 'ML_SKY3')
}

def get_wad_filename(wad_name):
    # return filename of first case-insensitive match
    wad_name += '.wad'
    for filename in os.listdir(SRC_WAD_DIR):
        if wad_name.lower() == filename.lower():
            return SRC_WAD_DIR + filename
    return None

def extract_master_levels():
    # check if present first
    first_ml_wad = get_wad_filename(MASTER_LEVELS_MAP_ORDER[0])
    if not first_ml_wad:
        print('Master Levels not found.')
        return
    print('Processing Master Levels...')
    for i,wad_name in enumerate(MASTER_LEVELS_MAP_ORDER):
        in_wad = omg.WAD()
        wad_filename = get_wad_filename(wad_name)
        in_wad.from_file(wad_filename)
        out_wad_filename = DEST_DIR + 'maps/' + MASTER_LEVELS_MAP_PREFIX + 'map'
        # extra zero for <10 map numbers, eg map01
        out_wad_filename += str(i + 1).rjust(2, '0') + '.wad'
        print('  Writing %s to %s' % (wad_filename, out_wad_filename))
        # grab first map we find in each wad
        map_name = in_wad.maps.find('*')[0]
        ed = omg.MapEditor(in_wad.maps[map_name])
        extract_map(in_wad, map_name, out_wad_filename)
    # save teeth map32 to map21 wad
    out_wad_filename = DEST_DIR + 'maps/' + MASTER_LEVELS_MAP_PREFIX + 'map21' + '.wad'
    print('  Writing %s map32 to %s' % (wad_filename, out_wad_filename))
    extract_map(in_wad, in_wad.maps.find('*')[1], out_wad_filename)
    # extract sky lumps
    for wad_name,patch_replace in MASTER_LEVELS_PATCHES.items():
        wad = omg.WAD()
        wad_filename = get_wad_filename(wad_name)
        wad.from_file(wad_filename)
        # manor stores sky in patches namespace, combine and virgil don't
        if patch_replace[0] in wad.data:
            lump = wad.data[patch_replace[0]]
        else:
            lump = wad.patches[patch_replace[0]]
        out_filename = DEST_DIR + 'patches/' + patch_replace[1] + '.lmp'
        print('  Writing %s lump from %s as %s' % (patch_replace[0],
                                                   wad_filename,
                                                   patch_replace[1]))
        lump.to_file(out_filename)

def tnt_map31_fix():
    print('Checking for TNT MAP31 fix...')
    wad = omg.WAD()
    wad_filename = DEST_DIR + 'maps/' + WAD_MAP_PREFIXES['tnt'] + 'MAP31.wad'
    wad.from_file(wad_filename)
    maped = omg.MapEditor(wad.maps['MAP31'])
    yellow_key = maped.things[470]
    if yellow_key.type != 6 or \
       (yellow_key.type == 6 and not yellow_key.get_multiplayer()):
        print('  TNT MAP31 already fixed.')
        return
    yellow_key.set_multiplayer(False)
    wad.maps['MAP31'] = maped.to_lumps()
    wad.to_file(wad_filename)
    print('  TNT MAP31 fix applied.')

def extract_map(in_wad, map_name, out_filename):
    out_wad = omg.WAD()
    ed = omg.MapEditor(in_wad.maps[map_name])
    out_wad.maps[map_name] = ed.to_lumps()
    out_wad.to_file(out_filename)

def extract_iwad_maps(wad_name, map_prefix):
    in_wad = omg.WAD()
    wad_filename = get_wad_filename(wad_name)
    in_wad.from_file(wad_filename)
    for map_name in in_wad.maps.find('*'):
        print('  Processing map %s...' % map_name)
        out_wad_filename = DEST_DIR + 'maps/' + map_prefix + map_name + '.wad'
        extract_map(in_wad, map_name, out_wad_filename)
        print('  Saved map %s' % out_wad_filename)

def extract_lumps(wad_name):
    if not wad_name in WAD_LUMP_LISTS:
        return
    wad = omg.WAD()
    wad_filename = get_wad_filename(wad_name)
    wad.from_file(wad_filename)
    for lump_list in WAD_LUMP_LISTS[wad_name]:
        # derive subdir from name of lump list
        try:
            lump_type = lump_list[:lump_list.index('_')]
        except ValueError:
            print("Couldn't identify type of lump list %s" % lump_list)
            continue
        lump_table = getattr(wad, lump_type, None)
        if not lump_table:
            print('  Lump type %s not found' % lump_type)
            continue
        print('  extracting %s...' % lump_list)
        # write PLAYPAL etc to pk3 root
        if lump_type == 'data':
            lump_subdir = DEST_DIR
        else:
            lump_subdir = DEST_DIR + lump_type + '/'
        # process each item in lump list
        for line in open(DATA_DIR + lump_list).readlines():
            line = line.strip()
            # ignore comments
            if line.startswith('//'):
                continue
            # no colon: extracted lump uses name from list
            if line.find(':') == -1:
                out_filename = line
                lump_name = line
            # colon: use filename to right of colon
            else:
                # split then strip
                lump_name, out_filename = line.split(':')
                lump_name = lump_name.strip()
                out_filename = out_filename.strip()
            if not lump_name in lump_table:
                print("  Couldn't find lump with name %s" % lump_name)
                continue
            lump = lump_table[lump_name]
            out_filename += '.lmp' if lump_type != 'music' else '.mus'
            print('    Writing %s' % lump_subdir + out_filename)
            lump.to_file(lump_subdir + out_filename)

def main():
    # make dirs if they don't exist
    if not os.path.exists(DEST_DIR):
        os.mkdir(DEST_DIR)
    for dirname in ['flats', 'graphics', 'music', 'maps', 'mapinfo', 'patches',
                    'sounds', 'sprites']:
        if not os.path.exists(DEST_DIR + dirname):
            os.mkdir(DEST_DIR + dirname)
    # extract lumps and maps from wads
    for iwad_name in IWADS:
        wad_filename = get_wad_filename(iwad_name)
        if not wad_filename:
            print('IWAD %s not found' % iwad_name)
            continue
        print('Processing IWAD %s...' % iwad_name)
        # TODO: uncomment when done
        #extract_lumps(iwad_name)
        #extract_iwad_maps(iwad_name, WAD_MAP_PREFIXES[iwad_name])
    extract_master_levels()
    if get_wad_filename('tnt'):
        tnt_map31_fix()
    # copy pre-authored lumps eg mapinfo
    for src_file in RES_FILES:
        print('Copying %s' % src_file)
        copyfile(RES_DIR + src_file, DEST_DIR + src_file)
    # create pk3
    print('Creating %s...' % DEST_FILENAME)
    pk3 = ZipFile(DEST_FILENAME, 'w')
    for dir_name, x, filenames in os.walk(DEST_DIR):
        for filename in filenames:
            src_name = dir_name + '/' + filename
            # exclude pk3/ top dir from name within archive
            dest_name = src_name[len(DEST_DIR):]
            pk3.write(src_name, dest_name)
    pk3.close()
    print('Done!')

if __name__ == "__main__":
    main()
