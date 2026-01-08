#!/bin/bash
sudo source .venv/bin/activate
sudo ip addr flush dev eth0
sudo ip addr add 192.168.1.10/24 dev eth0
sudo ip link set eth0 up
ip -br a
eth0  UP  192.168.1.10/24
ping 192.168.1.150
