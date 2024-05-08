#!/bin/bash



run_ansible() {
    cd ./ansible
    source ./venv/bin/activate
    ansible-playbook ./playbooks/setup-k3s-cluster.yml
}

run_ansible
