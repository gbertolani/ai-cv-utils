# -*- coding: utf-8 -*-
###############################################################################
#   Copyright (c) 2021 Gaston Alberto Bertolani
#   License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###############################################################################

import argparse

from utils.remove_background import BackgroundEliminator
from utils.separator import Separator
from utils.yolo_generator import Stage

parser = argparse.ArgumentParser(
    prog='ai_utils',
    description='Utilities for AI.',
)
subparsers = parser.add_subparsers(help='Operation type:')
# Remove Background
rmbg = subparsers.add_parser(
    'rmbg', help='Remove Backgraund of image')
rmbg.add_argument('-s', '--source', action='store', type=str,
                  required=True, help='Source (Folder/Image)')
rmbg.add_argument('-t', '--target', action='store', type=str,
                  help='Path to save (Folder/Image)')
rmbg.add_argument('-r', '--no-origin', action='store', type=bool,
                  help='Remove Old Image')
rmbg.add_argument('-g', '--with-groups', action='store', type=bool,
                  help='Create category folder of image in target folder')
rmbg.set_defaults(parser='rmbg')

# Separator
sepf = subparsers.add_parser(
    'split', help='Split files in folders')
sepf.add_argument('-s', '--source', action='store', type=str,
                  required=True, help='Source (Folder/Image)')
sepf.add_argument('-t', '--train', action='store', type=str,
                  required=True, help='Train Path (Folder)')
sepf.add_argument('-v', '--validation', action='store', type=str,
                  help='Validation path (Folder)')
sepf.add_argument('-x', '--test', action='store', type=str,
                  help='Test (Folder)')
sepf.add_argument('-tp', '--train-perc', action='store', type=float,
                  help='Train Percent')
sepf.add_argument('-vp', '--validation-perc', action='store', type=float,
                  help='Validation Perc')
sepf.add_argument('-xp', '--test-perc', action='store', type=float,
                  help='Test Percent')
sepf.add_argument('-f', '--format', action='store', type=str,
                  help='Format to find files e.g jpg,png,jepg')
sepf.add_argument('-r', '--remove', action='store', type=bool,
                  default=False, help='Remove Source Fields')
sepf.set_defaults(parser='split')

# Yolo Generator
yolog = subparsers.add_parser(
    'yologen', help='Generate Stages from images to train')
yolog.add_argument('-b', '--background', action='store', type=str,
                   required=True, help='Background Path')
yolog.add_argument('-s', '--samples', action='store', type=str,
                   required=True, help='Samples Folder Path')
yolog.add_argument('-o', '--output', action='store', type=str,
                   required=True, help='Output folder to save files')
yolog.add_argument('-q', '--quantity', action='store', type=int,
                   default=1, help='Quantity of Stages')
yolog.add_argument('-r', '--rgx', action='store', type=str,
                   help='Regex to get class from image file name')
yolog.add_argument('-f', '--format', action='store', type=str,
                   default='*.png', help='Format of images')

yolog.set_defaults(parser='yologen')

parsed_args = parser.parse_args()

if parsed_args.parser == 'rmbg':
    rmb = BackgroundEliminator(
        parsed_args.source,
        save_path=parsed_args.target,
        no_origin=parsed_args.no_origin,
        with_groups=parsed_args.with_groups,
    )
    rmb.remove_background()
elif parsed_args.parser == 'split':
    __import__('ipdb').set_trace()
    sep = Separator(
        parsed_args.source,
        parsed_args.train,
        validation_path=parsed_args.validation,
        test_path=parsed_args.test,
        train_perc=parsed_args.train_perc,
        validation_perc=parsed_args.validation_perc,
        test_perc=parsed_args.test_perc,
    )
    sep.split_samples(
        format=parsed_args.format,
        remove_source=parsed_args.remove,
    )
elif parsed_args.parser == 'yologen':
    __import__('ipdb').set_trace()
    stage = Stage(
        parsed_args.background,
        parsed_args.samples,
        parsed_args.output,
        class_rgx=parsed_args.rgx,
        format=parsed_args.format,
    )
    stage.generate_random_scenes(num_frames=parsed_args.quantity)
