# TODO
# - initrd build with uclibc on amd64 produces non-working binary (illegal instruction from open("/dev/null"))
#
# Conditional build:
%bcond_without	initrd	# build without udev-initrd
%bcond_without	uClibc	# link initrd version with static uClibc
%bcond_with	klibc	# link initrd version with static klibc
%bcond_with	dietlibc	# link initrd version with static dietlibc (currently broken and unsupported)
%bcond_with	glibc	# link initrd version with static glibc
%bcond_without	main	# don't compile main package, use for debugging initrd build

%ifarch %{x8664}
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
Summary(pl):	Implementacja devfs w przestrzeni u¿ytkownika
Name:		udev
Version:	075
Release:	1
Epoch:		1
License:	GPL
Group:		Base
Source0:	ftp://ftp.kernel.org/pub/linux/utils/kernel/hotplug/%{name}-%{version}.tar.bz2
# Source0-md5:	024ce408f74b05ff6b52b4ff250359da
Source1:	%{name}.rules
Source2:	%{name}.conf
Source3:	start_udev
Source4:	ftp://ftp.kernel.org/pub/linux/utils/kernel/hotplug/uevent_listen.c
# Source4-md5:	7b2b881a8531fd84da7cae9152dc4e39
# from Mandriva CVS:
# http://cvs.mandriva.com/cgi-bin/cvsweb.cgi/SPECS/udev/
# Needed for the automatic module loading w/o hotplug to work
# see:
# http://qa.mandrivalinux.com/twiki/bin/view/Main/Udev
# http://lwn.net/Articles/123932/
Source5:	%{name}_import_usermap
Source6:	%{name}-modprobe.rules
Source7:	%{name}-digicam
Source8:	%{name}-persistent.rules
Source9:	%{name}-hotplug_map.rules
# hotplug usb maps
Source10:	%{name}-usb.digicam
Source11:	%{name}-usb.distmap
Source12:	%{name}-usb.handmap
# helpers
Source20:	%{name}-ieee1394.helper
Source21:	%{name}-input.helper
Source22:	%{name}-net.helper
Source23:	%{name}-input-coldplug
Patch0:		%{name}-synthesize-02.patch
Patch1:		%{name}-synthesize-md
Patch2:		%{name}-synthesize-preserve_env
Patch3:		%{name}-coldplug.patch
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
Requires:	coreutils
Provides:	dev = 3.0.0
# Obsoletes:	hotplug
# Obsoletes:	hotplug-input
# Obsoletes:	hotplug-net
# Obsoletes:	hotplug-pci
# Obsoletes:	dev
Obsoletes:	udev-dev
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin
%define		extras		extras/ata_id extras/cdrom_id extras/dasd_id extras/edd_id extras/floppy extras/firmware extras/scsi_id extras/usb_id extras/volume_id

%description
A userspace implementation of devfs for 2.5 and higher kernels.

%description -l pl
Implementacja devfs w przestrzeni u¿ytkownika dla j±der 2.5 i
wy¿szych.

%package digicam
Summary:	udev agent for USB digital cameras
Summary(pl):	Agent udev dla aparatów cyfrowych na USB
Group:		Applications/System
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(postun):	/usr/sbin/groupdel
Requires:	%{name} = %{epoch}:%{version}-%{release}
Provides:	group(digicam)
Obsoletes:	hotplug-digicam
                                                                                                         
%description digicam
udev agent for USB digital cameras.

%description digicam -l pl
Agent udev dla aparatów cyfrowych na USB.

%package initrd
Summary:	A userspace implementation of devfs - static binary for initrd
Summary(pl):	Implementacja devfs w przestrzeni u¿ytkownika - statyczna binarka dla initrd
Group:		Base
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description initrd
A userspace implementation of devfs - static binary for initrd.

%description initrd -l pl
Implementacja devfs w przestrzeni u¿ytkownika - statyczna binarka dla
initrd.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

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
	OPTIMIZATION="%{rpmcflags}" \
	USE_KLIBC=%{!?with_klibc:false}%{?with_klibc:true} \
	USE_LOG=true \
	USE_SELINUX=false \
	EXTRAS=""

cp -a udev initrd-udev
%if %{with main}
%{__make} clean
%endif
%endif

%if %{with main}
%{__make} \
	udevdir=/dev \
	CC="%{__cc}" \
	DEBUG=%{!?debug:false}%{?debug:true} \
	OPTIMIZATION="%{rpmcflags}" \
	USE_KLIBC=false \
	USE_LOG=true \
	EXTRAS="%{extras}"

%{__cc} %{rpmcflags} %{SOURCE4} -o uevent_listen
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with main}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/udev/{agents.d/usb,rules.d,scripts,devices}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	initdir=%{_initrddir} \
	EXTRAS="%{extras}"

