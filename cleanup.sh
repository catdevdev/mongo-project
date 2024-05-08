#!/bin/bash

run_ansible() {
    cd ./ansible
    source ./venv/bin/activate
    ansible-playbook ./playbooks/remove-k3s-from-on-prem.yml
}

run_terraform() {
    cd ./terraform
    terraform destroy --auto-approve
}

run_ansible &
run_terraform &

wait
