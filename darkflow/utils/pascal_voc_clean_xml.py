"""
parse PASCAL VOC xml annotations
"""

import os
import sys
import xml.etree.ElementTree as ET
import glob


def _pp(l): # pretty printing 
    for i in l:
        print(f'{i}: {l[i]}')

def pascal_voc_clean_xml(ANN, pick, exclusive = False):
    print(f"Parsing for {pick} {'exclusively' * int(exclusive)}")

    dumps = []
    cur_dir = os.getcwd()
    os.chdir(ANN)
    annotations = os.listdir('.')
    annotations = glob.glob(f'{str(annotations)}*.xml')
    size = len(annotations)

    for i, file in enumerate(annotations):
        # progress bar      
        sys.stdout.write('\r')
        percentage = 1. * (i+1) / size
        progress = int(percentage * 20)
        bar_arg = [progress*'=', ' '*(19-progress), percentage*100]
        bar_arg += [file]
        sys.stdout.write('[{}>{}]{:.0f}%  {}'.format(*bar_arg))
        sys.stdout.flush()

        with open(file) as in_file:
            tree=ET.parse(in_file)
            root = tree.getroot()
            jpg = str(root.find('filename').text)
            imsize = root.find('size')
            w = int(imsize.find('width').text)
            h = int(imsize.find('height').text)
            all = []

            for obj in root.iter('object'):
                current = []
                name = obj.find('name').text
                if name not in pick:
                        continue

                xmlbox = obj.find('bndbox')
                xn = int(float(xmlbox.find('xmin').text))
                xx = int(float(xmlbox.find('xmax').text))
                yn = int(float(xmlbox.find('ymin').text))
                yx = int(float(xmlbox.find('ymax').text))
                current = [name,xn,yn,xx,yx]
                all += [current]

            add = [[jpg, [w, h, all]]]
            dumps += add
    # gather all stats
    stat = dict()
    for dump in dumps:
        all = dump[1][2]
        for current in all:
            if current[0] in pick:
                if current[0] in stat:
                    stat[current[0]]+=1
                else:
                    stat[current[0]] =1

    print('\nStatistics:')
    _pp(stat)
    print(f'Dataset size: {len(dumps)}')

    os.chdir(cur_dir)
    return dumps