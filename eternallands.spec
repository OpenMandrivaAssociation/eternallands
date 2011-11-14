Name:		eternallands
Summary:	A free to play, graphical MMORPG client
Version:	1.9.2
Release:	%mkrel 1
License:	QTPL-based
Group:		Games/Adventure
URL:		http://www.eternal-lands.com
# it's better to get sources from here than from git:
# http://ppa.launchpad.net/pjbroad/ppa/ubuntu/pool/main/e/
Source0:	%{name}-%{version}.tar.gz
Patch0:		eternallands-1.9.2-wrapper.patch
Patch1:		eternallands-1.9.2-linking.patch
Patch2:		eternallands-1.9.2-verbose.patch
BuildRequires:	cal3d-devel
BuildRequires:	libvorbis-devel
BuildRequires:	libxml2-devel
BuildRequires:	MesaGL-devel
BuildRequires:	MesaGLU-devel
BuildRequires:	openal-devel
BuildRequires:	png-devel
BuildRequires:	SDL-devel
BuildRequires:	SDL_image-devel
BuildRequires:	SDL_net-devel
BuildRequires:	libx11-devel
BuildRequires:	zlib-devel
Requires:	zenity
Requires:	%{name}-data = %{version}
BuildRoot:	%{_tmppath}/%{oname}-%{version}-%{release}-buildroot

%description
Eternal Lands is a free to play, graphical MMORPG (massively-multi-player
online role-playing game).  Different from other role-playing games, there are
no fixed classes so you can improve any of the many skills.  There is a choice
of several character races but all are equal.

%prep
%setup -q
%patch0 -p1 -b .wrapper
%patch1 -p1 -b .linking
%patch2 -p1 -b .verbose

%build
sed -i s,-march=i686,,g make.conf
%make -f Makefile.linux

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Eternal Lands
Comment=%{summary}
Exec=%{_gamesbindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=Game;AdventureGame;
EOF

install -d %{buildroot}%{_datadir}/pixmaps
cp pkgfiles/%{name}.png %{buildroot}%{_datadir}/pixmaps/

# game binary and wrapper
install -d %{buildroot}%{_gamesbindir}
cp el.x86.linux.bin %{buildroot}%{_gamesbindir}/
cp pkgfiles/%{name} %{buildroot}%{_gamesbindir}/

# man files 
install -d %{buildroot}%{_mandir}/man6
cp pkgfiles/*.6 %{buildroot}%{_mandir}/man6/

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%files
%defattr(-,root,root)
%doc CHANGES TODO eternal_lands_license.txt
%{_gamesbindir}/*
%{_datadir}/applications/mandriva-%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_mandir}/man6/*

