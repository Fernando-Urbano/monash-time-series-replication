# Set a CRAN mirror
options(repos = c(CRAN = "https://cloud.r-project.org"))

# Required packages with their versions specified
packages_with_versions <- list(
  forecast = "8.13" # Specified in the original repository
  # glmnet = "4.0.2", # Specified in the original repository
  # smooth = "2.6.0" # Specified in the original repository
)

# Function to install specific versions of packages if they are not already installed
install_if_missing_with_version <- function(packages_with_versions) {
  # Ensure the remotes package is installed
  if (!"remotes" %in% installed.packages()[, "Package"]) {
    install.packages("remotes")
  }
  
  for (package in names(packages_with_versions)) {
    version <- packages_with_versions[[package]]
    
    # Check if package is installed
    if (!package %in% installed.packages()[, "Package"]) {
      remotes::install_version(package, version)
    } else {
      # Check if installed version matches the desired version
      installed_version <- as.character(packageVersion(package))
      if (installed_version != version) {
        message(sprintf("Updating %s from version %s to %s", package, installed_version, version))
        remotes::install_version(package, version)
      }
    }
  }
}

# Install the packages with specified versions
install_if_missing_with_version(packages_with_versions)
