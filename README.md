# tyler
Pack and unpack level maps with tilesheets. Level maps consists of a 2
dimensional array, with each tile being specified as `[x, y]`, a position on
the tilesheet image (*tilesheet.png* by default). tyler can receive maps and a
tilesheet to turn them into level images and accept level images and turn them
into a level maps and a tilesheet.

## Requirements
 * Python 3
 * NumPy
 * PIL

    `# apt-get install python3{,-numpy,-pil}`

## Usage
```
usage: tyler.py [-h] [-t TILESHEET] [-o OUTPUT] [-s SIZE] [-n]
                sources [sources ...]

pack and unpack level maps with tilesheets

positional arguments:
  sources               png files to unpack or json files to pack

optional arguments:
  -h, --help            show this help message and exit
  -t TILESHEET, --tilesheet TILESHEET
                        tilesheet png file (default: ./tilesheet.png)
  -o OUTPUT, --output OUTPUT
                        output directory for images or maps (default: .)
  -s SIZE, --size SIZE  size of each tile in pixels (default: 16)
  -n, --no-compress     don't compress output tilesheet columns in unpacking
                        (default: False)
```

## Example
Use tyler to turn tiled images into a JSON matrix and tilesheet image.

*level.png:*

![Beinning of SMB level.](http://i.imgur.com/F79VTNK.png)

    $ ./tyler.py level.png
    $ sed 's/]],/]],\n/g' level.json

**Outputs:**
```
[[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]...
[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0...
[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0...
[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0...
[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0...
...
[[0,0],[0,0],[2,9],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0...
[[0,0],[1,10],[2,10],[3,10],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[...
[[1,10],[2,10],[2,11],[3,11],[3,10],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[4,11...
[[0,12],[0,12],[0,12],[0,12],[0,12],[0,12],[0,12],[0,12],[0,12],[0,12],[0,12]...
```

*tilesheet.png:*

![Tiles from the level image.](https://i.imgur.com/j2NKWDO.png)

You can then turn *level.json* back into an image using a different tilesheet:

![New tilesheet.](http://i.imgur.com/FlarUsS.png)

    $ ./tyler.py -t new-tilesheet.png level.json

**Outputs:**

*level.png:*

![Level generated with new tilesheet.](http://i.imgur.com/STqX5TG.png)

## License
Copyright (C) 2015 Mister Hat

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
