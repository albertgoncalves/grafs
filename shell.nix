with import <nixpkgs> {};
mkShell {
    buildInputs = [
        (python37.withPackages(ps: with ps; [
            flake8
            matplotlib
            pytest
        ]))
        go
        shellcheck
    ];
    shellHook = ''
        . .shellhook
    '';
}
