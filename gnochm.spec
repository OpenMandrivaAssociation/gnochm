Summary: 	A chm file viewer for gnome
Name: 		gnochm
Version: 	0.9.11
Release: 	8
License: GPL
Group: 		Graphical desktop/GNOME
URL: http://gnochm.sourceforge.net/

Source: 	http://prdownloads.sourceforge.net/gnochm/%{name}-%{version}.tar.bz2
Source1:	%name-16.png
Source2:	%name-32.png
Source3:	%name.png

Patch:		gnochm-makefile.patch
Patch1:         gnochm.py.in.patch
Patch2:		gnochm-desktop.patch

BuildRequires: scrollkeeper libGConf2-devel
BuildRequires: intltool gettext-devel gnome-common
%py_requires
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
%patch2 -p0 -b .desktop

%build
NOCONFIGURE=yes gnome-autogen.sh 
%configure2_5x

%make

%install
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std UPDATE_MIME_DATABASE=true UPDATE_DESKTOP_DATABASE=true

%find_lang %name --with-gnome

# icon
mkdir -p %buildroot/{%_liconsdir,%_iconsdir,%_miconsdir}
#install -m 644 src/pixmaps/%name.png %buildroot/%_datadir/pixmaps/%name.png
install -m 644 %SOURCE1 %buildroot/%_miconsdir/%name.png
install -m 644 %SOURCE2 %buildroot/%_liconsdir/%name.png
install -m 644 %SOURCE3 %buildroot/%_iconsdir/%name.png

%post
touch %{_datadir}/gnome/help/%{name}/C/%{name}.html
if [ -x %{_bindir}/yelp-pregenerate ]; then %{_bindir}/yelp-pregenerate %{_datadir}/gnome/help/%{name}/*/%name.xml > /dev/null; fi

%preun
%preun_uninstall_gconf_schemas gnochm

%files -f %name.lang
%defattr(-,root,root)
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
%_liconsdir/%name.png
%_miconsdir/%name.png
%_iconsdir/%name.png


%changelog
* Mon May 23 2011 Funda Wang <fwang@mandriva.org> 0.9.11-7mdv2011.0
+ Revision: 677706
- rebuild to add gconftool as req

* Fri Nov 05 2010 Funda Wang <fwang@mandriva.org> 0.9.11-6mdv2011.0
+ Revision: 593661
- rebuild for py2.7

* Sun Aug 15 2010 Funda Wang <fwang@mandriva.org> 0.9.11-5mdv2011.0
+ Revision: 569916
- fix desktop file
- BR python for startup script

* Tue Feb 16 2010 Funda Wang <fwang@mandriva.org> 0.9.11-4mdv2010.1
+ Revision: 506730
- fix build

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 0.9.11-3mdv2009.0
+ Revision: 246342
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas
    - use %%update_scrollkeeper/%%clean_scrollkeeper
    - use %%post_install_gconf_schemas/%%preun_uninstall_gconf_schemas

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Fri Oct 12 2007 JÃ©rÃ´me Soyer <saispo@mandriva.org> 0.9.11-1mdv2008.1
+ Revision: 97321
- New release 0.9.11

  + Thierry Vignaud <tv@mandriva.org>
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'

* Sat Jul 21 2007 Funda Wang <fwang@mandriva.org> 0.9.10-1mdv2008.0
+ Revision: 54192
- build arch pacakges
- New version


* Thu Nov 16 2006 JÃ©rÃ´me Soyer <saispo@mandriva.org> 0.9.9-1mdv2007.0
+ Revision: 84732
- New release 0.9.9
- Import gnochm

* Sat May 27 2006 Jerome Soyer <saispo@mandriva.org> 0.9.8-1mdv2007.0
- New release 0.9.8

* Thu Jan 26 2006 Jerome Soyer <saispo@mandriva.org> 0.9.7-1mdk
- New release 0.9.7

* Thu Dec 22 2005 Michael Scherer <misc@mandriva.org> 0.9.6-3mdk
- fix BuildREquires

* Sat Nov 26 2005 Thierry Vignaud <tvignaud@mandriva.com> 0.9.6-2mdk
- fix requires (#17954)

* Sat Oct 01 2005 Michael Scherer <misc@mandriva.org> 0.9.6-1mdk
- New release 0.9.6

* Fri Jun 24 2005 Michael Scherer <misc@mandriva.org> 0.9.5-1mdk
- New release 0.9.5
- update patch0

* Fri Mar 18 2005 Nicolas Lécureuil <neoclust@mandrake.org> 0.9.4-4mdk
- fix mistake

* Fri Mar 18 2005 Nicolas Lécureuil <neoclust@mandrake.org> 0.9.4-3mdk
- fix mime update
- add patch1 --> fix #13717

* Mon Feb 14 2005 Jerome Soyer <saispo@mandrake.org> 0.9.4-2mdk
- Grrr ! Fix spec error

* Mon Feb 14 2005 Jerome Soyer <saispo@mandrake.org> 0.9.4-1mdk
- 0.9.4
- clean spec

* Mon Nov 08 2004 Lenny Cartier <lenny@mandrakesoft.com> 0.9.3-1mdk
- 0.9.3

* Mon Nov 01 2004 Michael Scherer <misc@mandrake.org> 0.9.2-2mdk
- Buildrequires

* Sun Aug 22 2004 Jerome Soyer <saispo@mandrake.org> 0.9.2-1mdk
- 0.9.2
- fix mime update

* Wed Aug 18 2004 Jerome Soyer <saispo@mandrake.org> 0.9.1-3mdk
- fix BuildRequires

* Mon Jul 26 2004 Michael Scherer <misc@mandrake.org> 0.9.1-2mdk 
- [DIRM]

* Sat Jul 03 2004 Jerome Soyer <jeromesoyer@yahoo.fr> 0.9.1-1mdk
- Compiling for Mandrake Cooker Release

