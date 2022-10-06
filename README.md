# Travis Packages

This repo holds code to generate & compare list of packages/tools installed in 2 different linux environments. 

## Generate Data

Package data is generated using `syft` tool. The [syft-csv.template](syft-csv.template) is used to generate csv format output. You can install `syft` from https://github.com/anchore/syft/releases.

```bash
$ sudo syft packages / -o template -t syft-csv.template --file data/sample/ppc64le_packages.csv
```

## Compare Data

CSV package data generated using `syft` is processed using [main.py](./main.py) to output missing & mis-matched version packages. 

```bash
$ python3 main.py -h
usage: main.py [-h] [-b BASEDATA] [-n NEWDATA] [-o OUTPUTDIR]

Script to compare 2 csv lists of packages.

  -h, --help            show this help message and exit
  -b BASEDATA, --baseData BASEDATA
                        csv file path of base data
  -n NEWDATA, --newData NEWDATA
                        csv file path of new data
  -o OUTPUTDIR, --outputDir OUTPUTDIR
                        directory to store output
```

The `--baseData` list is used as a base to compare and generated differences between lists.

```bash
$ python main.py -b data/sample/amd64_packages.csv -n .data/sample/ppc64le_packages.csv -o date/sample
```

## Travis Job 

The travis job generates list of packages using `syft` tool in stages and pushes them back to git repo to be used by final comparison stage which processes these new package lists using `main.py` python script to output missing and version mis-matched packages in travis base images.

[git-push.sh](.travis/git-push.sh) is a helper script to perform push from Travis-CI. The `GITHUB_USERNAME` & `GITHUB_TOKEN` env vars are set via Travis Environment Variables from travis web ui.

NOTE: Disable auto travis job trigger for the repo from travis web ui if the `[skip travis]` in commit message is not working as expected. More details: https://docs.travis-ci.com/user/customizing-the-build#skipping-a-build.