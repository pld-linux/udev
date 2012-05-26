# TODO
# - initrd needs love (is probably completly unusable in current form)
# - udev stores it's data now to /run/udev, but that dir is not owned and not even on tmpfs
#
# Conditional build:
%bcond_without	initrd		# build without udev-initrd
%bcond_with	uClibc		# link initrd version with static uClibc
%bcond_with	klibc		# link initrd version with static klibc
%bcond_with	dietlibc	# link initrd version with static dietlibc (currently broken and unsupported)
%bcond_without	glibc		# link initrd version with static glibc
%bcond_without	selinux		# build without SELinux support

%ifarch sparc sparc64
%define		with_glibc 1
%endif

# if one of the *libc is enabled disable default uClibc
%if %{with dietlibc} && %{with uClibc}
%undefine	with_uClibc
%endif

%if %{with glibc} && %{with uClibc}
%undefine	with_uClibc
%endif

%if %{with klibc} && %{with uClibc}
%undefine	with_uClibc
%endif

Summary:	Device manager for the Linux 2.6 kernel series
Summary(pl.UTF-8):	Zarządca urządzeń dla Linuksa 2.6
Name:		udev
# Verify ChangeLog and NEWS when updating (since there are incompatible/breaking changes very often)
Version:	182
Release:	6
Epoch:		1
License:	GPL v2+
Group:		Base
Source0:	http://www.kernel.org/pub/linux/utils/kernel/hotplug/%{name}-%{version}.tar.bz2
# Source0-md5:	e31c83159b017e8ab0fa2f4bca758a41
# rules
Source1:	%{name}-alsa.rules
Source2:	%{name}.rules
Source3:	%{name}-links.conf
# scripts / helpers
Source10:	%{name}-net.helper
Source11:	start_udev
# misc
Source20:	%{name}.blacklist
Source21:	fbdev.blacklist
Patch0:		%{name}-so.patch
Patch1:		%{name}-uClibc.patch
Patch2:		%{name}-ploop-rules.patch
BuildRequires:	acl-devel
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1:1.11
BuildRequires:	glib2-devel >= 1:2.22.0
BuildRequires:	glibc-misc
BuildRequires:	gobject-introspection-devel >= 0.6.2
BuildRequires:	gperf
BuildRequires:	gtk-doc >= 1.10
BuildRequires:	kmod-devel >= 5
BuildRequires:	libblkid-devel >= 2.20
%{?with_selinux:BuildRequires:	libselinux-devel >= 1.17.13}
BuildRequires:	libtool >= 2:2.0
BuildRequires:	libxslt-progs
BuildRequires:	pciutils
BuildRequires:	pkgconfig
BuildRequires:	python-modules
BuildRequires:	rpmbuild(macros) >= 1.628
BuildRequires:	sed >= 4.0
BuildRequires:	usbutils >= 0.82
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
%if %{with initrd}
BuildRequires:	acl-static
BuildRequires:	attr-static
%{?with_dietlibc:BuildRequires:	dietlibc-static}
BuildRequires:	glib2-static >= 1:2.22.0
%{?with_glibc:BuildRequires:	glibc-static}
%{?with_klibc:BuildRequires:	klibc-static}
BuildRequires:	kmod-libs-static >= 5
BuildRequires:	libblkid-static >= 2.20
%{?with_glibc:BuildRequires:	libselinux-static}
%{?with_glibc:BuildRequires:	libsepol-static}
%{?with_klibc:BuildRequires:	linux-libc-headers}
BuildRequires:	pcre-static
%{?with_uClibc:BuildRequires:	uClibc-static >= 4:0.9.30.3}
BuildRequires:	xz-static
BuildRequires:	zlib-static
%endif
# Build process broken - tries to links with system libs
# instead of just built libs. BC for now.
BuildConflicts:	udev-devel
Requires:	%{name}-core = %{epoch}:%{version}-%{release}
Provides:	dev = 3.5.0
Obsoletes:	dev
Obsoletes:	hotplug
Obsoletes:	hotplug-input
Obsoletes:	hotplug-net
Obsoletes:	hotplug-pci
Obsoletes:	udev-compat
Obsoletes:	udev-dev
Obsoletes:	udev-extras < 20090628
Obsoletes:	udev-tools
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
udev is the device manager for the Linux 2.6 kernel series. Its
primary function is managing device nodes in /dev. It is the successor
of devfs and hotplug.

%description -l pl.UTF-8
udev jest zarządcą urządzeń dla Linuksa 2.6. Jego główną funkcją jest
zarządzanie węzłami urządzeń w katalogu /dev. Jest następcą devfs i
hotpluga.

