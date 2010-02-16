# gnochm.spec
%define name gnochm
%define version 0.9.11
%define release %mkrel 4

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
BuildRequires: intltool gettext-devel gnome-common
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

Requires: pygtk2.0-libglade, gnome-python
Requires: gnome-python-bonobo gnome-python-gtkhtml2
Requires: gnome-python-gconf gnome-python-gnomevfs
Requires: python-chm

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

%build
NOCONFIGURE=yes gnome-autogen.sh 
%configure2_5x

%make

%install
rm -rf %buildroot
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std UPDATE_MIME_DATABASE=true UPDATE_DESKTOP_DATABASE=true

%find_lang %name --with-gnome

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
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
%if %mdkversion < 200900
%{update_desktop_database}
%endif

%if %mdkversion < 200900
%update_menus
%post_install_gconf_schemas gnochm
%update_scrollkeeper
%endif
touch %{_datadir}/gnome/help/%{name}/C/%{name}.html
if [ -x %{_bindir}/yelp-pregenerate ]; then %{_bindir}/yelp-pregenerate %{_datadir}/gnome/help/%{name}/*/%name.xml > /dev/null; fi
%if %mdkversion < 200900
%update_mime_database
%endif

%preun
%preun_uninstall_gconf_schemas gnochm

%if %mdkversion < 200900
%postun
%{clean_desktop_database}
%clean_menus
%clean_scrollkeeper
%clean_mime_database
%endif

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
%_liconsdir/%name.png
%_miconsdir/%name.png
%_iconsdir/%name.png
