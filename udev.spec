# TODO
# - initrd needs love (is probably completly unusable in current form)
# - initrd build with uclibc on amd64 produces non-working binary (illegal instruction from open("/dev/null"))
# - rewrite in sh/sed, or move to (tools?) subpackage udev_import_usermap (bc adds perl dep)
#
# Conditional build:
%bcond_without	initrd	# build without udev-initrd
%bcond_without	uClibc	# link initrd version with static uClibc
%bcond_with	klibc	# link initrd version with static klibc
%bcond_with	dietlibc	# link initrd version with static dietlibc (currently broken and unsupported)
%bcond_with	glibc	# link initrd version with static glibc
%bcond_without	main	# don't compile main package, use for debugging initrd build

%ifarch %{x8664} sparc alpha
%define		with_klibc 1
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

Summary:	A userspace implementation of devfs
Summary(pl):	Implementacja devfs w przestrzeni u�ytkownika
Name:		udev
Version:	097
Release:	1
Epoch:		1
License:	GPL
Group:		Base
Source0:	ftp://ftp.kernel.org/pub/linux/utils/kernel/hotplug/%{name}-%{version}.tar.bz2
# Source0-md5:	8299024491eb4de95e5ca6d53ec9bda9
# rules
Source1:	%{name}-alsa.rules
Source2:	%{name}-hotplug_map.rules
Source3:	%{name}-modprobe.rules
Source4:	%{name}.rules
Source5:	%{name}-example.rules
# configs
Source10:	%{name}.conf
Source11:	%{name}-links.conf
# scripts / helpers
Source20:	%{name}_import_usermap
Source21:	%{name}-net.helper
Source22:	start_udev
# misc
Source30:	%{name}-usb.distmap
Source31:	%{name}-usb.handmap
Source32:	%{name}.blacklist
URL:		http://www.kernel.org/pub/linux/utils/kernel/hotplug/udev.html
BuildRequires:	device-mapper-devel
BuildRequires:	libselinux-devel >= 1.17.13
BuildRequires:	sed >= 4.0
%if %{with initrd}
%{?with_dietlibc:BuildRequires:	dietlibc-static}
%{?with_uClibc:BuildRequires:	uClibc-static >= 0.9.28}
%{?with_glibc:BuildRequires:	glibc-static}
%{?with_klibc:BuildRequires:	klibc-static}
%{?with_klibc:BuildRequires:	linux-libc-headers}
%endif
Requires:	libvolume_id = %{epoch}:%{version}-%{release}
Requires:	coreutils
Provides:	dev = 3.0.0
Obsoletes:	dev
Obsoletes:	hotplug
Obsoletes:	hotplug-input
Obsoletes:	hotplug-net
Obsoletes:	hotplug-pci
Obsoletes:	udev-dev
Conflicts:	kernel < 3:2.6.15
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin
%define		extras		extras/ata_id extras/cdrom_id extras/dasd_id extras/edd_id extras/floppy extras/firmware extras/scsi_id extras/usb_id extras/volume_id
%define		static_extras	extras/ata_id extras/cdrom_id extras/dasd_id extras/edd_id extras/scsi_id extras/usb_id extras/volume_id

%description
A userspace implementation of devfs for 2.5 and higher kernels.

%description -l pl
Implementacja devfs w przestrzeni u�ytkownika dla j�der 2.5 i
wy�szych.

%package initrd
Summary:	A userspace implementation of devfs - static binary for initrd
Summary(pl):	Implementacja devfs w przestrzeni u�ytkownika - statyczna binarka dla initrd
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description initrd
A userspace implementation of devfs - static binary for initrd.

%description initrd -l pl
Implementacja devfs w przestrzeni u�ytkownika - statyczna binarka dla
initrd.

%package -n libvolume_id
Summary:	libvolume_id library
Summary(pl):	Biblioteka libvolume_id
Group:		Libraries

%description -n libvolume_id
libvolume_id library.

%description -n libvolume_id -l pl
Biblioteka libvolume_id.

%package -n libvolume_id-devel
Summary:	Header files for libvolume_id library
Summary(pl):	Pliki nag��wkowe biblioteki libvolume_id
Group:		Development/Libraries
Requires:	libvolume_id = %{epoch}:%{version}-%{release}

%description -n libvolume_id-devel
This is the package containing the header files for libvolume_id library.

%description -n libvolume_id-devel -l pl
Ten pakiet zawiera pliki nagB�wkowe biblioteki libvolume_id.

%package -n libvolume_id-static
Summary:	Static libvolume_id library
Summary(pl):	Statyczna biblioteka libvolume_id
Group:		Development/Libraries
Requires:	libvolume_id-devel = %{epoch}:%{version}-%{release}

%description -n libvolume_id-static
Static libvolume_id library.

%description -n libvolume_id-static -l pl
Statyczna biblioteka libvolume_id.

%prep
%setup -q
sed 's/$(CC) -shared/$(LD) -shared/' \
	 -i extras/volume_id/lib/Makefile

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

