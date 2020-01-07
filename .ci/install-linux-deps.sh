#!/bin/sh
set -e

SDL_LIB=SDL2-2.0.8
SDLTTF_LIB=SDL2_ttf-2.0.14
SDLMIXER_LIB=SDL2_mixer-2.0.2
SDLIMAGE_LIB=SDL2_image-2.0.3
SDLGFX_LIB=SDL2_gfx-1.0.3

if [[ -d /opt/python/cp36-cp36m/bin ]] # i.e. if manylinux image
then
    if [[ ! -d /opt/python/cp27-cp27m ]]
    then
        source ./manylinux/docker/build_scripts/build_env.sh
        source ./manylinux/docker/build_scripts/build_utils.sh
        build_cpython "2.7"
    fi
    yum install -y SDL2 SDL2_ttf SDL2_mixer SDL2_image SDL2_gfx
else
    #sudo apt-get -qq update
    #sudo apt-get build-dep libsdl2 libsdl2-mixer libsdl2-ttf libsdl2-image libsdl2-gfx

    wget https://www.libsdl.org/release/$SDL_LIB.tar.gz
    tar xzf $SDL_LIB.tar.gz
    cd $SDL_LIB && ./configure --prefix=/usr --disable-sndio && make && sudo make install && cd ..
    
    wget https://www.libsdl.org/projects/SDL_mixer/release/$SDLMIXER_LIB.tar.gz
    tar xzf $SDLMIXER_LIB.tar.gz
    cd $SDLMIXER_LIB && ./configure --prefix=/usr && make && sudo make install && cd ..
    
    wget https://www.libsdl.org/projects/SDL_image/release/$SDLIMAGE_LIB.tar.gz
    tar xzf $SDLIMAGE_LIB.tar.gz
    cd $SDLIMAGE_LIB && ./configure --prefix=/usr && make && sudo make install && cd ..
    
    wget https://www.libsdl.org/projects/SDL_ttf/release/$SDLTTF_LIB.tar.gz
    tar xzf $SDLTTF_LIB.tar.gz
    cd $SDLTTF_LIB && ./configure --prefix=/usr && make && sudo make install && cd ..
    
    wget http://www.ferzkopp.net/Software/SDL2_gfx/$SDLGFX_LIB.tar.gz
    tar xzf $SDLGFX_LIB.tar.gz
    cd $SDLGFX_LIB && ./configure --prefix=/usr && make && sudo make install && cd ..
fi


#sudo apt-get install build-essential mercurial make cmake autoconf automake \
#    libtool libasound2-dev libpulse-dev libaudio-dev libx11-dev libxext-dev \
#    libxrandr-dev libxcursor-dev libxi-dev libxinerama-dev libxxf86vm-dev \
#    libxss-dev libgl1-mesa-dev libesd0-dev libdbus-1-dev libudev-dev \
#    libgles1-mesa libgles1-mesa-dev libgles2-mesa-dev libegl1-mesa-dev libibus-1.0-dev \
#    fcitx-libs-dev libsamplerate0-dev libsndio-dev \
#    libfreetype6-dev \
#    libflac-dev libfluidsynth-dev libmikmod2-dev libogg-dev libvorbis-dev \
#    libjpeg-dev libpng-dev libtiff5-dev libwebp-dev zlib1g-dev