%package core
Summary:	A userspace implementation of devfs - core part of udev
Summary(pl.UTF-8):	Implementacja devfs w przestrzeni użytkownika - główna część udev
Group:		Base
Requires(post,preun,postun):	systemd-units >= 38
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	coreutils
Requires:	filesystem >= 3.0-45
Requires:	setup >= 2.6.1-1
Requires:	systemd-units >= 0.38
Requires:	uname(release) >= 2.6.32
Obsoletes:	udev-systemd
Conflicts:	rc-scripts < 0.4.5.3-1
Conflicts:	udev < 1:118-1

%description core
A userspace implementation of devfs - core part of udev.

%description core -l pl.UTF-8
Implementacja devfs w przestrzeni użytkownika - główna część udev.

%package libs
Summary:	Shared library to access udev device information
Summary(pl.UTF-8):	Biblioteka współdzielona do dostępu do informacji o urządzeniach udev
Group:		Libraries

%description libs
Shared libudev library to access udev device information.

%description libs -l pl.UTF-8
Biblioteka współdzielona libudev służąca do dostępu do informacji o
urządzeniach udev.

%package devel
Summary:	Header file for libudev library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki libudev
Group:		Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}

%description devel
Header file for libudev library.

%description devel -l pl.UTF-8
Plik nagłówkowy biblioteki libudev.

%package static
Summary:	Static libudev library
Summary(pl.UTF-8):	Biblioteka statyczna libudev
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static libudev library.

%description static -l pl.UTF-8
Biblioteka statyczna libudev.

%package apidocs
Summary:	libudev API documentation
Summary(pl.UTF-8):	Dokumentacja API libudev
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
libudev API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API libudev.

%package glib
Summary:	Shared libgudev library - GObject bindings for libudev
Summary(pl.UTF-8):	Biblioteka współdzielona libgudev - wiązania GObject do libudev
Group:		Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	glib2 >= 1:2.22.0

%description glib
Shared libgudev library - GObject bindings for libudev.

%description glib -l pl.UTF-8
Biblioteka współdzielona libgudev - wiązania GObject do libudev.

%package glib-devel
Summary:	Header file for libgudev library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki libgudev
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}
Requires:	%{name}-glib = %{epoch}:%{version}-%{release}
Requires:	glib2-devel >= 1:2.22.0

%description glib-devel
Header file for libgudev library.

%description glib-devel -l pl.UTF-8
Plik nagłówkowy biblioteki libgudev.

%package glib-static
Summary:	Static libgudev library
Summary(pl.UTF-8):	Biblioteka statyczna libgudev
Group:		Development/Libraries
Requires:	%{name}-glib-devel = %{epoch}:%{version}-%{release}

%description glib-static
Static libgudev library.

%description glib-static -l pl.UTF-8
Biblioteka statyczna libgudev.

%package glib-apidocs
Summary:	libgudev API documentation
Summary(pl.UTF-8):	Dokumentacja API libgudev
Group:		Documentation
Requires:	gtk-doc-common

%description glib-apidocs
libgudev API documentation.

%description glib-apidocs -l pl.UTF-8
Dokumentacja API libgudev.

%package initrd
Summary:	A userspace implementation of devfs - static binary for initrd
Summary(pl.UTF-8):	Implementacja devfs w przestrzeni użytkownika - statyczna binarka dla initrd
Group:		Base
Requires:	%{name}-core = %{epoch}:%{version}-%{release}
Conflicts:	geninitrd < 10000.10

%description initrd
A userspace implementation of devfs - static binary for initrd.

%description initrd -l pl.UTF-8
Implementacja devfs w przestrzeni użytkownika - statyczna binarka dla
initrd.

%prep
%setup -q
%patch0 -p1
%if %{with uClibc}
%patch1 -p1
%endif
%patch2 -p1

%build
%{__gtkdocize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoheader}
%{__autoconf}
%{__automake}
%if %{with initrd}
%configure \
%if "%{?configure_cache}" == "1"
	--cache-file=%{?configure_cache_file}%{!?configure_cache_file:configure}-initrd.cache \
%endif
	%{?with_uClibc:CC="%{_target_cpu}-uclibc-gcc"} \
	%{?with_dietlibc:CC="diet %{__cc} %{rpmcflags} %{rpmldflags} -Os -D_BSD_SOURCE"} \
	%{?with_klibc:CC="%{_bindir}/klcc"} \
	%{?debug:--enable-debug} \
	--libexecdir=/lib \
	--bindir=%{_sbindir} \
	--with-rootprefix="" \
	--with-rootlibdir=/%{_lib} \
	--disable-rule_generator \
	--disable-gudev \
	--disable-keymap \
	--disable-gtk-doc \
	--disable-introspection \
	--disable-logging \
	--disable-shared \
	--disable-silent-rules \
	--enable-static \
	--with-pci-ids-path=%{_sysconfdir}/pci.ids \
	--without-selinux

