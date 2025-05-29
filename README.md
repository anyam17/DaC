# DaaC: Detection-Engineering as a Code
This repository is used to conceptualize the automation of detection engineering, such that decoder and rule updates to SIEM tools are automated.

## Configuration
Perform the following configuration steps after cloning the repository.

### SIEM
Perform the following steps on the SIEM endpoint:

1. Navigate to the directory where the decoder and rule files are stored as the working directory. If the decoder and rules files are stored in separate directories, navigate to the parent directory:
```
cd <PATH_TO_RULESETS>
```
2. Create a `gitignore` file in the working directory to ignore other files in the directory from being added to Git:
```
nano .gitignore     # Add directories/files to ignore
```
3. Mark the working directory as safe for Git:
```
git config --global --add safe.directory <PATH_TO_RULESETS>
```
4. Initialize the working directory as a Git repository:
```
git init
```
5. Add a remote repository to your local git to push local changes:
```
git remote add origin <REMOTE_REPOSITORY>
```
6. Configure your Git user identity:
```
git config --global user.name <YOUR_NAME>
git config --global user.email <YOUR_EMAIL_ADDRESS>
```
7. Stage the files for commit in your local Git. Create a new branch `main` and switch to the new branch. Make an initial commit to your local Git:
```
git add .
git checkout -b main
git commit -m "Initial commit"
```
8. Push the changes from your local Git to the remote repository:
```
git push -u origin main
```