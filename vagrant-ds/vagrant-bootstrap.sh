#!/usr/bin/env bash

# zsh
sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

# pyenv and python 3.7
curl https://pyenv.run | bash

cat >> /home/vagrant/.zshrc << 'EOF'

export PATH="$PATH:/home/vagrant/.pyenv/bin"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
EOF

source .zshrc

# Python 3.7
pyenv install 3.7.3

pyenv global 3.7.3

# Update pip
#pip install --upgrade pip

# Jupyter and IPython
#pip install jupyter ipython
