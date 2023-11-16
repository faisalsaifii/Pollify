{
  description = "Pollify Slack App";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs";
  };

  outputs = { self, nixpkgs }:
    let

      allSystems = [
        "x86_64-linux" # 64-bit Intel/AMD Linux
        "aarch64-linux" # 64-bit ARM Linux
        "x86_64-darwin" # 64-bit Intel macOS
        "aarch64-darwin" # 64-bit ARM macOS
      ];

      forAllSystems = f: nixpkgs.lib.genAttrs allSystems (system: f {
        pkgs = import nixpkgs { inherit system; };
      });
    in
    {
      # Development environment output
      devShells = forAllSystems ({ pkgs }: {
        default =
          let
            python = pkgs.python311;
          in
          pkgs.mkShell {
            # The Nix packages provided in the environment
            packages = [
              # Python plus helper tools
              (python.withPackages (ps: with ps; [
                flask
                slack-bolt
                python-dotenv
                pymongo
                uuid
              ]))
            ];

            shellHook = ''
              FLASK_APP=app.py python3 -m flask --debug run -p 5001
            '';
          };
      });
    };
}