# shell.nix
let
    pkgs = import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/cf8cc1201be8bc71b7cbbbdaf349b22f4f99c7ae.tar.gz") {};
in pkgs.mkShell {
    buildInputs = [ 
        pkgs.libGL # for opengl
            #pkgs.mesa # for opengl
            #pkgs.vulkan-loader # for opengl

        # raylib's dependencies  
        pkgs.mesa
        pkgs.alsa-lib
        pkgs.xorg.libX11.dev # adding the dev doesn't make a difference as far as I can tell
        pkgs.xorg.libXft
        pkgs.xorg.libXinerama
        pkgs.xorg.xorgproto
    ];
    packages = [
        (pkgs.python3.withPackages (python-pkgs: [
            python-pkgs.pygame
            python-pkgs.pyopengl
            python-pkgs.tkinter
        ]))
    ];
    nativeBuildInputs = with pkgs; [
            #pkg-config
    ];
    shellHook = "
        export FONTCONFIG_FILE=${pkgs.fontconfig.out}/etc/fonts/fonts.conf
        export FONTCONFIG_PATH=${pkgs.fontconfig.out}/etc/fonts/
        #export LD_LIBRARY_PATH=${pkgs.vulkan-loader}/lib
        #export SDL_VIDEO_DRIVER=edl
    ";
}
