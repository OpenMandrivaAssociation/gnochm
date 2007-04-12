# gnochm.spec
%define name gnochm
%define version 0.9.9
%define release %mkrel 1

%define Summary A chm file viewer for gnome
%define title	Gnochm
%define section Applications/Publishing 

Summary: 	%Summary
Name: 		%name
Version: 	%version
Release: 	%release
License: GPL
Group: 		Graphical desktop/GNOME
URL: http://gnochm.sourceforge.net/

Source: 	http://prdownloads.sourceforge.net/gnochm/%{name}-%{version}.tar.bz2
Source1:	%name-16.png
Source2:	%name-32.png
Source3:	%name.png

Patch:		gnochm-makefile.patch
Patch1:         gnochm.py.in.patch

BuildRoot: 	%_tmppath/%{name}-%{version}-%{release}-buildroot

BuildRequires: scrollkeeper libGConf2-devel
# needed for aclocal
BuildRequires: intltool
Requires(post): desktop-file-utils 
Requires(postun): desktop-file-utils

Requires: pygtk2.0-libglade, gnome-python
Requires: gnome-python-bonobo gnome-python-gtkhtml2
Requires: gnome-python-gconf gnome-python-gnomevfs
Requires: python-chm 
BuildArch: noarch
%description
A CHM file viewer for Gnome. Features are:
  
  * Full text search
  * Bookmarks
  * Support for external ms-its links
  * Configurable support for http links 
  * Internationalisation

# Prep
%prep
%setup -q

%patch -p0 -b .makefile
%patch1 -p0 -b .makefile

#rebuild
aclocal
autoconf
automake

%build
%configure2_5x --prefix=%buildroot 

%make WARN_CFLAGS=""

%install
rm -rf %buildroot
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std UPDATE_MIME_DATABASE=true UPDATE_DESKTOP_DATABASE=true

%find_lang %name --with-gnome

# menu
mkdir -p %buildroot/%_menudir
cat > %buildroot/%_menudir/%name << EOF
?package(%name): \
command="%_bindir/%name" \
needs="x11" \
icon="%name.png" \
section="%section" \
title="%title" \
longtitle="%Summary" \
xdg="true"
EOF

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=GnoCHM
Comment=A chm file viewer for gnome
Exec=%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Office;Viewer;X-MandrivaLinux-Office-Presentations;
EOF


# icon
mkdir -p %buildroot/{%_liconsdir,%_iconsdir,%_miconsdir}
#install -m 644 src/pixmaps/%name.png %buildroot/%_datadir/pixmaps/%name.png
install -m 644 %SOURCE1 %buildroot/%_miconsdir/%name.png
install -m 644 %SOURCE2 %buildroot/%_liconsdir/%name.png
install -m 644 %SOURCE3 %buildroot/%_iconsdir/%name.png

%post
%{update_desktop_database}

%update_menus
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/gnochm.schemas > /dev/null
if [ -x %{_bindir}/scrollkeeper-update ]; then %{_bindir}/scrollkeeper-update -q; fi
touch %{_datadir}/gnome/help/%{name}/C/%{name}.html
if [ -x %{_bindir}/yelp-pregenerate ]; then %{_bindir}/yelp-pregenerate %{_datadir}/gnome/help/%{name}/*/%name.xml > /dev/null; fi
%{_bindir}/update-mime-database %{_datadir}/mime/

%preun
if [ $1 -eq 0 ]; then
  GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/gnochm.schemas > /dev/null
fi

%postun
%{clean_desktop_database}
%clean_menus
if [ -x %{_bindir}/scrollkeeper-update ]; then %{_bindir}/scrollkeeper-update -q; fi
if [ "$1" = "0" ]; then %{_bindir}/update-mime-database %{_datadir}/mime; fi

%clean
rm -rf %buildroot

%files -f %name.lang
%defattr(-,root,root)

%doc ABOUT-NLS AUTHORS COPYING ChangeLog NEWS README
%config(noreplace) %{_sysconfdir}/gconf/schemas/gnochm.schemas

%{_bindir}/gnochm
%dir %{_datadir}/gnochm/
%dir %{_datadir}/gnochm/glade/
%{_datadir}/gnochm/glade/*.glade
%{_datadir}/omf/gnochm/
%{_datadir}/pixmaps/*
%{_datadir}/applications/*
%{_datadir}/mime-info/gnochm.*
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/application-registry/gnochm.*
%_menudir/%name
%_liconsdir/%name.png
%_miconsdir/%name.png
%_iconsdir/%name.png

