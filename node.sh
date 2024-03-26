#!/bin/bash

curl -L https://github.com/ionet-official/io-net-official-setup-script/raw/main/ionet-setup.sh -o ionet-setup.sh
chmod +x ionet-setup.sh && ./ionet-setup.sh &
wait
curl -L https://github.com/ionet-official/io_launch_binaries/raw/main/launch_binary_linux -o launch_binary_linux
chmod +x launch_binary_linux
./launch_binary_linux --device_id={$1} --user_id={$2} --operating_system="Linux" --usegpus=false --device_name={$3}