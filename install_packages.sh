if [ -f ~/.bashrc ]; then
    source ~/.bashrc
fi

if [[ "$OSTYPE" == "darwin"* ]]; then
    while IFS= read -r line; do
        conda install -c conda-forge "$line" -y
    done < requirements_r_mac.txt
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    while IFS= read -r line; do
        conda install -c conda-forge "$line" -y
    done < requirements_r_linux.txt
elif [[ "$OSTYPE" == "msys"* || "$OSTYPE" == "cygwin"* || "$OSTYPE" == "win32"* ]]; then
    while IFS= read -r line; do
        conda install -c conda-forge "$line" -y
    done < requirements_r_windows.txt
fi

# Install Python packages from requirements_py.txt
pip install -r requirements_py.txt