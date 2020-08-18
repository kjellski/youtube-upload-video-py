#!/usr/bin/python

import os
import sys
import shutil

from string import Template
from pathlib import Path
from upload_video import get_authenticated_service, upload_video, VALID_PRIVACY_STATUSES
from apiclient.errors import HttpError
from oauth2client.tools import argparser

VIDEO_FILETYPES = ( ".mov", ".mpg", ".mpeg4", ".mp4", ".avi", ".wmv", ".mpegps", ".flv" )

def get_files_in_folder(basepath):
  folder_path = Path(basepath)
  return (entry for entry in folder_path.iterdir() if entry.is_file() and Path(entry).suffix.lower() in VIDEO_FILETYPES)

def backup_file(file, backup_path):
  source_path = file
  destination_path = os.path.join(backup_path, file.name)
  shutil.move(source_path, destination_path)

if __name__ == '__main__':
  argparser.add_argument("--folder", required=True, help="Video folder to upload from")

  argparser.add_argument("--category", default="27",
    help="Numeric video category. (default: Education)" +
      "See https://developers.google.com/youtube/v3/docs/videoCategories/list")
  argparser.add_argument("--keywords", help="Video keywords, comma separated",
    default="Schools_For_Fools")
  argparser.add_argument("--privacyStatus", choices=VALID_PRIVACY_STATUSES,
    default=VALID_PRIVACY_STATUSES[0], help="Video privacy status.")
  args = argparser.parse_args()
  videos_folder = args.folder

  if not os.path.exists(videos_folder):
    exit("Please specify a valid folder using the --folder= parameter.")

  backup_path = os.path.join(videos_folder, "uploaded")
  Path(backup_path).mkdir(parents=True, exist_ok=True)
  
  for file in get_files_in_folder(videos_folder):
    youtube = get_authenticated_service(args)
 
    description_template = Template('Filename: $file')
    description = description_template.substitute(file=file)

    args.title = str(file)
    args.description = description
    args.file = str(file)

    try:
      print('Uploading: ' + args.file + '...')
      upload_video(youtube, args)
      print('Uploaded : ' + args.file + '.')
      
      print('Backing up: ' + args.file + '...')
      backup_file(file, backup_path)
      print('Backed  up: ' + args.file + '.')
    except HttpError as e:
      print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))