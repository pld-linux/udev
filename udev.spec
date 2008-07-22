# TODO
# - ! *************** ! SOURCE4 - pld rules needs cleanup (leaving only these that differ from original one; avoid duplication)
# - initrd needs love (is probably completly unusable in current form)
# - initrd build with uclibc on amd64 produces non-working binary (illegal instruction from open("/dev/null"))
#
# Conditional build:
%bcond_without	initrd	# build without udev-initrd
%bcond_without	uClibc	# link initrd version with static uClibc
%bcond_with	klibc	# link initrd version with static klibc
%bcond_with	dietlibc	# link initrd version with static dietlibc (currently broken and unsupported)
%bcond_with	glibc	# link initrd version with static glibc
%bcond_without	main	# don't compile main package, use for debugging initrd build
%bcond_without	selinux	# build without SELinux support

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
Version:	125
Release:	1.1
Epoch:		1
License:	GPL
Group:		Base
Source0:	ftp://ftp.kernel.org/pub/linux/utils/kernel/hotplug/%{name}-%{version}.tar.bz2
# Source0-md5:	27832847086383309bb3acbde2486e29
# rules
Source1:	%{name}-alsa.rules
#Source2:	%{name}.rules
Source3:	%{name}-links.conf
# scripts / helpers
Source10:	%{name}-net.helper
Source11:	start_udev
# misc
Source20:	%{name}.blacklist
Patch0:		%{name}-lib64.patch
URL:		http://www.kernel.org/pub/linux/utils/kernel/hotplug/udev.html
BuildRequires:	device-mapper-devel
%{?with_selinux:BuildRequires:	libselinux-devel >= 1.17.13}
BuildRequires:	sed >= 4.0
%if %{with initrd}
%{?with_dietlibc:BuildRequires:	dietlibc-static}
%{?with_glibc:BuildRequires:	glibc-static}
%{?with_klibc:BuildRequires:	klibc-static}
%{?with_klibc:BuildRequires:	linux-libc-headers}
%{?with_uClibc:BuildRequires:	uClibc-static >= 0.9.28}
%endif
Requires:	%{name}-core = %{epoch}:%{version}-%{release}
Provides:	dev = 3.0.0
Obsoletes:	dev
Obsoletes:	hotplug
Obsoletes:	hotplug-input
Obsoletes:	hotplug-net
Obsoletes:	hotplug-pci
Obsoletes:	udev-dev
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin
%define		extras		extras/ata_id extras/cdrom_id extras/edd_id extras/floppy extras/firmware extras/path_id extras/scsi_id extras/usb_id extras/volume_id
%define		static_extras	extras/ata_id extras/cdrom_id extras/edd_id extras/floppy extras/scsi_id extras/usb_id extras/volume_id

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
Requires:	coreutils
Requires:	libvolume_id = %{epoch}:%{version}-%{release}
Requires:	uname(release) >= 2.6.15

%description core
A userspace implementation of devfs - core part of udev.

%description core -l pl.UTF-8
Implementacja devfs w przestrzeni użytkownika - główna część udev.

%package initrd
Summary:	A userspace implementation of devfs - static binary for initrd
Summary(pl.UTF-8):	Implementacja devfs w przestrzeni użytkownika - statyczna binarka dla initrd
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description initrd
A userspace implementation of devfs - static binary for initrd.

%description initrd -l pl.UTF-8
Implementacja devfs w przestrzeni użytkownika - statyczna binarka dla
initrd.

%package -n libvolume_id
Summary:	libvolume_id library
Summary(pl.UTF-8):	Biblioteka libvolume_id
Group:		Libraries

%description -n libvolume_id
libvolume_id library.

%description -n libvolume_id -l pl.UTF-8
Biblioteka libvolume_id.

%package -n libvolume_id-devel
Summary:	Header files for libvolume_id library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libvolume_id
Group:		Development/Libraries
Requires:	libvolume_id = %{epoch}:%{version}-%{release}

%description -n libvolume_id-devel
This is the package containing the header files for libvolume_id
library.

%description -n libvolume_id-devel -l pl.UTF-8
Ten pakiet zawiera pliki nagBówkowe biblioteki libvolume_id.

