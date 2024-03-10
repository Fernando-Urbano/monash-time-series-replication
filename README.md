Monash Time Series Forecasting Replication
==================

# About this project
[TODO]

# Quick Start
## 1. Install TexLive
Note that you must have TexLive installed on your computer and available in your path.

It can be downloaded in:
- [Windows installer](https://tug.org/texlive/windows.html#install)
- [Mac installer](https://tug.org/mactex/mactex-download.html)

## 2. Create virtual environment
Go to the home directory of the project and type in terminal the following commands:

```bash
conda deactivate
conda create -n mtsr -c conda-forge python=3.9.18 r-base=4.3.2
conda activate mtsr
```

The versions specified of R and Python are the ones that work with most packages for `osx-arm64`. The original project was done using: R: 4.0.2, Python: 3.7.4.

### 3. Install Packages
Inside command line run:
```bash
chmod +x install_packages.sh
./install_packages.sh
```

### 4. Run dodo
[TODO]

# Add more Packages to the Virtual Environment
If needed to add more packages to the environment use the `requirements_py.txt` to add Python packages and `requirements_r.txt` to add R packages.

It is necessary to specify the version used.

R packages have a bigger specification and are harder to add. Before adding an R package, run the the command line:

```bash
conda search -c conda-forge {package-name} --info
```

It will give you the version of the package that works for the current version of R we have in the virtual environment. Make sure to add the package version that is viasible for the current version of our environment.

For instance, if you want to install tidyverse:

```bash
conda search -c conda-forge tidyverse --info
```

We see that `v2.0.0` is for `r-base >=4.3,<4.4.0a0`, which is compatible with ours:

```bash
r-tidyverse 2.0.0 r43h6115d3f_0
-------------------------------
file name   : r-tidyverse-2.0.0-r43h6115d3f_0.conda
name        : r-tidyverse
version     : 2.0.0
build       : r43h6115d3f_0
build number: 0
size        : 414 KB
license     : MIT
subdir      : noarch
url         : https://repo.anaconda.com/pkgs/r/noarch/r-tidyverse-2.0.0-r43h6115d3f_0.conda
md5         : 19659846ac7b0101a848f53b392b833c
timestamp   : 2023-09-26 19:23:00 UTC
dependencies: 
  - r-base >=4.3,<4.4.0a0
  - r-broom >=1.0.3
  - r-cli >=3.6.0
  - r-conflicted >=1.2.0
  - r-dbplyr >=2.3.0
  - r-dplyr >=1.1.0
  - r-dtplyr >=1.2.2
  - r-forcats >=1.0.0
  - r-ggplot2 >=3.4.1
  - r-googledrive >=2.0.0
  - r-googlesheets4 >=1.0.1
  - r-haven >=2.5.1
  - r-hms >=1.1.2
  - r-httr >=1.4.4
  - r-jsonlite >=1.8.4
  - r-lubridate >=1.9.2
  - r-magrittr >=2.0.3
  - r-modelr >=0.1.10
  - r-pillar >=1.8.1
  - r-purrr >=1.0.1
  - r-ragg >=1.2.5
  - r-readr >=2.1.4
  - r-readxl >=1.4.2
  - r-reprex >=2.0.2
  - r-rlang >=1.0.6
  - r-rstudioapi >=0.14
  - r-rvest >=1.0.3
  - r-stringr >=1.5.0
  - r-tibble >=3.1.8
  - r-tidyr >=1.3.0
  - r-xml2 >=1.3.3
  - _r-mutex 1.* anacondar_1
```

Therefore, we install it:

```bash
conda install -c conda-forge r-tidyverse=2.0.0
```

As we can see above, we change the space between the package and its version to a `=` sign.

An alternative to running R packages using conda is to use Rscript and download the packages from CRAN. It is not the recommended path.

```bash
Rscript install_packages.R
``` 

When running it, make sure to add all the necessary packages that are also in `requirements_r.txt`.

# General Directory Structure

 - The `assets` folder is used for things like hand-drawn figures or other pictures that were not generated from code. These things cannot be easily recreated if they are deleted.

 - The `output` folder, on the other hand, contains tables and figures that are generated from code. The entire folder should be able to be deleted, because the code can be run again, which would again generate all of the contents.

 - I'm using the `doit` Python module as a task runner. It works like `make` and the associated `Makefile`s. To rerun the code, install `doit` (https://pydoit.org/) and execute the command `doit` from the `src` directory. Note that doit is very flexible and can be used to run code commands from the command prompt, thus making it suitable for projects that use scripts written in multiple different programming languages.

 - I'm using the `.env` file as a container for absolute paths that are private to each collaborator in the project. You can also use it for private credentials, if needed. It should not be tracked in Git.

