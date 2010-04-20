# TODO
# - initrd needs love (is probably completly unusable in current form)
#
# Conditional build:
%bcond_without	initrd		# build without udev-initrd
%bcond_without	uClibc		# link initrd version with static uClibc
%bcond_with	klibc		# link initrd version with static klibc
%bcond_with	dietlibc	# link initrd version with static dietlibc (currently broken and unsupported)
%bcond_with	glibc		# link initrd version with static glibc
%bcond_without	selinux		# build without SELinux support
%bcond_without	ConsoleKit	# build without ConsoleKit support

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
Version:	152
Release:	1
Epoch:		1
License:	GPL
Group:		Base
Source0:	ftp://ftp.kernel.org/pub/linux/utils/kernel/hotplug/%{name}-%{version}.tar.bz2
# Source0-md5:	14944d0ff630f639cf3a9fc9d9ae40b5
# rules
Source1:	%{name}-alsa.rules
Source2:	%{name}.rules
Source3:	%{name}-links.conf
Source4:	%{name}-compat.rules
# scripts / helpers
Source10:	%{name}-net.helper
Source11:	start_udev
# misc
Source20:	%{name}.blacklist
# initramfs
Source30:	%{name}-initramfs-bottom
Source31:	%{name}-initramfs-hook
Source32:	%{name}-initramfs-premount
Patch0:		%{name}-so.patch
Patch1:		%{name}-uClibc.patch
URL:		http://www.kernel.org/pub/linux/utils/kernel/hotplug/udev.html
%{?with_ConsoleKit:BuildRequires:	ConsoleKit-devel >= 0.4.1}
BuildRequires:	acl-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	device-mapper-devel
%{?debug:BuildRequires:	gir-repository-devel}
BuildRequires:	glib2-devel
BuildRequires:	glibc-misc
BuildRequires:	gobject-introspection-devel
BuildRequires:	gperf
BuildRequires:	gtk-doc
%{?with_selinux:BuildRequires:	libselinux-devel >= 1.17.13}
BuildRequires:	libtool
BuildRequires:	libusb-compat-devel
BuildRequires:	libxslt-progs
BuildRequires:	pciutils
BuildRequires:	pkgconfig
BuildRequires:	python-modules
BuildRequires:	sed >= 4.0
BuildRequires:	usbutils >= 0.82
%if %{with initrd}
BuildRequires:	acl-static
BuildRequires:	attr-static
%{?with_dietlibc:BuildRequires:	dietlibc-static}
BuildRequires:	glib2-static
%{?with_glibc:BuildRequires:	glibc-static}
%{?with_klibc:BuildRequires:	klibc-static}
%{?with_glibc:BuildRequires:	libselinux-static}
%{?with_glibc:BuildRequires:	libsepol-static}
BuildRequires:	libusb-compat-static
BuildRequires:	libusb-static
%{?with_klibc:BuildRequires:	linux-libc-headers}
BuildRequires:	pcre-static
%{?with_uClibc:BuildRequires:	uClibc-static >= 3:0.9.30.2-2}
%endif
Requires:	%{name}-core = %{epoch}:%{version}-%{release}
Provides:	dev = 3.5.0
Obsoletes:	dev
Obsoletes:	hotplug
Obsoletes:	hotplug-input
Obsoletes:	hotplug-net
Obsoletes:	hotplug-pci
Obsoletes:	udev-dev
Obsoletes:	udev-extras < 20090628
Obsoletes:	udev-tools
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin
%define		static_extras	extras/ata_id extras/cdrom_id extras/edd_id extras/floppy extras/usb_id extras/volume_id extras/scsi_id
%define		extras		%{static_extras} extras/firmware extras/path_id

%description
udev is the device manager for the Linux 2.6 kernel series. Its
primary function is managing device nodes in /dev. It is the successor
of devfs and hotplug.

%description -l pl.UTF-8
udev jest zarządcą urządzeń dla Linuksa 2.6. Jego główną funkcją jest
zarządzanie węzłami urządzeń w katalogu /dev. Jest następcą devfs i
hotpluga.

%package acl
Summary:	Control device ACL via ConsoleKit
Group:		Base
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}

%description acl
ConsoleKit hook to control permissions of system devices.

%package compat
Summary:	Compatibility rules for kernels < 2.6.31
Group:		Base
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}

%description compat
Compatibility rules for kernels < 2.6.31.

%package core
Summary:	A userspace implementation of devfs - core part of udev
Summary(pl.UTF-8):	Implementacja devfs w przestrzeni użytkownika - główna część udev
Group:		Base
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	coreutils
Requires:	setup >= 2.6.1-1
Requires:	uname(release) >= 2.6.25
Suggests:	%{name}-acl
Suggests:	%{name}-compat
Conflicts:	udev < 1:118-1

%description core
A userspace implementation of devfs - core part of udev.

%description core -l pl.UTF-8
Implementacja devfs w przestrzeni użytkownika - główna część udev.

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

