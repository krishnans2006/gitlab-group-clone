# Gitlab Group Clone

```text
usage: main.py [-h] [--domain DOMAIN] [-d DIRECTORY] [-a] group_id token

Recursively clone all projects in a Gitlab group to a new directory in the
current folder

positional arguments:
  group_id              GitLab Group ID (found under group name)
  token                 GitLab personal access token (PAT) with at least
                        `read_api` and `read_repository` scopes

options:
  -h, --help            show this help message and exit
  --domain DOMAIN       GitLab instance to use, defaults to gitlab.com
  -d DIRECTORY, --directory DIRECTORY
                        Directory to clone projects into, defaults to current
                        directory
  -a, --archived        Include archived repos
```
