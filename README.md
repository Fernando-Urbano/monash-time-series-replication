Monash Time Series Forecasting Replication
==================

# About this project
[TODO]

# Build the Enviromnet
Using R and Python together inside conda is sometimes a problem, specially when dealing with older package versions.

During the creation and updates of the project, we have run into different problems and have found ways to work with both Mac and Windows.

## 1. Install TexLive
Check that you have installed TexLive. TexLive is useful to generate pdfs from latex files. If it is not currently installed in your computer, you can download it here:

- [Windows installer](https://tug.org/texlive/windows.html#install)
- [Mac installer](https://tug.org/mactex/mactex-download.html)

## 2. Update Your Version of Conda
Afterwards, check you version of conda is recent. Some versions from 2023, like `23.7.4`, are not expected to work due to problems with `Rcpp` and `RArmadillo`, which are necessary for running the models.

Run the following to check conda version:

```bash
conda --version
```

The output should be your current conda version. We strongly recommend using `24.1.2`, while also believing that even newer versions should not cause a problem.

If your version is `24.1.2`, go to step 3.

Ideally, update conda version to `24.1.2`, run:

```bash
conda install -n base -c defaults conda=24.1.2
```

Close and open the terminal, and run the following to check you version:

```bash
conda --version
```

If you version is now `24.1.2`, go to step 3.

Your version might still show up as the one that you already had. In this case, run:

```bash
conda install -n base -c defaults conda=24.1.2 --force-reinstall
```

Close and open the terminal, and run the following to check you version:

```bash
conda --version
```

If you version is now `24.1.2`, go to step 3.

If you version is still another one, we recommend uninstalling `anaconda` and installing it again. Simple tutorials on how to do this can be found here:

- [Uninstall Anaconda](https://docs.anaconda.com/free/anaconda/install/uninstall/)
- [Install Anaconda](https://www.anaconda.com/download)

After installing it, you must make sure that `conda` shortcut is accessible.

Again, run the following to make sure that your version is the right one:

```bash
conda --version
```

## 3. Install CMake
CMake is a software helpful (and sometimes necessary) to run specific R packages with C and C++ dependencies.

Check if CMake is already installed in your computer. If it is installed, go to step 4.

If not, acess the following link or install it via `brew`:

- [Install CMake](https://cmake.org/download/)

Or:

```bash
brew install cmake
```

## 4. Create Conda Virtual Env
Clone the repository in your local machine, open a terminal in the main folder and run:

```bash
conda deactivate
```

```bash
conda create -n mtsr -c conda-forge python=3.11.8 r-base=4.3.2
```

```bash
conda activate mtsr
```

The versions specified of R and Python are the ones that work best for the anaconda distribution.

The original project was created using R: `4.0.2`, Python: `3.7.4`, which is not a possible option, considering recent versions of conda.

Inside command line, run:

```bash
chmod +x install_packages.sh
```

This should make `install_packages` executable. Afterwards, run the following:

```bash
./install_packages.sh
```

For the following steps, make sure that the `mtsr` virtual environment is current active.

The `install_packages.sh` is a bash script that:
- In the case of Windows, uses `source ~/.bashrc` in case it exists to ensure the rest of the file executable.
- iterates and install R packages via `conda forge`.
- Install Python packages via `pip`.

All the installed packages can be found in `requirements_py.txt` and `requirements_r.txt`.

If other packages need to be installed and you would like to check their versioning, refer to the Appendix (in the end of README).

### 4. Run dodo
Dodo is a similar tool to Makefile optimized for Python use.

In our `dodo.py` file, we have all the tasks to:
- Downlaod datasets used to run the models.
- Define the models and datasets that will run.
- Run the selected models for the selected datasets
- Generate Table 1 from the paper
- Generate Table 2 from the paper
- Generate other error metrics tables
- Transform tables to latex
- Update pdf of the output latex

Before running the `dodo.py`, go to the start of the `dodo.py` and define for which models and datasets you would like to update the results.

```python
CHOSEN_MODELS = [
    'arima'
]


CHOSEN_DATASETS = [
    'm1_yearly_dataset'
]
```

If you select `all` for `CHOSEN_MODELS`, all available models will be updated for the selected dataset.

If you select `all` for `CHOSEN_DATASETS`, all available datasets will be updated for the selected models.

If one of the two lists is empty, no model will be update.

In your first trial, we invite you to check with one of the lists empty, in order to ensure that the Latex file is updated.

After setting the lists as wanted, run (from the main folder - not from `src`) inside the command line:

```
doit
```

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