%package -n libvolume_id-static
Summary:	Static libvolume_id library
Summary(pl.UTF-8):	Statyczna biblioteka libvolume_id
Group:		Development/Libraries
Requires:	libvolume_id-devel = %{epoch}:%{version}-%{release}

%description -n libvolume_id-static
Static libvolume_id library.

%description -n libvolume_id-static -l pl.UTF-8
Statyczna biblioteka libvolume_id.

%prep
%setup -q
%patch0 -p1

sed -i -e 's/$(CC) -shared/$(LD) -shared/' extras/volume_id/lib/Makefile
sed -i -e 's#/lib/udev/#/%{_lib}/udev/#g' *.c extras/rule_generator/write_*

%build
%if %{with initrd}
%{__make} \
%ifarch athlon
	ARCH=i386 \
%endif
	udevdir=/dev \
	%{?with_uClibc:CC="%{_target_cpu}-uclibc-gcc"} \
	%{?with_uClibc:LD="%{_target_cpu}-uclibc-gcc %{rpmldflags} -static"} \
	%{?with_dietlibc:CC="%{_target_cpu}-dietlibc-gcc"} \
	%{?with_dietlibc:LD="%{_target_cpu}-dietlibc-gcc %{rpmldflags} -static"} \
	%{?with_glibc:CC="%{_target_cpu}-pld-linux-gcc"} \
	%{?with_glibc:LD="%{_target_cpu}-pld-linux-gcc %{rpmldflags} -static"} \
	%{?with_klibc:KLCC=%{_bindir}/klcc CC="klcc"} \
	%{?with_klibc:LD="klcc %{rpmldflags} -static"} \
	DEBUG=%{!?debug:false}%{?debug:true} \
	STRIP="/bin/true" \
	USE_KLIBC=%{!?with_klibc:false}%{?with_klibc:true} \
	USE_LOG=false \
	USE_SELINUX=false \
	USE_STATIC=true \
	EXTRAS="%{static_extras}" \
	V=1

cp -a udevd initrd-udevd
cp -a udevadm initrd-udevadm

# What is this FIXME business and why is initrd
# broken, if it's fine?
# FIXME, cause I'm broken - your initrd
%if 0
cp -a extras/ata_id/ata_id initrd-ata_id
cp -a extras/cdrom_id/cdrom_id initrd-cdrom_id
cp -a extras/edd_id/edd_id initrd-edd_id
cp -a extras/scsi_id/scsi_id initrd-scsi_id
cp -a extras/usb_id/usb_id initrd-usb_id
cp -a extras/volume_id/vol_id initrd-vol_id
%endif

%if %{with main}
%{__make} clean \
	EXTRAS="%{static_extras}" \
	V=1
%endif
%endif

%if %{with main}
%{__make} \
	libudevdir=/%{_lib}/udev \
	libdir=/%{_lib} \
	usrlibdir=%{_libdir} \
	udevdir=/dev \
	CC="%{__cc}" \
	LD="%{__cc} %{rpmldflags}" \
	DEBUG=%{!?debug:false}%{?debug:true} \
	OPTFLAGS="%{rpmcflags}" \
	USE_KLIBC=false \
	USE_LOG=true \
	EXTRAS="%{extras}" \
	V=1
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with main}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{modprobe.d,udev/rules.d} \
	$RPM_BUILD_ROOT/%{_lib}/udev/devices

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	initdir=/etc/rc.d/init.d \
        libudevdir=/%{_lib}/udev \
        libdir=/%{_lib} \
        usrlibdir=%{_libdir} \
        udevdir=/dev \
	EXTRAS="%{extras}"

rm -f $RPM_BUILD_ROOT%{_sysconfdir}/udev/udev.rules
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/udev/udev.permissions
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/init.d/udev

# install additional rules
install rules/suse/64-device-mapper.rules $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/40-alsa.rules
#install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/50-udev-pld.rules

# needed on kernels < 2.6.25
cat <<EOF >$RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/05-udev-early.rules
# sysfs is populated after the event is sent
ACTION=="add", SUBSYSTEM=="scsi", WAIT_FOR_SYSFS="ioerr_cnt"
EOF

# install configs
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/udev/links.conf

# install executables (scripts, helpers, etc.)
install %{SOURCE10} $RPM_BUILD_ROOT/%{_lib}/udev/net_helper
install %{SOURCE11} $RPM_BUILD_ROOT%{_sbindir}/start_udev

