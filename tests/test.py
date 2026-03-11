from imports import *
import os
from abstract_utilities import *
abstractEnv()
caller_dir = get_caller_dir()
directories = [caller_dir,os.path.dirname(caller_dir),'~/','~/Documents']

get_files_and_dirs(allowed_exts=['.env'])
