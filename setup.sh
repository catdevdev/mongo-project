#!/bin/bash

run_terraform() {
    cd ./terraform
    terraform apply --auto-approve
    cd -
}

run_ansible() {
    cd ./ansible
    source ./venv/bin/activate
    ansible-playbook ./playbooks/setup-k3s-cluster.yml
}
run_terraform
sleep 100
run_ansible
