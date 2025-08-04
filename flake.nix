{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    treefmt-nix.url = "github:numtide/treefmt-nix";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      self,
      nixpkgs,
      treefmt-nix,
      flake-utils,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};

        treefmtEval = treefmt-nix.lib.evalModule pkgs ./treefmt.nix;
        defaultPkg = self.packages.${system}.default;
      in
      {
        packages = {
          default = pkgs.callPackage ./. {
            inherit (pkgs.python3Packages)
              buildPythonApplication
              orjson
              pydantic
              wikipedia
              pytestCheckHook
              setuptools
              setuptools-scm
              thefuzz
              ;
          };
        };

        devShells = {
          default = pkgs.mkShell {
            venvDir = ".venv";
            packages =
              with pkgs;
              [
                python3
                meson
              ]
              ++ (with pkgs.python3Packages; [
                pip
                venvShellHook
                setuptools
                setuptools-scm
                pytest
              ])
              ++ defaultPkg.dependencies;
          };
        };

        formatter = treefmtEval.config.build.wrapper;

        checks = {
          formatting = treefmtEval.config.build.check self;
        };
      }
    );
}