rm -f $RPM_BUILD_ROOT%{_sysconfdir}/udev/udev.rules
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/udev/udev.permissions
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/init.d/udev

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/udev.rules
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/udev/udev.conf
install %{SOURCE3} $RPM_BUILD_ROOT%{_sbindir}/start_udev
install %{SOURCE5} $RPM_BUILD_ROOT%{_prefix}/sbin/udev_import_usermap
install %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/modprobe.rules
install %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/udev/agents.d/usb/digicam
install %{SOURCE8} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/persistent.rules
install %{SOURCE9} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/hotplug_map.rules

install %{SOURCE20} $RPM_BUILD_ROOT%{_sbindir}/udev_ieee1394_helper
install %{SOURCE21} $RPM_BUILD_ROOT%{_sbindir}/udev_input_helper
install %{SOURCE22} $RPM_BUILD_ROOT%{_sbindir}/udev_net_helper
install %{SOURCE23} $RPM_BUILD_ROOT%{_sbindir}/udev_input_coldplug

install extras/path_id $RPM_BUILD_ROOT%{_sbindir}
install extras/dvb.sh $RPM_BUILD_ROOT%{_sysconfdir}/udev/scripts
install extras/raid-devfs.sh $RPM_BUILD_ROOT%{_sysconfdir}/udev/scripts
install extras/eventrecorder.sh $RPM_BUILD_ROOT%{_sbindir}
install uevent_listen $RPM_BUILD_ROOT%{_sbindir}
install udevsynthesize $RPM_BUILD_ROOT%{_sbindir}

%endif

%if %{with initrd}
install -d $RPM_BUILD_ROOT%{_sbindir}
install -m755 initrd-udev $RPM_BUILD_ROOT%{_sbindir}/initrd-udev
ln -s initrd-udev $RPM_BUILD_ROOT%{_sbindir}/udevstart.initrd
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%pre digicam
%groupadd -P %{name}-digicam -g 135 digicam

%postun digicam
if [ "$1" = "0" ]; then
	%groupremove digicam
fi
	    
%triggerpostun -- dev
if [ "$2" = 0 ]; then
	# need to kill and restart udevd as after obsoleting dev package the
	# /dev tree will remain empty. umask is needed as otherwise udev will
	# create devices with strange permissions (udev bug probably)
	umask 000
	/sbin/start_udev || exit 0
fi

%if %{with main}
%files
%defattr(644,root,root,755)
%doc ChangeLog FAQ README RELEASE-NOTES TODO
%doc docs/{overview,udev_vs_devfs,writing_udev_rules}
%doc libsysfs/libsysfs.txt
%doc extras/start_udev

%attr(755,root,root) %{_sbindir}/ata_id
%attr(755,root,root) %{_sbindir}/cdrom_id
%attr(755,root,root) %{_sbindir}/dasd_id
%attr(755,root,root) %{_sbindir}/edd_id
%attr(755,root,root) %{_sbindir}/path_id
%attr(755,root,root) %{_sbindir}/scsi_id
%attr(755,root,root) %{_sbindir}/usb_id
%attr(755,root,root) %{_sbindir}/vol_id

%attr(755,root,root) %{_sbindir}/create_floppy_devices
%attr(755,root,root) %{_sbindir}/firmware_helper
%attr(755,root,root) %{_sbindir}/udev_ieee1394_helper
%attr(755,root,root) %{_sbindir}/udev_input_coldplug
%attr(755,root,root) %{_sbindir}/udev_input_helper
%attr(755,root,root) %{_sbindir}/udev_net_helper

%attr(755,root,root) %{_sbindir}/start_udev
%attr(755,root,root) %{_sbindir}/udev
%attr(755,root,root) %{_sbindir}/udevcontrol
%attr(755,root,root) %{_sbindir}/udevd
%attr(755,root,root) %{_sbindir}/udevsend
%attr(755,root,root) %{_sbindir}/udevstart
%attr(755,root,root) %{_sbindir}/udevsynthesize
%attr(755,root,root) %{_sbindir}/uevent_listen
 
%attr(755,root,root) %{_sbindir}/eventrecorder.sh

%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_prefix}/sbin/*

%dir %{_sysconfdir}/udev
%dir %{_sysconfdir}/udev/agents.d
%dir %{_sysconfdir}/udev/agents.d/usb
%dir %{_sysconfdir}/udev/devices
%dir %{_sysconfdir}/udev/rules.d
%dir %{_sysconfdir}/udev/scripts

%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/scsi_id.config
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/udev.rules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/modprobe.rules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/persistent.rules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/udev.conf
%{_sysconfdir}/udev/rules.d/hotplug_map.rules

%attr(755,root,root) %{_sysconfdir}/udev/scripts/*

%{_mandir}/man8/*

%dev(c,1,3) %attr(666,root,root) /dev/null
%dev(c,5,1) %attr(660,root,console) /dev/console
%dev(c,1,5) %attr(666,root,root) /dev/zero
%endif

%if %{with initrd}
%files initrd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/initrd-udev
%attr(755,root,root) %{_sbindir}/udevstart.initrd
%endif

%files digicam
%defattr(644,root,root,755)
%attr(755,root,root) %{_sysconfdir}/udev/agents.d/usb/digicam
