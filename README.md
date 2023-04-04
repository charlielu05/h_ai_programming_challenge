# h_ai_programming_challenge

Submission for Harrison AI

## Dependencies and Setup
```
Host OS: Ventura 13.2.1 (Mac)
Host Docker: 20.10.17, build 100c701
OS: Debian, 11-Bullseye
Python: 3.10.10
```
VS Code Devcontainers used for development environment setup. There are three ways to reproduce environment: <br>
- Github Instructions: https://docs.github.com/en/codespaces/getting-started/quickstart
- VSCode Instructions: https://code.visualstudio.com/docs/devcontainers/containers
- Manual setup: The Dockerfile specs used can be found here: https://github.com/microsoft/vscode-dev-containers/blob/main/containers/python-3/README.md
    - Pip Tools was added to generate the `requirements.txt`
        - `pip install pip-tools`

### Host Docker Settings
```
CPU: 6
Memory: 12GB
Swap: 3GB
Disk Image: 200GB
Experimental Features: All disabled
```