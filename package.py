# -*- coding: utf-8 -*-
import inspect
import os

# Force calculate current file path from source file of dummy function
__file__ = os.path.abspath(inspect.getsourcefile(lambda: None))
__dir__ = os.path.dirname(__file__)

name = "vscodium"

# Vendor packages: <vendor_version>+local.<our_version>
__version__ = "1.59.0"
version = __version__ + "+local.1.0.0"

description = "Vim-fork focused on extensibility and usability."

authors = ["Joseph Yu"]

variants = [["os-centos-7", "arch-x86_64"]]

tools = ["vscodium"]
# @late()
# def tools():
#     import os
#     bin_path = os.path.join(str(this.root), 'bin')
#     executables = []
#     for item in os.listdir(bin_path):
#         path = os.path.join(bin_path, item)
#         if os.access(path, os.X_OK) and not os.path.isdir(path):
#             executables.append(item)
#     return executables

build_requires = ["requests"]

# build_command = [os.sys.executable, os.path.join(__dir__, "install.py")]
build_command = r"""
set -euf -o pipefail

CURL_FLAGS=("-L")
[ -t 1 ] && CURL_FLAGS+=("-#") || CURL_FLAGS+=("-sS")

if [ ! -x vscodium.appimage ]
then
    # Mostly targeting latest release hence page=1&per_page=1
    read -r URL < <( curl -H "Accept: application/vnd.github.v3+json" \
      'https://api.github.com/repos/VSCodium/vscodium/releases?page=1&per_page=1' \
      | grep -oP '(?<="browser_download_url": ").*{version}.*appimage')

    curl "{CURL_FLAGS}" "$URL" > vscodium.appimage
    chmod u+x vscodium.appimage

    ./vscodium.appimage --appimage-extract &> /dev/null
fi

if [ $REZ_BUILD_INSTALL -eq 1 ]
then
    cd "$REZ_BUILD_INSTALL_PATH"
    cp -r -t . \
        "$REZ_BUILD_PATH"/squashfs-root/usr/share \
        "$REZ_BUILD_PATH"/vscodium.appimage

    mkdir bin
    ln -vrsf vscodium.appimage bin/vscodium
fi
""".format(
    version=__version__,
    CURL_FLAGS="${{CURL_FLAGS[@]}}",
)


def commands():
    """Commands to set up environment for ``rez env vscodium``"""
    import os
    env.PATH.append(os.path.join("{root}", "bin"))
    env.XDG_DATA_DIRS.append(os.path.join("{root}", "share"))

