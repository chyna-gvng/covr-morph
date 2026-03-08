{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python312
    uv
    pango
    glib
    cairo
    fontconfig
    harfbuzz
  ];

  shellHook = ''
    export LD_LIBRARY_PATH=${pkgs.lib.makeLibraryPath (with pkgs; [
      pango
      glib
      cairo
      fontconfig
      harfbuzz
    ])}
    export OPENROUTER_API_KEY="{YOUR_KEY}"
  '';
}
