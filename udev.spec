#
# Conditional build:
%bcond_without	initrd	# build without udev-initrd
%bcond_without	uClibc	# link initrd version with static dietlibc instead of uClibc
#
Summary:	A userspace implementation of devfs
Summary(pl):	Implementacja devfs w przestrzeni u¿ytkownika
Name:		udev
Version:	068
Release:	4
Epoch:		1
License:	GPL
Group:		Base
Source0:	ftp://ftp.kernel.org/pub/linux/utils/kernel/hotplug/%{name}-%{version}.tar.bz2
# Source0-md5:	fd9db7375dae81e8aa634414b5ede0d6
Source1:	%{name}.rules
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
%{!?with_uClibc:BuildRequires:	dietlibc-static}
%{?with_uClibc:BuildRequires:	uClibc-static >= 0.9.28}
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
	%{!?with_uClibc:CC="%{_target_cpu}-dietlibc-gcc"} \
	%{!?with_uClibc:LD="%{_target_cpu}-dietlibc-gcc %{rpmldflags} -static"} \
	%{!?debug:DEBUG=false} \
	OPTIMIZATION="%{rpmcflags}" \
	USE_KLIBC=false \
	USE_LOG=true \
	USE_SELINUX=false \
	EXTRAS=""

cp -a udev initrd-udev
%{__make} clean
%endif

%{__make} -C devmap_name \
	CC="%{__cc}" \
	OPTFLAGS="%{rpmcflags}"

%{__make} \
	udevdir=/dev \
	CC="%{__cc}" \
	%{!?debug:DEBUG=false} \
	OPTIMIZATION="%{rpmcflags}" \
	USE_KLIBC=false \
	USE_LOG=true \
	EXTRAS="%{extras}"

%{__cc} %{rpmcflags} %{SOURCE6} -o uevent_listen

%install
rm -rf $RPM_BUILD_ROOT

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
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/udev/udev.conf
install %{SOURCE4} $RPM_BUILD_ROOT%{_sbindir}/start_udev
install extras/path_id $RPM_BUILD_ROOT%{_sbindir}
install extras/dvb.sh $RPM_BUILD_ROOT%{_sysconfdir}/udev/scripts
install extras/raid-devfs.sh $RPM_BUILD_ROOT%{_sysconfdir}/udev/scripts

ln -s %{_sbindir}/udevsend $RPM_BUILD_ROOT%{_sysconfdir}/hotplug.d/default/10-udev.hotplug

%if %{with initrd}
install -m755 initrd-udev $RPM_BUILD_ROOT%{_sbindir}/initrd-udev
ln -s initrd-udev $RPM_BUILD_ROOT%{_sbindir}/udevstart.initrd
%endif

install devmap_name/devmap_name $RPM_BUILD_ROOT%{_sbindir}/devmap_name
install uevent_listen $RPM_BUILD_ROOT%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%triggerpostun -- dev
# need to kill and restart udevd as after obsoleting dev package the
# /dev tree will remain empty. umask is needed as otherwise udev will
# create devices with strange permissions (udev bug probably)
umask 000
/sbin/start_udev

%files
%defattr(644,root,root,755)
%doc ChangeLog FAQ HOWTO-udev_for_dev README TODO
%doc docs/{overview,udev_vs_devfs,libsysfs.txt}
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
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/scsi_id.config

%attr(755,root,root) %{_sysconfdir}/udev/scripts/*

%{_mandir}/man8/*

%dev(c,1,3) %attr(666,root,root) /dev/null
%dev(c,5,1) %attr(660,root,console) /dev/console
%dev(c,1,5) %attr(666,root,root) /dev/zero

%if %{with initrd}
%files initrd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*initrd*
%endif
