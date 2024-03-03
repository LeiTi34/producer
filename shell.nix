{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
    name = "python-shell";
    req = ./requirements.txt;
    venv = ".venv";
    buildInputs = with pkgs;with pkgs; [
        gcc
        glibc
        libcxx
        python3Full
        python3Packages.pip
        git
        gitRepo 
    ];
    # system = builtins.currentSystem;
    shellHook = ''
        export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${pkgs.stdenv.cc.cc.lib}/lib/
        # Setup the virtual environment if it doesn't already exist.
        if test ! -d $venv; then
          virtualenv $venv
          source ./$venv/bin/activate
          pip install -r $req
        else
          source ./$venv/bin/activate
        fi
    '';
}
