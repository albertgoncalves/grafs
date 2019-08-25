with import <nixpkgs> {};
mkShell {
    buildInputs = [
        (with ocaml-ng.ocamlPackages_4_07; [
            findlib
            ocaml
            ocp-indent
        ])
        (python37.withPackages(ps: with ps; [
            flake8
            matplotlib
        ]))
        shellcheck
    ];
    shellHook = ''
        . .shellhook
    '';
}