cp -a udev initrd-udev

# FIXME, cause I'm broken - your initrd
%if 0
cp -a extras/ata_id/ata_id initrd-ata_id
cp -a extras/cdrom_id/cdrom_id initrd-cdrom_id
cp -a extras/dasd_id/dasd_id initrd-dasd_id
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
	udevdir=/dev \
	libdir=/%{_lib} \
	usrlibdir=%{_libdir} \
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
	$RPM_BUILD_ROOT/lib/udev/devices

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	initdir=/etc/rc.d/init.d \
	libdir=/%{_lib} \
	usrlibdir=%{_libdir} \
	EXTRAS="%{extras}"

rm -f $RPM_BUILD_ROOT%{_sysconfdir}/udev/udev.rules
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/udev/udev.permissions
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/init.d/udev

# install rules
install etc/udev/rules.d/*.rules $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/40-alsa.rules
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/55-hotplug_map.rules
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/51-modprobe.rules
install %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/50-udev-default.rules
install %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/10-udev-example.rules

# install configs
install %{SOURCE10} $RPM_BUILD_ROOT%{_sysconfdir}/udev
install %{SOURCE11} $RPM_BUILD_ROOT%{_sysconfdir}/udev/links.conf

# install executables (scripts, helpers, etc.)
install %{SOURCE20} $RPM_BUILD_ROOT%{_prefix}/sbin/udev_import_usermap
install %{SOURCE21} $RPM_BUILD_ROOT/lib/udev/net_helper
install %{SOURCE22} $RPM_BUILD_ROOT%{_sbindir}/start_udev
install extras/path_id/path_id $RPM_BUILD_ROOT/lib/udev
%endif

# install misc
install %{SOURCE32} $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/udev_blacklist.conf

%if %{with initrd}
install -d $RPM_BUILD_ROOT%{_sbindir}
install -m755 initrd-* $RPM_BUILD_ROOT%{_sbindir}
ln -s initrd-udev $RPM_BUILD_ROOT%{_sbindir}/udevstart.initrd
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%triggerpostun -- dev
if [ "$2" = 0 ]; then
	# need to kill and restart udevd as after obsoleting dev package the
	# /dev tree will remain empty. umask is needed as otherwise udev will
	# create devices with strange permissions (udev bug probably)
	umask 000
	/sbin/start_udev || exit 0
fi

%post	-n libvolume_id -p /sbin/ldconfig
%postun	-n libvolume_id -p /sbin/ldconfig

%if %{with main}
%files
%defattr(644,root,root,755)
%doc ChangeLog FAQ README RELEASE-NOTES TODO
%doc docs/{overview,udev_vs_devfs,writing_udev_rules}

%dir /lib/udev

# /lib/udev/devices is recommended as a directory where packages or
# the user can place real device nodes, which get copied over to /dev at
# every boot. This should replace the various solutions with custom config
# files.
%dir /lib/udev/devices

%attr(755,root,root) /lib/udev/create_floppy_devices
%attr(755,root,root) /lib/udev/firmware.sh

%attr(755,root,root) /lib/udev/*_helper

%attr(755,root,root) /lib/udev/ata_id
%attr(755,root,root) /lib/udev/cdrom_id
%attr(755,root,root) /lib/udev/dasd_id
%attr(755,root,root) /lib/udev/edd_id
%attr(755,root,root) /lib/udev/path_id
%attr(755,root,root) /lib/udev/scsi_id
%attr(755,root,root) /lib/udev/usb_id
%attr(755,root,root) /lib/udev/vol_id

%attr(755,root,root) %{_sbindir}/start_udev
%attr(755,root,root) %{_sbindir}/udevcontrol
%attr(755,root,root) %{_sbindir}/udevd
%attr(755,root,root) %{_sbindir}/udevsettle
%attr(755,root,root) %{_sbindir}/udevtrigger
 
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_prefix}/sbin/*

%dir %{_sysconfdir}/udev
%dir %{_sysconfdir}/udev/rules.d

%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/modprobe.d/udev_blacklist.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/scsi_id.config
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/links.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/05-udev-early.rules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/40-alsa.rules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/50-udev-default.rules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/51-modprobe.rules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/60-persistent-input.rules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/60-persistent-storage.rules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/95-udev-late.rules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/udev.conf
%{_sysconfdir}/udev/rules.d/10-udev-example.rules
%{_sysconfdir}/udev/rules.d/55-hotplug_map.rules

%{_mandir}/man7/*
%{_mandir}/man8/*

%dev(c,1,3) %attr(666,root,root) /dev/null
%dev(c,5,1) %attr(660,root,console) /dev/console
%dev(c,1,5) %attr(666,root,root) /dev/zero
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

%files -n libvolume_id-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvolume_id.so
%{_includedir}/*.h
%{_pkgconfigdir}/*.pc

%files -n libvolume_id-static
%defattr(644,root,root,755)
%{_libdir}/libvolume_id.a
