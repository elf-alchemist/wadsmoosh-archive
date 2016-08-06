
import os
from shutil import copyfile
from zipfile import ZipFile

import omg

# TODO:
# tnt map23 switch (SW1BRN1 in SW corner) - find and substitute all doom1vs2 texture def conflicts?
# same error also shows up in plutonia map30

# if False, do a dry run with no actual file writing
should_extract = True

SRC_WAD_DIR = 'source_wads/'
DATA_DIR = 'data/'
DEST_DIR = 'pk3/'
DEST_FILENAME = 'doom_complete.pk3'
LOG_FILENAME = 'wadsmoosh.log'
RES_DIR = 'res/'
DATA_TABLES_FILE = 'wadsmoosh_data.py'

# forward-declare all the stuff in DATA_TABLES_FILE for clarity
RES_FILES = []
IWADS = []
COMMON_LUMPS = []
DOOM1_LUMPS = []
DOOM2_LUMPS = []
WAD_LUMP_LISTS = {}
WAD_MAP_PREFIXES = {}
TEXTURE_REPLACEMENTS = {}
MASTER_LEVELS_MAP_ORDER = []

logfile = None

exec(open(DATA_TABLES_FILE).read())

MASTER_LEVELS_MAP_PREFIX = WAD_MAP_PREFIXES.get('masterlevels', '')

def logg(line):
    global logfile
    if not logfile:
        logfile = open(LOG_FILENAME, 'w')
    print(line)
    logfile.write(line + '\n')

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
        logg('Master Levels not found.')
        return
    logg('Processing Master Levels...')
    for i,wad_name in enumerate(MASTER_LEVELS_MAP_ORDER):
        in_wad = omg.WAD()
        wad_filename = get_wad_filename(wad_name)
        in_wad.from_file(wad_filename)
        out_wad_filename = DEST_DIR + 'maps/' + MASTER_LEVELS_MAP_PREFIX + 'map'
        # extra zero for <10 map numbers, eg map01
        out_wad_filename += str(i + 1).rjust(2, '0') + '.wad'
        logg('  Extracting %s to %s' % (wad_filename, out_wad_filename))
        # grab first map we find in each wad
        map_name = in_wad.maps.find('*')[0]
        ed = omg.MapEditor(in_wad.maps[map_name])
        extract_map(in_wad, map_name, out_wad_filename)
    # save teeth map32 to map21 wad
    out_wad_filename = DEST_DIR + 'maps/' + MASTER_LEVELS_MAP_PREFIX + 'map21' + '.wad'
    logg('  Extracting %s map32 to %s' % (wad_filename, out_wad_filename))
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
        logg('  Extracting %s lump from %s as %s' % (patch_replace[0],
                                                   wad_filename,
                                                   patch_replace[1]))
        lump.to_file(out_filename)

def tnt_map31_fix():
    logg('Checking for TNT MAP31 fix...')
    wad = omg.WAD()
    wad_filename = DEST_DIR + 'maps/' + WAD_MAP_PREFIXES['tnt'] + 'MAP31.wad'
    wad.from_file(wad_filename)
    maped = omg.MapEditor(wad.maps['MAP31'])
    yellow_key = maped.things[470]
    if yellow_key.type != 6 or \
       (yellow_key.type == 6 and not yellow_key.get_multiplayer()):
        logg('  TNT MAP31 already fixed.')
        return
    yellow_key.set_multiplayer(False)
    wad.maps['MAP31'] = maped.to_lumps()
    wad.to_file(wad_filename)
    logg('  TNT MAP31 fix applied.')

