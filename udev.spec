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
Version:	070
Release:	4
Epoch:		1
License:	GPL
Group:		Base
Source0:	ftp://ftp.kernel.org/pub/linux/utils/kernel/hotplug/%{name}-%{version}.tar.bz2
# Source0-md5:	e990dcdc3a245f00373cd51a9e09b27f
Source1:	%{name}.rules
Source2:	%{name}-firmware.rules
Source3:	%{name}.conf
Source4:	start_udev
Source5:	devmap_name.tar.gz
# Source5-md5:	f72f557299436af5d6ad66815b80a641
Source6:	ftp://ftp.kernel.org/pub/linux/utils/kernel/hotplug/uevent_listen.c
# Source6-md5:	7b2b881a8531fd84da7cae9152dc4e39
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
Requires:	hotplug >= 2003_08_05
Provides:	dev = 3.0.0
# Obsoletes:	dev
Obsoletes:	udev-dev
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin
%define		extras		extras/ata_id extras/cdrom_id extras/chassis_id extras/dasd_id extras/floppy extras/firmware extras/run_directory extras/scsi_id extras/usb_id extras/volume_id

%description
A userspace implementation of devfs for 2.5 and higher kernels.

%description -l pl
Implementacja devfs w przestrzeni u¿ytkownika dla j±der 2.5 i
wy¿szych.

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
%setup -q -a5
sed -i -e 's#gcc#$(CC)#g' devmap_name/Makefile

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
	%{?with_klibc:CC="klcc"} \
	%{?with_klibc:LD="klcc %{rpmldflags} -static"} \
	DEBUG=%{!?debug:false}%{?debug:true} \
	OPTIMIZATION="%{rpmcflags}" \
	USE_KLIBC=false \
	USE_LOG=true \
	USE_SELINUX=false \
	EXTRAS=""

cp -a udev initrd-udev
%if %{without main}
%{__make} clean
%endif
%endif

%if %{with main}
%{__make} -C devmap_name \
	CC="%{__cc}" \
	OPTFLAGS="%{rpmcflags}"

%{__make} \
	udevdir=/dev \
	CC="%{__cc}" \
	DEBUG=%{!?debug:false}%{?debug:true} \
	OPTIMIZATION="%{rpmcflags}" \
	USE_KLIBC=false \
	USE_LOG=true \
	EXTRAS="%{extras}"

%{__cc} %{rpmcflags} %{SOURCE6} -o uevent_listen
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with main}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/udev/{rules.d,scripts}

# use of /etc/dev.d/ is no longer recommended
#install -d $RPM_BUILD_ROOT%{_sysconfdir}/dev.d/{default,net,snd}

install -d $RPM_BUILD_ROOT%{_sysconfdir}/hotplug.d/default

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	initdir=%{_initrddir} \
	EXTRAS="%{extras}"

rm -f $RPM_BUILD_ROOT%{_sysconfdir}/udev/udev.rules
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/udev/udev.permissions
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/init.d/udev

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/50-udev.rules
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/999-firmware.rules
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/udev/udev.conf
install %{SOURCE4} $RPM_BUILD_ROOT%{_sbindir}/start_udev
install extras/path_id $RPM_BUILD_ROOT%{_sbindir}
install extras/dvb.sh $RPM_BUILD_ROOT%{_sysconfdir}/udev/scripts
install extras/raid-devfs.sh $RPM_BUILD_ROOT%{_sysconfdir}/udev/scripts

ln -s %{_sbindir}/udevsend $RPM_BUILD_ROOT%{_sysconfdir}/hotplug.d/default/10-udev.hotplug

install devmap_name/devmap_name $RPM_BUILD_ROOT%{_sbindir}/devmap_name
install uevent_listen $RPM_BUILD_ROOT%{_sbindir}

%endif

%if %{with initrd}
install -d $RPM_BUILD_ROOT%{_sbindir}
install -m755 initrd-udev $RPM_BUILD_ROOT%{_sbindir}/initrd-udev
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

%if %{with main}
%files
%defattr(644,root,root,755)
%doc ChangeLog FAQ HOWTO-udev_for_dev README TODO
%doc docs/{overview,udev_vs_devfs}
%doc libsysfs/libsysfs.txt
%doc extras/start_udev
%attr(755,root,root) %{_sbindir}/*
%if %{with initrd}
%exclude %{_sbindir}/*initrd*
%endif
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_prefix}/sbin/*

%attr(755,root,root) %{_sysconfdir}/hotplug.d/default/10-udev.hotplug

# use of /etc/dev.d/ is no longer recommended
#%attr(755,root,root) %dir %{_sysconfdir}/dev.d
#%attr(755,root,root) %dir %{_sysconfdir}/dev.d/default
#%attr(755,root,root) %dir %{_sysconfdir}/dev.d/net
#%attr(755,root,root) %dir %{_sysconfdir}/dev.d/snd

%attr(755,root,root) %dir %{_sysconfdir}/udev
%attr(755,root,root) %dir %{_sysconfdir}/udev/rules.d
%attr(755,root,root) %dir %{_sysconfdir}/udev/scripts

%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/udev/udev.conf
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/udev/rules.d/50-udev.rules
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/udev/rules.d/999-firmware.rules
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/scsi_id.config

%attr(755,root,root) %{_sysconfdir}/udev/scripts/*

%{_mandir}/man8/*

%dev(c,1,3) %attr(666,root,root) /dev/null
%dev(c,5,1) %attr(660,root,console) /dev/console
%dev(c,1,5) %attr(666,root,root) /dev/zero
%endif

%if %{with initrd}
%files initrd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*initrd*
%endif
