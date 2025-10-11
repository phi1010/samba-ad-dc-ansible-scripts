How to use:
```sh
# Install uv first
# Create a venv
# Install ansible
# Optional: install xfreedrp3 or remmina for RDP (required by rdp.py)
# Optional: install sshpass for ansible ssh password authentication (required by pssh.sh)
./build.sh
./ansible-playbook.sh install-playbook.yaml
./ansible-playbook.sh maintain-playbook.yaml
./rdp.py --domain "." to log in with the local user to the windows machine
./rdp.py --domain "AD" to log in with the AD user to the windows machine
```