%{__make} \
	LDFLAGS="-all-static" \
	KMOD_LIBS="-lkmod -lz -llzma"

DEST=$(pwd)/udev-initrd
%{__make} -j1 install \
	DESTDIR=${DEST}

%{__make} clean
%endif

%configure \
	%{?debug:--enable-debug} \
	--libexecdir=/lib \
	--with-html-dir=%{_gtkdocdir} \
	--bindir=%{_sbindir} \
	--with-rootprefix="" \
	--with-rootlibdir=/%{_lib} \
	--disable-silent-rules \
	--enable-gtk-doc \
	--enable-introspection \
	--enable-floppy \
	--enable-logging \
	--enable-shared \
	--enable-static \
	--with-pci-ids-path=%{_sysconfdir}/pci.ids \
	--with-systemdsystemunitdir=%{systemdunitdir} \
	--with%{!?with_selinux:out}-selinux
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{modprobe.d,udev/rules.d} \
	$RPM_BUILD_ROOT{/lib/udev/devices,/usr/lib,%{_bindir}}

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

ln -s /lib/udev/udevd $RPM_BUILD_ROOT%{_sbindir}/udevd

# compat symlinks for "/ merged into /usr" programs
ln -s %{_sbindir}/udevadm $RPM_BUILD_ROOT%{_bindir}

# install custom rules from pld package
cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/40-alsa-restore.rules
cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/70-udev-pld.rules

# install configs
cp -a %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/udev/links.conf

# install executables (scripts, helpers, etc.)
install -p %{SOURCE10} $RPM_BUILD_ROOT/lib/udev/net_helper
install -p %{SOURCE11} $RPM_BUILD_ROOT%{_sbindir}/start_udev

# install misc
cp -a %{SOURCE20} $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/udev_blacklist.conf
cp -a %{SOURCE21} $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/fbdev-blacklist.conf

