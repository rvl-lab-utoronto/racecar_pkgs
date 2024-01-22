#!/bin/bash
# reference: https://forums.developer.nvidia.com/t/vs-code-can-t-launch-with-jetpack-5-0/213980/14
cd
mkdir git 
cd git 
wget https://update.code.visualstudio.com/1.50.0/linux-deb-arm64/stable -O stable.deb
sudo dpkg -i stable.deb

