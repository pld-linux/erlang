# NOTE: Building requires working DNS setup. Build may hang
#       even if _only_ first dns specified in resolv.conf
#       is unreachable.
# TODO
# - separate -devel (at least header files!)
# - modularize (odbc, etc)
# - manuals to %{_mandir}
# - investigate fPIC.patch
#
# Conditional build:
%bcond_with	java		# with Java support
%bcond_without	odbc		# without unixODBC support
#
Summary:	OpenSource Erlang/OTP
Summary(pl.UTF-8):	Erlang/OTP z otwartymi źródłami
Name:		erlang
# A - unstable, B - stable line, keep stable
Version:	R16B02
Release:	1
Epoch:		1
%define		_version	%(echo %{version} | tr _ -)
License:	distributable
Group:		Development/Languages
Source0:	http://www.erlang.org/download/otp_src_%{_version}.tar.gz
# Source0-md5:	ca63bcde0e5ae0f2df9457f97b3115a4
Source1:	http://www.erlang.org/download/otp_doc_man_%{_version}.tar.gz
# Source1-md5:	fe3ff42375090d33ce1ba98c28218cf3
Patch0:		%{name}-fPIC.patch
Patch1:		%{name}-tinfo.patch
URL:		http://www.erlang.org/
%{?with_java:BuildRequires:	/usr/bin/jar}
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	flex
%{?with_java:BuildRequires:	jdk >= 1.2}
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel >= 0.9.7
BuildRequires:	openssl-tools
BuildRequires:	perl-base
%if %{with odbc}
BuildRequires:	unixODBC-devel
%else
BuildConflicts:	unixODBC-devel
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define _erl_target %(echo %{_build}-gnu | sed -e's/amd64/x86_64/;s/athlon/i686/;s/ppc/powerpc/')

%description
Erlang is a programming language designed at the Ericsson Computer
Science Laboratory. Open-source Erlang is being released to help
encourage the spread of Erlang outside Ericsson.

%description -l pl.UTF-8
Erlang to język programowania opracowany w Ericsson Computer Science
Laboratory. Open-source Erlang został wydany, aby pomóc w
rozpowszechnianiu Erlanga poza Ericssonem.

%prep
%setup -q -n otp_src_%{_version}
%{__tar} xzf %{SOURCE1} man/ COPYRIGHT
#%patch0 -p1
%patch1 -p1

%build
find . -name config.sub | xargs -n 1 cp -f /usr/share/automake/config.sub
curd=$(pwd)
for i in $(find . -type f -name configure.in); do
	cd $(dirname $i)
	%{__autoconf}
	cd $curd
done
%configure \
%ifarch sparc
	CFLAGS="%{rpmcflags} -mv8plus" \
%endif
	--with-javac%{!?with_java:=no}
rm -f lib/ssl/SKIP
ERL_TOP=`pwd`; export ERL_TOP
 %{__make} -j1 \
	TARGET="%{_erl_target}" \
	|| { find . -name erl_crash.dump | xargs cat ; exit 1 ; }

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	TARGET="%{_erl_target}" \
	INSTALL_PREFIX=$RPM_BUILD_ROOT

sed -i -e"s#$RPM_BUILD_ROOT##" \
	$RPM_BUILD_ROOT%{_libdir}/%{name}/bin/{erl,start,start_erl}

cp -r man $RPM_BUILD_ROOT%{_libdir}/%{name}
find $RPM_BUILD_ROOT%{_libdir}/%{name}/man -type f | xargs gzip -9

# some files in the library need +x, so we build the list here
echo "%%defattr(644,root,root,755)" > lib.list
find $RPM_BUILD_ROOT%{_libdir}/%{name}/lib -type d \
	| sed -e"s#^$RPM_BUILD_ROOT%{_libdir}/%{name}/#%%dir %%{_libdir}/%%{name}/#" >> lib.list
find $RPM_BUILD_ROOT%{_libdir}/%{name}/lib -type f -perm -500 \
	| sed -e"s#^$RPM_BUILD_ROOT%{_libdir}/%{name}/#%%attr(755,root,root) %%{_libdir}/%%{name}/#" >> lib.list
