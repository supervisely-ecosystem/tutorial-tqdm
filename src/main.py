import os
import time
from dotenv import load_dotenv

from tqdm import tqdm

import supervisely as sly

if sly.is_development():
    load_dotenv("local.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))

api = sly.Api()

# get variables from enviroment
project_id = sly.env.project_id()
team_id = sly.env.team_id()

# Example 1. Use tqdm in the loop.
batch_size = 10
data = range(100)

with tqdm(total=len(data)) as pbar:
    for batch in sly.batched(data, batch_size):
        for item in batch:
            time.sleep(0.1)
        pbar.update(batch_size)

# Example 2. Download image project and upload it into Team files using tqdm progress bar.
local_dir = 'your/local/dir/'
team_files_dir = '/your/teamfiles/dir/'

# download
n_count = api.project.get_info_by_id(project_id).items_count
p = tqdm(desc="Downloading", total=n_count)

sly.download(api, project_id, local_dir, progress_cb=p)

# upload
p = tqdm(
    desc="Uploading",
    total=sly.fs.get_directory_size(local_dir),
    unit="B",
    unit_scale=True,
)
api.file.upload_directory(
    team_id,
    local_dir,
    team_files_dir,
    progress_size_cb=p,
)

# Example 3 (advanced). Use native sly.Progress functions for downloading.
local_dir = 'your/local/dir/'
team_files_dir = '/your/teamfiles/dir/'

# download
n_count = api.project.get_info_by_id(project_id).items_count
p = sly.Progress("Downloading", n_count)

sly.download(api, project_id, local_dir, progress_cb=p)

# upload
p = sly.Progress(
    "Uploading",
    sly.fs.get_directory_size(local_dir), 
    is_size=True,
)
api.file.upload_directory(
    team_id,
    local_dir,
    team_files_dir,
    progress_size_cb=p,
)