#!/usr/bin/env python3

# tyler.py - pack and unpack level maps with tilesheets
# Copyright (C) 2015 Mister Hat
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from PIL import Image
import argparse
import imghdr
import json
import numpy
import operator
import os


def image_to_sheet(image, size=16):
    """Slice an image into a 2D list of cropped images."""
    width = image.size[0]
    height = image.size[1]
    sheet = []

    for y in range(0, height, size):
        chopped.append([])
        for x in range(0, width, size):
            sheet[-1].append(image.crop((x, y, x + size, y + size)))

    return sheet


def dedupe_sheet(sheet, found=set()):
    """Remove all of the duplicate tiles from the sheet."""
    deduped = []

    for row in sheet:
        deduped.append([])
        for tile in row:
            hashed = tile.tobytes()
            if hashed not in found:
                found.add(hashed)
                deduped[-1].append(tile)
            else:
                deduped[-1].append(-1)

    return deduped


def sheet_to_map(sheet, tiles):
    """Convert an image sheet into a matrix."""
    tile_locs = {}

    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            if tile != -1:
                tile_locs[tile.tobytes()] = (x, y)

    width = len(sheet[0])
    height = len(sheet)
    mapped = []

    for y in range(height):
        mapped.append([])
        for x in range(width):
            tile = sheet[y][x]
            if tile != -1:
                tile = tile_locs[tile.tobytes()]
            mapped[-1].append(tile)

    return mapped


def map_to_sheet(mapped, tilesheet, size=16):
    """
    Convert a matrix of tile locations and a tilesheet image to an image
    matrix.
    """
    width = len(mapped[0])
    height = len(mapped)
    sheet = []

    for y in range(height):
        sheet.append([])
        for x in range(width):
            tile = mapped[y][x]
            cropped = tilesheet.crop((tile[0] * size, tile[1] * size,
                                     (tile[0] * size) + size,
                                     (tile[1] * size) + size))
            sheet[-1].append(cropped)

    return sheet


def compress_sheet(sheet):
    """Remove empty columns in a tilesheet."""
    width = len(sheet[0])
    height = len(sheet)
    last_tile = None
    compressed = [[] for y in range(height)]

    for x in range(width):
        empty = 0
        column = []
        for y in range(height):
            tile = sheet[y][x]
            column.append(tile)
            if numpy.array_equal(tile, last_tile):
                empty += 1
            last_tile = sheet[y][x]
        if empty < height:
            for i, tile in enumerate(column):
                compressed[i].append(tile)

    return compressed


def sheet_to_image(sheet, size=16):
    """Create an image out of a tilesheet."""
    width = max(len(row) for row in sheet)
    height = len(sheet)
    image = Image.new('RGBA', (width * size, height * size))

    for x in range(width):
        for y in range(height):
            try:
                tile = sheet[y][x]
            except:
                tile = -1
            if tile != -1:
                image.paste(tile, (x * size, y * size))

    return image


if __name__ == '__main__':
    description = 'pack and unpack level maps with tilesheets'
    parser_format = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=parser_format)
    parser.add_argument('sources', type=str, nargs='+',
                        help='png files to unpack or json files to pack')
    parser.add_argument('-t', '--tilesheet', type=str,
                        default='./tilesheet.png',
                        help='tilesheet png file')
    parser.add_argument('-o', '--output', type=str, default='.',
                        help='output directory for images or maps')
    parser.add_argument('-s', '--size', type=int, default=16,
                        help='size of each tile in pixels')
    parser.add_argument('-n', '--no-compress', action='store_true',
                        help='don\'t compress output tilesheet columns in '
                             'unpacking')
    args = parser.parse_args()

    sources = args.sources
    tilesheet = args.tilesheet
    output = args.output
    size = args.size
    no_compress = args.no_compress

    try:
        os.makedirs(output)
    except:
        pass

    packing = imghdr.what(sources[0]) == 'png'

    if packing:
        sheets = [image_to_sheet(Image.open(image), size) for image in sources]
        found = set()
        output_sheet = []

        for sheet in sheets:
            sheet = dedupe_sheet(sheet, found)
            if not no_compress:
                sheet = compress_sheet(sheet)
            output_sheet += sheet

        for name, sheet in zip(sources, sheets):
            mapped = sheet_to_map(sheet, output_sheet)

            name = os.path.basename(name)
            name = os.path.join(output, os.path.splitext(name)[0] + '.json')
            json.dump(mapped, open(name, 'w'), separators=(',', ':'))

        sheet_to_image(output_sheet).save(tilesheet, 'png')
    else:
        input_sheet = Image.open(tilesheet)

        for mapped in sources:
            name = os.path.basename(mapped)
            name = os.path.join(output, os.path.splitext(name)[0] + '.png')

            mapped = json.load(open(mapped, 'r'))
            sheet = map_to_sheet(mapped, input_sheet, size)
            sheet_to_image(sheet, size).save(name)
