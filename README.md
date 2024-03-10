Monash Time Series Forecasting Replication
==================

# 1. About this Project
In this project we attempt to replicate results from a 2021 paper on the motivation and creation of the Monash Time Series Forecasting Archive, a project spearheaded by a group time series researchers from Monash University and the University of Sydney.

The archive contains datasets spanning multiple domains (industries) as well as 13 forecasting models, 6 of which are canonical univariate models, and 7 of which are global models that have shown positive results in recent years.

The researchers aimed to generate a repository and paper to showcase and compare the performance of time-series models in different public datasets.

We invite you to take a look at their work as well:
- [Website](https://forecastingdata.org/)
- [Paper](https://openreview.net/pdf?id=wEc1mgAjU-)
- [Repository](https://github.com/rakshitha123/TSForecasting)

## 1.1. Goal
Our main goal is to replicate Table 1 and Table 2 from the paper in an automated way using `conda` environment and `dodo`, generating a Latex file with a short analysis and challenges found in the process.

# 2. Build the Enviromnet
Using R and Python together inside conda is sometimes a problem, specially when dealing with older package versions.

During the creation and updates of the project, we have run into different problems and have found ways to work with both Mac and Windows.

## 2.1. Install TexLive
Check that you have installed TexLive. TexLive is useful to generate pdfs from latex files. If it is not currently installed in your computer, you can download it here:

- [Windows installer](https://tug.org/texlive/windows.html#install)
- [Mac installer](https://tug.org/mactex/mactex-download.html)

## 2.2. Update Your Version of Conda
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

## 2.3. Install CMake
CMake is a software helpful (and sometimes necessary) to run specific R packages with C and C++ dependencies.

Check if CMake is already installed in your computer. If it is installed, go to step 4.

If not, acess the following link or install it via `brew`:

- [Install CMake](https://cmake.org/download/)

Or:

```bash
brew install cmake
```

## 2.4. Create Conda Virtual Env
Clone the repository in your local machine, open a terminal in the main folder and run:

```bash
conda deactivate
```

If you have already created a `mtsr` before, delete it before recreating:

```bash
conda remove --name mtsr --all
```

If your operating system is Mac or Linux, run:

```bash
conda create -n mtsr -c conda-forge python=3.11.8 r-base=4.3.2
```

If your operating system is Windows:

```bash
conda create -n mtsr -c conda-forge python=3.11.8 r-base=4.1.3
```

Finally, activate the virtual environment created.

```bash
conda activate mtsr
```

The versions specified of R and Python are the ones that work best for the anaconda distribution. Windows and Mac have different versions of `r-base` given the same `conda` version. The same divergence happens for `r-glmnet` package.

The original project was created using R: `4.0.2`, Python: `3.7.4`, which is not a possible option, considering recent versions of `conda`.

For the following steps, it is crucial that the `mtsr` virtual environment is current active.

Inside command line, run:

```bash
chmod +x install_packages.sh
```

This should make `install_packages` executable.

If running in Windows, ensure that you can add the run `bashrc` by specifying the paths:

```
. C:/{path-to-conda}/anaconda3/etc/profile.d/conda.sh
export PATH="C:/Users/{path-to-conda}/anaconda3/bin/Scripts:$PATH"
```

If you are running in Windows and it does not work, copy the content `install_packages.sh`, paste into the command line and run it (while less automated, it might even be a simpler solution for Windows).

Otherwise, run the following:

```bash
./install_packages.sh
```

If the script does not work, do the same procedure suggested for Windows before: copy the content `install_packages.sh`, paste into the command line and run it.

The `install_packages.sh` is a bash script that:
- In the case of Windows, uses `source ~/.bashrc` in case it exists to ensure the rest of the file executable.
- iterates and install R packages via `conda forge` based on the OS system that you have.
- Install Python packages via `pip`.

The different OS systems have different versions of the R packages inside conda. This happen even when the version of conda is the same.

Currently:
- `r-glmnet` best version available in Windows is `r-glmnet=4.1_2` and in Mac is `r-glmnet=4.1.8`.
- `r-base` best version available in Windows is `4.1.3` and in Mac `4.3.2`.

All the installed packages can be found in:
- `requirements_py.txt`
- `requirements_r_mac.txt`
- `requirements_r_windows.txt`
- `requirements_r_linux.txt`

If other packages need to be installed and you would like to check their versioning, refer to the Appendix (in the end of README).

Make sure to check the versions of R packages available in conda for other OS systems.

## 2.5. Run dodo
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
CHOSEN_MODELS = {
    'all': False, # All overrides the rest
    'arima': False,
    'catboost': False,
    'ets': False,
    'pooled_regression': False,
    'tbats': False,
    'ses': False,
    'theta': False,
    'dhr_arima': False,
}


CHOSEN_DATASETS = [
    'm1_yearly_dataset'
]
```

If you select `all` for `CHOSEN_MODELS`, all available models will be updated for the selected dataset.

If you select `all` for `CHOSEN_DATASETS`, all available datasets will be updated for the selected models.

If the `CHOSEN_DATASETS` list is empty or the `CHOSEN_MODELS` values are all `False`, no models will be updated.

In your first trial, we invite you to check the results with all the `CHOSEN_MODELS` values equal to `False` in order to ensure that the Latex file is updated. It would still work, since we keep the key results from previous updates.

After setting the lists as wanted, run (from the main folder - not from `src`) inside the command line:

```bash
doit
```

The command should do every step from downloading the data until updating the pdf.

# 3. General Directory Structure
For our project, we are using the `doit` Python module as a task runner. It works like `make` and the associated `Makefile`s. To rerun the code, install `doit` (https://pydoit.org/) and execute the command `doit`. Note that doit is very flexible and can be used to run code commands from the command prompt, thus making it suitable for projects that use scripts written in multiple different programming languages.

Furthermore, `doit` can be executed specifying which tasks will run. For instance, if you want to just run the models:

```bash
doit download_data
```

```bash
doit update_chosen_models_and_datasets
```

```bash
doit run_fixed_horizon_R_script
```

 - The `output` folder contains tables and figures that are generated from code. The entire folder should be able to be deleted, because the code can be run again, which would again generate all of the contents.

- The `results` is the folder in which the results of the models are stored. Inside, we have:
  - `fixed_horizon_errors`: has the error metric for each time-series of the dataset and a joint error metric for the dataset.
  - ``

# 3. Appendix: Add more Packages to the Virtual Environment
If needed to add more packages to the environment use the `requirements_py.txt` to add Python packages and `requirements_r.txt` to add R packages.

It is necessary to specify the version used.

R packages have a bigger specification and are harder to add. Before adding an R package, run the the command line:

```bash
conda search -c conda-forge r-{package-name} --info
```

It will give you the version of the package that works for the current version of R we have in the virtual environment. Make sure to add the package version that is viasible for the current version of our environment.

For instance, if you want to install tidyverse:

```bash
conda search -c conda-forge r-tidyverse --info
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
