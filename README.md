# dirsum

Print a hash for your current working directory as well as for each file within. Can specify a `.containerignore` file to filter out files.

Created to help diagnose cache invalidation issues when building containers with `COPY` statements.

## Usage

```text
usage: dirsum [-h] [-i IGNORE] [-p]

options:
  -h, --help            show this help message and exit
  -i IGNORE, --ignore IGNORE
                        Path to ignorefile
  -p, --pretty          Show colourful output
```