install extras/path_id/path_id $RPM_BUILD_ROOT/%{_lib}/udev

install extras/volume_id/lib/*.a $RPM_BUILD_ROOT%{_libdir}
%endif

# install misc
install %{SOURCE20} $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/udev_blacklist.conf

%if %{with initrd}
install -d $RPM_BUILD_ROOT%{_sbindir}
install initrd-* $RPM_BUILD_ROOT%{_sbindir}
ln -s initrd-udevd $RPM_BUILD_ROOT%{_sbindir}/udevstart.initrd
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
sed -i -e 's#IMPORT{program}="/sbin/#IMPORT{program}="#g' /etc/udev/rules.d/*.rules
sed -i -e 's#/lib/udev/#/%{_lib}/udev/#g' /etc/udev/rules.d/*.rules

%post	-n libvolume_id -p /sbin/ldconfig
%postun	-n libvolume_id -p /sbin/ldconfig

%if %{with main}
%files
%defattr(644,root,root,755)
%dev(c,1,3) %attr(666,root,root) /dev/null
%dev(c,5,1) %attr(660,root,console) /dev/console
%dev(c,1,5) %attr(666,root,root) /dev/zero

%files core
%defattr(644,root,root,755)
%doc ChangeLog FAQ README RELEASE-NOTES TODO
%doc docs/writing_udev_rules

%dir /%{_lib}/udev

# /%{_lib}/udev/devices is recommended as a directory where packages or
# the user can place real device nodes, which get copied over to /dev at
# every boot. This should replace the various solutions with custom config
# files.
%dir /%{_lib}/udev/devices

%attr(755,root,root) /%{_lib}/udev/create_floppy_devices
%attr(755,root,root) /%{_lib}/udev/firmware.sh

%attr(755,root,root) /%{_lib}/udev/*_helper

%attr(755,root,root) /%{_lib}/udev/ata_id
%attr(755,root,root) /%{_lib}/udev/cdrom_id
%attr(755,root,root) /%{_lib}/udev/edd_id
%attr(755,root,root) /%{_lib}/udev/path_id
%attr(755,root,root) /%{_lib}/udev/scsi_id
%attr(755,root,root) /%{_lib}/udev/usb_id
%attr(755,root,root) /%{_lib}/udev/vol_id

%attr(755,root,root) %{_sbindir}/start_udev
%attr(755,root,root) %{_sbindir}/udevd
%attr(755,root,root) %{_sbindir}/udevadm
%attr(755,root,root) %{_sbindir}/udevsettle

%attr(755,root,root) %{_bindir}/udevinfo

%dir %{_sysconfdir}/udev
%dir %{_sysconfdir}/udev/rules.d

%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/modprobe.d/udev_blacklist.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/scsi_id.config
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/links.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/05-udev-early.rules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/40-alsa.rules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/64-device-mapper.rules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/udev.conf

# rules below are NOT supposed to be changed by users
%dir /%{_lib}/udev/rules.d
/%{_lib}/udev/rules.d/50-udev-default.rules
/%{_lib}/udev/rules.d/60-cdrom_id.rules
/%{_lib}/udev/rules.d/60-persistent-input.rules
/%{_lib}/udev/rules.d/60-persistent-storage-tape.rules
/%{_lib}/udev/rules.d/60-persistent-storage.rules
/%{_lib}/udev/rules.d/60-persistent-v4l.rules
/%{_lib}/udev/rules.d/61-persistent-storage-edd.rules
/%{_lib}/udev/rules.d/80-drivers.rules
/%{_lib}/udev/rules.d/95-udev-late.rules

%{_mandir}/man7/udev.7*
%{_mandir}/man8/*
%endif

%if %{with initrd}
%files initrd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/initrd-*
%attr(755,root,root) %{_sbindir}/udevstart.initrd
%endif

%files -n libvolume_id
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libvolume_id.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libvolume_id.so.0

%files -n libvolume_id-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvolume_id.so
%{_includedir}/libvolume_id.h
%{_pkgconfigdir}/libvolume_id.pc

%files -n libvolume_id-static
%defattr(644,root,root,755)
%{_libdir}/libvolume_id.a
