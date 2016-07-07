# WadSmoosh - simple IWAD merge utility

WadSmoosh merges your provided Ultimate Doom, Doom 2, Master Levels, No Rest for the Living, and Final Doom data into a single IWAD file that can be played in ZDoom and GZDoom, with each game as its own entry in the episode list. This makes it very easy to play all of them without relaunching the game with different settings.

It's fine if you don't have all of the Doom games, eg you have Doom 2 but not Final Doom - WadSmoosh will package up everything it can find.

If you new to Doom and just bought these games off Steam, GoG, etc, see the **Absolute Beginner's Guide** section below.

## Usage

Simply copy all your WADs into the `source_wads/` subfolder, then run WadSmoosh.

If you're in Windows, click `wadsmoosh.exe`.

If you're in macOS or Linux, run the `wadsmoo.sh` shell script - only Python 2 is supported at the moment.

WadSmoosh will create a new file called `doom_complete.pk3` with all the game content in it. You can run this in ZDoom / GZDoom with `-iwad doom_complete.pk3` at the command line, or even rename it to `doom2.wad` and run without any command line needed.

## Absolute Beginner's Guide

1. [Download WadSmoosh](https://bitbucket.org/JPLeBreton/wadsmoosh/downloads) and extract it to a folder.
2. Find the folder(s) where Steam/GoG installed your game(s). For Steam, this will be something like `<Steam folder>\SteamApps\Common\<game name>\base`.
3. Copy any files you find with a `.WAD` extension to the `source_mods/` subfolder where you extracted WadSmoosh.
4. Double-click `wadsmoosh.exe`. A console window will pop up to show progress.
5. When it closes, you should have a file in the WadSmoosh folder called `doom_complete.pk3`.
6. Download [ZDoom](http://zdoom.org) or [GZDoom](http://gzdoom.drdteam.org) - use GZDoom if you want to be able to look up and down - and extract it to a folder.
7. Copy the `doom_complete.pk3` file to G/ZDoom's folder and rename it to `doom2.wad`.
8. Launch G/ZDoom and play!
