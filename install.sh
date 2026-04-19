#!/bin/bash

set -e

echo "Installing 'speedtype'."

if ! command -v uv &> /dev/null
then
    echo "'uv' is missing. Installing 'uv'."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    echo "'uv' installed"

    if [ -x ~/.local/bin/uv ]; then
        ~/.local/bin/uv tool install --python 3.14 git+https://github.com/TypeSpeedOrg/speedtype
    else
        echo "Please restart your shell and run this script again."
        exit 0
    fi
else
    uv tool install --python 3.14 git+https://github.com/TypeSpeedOrg/speedtype
fi

echo ""
echo "'speedtype' is installed!"
echo ""
echo "Run 'speedtype' to launch."
