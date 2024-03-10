if [ -f ~/.bashrc ]; then
    source ~/.bashrc
fi

# Install Python packages from requirements_py.txt
pip install -r requirements_py.txt

# Install R packages from requirements_r.txt
while IFS= read -r line; do
    conda install -c conda-forge $line -y
done < requirements_r.txt