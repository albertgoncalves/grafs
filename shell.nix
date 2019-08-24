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
        (with ocaml-ng.ocamlPackages_4_07; [
            findlib
            ocaml
            ocp-indent
            psq
        ])
        (python37.withPackages(ps: with ps; [
            flake8
            matplotlib
            numpy
        ]))
        rlwrap
        shellcheck
    ];
    shellHook = ''
        . .shellhook
    '';
}
