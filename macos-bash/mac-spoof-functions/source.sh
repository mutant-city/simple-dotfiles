alias rand_mac="openssl rand -hex 6 | sed 's/\(..\)/\1:/g;s/.$//'"

# changes the mac address, this will be reset back to factory Mac upon reboot
# the parameter is the interface you want to change(typically en0)
spoof_mac(){
    NEW_MAC=`rand_mac`
    sudo ifconfig $1 ether $NEW_MAC
    echo "New mac addy: $NEW_MAC"
}
alias spoof_mac=spoof_mac
