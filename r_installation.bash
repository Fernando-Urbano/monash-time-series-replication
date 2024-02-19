install_package() {
    package=$1
    version=$2
    echo "Attempting to install $package version $version..."

    # Try installing binary version first
    Rscript -e "options(pkgType = 'binary'); install.packages('$package', version = '$version')"

    if [ $? -ne 0 ]; then
        echo "Binary installation for $package failed. Attempting source installation..."
        # If binary installation fails, try installing from source
        Rscript -e "options(pkgType = 'source'); install.packages('$package', version = '$version')"
    fi

    if [ $? -ne 0 ]; then
        echo "Installation for $package failed."
    else
        echo "$package installed successfully."
    fi
}

declare -A packages=(
    ["RcppArmadillo"]="0.12.8.0.0"
    ["forecast"]="8.12"
    ["glmnet"]="4.0.2"
    ["smooth"]="2.6.0"
)

# Loop through the packages array and install each
for package in "${!packages[@]}"; do
    install_package $package ${packages[$package]}
done

echo "All installations attempted."