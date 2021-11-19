# -*- coding: utf-8 -*-
###############################################################################
#   Copyright (c) 2021 Gaston Alberto Bertolani
#   License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###############################################################################

import random
from PIL import Image
from glob import glob
from pathlib import Path
import os
import re
import math


class Sample(object):

    def __init__(self, class_id, image, x, y,
                 bg_w, bg_h, max_classes):
        self.idx = class_id
        self.image = image
        self.width, self.height = image.size
        self.lx = x - self.width // 2
        self.rx = x + self.width // 2
        self.ly = y - self.height // 2
        self.ry = y + self.height // 2
        self.center_x = x
        self.center_y = y
        self.bg_w = bg_w
        self.bg_h = bg_h
        self.max_classes = max_classes

    def _truncate(self, number):
        """
        Returns a value truncated to a specific
        number of decimal places.
        """
        factor = 10.0 ** 6
        number += 0.0000001  # Sum lost decimals
        return str(math.trunc(number * factor) / factor).ljust(8, '0')

    def get_yolo_format(self):
        return [
            str(self.idx).zfill(len(str(self.max_classes))),
            self._truncate((self.lx + self.rx)/2/self.bg_w),
            self._truncate((self.ly + self.ry)/2/self.bg_h),
            self._truncate((self.rx - self.lx)/self.bg_w),
            self._truncate((self.ry - self.ly)/self.bg_h),
        ]


class Stage(object):

    def __init__(self, bg_path, input_path, output_path,
                 class_rgx='', format='*.png',
                 sample_perc_size=1.0):
        """ Init Stage

        @param bg_path: Path to background to render samples

        @param input_path: Folder Path to find samples.
                            Can be splitted in many categories
                            with different subfolders names

        @param output_path: Folder Path to save images.

        @param class_rgx: Regex to match different categories
                          when there are multiple
                          samples in same folder

        @param sample_perc_size: Size of sample to render (normalized)

        @param format: format of images to locate
        """
        self.background_path = bg_path
        self.sample_folder = input_path
        self.output_path = output_path
        self.class_rgx = class_rgx
        self.format = format
        self.sample_perc_size = sample_perc_size
        if '*.' not in self.format:
            self.format = '*.' + self.format
        self.class_folders = {}
        self.class_samples = {}
        if self.class_rgx:
            self._load_samples_by_rgx()
        else:
            self._load_samples_by_folders()

        # Check samples
        self.enable_generator = False
        print("******   Checking Samples  *****")
        for cls_name, sample_lst in self.class_samples.items():
            if not len(sample_lst):
                print("There are not samples in class name %s" % cls_name)
            else:
                self.enable_generator = True
        print("******   Finish Checking  *****")

        # Save and wrie class.obj
        self.class_idx = {}
        class_obj_path = os.path.join(self.output_path, 'class.obj.txt')
        f = open(class_obj_path, 'w+')
        for i, class_name in enumerate(self.class_samples.keys()):
            if class_name not in self.class_idx:
                self.class_idx[class_name] = i
                f.write(class_name + '\n')
        f.close()

    def _load_samples_by_rgx(self):
        """
        Search in folder path all samples
        """
        for sample_path in glob(self.folder_path + '/' + self.format):
            spath = Path(sample_path)
            rgx = re.search(self.class_rgx, spath.suffix)
            if not rgx:
                continue
            class_name = ','.join(rgx.groups())
            if class_name not in self.class_samples:
                self.class_samples[class_name] = []
            self.class_samples[class_name].append(sample_path)
        return True

    def _load_samples_by_folders(self):
        """
        Search samples in subfolders and
        create class name with folder's name
        """
        self._cfolders = glob(self.sample_folder + '/*/')
        for folder_path in self._cfolders:
            class_name = os.path.basename(
                os.path.normpath(folder_path)
            )
            self.class_folders[class_name] = folder_path
            samples_path_lst = glob(folder_path + '/' + self.format)
            self.class_samples[class_name] = samples_path_lst
        return True

    def _generate_random_scene(self, uuid=0):
        """
        Draw random samples in random positions
        """
        bg = Image.open(self.background_path)
        bg_w, bg_h = bg.size
        perc_area = random.random()
        bg_area = bg_w * bg_h * perc_area
        samples = []
        while bg_area > 0.0:
            # Select random category name
            class_name_lst = list(self.class_samples.keys())
            class_name = random.choice(class_name_lst)
            class_id = self.class_idx[class_name]
            if not self.class_samples[class_name]:
                print("There are not samples in %s" % class_name)
                continue
            sample_path = random.choice(self.class_samples[class_name])
            img = Image.open(sample_path)
            img_w, img_h = img.size
            img_w *= self.sample_perc_size
            img_h *= self.sample_perc_size
            img.resize((img_w, img_h))
            if img_w * img_h > bg_w * bg_h:
                print("sample %s is greater than background" % sample_path)
                continue
            bg_area -= img_w * img_h
            pos_x = random.randint(-img_w // 2, bg_w - img_w // 2)
            pos_y = random.randint(-img_h // 2, bg_h - img_h // 2)
            samples.append(
                Sample(class_id, img, pos_x, pos_y,
                       bg_w, bg_h, len(class_name_lst))
            )
            # bg.paste(img, (pos_x, pos_y))
            bg = Image.alpha_composite(
                Image.new("RGBA", bg.size),
                bg.convert('RGBA')
            )
            bg.paste(img, (pos_x, pos_y), img)

        # Write File
        file_path = os.path.join(self.output_path, 'frame_%s.txt' % str(uuid))
        f = open(file_path, 'w+')
        f.writelines([' '.join(x.get_yolo_format()) + '\n' for x in samples])
        f.close()
        # Save Image
        img_path = os.path.join(self.output_path, 'frame_%s.png' % str(uuid))
        bg.save(img_path)
        return True

    def generate_random_scenes(self, num_frames=1):
        if not self.enable_generator:
            return True
        files_qty = len(glob(self.output_path + '/*.png'))
        for i in range(0, num_frames):
            print("Creating Random scene %s of %s" % (i + 1, num_frames))
            self._generate_random_scene(files_qty + i)
        return True
