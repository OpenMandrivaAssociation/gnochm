Summary:	A chm file viewer for gnome
Name:		gnochm
Version:	0.9.11
Release:	9
License:	GPLv2+
Group:		Graphical desktop/GNOME
Url:		http://gnochm.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/gnochm/%{name}-%{version}.tar.bz2
Source1:	%{name}-16.png
Source2:	%{name}-32.png
Source3:	%{name}.png
Patch0:		gnochm-makefile.patch
Patch1:		gnochm.py.in.patch
Patch2:		gnochm-desktop.patch
BuildRequires:	gnome-common
BuildRequires:	intltool
BuildRequires:	scrollkeeper
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(gconf-2.0)
Requires:	pygtk2.0-libglade
Requires:	gnome-python
Requires:	gnome-python-bonobo
Requires:	gnome-python-gconf
Requires:	gnome-python-gnomevfs
Requires:	gnome-python-gtkhtml2
Requires:	python-chm
BuildArch:	noarch

%description
A CHM file viewer for Gnome. Features are:

  * Full text search
  * Bookmarks
  * Support for external ms-its links
  * Configurable support for http links
  * Internationalisation

%files -f %{name}.lang
%doc ABOUT-NLS AUTHORS COPYING ChangeLog NEWS README
%config(noreplace) %{_sysconfdir}/gconf/schemas/gnochm.schemas
%{_bindir}/gnochm
%dir %{_datadir}/gnochm/
%dir %{_datadir}/gnochm/glade/
%{_datadir}/gnochm/glade/*.glade
%{_datadir}/pixmaps/*
%{_datadir}/applications/*
%{_datadir}/mime-info/gnochm.*
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/application-registry/gnochm.*
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png

%preun
%preun_uninstall_gconf_schemas gnochm

#----------------------------------------------------------------------------

%prep
%setup -q
%patch0 -p0 -b .makefile
%patch1 -p0 -b .makefile
%patch2 -p0 -b .desktop

%build
NOCONFIGURE=yes gnome-autogen.sh
%configure2_5x

%make

%install
%makeinstall_std

%find_lang %{name} --with-gnome

# icon
mkdir -p %{buildroot}%{_liconsdir}
mkdir -p %{buildroot}%{_iconsdir}
mkdir -p %{buildroot}%{_miconsdir}
install -m 644 %{SOURCE1} %{buildroot}%{_miconsdir}/%{name}.png
install -m 644 %{SOURCE2} %{buildroot}%{_liconsdir}/%{name}.png
install -m 644 %{SOURCE3} %{buildroot}%{_iconsdir}/%{name}.png

