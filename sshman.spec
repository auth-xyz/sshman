Name:     sshman
Version:  0.2.4
Release:  1%{?dist}
Summary:  A SSH manager based on sessions
License:  MIT
URL:      https://github.com/auth-xyz/sshman
Source0:  https://github.com/auth-xyz/sshman/releases/download/v0.2.4/linux-snow-dome.tar.gz

<<<<<<< HEAD
BuildRequires: python3
BuildRequires: wget
=======
BuildRequires: python3 wget
>>>>>>> refs/remotes/origin/main

Requires(post): info
Requires(preun): info

%define url https://github.com/auth-xyz/sshman/releases/download/v0.2.4/linux-snow-dome.tar.gz

%description
sshman is a simple SSH manager which creates and manages sessions.

%prep
# Making directories
mkdir -p $HOME/.sshm/
mkdir -p $HOME/.sshm/.bin
mkdir -p $HOME/.sshm/.cache

# Downloading latest version and extracting
wget %{url} -O %{_sourcedir}/linux-snow-dome.tar.gz
tar xvfz %{_sourcedir}/linux-snow-dome.tar.gz --directory %{_sourcedir}

mv %{_sourcedir}/sshman $HOME/.sshm/.bin/
sudo ln -s $HOME/.sshm/.bin/sshman /usr/bin


%build
# nothing to build

%install
#%make_install
#%find_lang %{name}
rm -f %{buildroot}/%{_infodir}/dir


%post
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :


%doc README.md

%changelog
* Sat Aug 19 2023 Auth P <smmc.auth@gmail.com> 
- Initial version of the package

