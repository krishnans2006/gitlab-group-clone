import argparse
import os
import requests
import sys

from git import Repo
from git.exc import GitCommandError

# Parse arguments

# fmt: off
parser = argparse.ArgumentParser(sys.argv[0], description="Recursively clone all projects in a Gitlab group to a new directory in the current folder")
parser.add_argument("group_id", help="GitLab Group ID (found under group name)")
parser.add_argument("token", help="GitLab personal access token (PAT) with at least `read_api` and `read_repository` scopes")
parser.add_argument("--domain", help="GitLab instance to use, defaults to gitlab.com", default="gitlab.com")
parser.add_argument("-d", "--directory", help="Directory to clone projects into, defaults to current directory", default=".")
parser.add_argument("-a", "--archived", help="Include archived repos", action="store_true")
args = parser.parse_args()
# fmt: on


# Fetch projects list
root_url = f"https://{args.domain}/api/v4"
res = requests.get(
    f"{root_url}/groups/{args.group_id}/projects?per_page=9999&page=1&include_subgroups=true",
    headers={"PRIVATE-TOKEN": args.token},
)
projects = res.json()

# Set up cloning directory
if args.directory.startswith("~"):
    abs_dir = os.path.expanduser(args.directory)
else:
    abs_dir = os.path.abspath(args.directory)
os.makedirs(abs_dir, exist_ok=True)

# Start message
group_name = os.path.commonprefix([p["namespace"]["full_path"] for p in projects])
confirm = input(f"Found {len(projects)} projects in group `{group_name}`, continue? (y/N) ")
if not confirm.lower().startswith("y"):
    print("Aborting")
    sys.exit(1)

# Main loop
for p in projects:
    display_name = p["name_with_namespace"]
    ssh_url = p["ssh_url_to_repo"]
    is_archived = p["archived"]

    gitlab_path = p["path_with_namespace"]
    parent_gitlab_path = p["namespace"]["full_path"]

    filesystem_path = os.path.join(abs_dir, gitlab_path)
    parent_filesystem_path = os.path.join(abs_dir, parent_gitlab_path)

    print(f"\nCloning project: {display_name}")

    if is_archived and not args.archived:
        print("       Skipping: Archived")
        continue

    if os.path.exists(filesystem_path):
        print("       Skipping: Folder already exists")
        continue

    print(f"           From: {ssh_url}")
    print(f"             To: {filesystem_path}")

    os.makedirs(parent_filesystem_path, exist_ok=True)

    try:
        Repo.clone_from(ssh_url, filesystem_path)
    except GitCommandError as e:
        print(" Cloning failed:", repr(e).replace("\n", "\n                 "))
