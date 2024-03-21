{ pkgs }: {
  deps = [
    pkgs.redis
    pkgs.python-launcher
    pkgs.vim-full
  ];
  environment.systemPackages = [
    pkgs.redis
  ];
}