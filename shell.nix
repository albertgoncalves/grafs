with import <nixpkgs> {};
mkShell {
    buildInputs = [
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
