# -*- mode: ruby -*-
# vi: set ft=ruby :


Vagrant.configure(2) do |config|
 

  config.vm.provision "shell", path: "pg_config.sh"
  config.vm.box = "ubuntu/trusty64"
  config.vm.network "forwarded_port", guest: 5005, host: 5005
  
  
end
