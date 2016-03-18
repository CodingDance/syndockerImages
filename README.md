# syndockerImages

###This project is used to syn the images from the dockerhub. This project is written by python.

### In the docker,docker images is the most important. Docker hub develop some images,and that is tested by Official.So we can trust this images.

###This tools is to pull the offical images and push to your private repo.




### Before you run this project，first you need to install some software.
- install pip: "sudo apt-get install python-pip"
- install configobj: "install configobj"
- install daomonit: "curl -L -o /tmp/daomonit_amd64.deb https://get.daocloud.io/daomonit/daomonit_amd64.deb
- sudo dpkg -i /tmp/daomonit_amd64.deb"


###config daomonit ,so you can use dao cmd to speed pull images
- sudo daomonit -token=e3240fa65bed6b4c4c5585c348a95cc5a6c17db1 save-config
- sudo service daomonit start