%if %{with initrd}
install -d $RPM_BUILD_ROOT%{_libdir}/initrd/udev
install -p udev-initrd/sbin/udevadm $RPM_BUILD_ROOT%{_libdir}/initrd
install -p udev-initrd/lib/udev/udevd $RPM_BUILD_ROOT%{_libdir}/initrd
ln -s udevd $RPM_BUILD_ROOT%{_libdir}/initrd/udevstart
install -p udev-initrd/lib/udev/*_id $RPM_BUILD_ROOT%{_libdir}/initrd/udev
install -p udev-initrd/lib/udev/collect $RPM_BUILD_ROOT%{_libdir}/initrd/udev
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%triggerpostun core -- dev
if [ "$2" = 0 ]; then
	# need to kill and restart udevd as after obsoleting dev package the
	# /dev tree will remain empty. umask is needed as otherwise udev will
	# create devices with strange permissions (udev bug probably)
	umask 000
	/sbin/start_udev || exit 0
fi

%triggerpostun core -- udev < 108
%{__sed} -i -e 's#IMPORT{program}="/sbin/#IMPORT{program}="#g' /etc/udev/rules.d/*.rules
%if "%{_lib}" != "lib"
%{__sed} -i -e 's#/%{_lib}/udev/#/lib/udev/#g' /etc/udev/rules.d/*.rules
%endif

%triggerpostun core -- udev < 165
/sbin/udevadm info --convert-db

%triggerpostun core -- %{name}-core < 1:175-4
%systemd_trigger udev-settle.service

%post core
if [ $1 -gt 1 ]; then
	if [ ! -x /bin/systemd_booted ] || ! /bin/systemd_booted; then
		if grep -qs devtmpfs /proc/mounts && [ -n "$(pidof udevd)" ]; then
			/sbin/udevadm control --exit
			/lib/udev/udevd --daemon
		fi
	else
		SYSTEMD_LOG_LEVEL=warning SYSTEMD_LOG_TARGET=syslog \
		/bin/systemctl --quiet try-restart udev.service || :
	fi
fi
%systemd_post udev-settle.service

%preun core
%systemd_preun udev-settle.service

%postun core
%systemd_reload

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post	glib -p /sbin/ldconfig
%postun	glib -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%dev(c,1,3) %attr(666,root,root) /dev/null
%dev(c,5,1) %attr(660,root,console) /dev/console
%dev(c,1,5) %attr(666,root,root) /dev/zero

%files core
%defattr(644,root,root,755)
%doc ChangeLog TODO

%dir /lib/udev

# /lib/udev/devices is recommended as a directory where packages or
# the user can place real device nodes, which get copied over to /dev at
# every boot. This should replace the various solutions with custom config
# files.
%dir /lib/udev/devices

%attr(755,root,root) /lib/udev/create_floppy_devices
%attr(755,root,root) /lib/udev/collect

%attr(755,root,root) /lib/udev/keyboard-force-release.sh

%attr(755,root,root) /lib/udev/net_helper

%attr(755,root,root) /lib/udev/ata_id
%attr(755,root,root) /lib/udev/cdrom_id
%attr(755,root,root) /lib/udev/mtd_probe
%attr(755,root,root) /lib/udev/scsi_id
%attr(755,root,root) /lib/udev/v4l_id

%attr(755,root,root) /lib/udev/udevd

%attr(755,root,root) /lib/udev/keymap
%dir /lib/udev/keymaps
/lib/udev/keymaps/*

%attr(755,root,root) /lib/udev/accelerometer
%attr(755,root,root) /lib/udev/findkeyboards

%attr(755,root,root) %{_sbindir}/start_udev
%attr(755,root,root) %{_sbindir}/udevd
%attr(755,root,root) %{_sbindir}/udevadm
%attr(755,root,root) %{_bindir}/udevadm

%dir %{_sysconfdir}/udev
%dir %{_sysconfdir}/udev/rules.d

%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/modprobe.d/fbdev-blacklist.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/modprobe.d/udev_blacklist.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/links.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/40-alsa-restore.rules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/70-udev-pld.rules

%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/udev.conf

# rules below are NOT supposed to be changed by users
/lib/udev/rules.d/42-usb-hid-pm.rules
/lib/udev/rules.d/50-udev-default.rules
/lib/udev/rules.d/60-cdrom_id.rules
/lib/udev/rules.d/60-floppy.rules
/lib/udev/rules.d/60-persistent-alsa.rules
/lib/udev/rules.d/60-persistent-input.rules
/lib/udev/rules.d/60-persistent-serial.rules
/lib/udev/rules.d/60-persistent-storage-tape.rules
/lib/udev/rules.d/60-persistent-storage.rules
/lib/udev/rules.d/60-persistent-v4l.rules
/lib/udev/rules.d/61-accelerometer.rules
/lib/udev/rules.d/75-net-description.rules
/lib/udev/rules.d/75-probe_mtd.rules
/lib/udev/rules.d/75-tty-description.rules
/lib/udev/rules.d/78-sound-card.rules
/lib/udev/rules.d/80-drivers.rules
/lib/udev/rules.d/95-keyboard-force-release.rules
/lib/udev/rules.d/95-keymap.rules
/lib/udev/rules.d/95-udev-late.rules

%{_mandir}/man7/udev.7*
%{_mandir}/man8/*

%{systemdunitdir}/basic.target.wants/udev-trigger.service
%{systemdunitdir}/basic.target.wants/udev.service
%{systemdunitdir}/sockets.target.wants/udev-control.socket
%{systemdunitdir}/sockets.target.wants/udev-kernel.socket
%{systemdunitdir}/udev-control.socket
%{systemdunitdir}/udev-kernel.socket
%{systemdunitdir}/udev-settle.service
%{systemdunitdir}/udev-trigger.service
%{systemdunitdir}/udev.service

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libudev.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libudev.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libudev.so
%{_libdir}/libudev.la
%{_includedir}/libudev.h
%{_pkgconfigdir}/libudev.pc
%{_npkgconfigdir}/udev.pc

%files static
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libudev.a

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libudev

%files glib
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libgudev-1.0.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libgudev-1.0.so.0
%{_libdir}/girepository-1.0/GUdev-1.0.typelib

%files glib-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgudev-1.0.so
%{_libdir}/libgudev-1.0.la
%{_includedir}/gudev-1.0
%{_pkgconfigdir}/gudev-1.0.pc
%{_datadir}/gir-1.0/GUdev-1.0.gir

%files glib-static
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgudev-1.0.a

%files glib-apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gudev

%if %{with initrd}
%files initrd
%defattr(644,root,root,755)
%dir %{_libdir}/initrd/udev
%attr(755,root,root) %{_libdir}/initrd/udevd
%attr(755,root,root) %{_libdir}/initrd/udevadm
%attr(755,root,root) %{_libdir}/initrd/udevstart
%attr(755,root,root) %{_libdir}/initrd/udev/*_id
%attr(755,root,root) %{_libdir}/initrd/udev/collect
%endif