%package initramfs
Summary:	A userspace implementation of devfs - support scripts for initramfs-tools
Summary(pl.UTF-8):	Implementacja devfs w przestrzeni użytkownika - skrypty dla initramfs-tools
Group:		Base
Requires:	%{name}-core = %{epoch}:%{version}-%{release}
Requires:	initramfs-tools

%description initramfs
A userspace implementation of devfs - support scripts for
initramfs-tools.

%description initramfs -l pl.UTF-8
Implementacja devfs w przestrzeni użytkownika - skrypty dla
initramfs-tools.

%package libs
Summary:	Shared libudev library
Summary(pl.UTF-8):	Biblioteka współdzielona libudev
Group:		Libraries
Requires:	libselinux >= 1.17.13

%description libs
Shared libudev library.

%description libs -l pl.UTF-8
Biblioteka współdzielona libudev.

%package devel
Summary:	Header file for libudev library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki libudev
Group:		Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	libselinux-devel >= 1.17.13

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
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
libudev API documentation.

%package glib
Summary:	Shared libgudev library
Summary(pl.UTF-8):	Biblioteka współdzielona libgudev
Group:		Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}

%description glib
Shared libgudev library.

%description glib -l pl.UTF-8
Biblioteka współdzielona libgudev.

%package glib-devel
Summary:	Header file for libgudev library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki libgudev
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}
Requires:	%{name}-glib = %{epoch}:%{version}-%{release}

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
Group:		Documentation
Requires:	gtk-doc-common

%description glib-apidocs
libgudev API documentation.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

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
	--libexecdir=/lib/udev \
	--with-rootlibdir=/%{_lib} \
	--disable-gtk-doc \
	--disable-logging \
	--disable-shared \
	--enable-static \
	--with-pci-ids-path=%{_sysconfdir} \
	--without-selinux \
	--disable-introspection \
	--disable-extras

%{__make} \
	LDFLAGS="-all-static"

DEST=$(pwd)/udev-initrd
%{__make} -j1 install \
	DESTDIR=${DEST}

%{__make} clean
%endif

%configure \
	%{?debug:--enable-debug} \
	--libexecdir=/lib/udev \
	--with-html-dir=%{_gtkdocdir} \
	--with-rootlibdir=/%{_lib} \
	--enable-extras \
	--enable-gtk-doc \
	--enable-introspection \
	--enable-logging \
	--enable-shared \
	--enable-static \
	--with-pci-ids-path=%{_sysconfdir} \
	--with%{!?with_selinux:out}-selinux
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{modprobe.d,udev/rules.d} \
	$RPM_BUILD_ROOT/lib/udev/devices

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_sysconfdir}/udev/udev.rules
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/udev/udev.permissions
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/init.d/udev

# install additional rules from udev package
cp -a rules/packages/40-pilot-links.rules $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d
cp -a rules/suse/64-device-mapper.rules $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d

# install custom rules from pld package
cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/40-alsa-restore.rules
cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/70-udev-pld.rules

# compatibility rules for older kernels
cp -a %{SOURCE4} $RPM_BUILD_ROOT/lib/udev/rules.d/30-kernel-compat.rules

# install configs
cp -a %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/udev/links.conf

# install executables (scripts, helpers, etc.)
install -p %{SOURCE10} $RPM_BUILD_ROOT/lib/udev/net_helper
install -p %{SOURCE11} $RPM_BUILD_ROOT%{_sbindir}/start_udev

# install misc
cp -a %{SOURCE20} $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/udev_blacklist.conf

install -d $RPM_BUILD_ROOT%{_datadir}/initramfs-tools/{hooks,scripts/init-{bottom,premount}}
# install support for initramfs-tools
install -p %{SOURCE30} $RPM_BUILD_ROOT%{_datadir}/initramfs-tools/scripts/init-bottom/udev
install -p %{SOURCE31} $RPM_BUILD_ROOT%{_datadir}/initramfs-tools/hooks/udev
install -p %{SOURCE32} $RPM_BUILD_ROOT%{_datadir}/initramfs-tools/scripts/init-premount/udev

