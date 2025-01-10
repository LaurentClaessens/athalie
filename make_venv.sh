#!/bin/bash

set -u

MAIN_DIR=$(pwd)
VENV_DIR="$MAIN_DIR/venv"
BIN_DIR="$VENV_DIR/bin"
PYTHON_VERSION=3.13.1
pyenv_dst=~/.pyenv
PYTHON3="$pyenv_dst/versions/$PYTHON_VERSION/bin/python3"



function install_pyenv()
{
	if [ -e "$PYTHON3" ]; then
  	echo "The pyenv binary $PYTHON3 exists."
		return
  fi

	echo "I will install pyenv in $pyenv_dst".
	read -p "Is it ok ? " -n 1 -r
	echo
	if [[ $REPLY =~ ^[Yy]$ ]]
	then
		git clone https://github.com/pyenv/pyenv.git $pyenv_dst
		cd $pyenv_dst
		git pull
		yes n | $pyenv_dst/bin/pyenv install -v $PYTHON_VERSION
	else
		echo "Change the variable `pyenv_dst` in `make_pyenv.sh`"
		echo "and launch again."
		exit 1
	fi

}

function create_venv()
{
	echo "Creating the virtual environment"
	"$PYTHON3" -m venv "$VENV_DIR"

	cd "$BIN_DIR" || exit 1
	./python3 -m pip install --upgrade pip
}

function pip_install()
{
	cd "$BIN_DIR" || exit 1
	./pip3 install -r "$MAIN_DIR/requirements.txt"
	# ./pip3 freeze
}


install_pyenv
create_venv
pip_install
