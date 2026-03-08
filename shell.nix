{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python312
    uv
  ];

  shellHook = ''
    export OPENROUTER_API_KEY="{YOUR_KEY}"
  '';
}