%if %{with initrd}
install -d $RPM_BUILD_ROOT%{_libdir}/initrd/udev
install -p udev-initrd/sbin/udevadm $RPM_BUILD_ROOT%{_libdir}/initrd
install -p udev-initrd/sbin/udevd $RPM_BUILD_ROOT%{_libdir}/initrd
ln -s udevd $RPM_BUILD_ROOT%{_libdir}/initrd/udevstart
install -p udev-initrd/lib/udev/*_id $RPM_BUILD_ROOT%{_libdir}/initrd/udev
install -p udev-initrd/lib/udev/collect $RPM_BUILD_ROOT%{_libdir}/initrd/udev
install -p udev-initrd/lib/udev/create_floppy_devices $RPM_BUILD_ROOT%{_libdir}/initrd/udev
install -p udev-initrd/lib/udev/firmware $RPM_BUILD_ROOT%{_libdir}/initrd/udev
install -p udev-initrd/lib/udev/fstab_import $RPM_BUILD_ROOT%{_libdir}/initrd/udev
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

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%dev(c,1,3) %attr(666,root,root) /dev/null
%dev(c,5,1) %attr(660,root,console) /dev/console
%dev(c,1,5) %attr(666,root,root) /dev/zero

%if %{with ConsoleKit}
%files acl
%defattr(644,root,root,755)
%attr(755,root,root) /lib/udev/udev-acl
%attr(755,root,root) /usr/lib/ConsoleKit/run-seat.d/udev-acl.ck
/lib/udev/rules.d/70-acl.rules
%endif

%files compat
%defattr(644,root,root,755)
/lib/udev/rules.d/30-kernel-compat.rules

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
%attr(755,root,root) /lib/udev/firmware
%attr(755,root,root) /lib/udev/fstab_import

%attr(755,root,root) /lib/udev/keyboard-force-release.sh

%attr(755,root,root) /lib/udev/*_helper
%attr(755,root,root) /lib/udev/*_rules

%attr(755,root,root) /lib/udev/ata_id
%attr(755,root,root) /lib/udev/cdrom_id
%attr(755,root,root) /lib/udev/edd_id
%attr(755,root,root) /lib/udev/input_id
%attr(755,root,root) /lib/udev/path_id
%attr(755,root,root) /lib/udev/scsi_id
%attr(755,root,root) /lib/udev/usb_id
%attr(755,root,root) /lib/udev/v4l_id

%attr(755,root,root) /lib/udev/keymap
%dir /lib/udev/keymaps
/lib/udev/keymaps/*

%attr(755,root,root) /lib/udev/pci-db
%attr(755,root,root) /lib/udev/usb-db

%attr(755,root,root) /lib/udev/findkeyboards
%attr(755,root,root) /lib/udev/hid2hci
%attr(755,root,root) /lib/udev/mobile-action-modeswitch

%attr(755,root,root) %{_sbindir}/start_udev
%attr(755,root,root) %{_sbindir}/udevd
%attr(755,root,root) %{_sbindir}/udevadm

%dir %{_sysconfdir}/udev
%dir %{_sysconfdir}/udev/rules.d

%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/modprobe.d/udev_blacklist.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/links.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/40-alsa-restore.rules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/40-pilot-links.rules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/64-device-mapper.rules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/70-udev-pld.rules

%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/udev.conf

# rules below are NOT supposed to be changed by users
/lib/udev/rule_generator.functions
%dir /lib/udev/rules.d
/lib/udev/rules.d/50-firmware.rules
/lib/udev/rules.d/50-udev-default.rules
/lib/udev/rules.d/60-cdrom_id.rules
/lib/udev/rules.d/60-floppy.rules
/lib/udev/rules.d/60-persistent-alsa.rules
/lib/udev/rules.d/60-persistent-input.rules
/lib/udev/rules.d/60-persistent-serial.rules
/lib/udev/rules.d/60-persistent-storage-tape.rules
/lib/udev/rules.d/60-persistent-storage.rules
/lib/udev/rules.d/60-persistent-v4l.rules
/lib/udev/rules.d/61-mobile-action.rules
/lib/udev/rules.d/61-persistent-storage-edd.rules
/lib/udev/rules.d/70-hid2hci.rules
/lib/udev/rules.d/75-cd-aliases-generator.rules
/lib/udev/rules.d/75-net-description.rules
/lib/udev/rules.d/75-tty-description.rules
# It autogenerates network rules
# /lib/udev/rules.d/75-persistent-net-generator.rules
/lib/udev/rules.d/78-sound-card.rules
/lib/udev/rules.d/79-fstab_import.rules
/lib/udev/rules.d/80-drivers.rules
/lib/udev/rules.d/95-keyboard-force-release.rules
/lib/udev/rules.d/95-keymap.rules
/lib/udev/rules.d/95-udev-late.rules

%{_mandir}/man7/udev.7*
%{_mandir}/man8/*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libudev.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libudev.so.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libudev.la
%attr(755,root,root) %{_libdir}/libudev.so
%{_includedir}/libudev.h
%{_pkgconfigdir}/libudev.pc
%{_datadir}/pkgconfig/udev.pc

%files static
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libudev.a

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libudev

%files glib
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgudev-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgudev-1.0.so.0
%{_libdir}/girepository-1.0/*.typelib

%files glib-devel
%defattr(644,root,root,755)
%{_libdir}/libgudev-1.0.la
%attr(755,root,root) %{_libdir}/libgudev-1.0.so
%{_includedir}/gudev-1.0
%{_pkgconfigdir}/gudev-1.0.pc
%{_datadir}/gir-1.0/*.gir

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
%attr(755,root,root) %{_libdir}/initrd/udev/create_floppy_devices
%attr(755,root,root) %{_libdir}/initrd/udev/firmware
%attr(755,root,root) %{_libdir}/initrd/udev/fstab_import
%endif

%files initramfs
%defattr(644,root,root,755)
%attr(755,root,root) %{_datadir}/initramfs-tools/scripts/init-bottom/udev
%attr(755,root,root) %{_datadir}/initramfs-tools/hooks/udev
%attr(755,root,root) %{_datadir}/initramfs-tools/scripts/init-premount/udev
