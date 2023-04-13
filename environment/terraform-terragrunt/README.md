TODO: move to ansible automation

1. Install Terraform

https://developer.hashicorp.com/terraform/downloads

2. Or install tfenv

git clone --depth=1 https://github.com/tfutils/tfenv.git ~/.tfenv

3. Install tgenv

3.1 git clone https://github.com/cunymatthieu/tgenv.git ~/.tgenv

4. Install deprecated terragrunt version

Terragrunt v0.18.7 We recommend use of tgenv to install and handle different versions. After the installation of tgevn, you would notice that it is not possible to install v0.18.7 using $ tgenv install 0.18.7 because the version has been deprecated and can only be installed manually. To manually install v0.18.7: 

Download the terragrunt executable from terragrunt releases manually (https://github.com/gruntwork-io/terragrunt/releases/tag/v0.18.7) to your ~/Downloads directory (don't use any command). Using curl to download in macOS has given some errors therefore its advisable to download manually by right clicking on the corresponding version and clicking 'Download'.

Create a directory named after the version of terragrunt downloaded (0.18.7 in this case) and : mkdir -p  ~/.tgenv/versions/0.18.7/ 

Move the download executable to the newly created directory:cd ~/.tgenv/versions/0.18.7/ && mv ~/Downloads/terragrunt_darwin_amd64 .

Rename the executable to “terragrunt”:mv terragrunt_darwin_amd64 terragrunt

Make the downloaded executable runnable from your machine:chmod u+x terragrunt

Confirm everything by using this new version: tgenv use 0.18.7

Add tgenv to the PATH adding to your .bash_profile or .zshrc file the following line: export PATH="$HOME/.tgenv/bin:$PATH"

5. Edit PATH

export PATH=$HOME/bin:/home/${DEFAULT_USER}/.local/bin:$HOME/.tgenv/bin:$HOME/.tfenv/bin:$PATH

6. Test 

tfenv
tgenv