find $RPM_BUILD_ROOT%{_libdir}/%{name}/lib -type f '!' -perm -500 \
	| sed -e"s#^$RPM_BUILD_ROOT%{_libdir}/%{name}/#%%{_libdir}/%%{name}/#" >> lib.list

%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/%{name}/erts-*/lib
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/%{name}/erts-*/include/internal

%clean
rm -rf $RPM_BUILD_ROOT

%files -f lib.list
%defattr(644,root,root,755)
%doc AUTHORS EPLICENCE COPYRIGHT
%attr(755,root,root) %{_bindir}/ct_run
%attr(755,root,root) %{_bindir}/dialyzer
%attr(755,root,root) %{_bindir}/epmd
%attr(755,root,root) %{_bindir}/erl
%attr(755,root,root) %{_bindir}/erlc
%attr(755,root,root) %{_bindir}/escript
%attr(755,root,root) %{_bindir}/run_erl
%attr(755,root,root) %{_bindir}/to_erl
%attr(755,root,root) %{_bindir}/typer
%dir %{_libdir}/erlang
%dir %{_libdir}/%{name}/bin
%attr(755,root,root) %{_libdir}/%{name}/bin/ct_run
%attr(755,root,root) %{_libdir}/%{name}/bin/dialyzer
%attr(755,root,root) %{_libdir}/%{name}/bin/epmd
%attr(755,root,root) %{_libdir}/%{name}/bin/erl
%attr(755,root,root) %{_libdir}/%{name}/bin/erlc
%attr(755,root,root) %{_libdir}/%{name}/bin/escript
%attr(755,root,root) %{_libdir}/%{name}/bin/run_erl
%attr(755,root,root) %{_libdir}/%{name}/bin/start
%attr(755,root,root) %{_libdir}/%{name}/bin/start_erl
%attr(755,root,root) %{_libdir}/%{name}/bin/to_erl
%attr(755,root,root) %{_libdir}/%{name}/bin/typer
%{_libdir}/%{name}/bin/start*.*
%dir %{_libdir}/%{name}/erts-*
%{_libdir}/%{name}/erts-*/doc
%{_libdir}/%{name}/erts-*/man
%{_libdir}/%{name}/erts-*/src
%{_libdir}/%{name}/erts-*/include
#%{_libdir}/%{name}/erts-*/*.ear
%dir %{_libdir}/%{name}/erts-*/bin
%attr(755,root,root) %{_libdir}/%{name}/erts-*/bin/beam*
%attr(755,root,root) %{_libdir}/%{name}/erts-*/bin/child*
%attr(755,root,root) %{_libdir}/%{name}/erts-*/bin/ct_run
%attr(755,root,root) %{_libdir}/%{name}/erts-*/bin/dialyzer
%attr(755,root,root) %{_libdir}/%{name}/erts-*/bin/dyn_erl
%attr(755,root,root) %{_libdir}/%{name}/erts-*/bin/e*
%attr(755,root,root) %{_libdir}/%{name}/erts-*/bin/heart*
%attr(755,root,root) %{_libdir}/%{name}/erts-*/bin/inet_gethost
%attr(755,root,root) %{_libdir}/%{name}/erts-*/bin/run_erl
%attr(755,root,root) %{_libdir}/%{name}/erts-*/bin/start
%attr(755,root,root) %{_libdir}/%{name}/erts-*/bin/to_erl
%attr(755,root,root) %{_libdir}/%{name}/erts-*/bin/typer
%{_libdir}/%{name}/erts-*/bin/start*.*
# (file list dynamically generated) %{_libdir}/%{name}/lib
%dir %{_libdir}/%{name}/misc
%attr(755,root,root) %{_libdir}/%{name}/misc/*
%{_libdir}/%{name}/releases
%{_libdir}/%{name}/usr
%doc %{_libdir}/%{name}/man
%attr(755,root,root) %{_libdir}/%{name}/Install