def do_texture_replacements_in_map(map_filename, map_name, replacements):
    # replace textures in given table for given map in given wad
    wad = omg.WAD()
    wad.from_file(map_filename)
    maped = omg.MapEditor(wad.maps[map_name])
    for i,sidedef in enumerate(maped.sidedefs):
        for src,dest in replacements.items():
            if sidedef.tx_low == src:
                sidedef.tx_low = dest
                logg('    Replaced %s with %s on sidedef #%s lower' % (src, dest, i))
            if sidedef.tx_mid == src:
                sidedef.tx_mid = dest
                logg('    Replaced %s with %s on sidedef #%s mid' % (src, dest, i))
            if sidedef.tx_up == src:
                sidedef.tx_up = dest
                logg('    Replaced %s with %s on sidedef #%s upper' % (src, dest, i))
    wad.maps[map_name] = maped.to_lumps()
    wad.to_file(map_filename)

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
        logg('  Extracting map %s...' % map_name)
        out_wad_filename = DEST_DIR + 'maps/' + map_prefix + map_name + '.wad'
        extract_map(in_wad, map_name, out_wad_filename)
        # do any texture replacements
        replacements = TEXTURE_REPLACEMENTS.get(wad_name, None)
        if replacements:
            do_texture_replacements_in_map(out_wad_filename, map_name,
                                           replacements)
        #logg('  Saved map %s' % out_wad_filename)

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
            logg("Couldn't identify type of lump list %s" % lump_list)
            continue
        lump_table = getattr(wad, lump_type, None)
        if not lump_table:
            logg('  Lump type %s not found' % lump_type)
            continue
        logg('  extracting %s...' % lump_list)
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
                logg("  Couldn't find lump with name %s" % lump_name)
                continue
            lump = lump_table[lump_name]
            out_filename += '.lmp' if lump_type != 'music' else '.mus'
            logg('    Extracting %s' % lump_subdir + out_filename)
            lump.to_file(lump_subdir + out_filename)

def copy_resources():
    for src_file in RES_FILES:
        # don't copy texture lumps for files that aren't present
        if src_file.startswith('textures.doom1') and not get_wad_filename('doom'):
            continue
        elif src_file == 'textures.doom2' and not get_wad_filename('doom2'):
            # DO copy if final doom exists and doom2 doesn't
            if not get_wad_filename('tnt'):
                continue
        elif src_file == 'textures.tnt' and not get_wad_filename('tnt'):
            continue
        elif src_file == 'textures.plut' and not get_wad_filename('plutonia'):
            continue
        logg('Copying %s' % src_file)
        copyfile(RES_DIR + src_file, DEST_DIR + src_file)

def main():
    # make dirs if they don't exist
    if not os.path.exists(DEST_DIR):
        os.mkdir(DEST_DIR)
    for dirname in ['flats', 'graphics', 'music', 'maps', 'mapinfo', 'patches',
                    'sounds', 'sprites']:
        if not os.path.exists(DEST_DIR + dirname):
            os.mkdir(DEST_DIR + dirname)
    # copy pre-authored lumps eg mapinfo
    if should_extract:
        copy_resources()
    # if final doom present but not doom1/2, extract doom2 resources from it
    if get_wad_filename('tnt') and not get_wad_filename('doom2'):
        WAD_LUMP_LISTS['tnt'] += DOOM2_LUMPS
        # if doom 1 also isn't present (weird) extract all common resources
        if not get_wad_filename('doom'):
            WAD_LUMP_LISTS['tnt'] += COMMON_LUMPS
    # extract lumps and maps from wads
    for iwad_name in IWADS:
        wad_filename = get_wad_filename(iwad_name)
        if not wad_filename:
            logg('IWAD %s not found' % iwad_name)
            continue
        if iwad_name == 'nerve' and not get_wad_filename('doom2'):
            logg('Skipping nerve.wad as doom2.wad is not present')
            continue
        logg('Processing IWAD %s...' % iwad_name)
        if should_extract:
            extract_lumps(iwad_name)
            extract_iwad_maps(iwad_name, WAD_MAP_PREFIXES[iwad_name])
    if get_wad_filename('doom2'):
        if should_extract:
            extract_master_levels()
    else:
        logg('Skipping Master Levels as doom2.wad is not present')
    if get_wad_filename('tnt') and should_extract:
        tnt_map31_fix()
    # create pk3
    logg('Creating %s...' % DEST_FILENAME)
    pk3 = ZipFile(DEST_FILENAME, 'w')
    for dir_name, x, filenames in os.walk(DEST_DIR):
        for filename in filenames:
            src_name = dir_name + '/' + filename
            # exclude pk3/ top dir from name within archive
            dest_name = src_name[len(DEST_DIR):]
            pk3.write(src_name, dest_name)
    pk3.close()
    logg('Done!')
    logfile.close()

if __name__ == "__main__":
    main()
