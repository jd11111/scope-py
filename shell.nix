{ pkgs ? import <nixpkgs> {} }:
(pkgs.buildFHSUserEnv {
  name = "simple-python-env";
  targetPkgs = pkgs: (with pkgs; [
    libusb1
    python3
  ]);
  runScript ="bash";
}).env

