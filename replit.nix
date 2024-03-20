{ pkgs }: {
  deps = [
    pkgs.python-launcher
    pkgs.vim-full
  ];
  environment.systemPackages = [
    pkgs.rabbitmq-server
  ];
}