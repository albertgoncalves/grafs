with import <nixpkgs> {};
mkShell {
    buildInputs = [
        (haskell.packages.ghc865.ghcWithPackages (pkgs: [
            pkgs.containers
            pkgs.hindent
            pkgs.hlint
            pkgs.hoogle
            pkgs.HUnit
            pkgs.psqueues
            pkgs.vector
        ]))
        (python37.withPackages(ps: with ps; [
            flake8
            matplotlib
            numpy
        ]))
        shellcheck
    ];
    shellHook = ''
        . .shellhook
    '';
}
