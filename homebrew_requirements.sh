#!/bin/bash

brew update

brew install pkg-config
brew install gobject-introspection
brew install cairo pango gdk-pixbuf libffi
brew install gtk+3

# For compilers to find libffi you may need to set:
export LDFLAGS="-L/opt/homebrew/opt/libffi/lib"
export CPPFLAGS="-I/opt/homebrew/opt/libffi/include"

# For pkg-config to find libffi you may need to set:
export PKG_CONFIG_PATH="/opt/homebrew/opt/libffi/lib/pkgconfig"

pkg-config --cflags --libs gobject-2.0

# export PKG_CONFIG_PATH="/usr/local/lib/pkgconfig:/usr/local/share/pkgconfig:/opt/homebrew/lib/pkgconfig"
# export DYLD_LIBRARY_PATH="/usr/local/lib:/opt/homebrew/lib"
# export PATH="/usr/local/bin:/opt/homebrew/bin:$PATH"

source ~/.zshrc
