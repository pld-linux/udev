Summary:	A userspace implementation of devfs
Summary(pl):	Implementacja devfs w przestrzeni u¿ytkownika
Name:		udev
Version:	004
Release:	1
License:	GPL
Group:		Base
Source0:	http://www.kernel.org/pub/linux/utils/kernel/hotplug/%{name}-%{version}.tar.bz2
# Source0-md5:	1f3cd6ba984ed947aa004be29ca362cf
BuildRequires:	sed >= 4.0
Requires:	coreutils
Requires:	hotplug >= 2003_08_05
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A userspace implementation of devfs for 2.5 and higher kernels.

%description -l pl
Implementacja devfs w przestrzeni u¿ytkownika dla j±der 2.5 i
wy¿szych.

%prep
%setup -q

%build
sed -i -e 's#CFLAGS = .*#CFLAGS = %{rpmcflags}#g' libsysfs/Makefile
%{__make} \
	udevdir=/dev \
	CC="%{__cc}" \
	%{!?debug:DEBUG=false} \
	OPTIMIZATION="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man{5,8},%{_sysconfdir}/{udev,hotplug.d/default}}

install udev $RPM_BUILD_ROOT%{_sbindir}
install namedev.config namedev.permissions $RPM_BUILD_ROOT%{_sysconfdir}/udev

ln -s /sbin/udev $RPM_BUILD_ROOT/etc/hotplug.d/default/udev.hotplug

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README TODO ChangeLog docs/*
%attr(750,root,root) %dir /etc/udev
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/udev/*
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_sysconfdir}/hotplug.d/default/*.hotplug
