toolbox create -y | true
toolbox run python3 -m pip install pipreqs
toolbox run python -m ensurepip --upgrade
toolbox run sudo dnf install -y python3-tkinter zsh
toolbox run python3 -m pip install -r requirements.txt
toolbox run zsh
# toolbox enter