Summary:	OpenSource Erlang/OTP
Summary(pl):	Erlang/OTP z otwartymi ¼ród³ami
Name:		otp
Version:	R9C_2
Release:	0.1
Epoch:		1
License:	distributable
Group:		Development/Languages
%define		_version	%(echo %{version} | tr _ -)
Source0:	http://www.erlang.org/download/%{name}_src_%{_version}.tar.gz
URL:		http://www.erlang.org/
BuildRequires:	XFree86-devel
BuildRequires:	autoconf
BuildRequires:	flex
BuildRequires:	perl-base
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Erlang is a programming language designed at the Ericsson Computer
Science Laboratory. Open-source Erlang is being released to help
encourage the spread of Erlang outside Ericsson.

%description -l pl
Erlang to jêzyk programowania opracowany w Ericsson Computer Science
Laboratory. Open-source Erlang zosta³ wydany, aby pomóc w
rozpowszechnianiu Erlanga poza Ericssonem.

%prep
%setup -q -n %{name}_src_%{_version}

%build
%{__autoconf}
cd lib
%{__autoconf}
cd erl_interface
%{__autoconf}
cd ../gs
%{__autoconf}
cd ../megaco
%{__autoconf}
cd ../snmp
%{__autoconf}
cd ../../erts/
%{__autoconf}
cd ..
%configure
ERL_TOP=`pwd`; export ERL_TOP
%{__make} \
	TARGET="%{_build}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	TARGET="%{_build}" \
	INSTALL_PREFIX=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/erlang/erts-*/*.html

sed -i -e"s#$RPM_BUILD_ROOT##" \
	$RPM_BUILD_ROOT%{_libdir}/erlang/bin/{erl,start,start_erl}

for l in erl erlc ; do
	ln -sf %{_libdir}/erlang/bin/$l $RPM_BUILD_ROOT%{_bindir}
done
ERTSDIR=`echo $RPM_BUILD_ROOT%{_libdir}/erlang/erts-* | sed -e"s#^$RPM_BUILD_ROOT##"`
for l in ear ecc elink escript ; do
	ln -sf $ERTSDIR/bin/$l $RPM_BUILD_ROOT%{_bindir}
done
ln -sf $ERTSDIR/bin/epmd $RPM_BUILD_ROOT%{_libdir}/erlang/bin

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS EPLICENCE README erts/notes.html
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/erlang
%attr(755,root,root) %{_libdir}/erlang/bin/epmd
%attr(755,root,root) %{_libdir}/erlang/bin/erl
%attr(755,root,root) %{_libdir}/erlang/bin/erlc
%attr(755,root,root) %{_libdir}/erlang/bin/run_erl
%attr(755,root,root) %{_libdir}/erlang/bin/start
%attr(755,root,root) %{_libdir}/erlang/bin/start_erl
%attr(755,root,root) %{_libdir}/erlang/bin/to_erl
%{_libdir}/erlang/bin/start*.*
%dir %{_libdir}/erlang/erts-*
%{_libdir}/erlang/erts-*/doc
%{_libdir}/erlang/erts-*/man
%{_libdir}/erlang/erts-*/src
%{_libdir}/erlang/erts-*/*.ear
%attr(755,root,root) %{_libdir}/erlang/erts-*/bin/beam*
%attr(755,root,root) %{_libdir}/erlang/erts-*/bin/child*
%attr(755,root,root) %{_libdir}/erlang/erts-*/bin/e*
%attr(755,root,root) %{_libdir}/erlang/erts-*/bin/heart*
%attr(755,root,root) %{_libdir}/erlang/erts-*/bin/inet_gethost
%attr(755,root,root) %{_libdir}/erlang/erts-*/bin/run_erl
%attr(755,root,root) %{_libdir}/erlang/erts-*/bin/start
%attr(755,root,root) %{_libdir}/erlang/erts-*/bin/to_erl
%{_libdir}/erlang/erts-*/bin/start*.*
%{_libdir}/erlang/lib
%dir %{_libdir}/erlang/misc
%attr(755,root,root) %{_libdir}/erlang/misc/*
%{_libdir}/erlang/releases
%{_libdir}/erlang/usr
%attr(755,root,root) %{_libdir}/erlang/Install
