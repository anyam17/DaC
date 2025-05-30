# DaaC: Detection-Engineering as a Code

This repository is used to conceptualize the automation of detection engineering, in a way that the integration of rulesets such as: decoders and rules to SIEM tools are automated. This approach to detection engineering allows for faster and effective collaboration among security engineers. It also limits access to the SIEM endpoint and reduces collaboration errors in production environments.

This concept can be adapted to work with any SIEM solution by following the guide, even though [Wazuh](https://wazuh.com/) is used to develop and test this concept.

# Guide

## Requirements
Ensure that the following requirements are met to use this repository with ease:
* Ensure that [Git](https://git-scm.com/) is installed on the SIEM host.
* Ensure that the SIEM host is accessible on the internet by assigning a public IP or NAT if behind a firewall.
* Ensure that port `22` or your custom SSH port is open on the public IP address.
* Ensure that the SIEM host is provisioned with a public/private key pair, to allow for SSH login.
* Clone the parent [DaaC](https://github.com/SamsonIdowu/DaaC.git) repository to use its GitHub Actions workflow file.


## Configuration
Perform the configuration steps after meeting the above requirements.

### SIEM
Perform the following steps on the SIEM endpoint:

1. Navigate to the directory where the decoder and rule files are stored. If the decoder and rules files are stored in separate directories, navigate to the parent directory:
```
cd <FULL_PATH_TO_RULESETS>    # Working directory
```
2. Create a `.gitignore` file in the working directory to ignore other files in the directory from being added to Git:
```
nano .gitignore     # Add directories/files to ignore
```
3. Mark the working directory as safe for Git:
```
git config --global --add safe.directory <FULL_PATH_TO_RULESETS>
```
4. Initialize the working directory as a Git repository:
```
git init
```
5. Add a remote repository to your local Git to push local changes:
```
git remote add origin <REMOTE_REPOSITORY>
```
6. Configure your Git user identity:
```
git config --global user.name <YOUR_NAME>
git config --global user.email <YOUR_EMAIL_ADDRESS>
```
7. Stage the files for commit in your local Git. Create a new branch `main` and switch to the new branch. Make an initial commit to your local Git repository:
```
git add .
git checkout -b main
git commit -m "Initial commit"
```
8. Push the changes from your local Git repository to the `main` branch of remote repository:
```
git push -u origin main --force
```

### GitHub (Remote Repository)

Perform the following steps on your GitHub repository (remote repository) after pushing local changes:

1. Edit the GitHub Actions workflow file `.github/workflows` > `automation.yml` to adapt it to your SIEM tool.
2. Navigate to **Settings** > **Secrets and variables** > **Actions** > **Secrets** to create the following repository secrets to be used by GitHub Actions:

|**Name**     |**Secret**                     |
|-------------|-------------------------------|
| USERNAME    | <USERNAME_OF_SIEM_HOST>       |
| HOST        | <PUBLIC_IP_OF_SIEM_HOST>      |
| SSH_KEY     | <PUBLIC_KEY_OF_SIEM_HOST>     |
| PORT        | <SSH_PORT_OF_SIEM_HOST>       |
3. Ensure that a `dev` branch is created if it does not not already exist.
4. Create a pull request to merge the changes on the `main` branch to the `dev` branch. This will update the `dev` branch with the recent changes from the local Git repository and the `automation.yml` file.


## Usage
This guides the use of the repository to create new or modify existing rulesets for automatic integration with the SIEM after completing configuration.

### **Warning:** 
*Perform all usage operations in the `dev` branch for code reviews before merging to the `main` branch to minimize deployment errors in production.*

- ### Creating or Modifying Custom Decoders
Create new or modify existing custom decoders in the `decoders` directory of the repository. This may vary depending on the directory structure of your SIEM.

- ### Creating or Modifying Custom Rules
Create new or modify existing custom rules in the `rules` directory of the repository. This may vary depending on the directory structure of your SIEM.

