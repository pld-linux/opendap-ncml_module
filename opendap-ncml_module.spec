# NOTE: for versions >= 1.4.1 see bes.spec
#
# Conditional build:
%bcond_with	tests	# make check (requires BES server)
#
Summary:	NCML module for the OPeNDAP data server
Summary(pl.UTF-8):	Moduł NCML dla serwera danych OPeNDAP
Name:		opendap-ncml_module
Version:	1.2.4
Release:	5
License:	LGPL v2.1+
Group:		Daemons
Source0:	http://www.opendap.org/pub/source/ncml_module-%{version}.tar.gz
# Source0-md5:	959411980d1653a384ef3a0e37ed2447
Patch0:		%{name}-includes.patch
URL:		http://opendap.org/
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake
%{?with_tests:BuildRequires:	bes >= 3.13.0}
BuildRequires:	bes-devel >= 3.13.0
BuildRequires:	bes-devel < 3.14
BuildRequires:	curl-devel
BuildRequires:	libdap-devel >= 3.13.0
BuildRequires:	libicu-devel >= 3.6
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	perl-base
BuildRequires:	pkgconfig
Requires:	bes >= 3.13.0
Requires:	libdap >= 3.13.0
Requires:	libicu >= 3.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is the NcML module for the OPeNDAP data server. It parses NcML
files to add metadata to other local datasets on the local Hyrax
server. It also allows authors to create joinNew and union
aggregations of other datasets.

%description -l pl.UTF-8
Ten pakiet zawiera moduł NcML dla serwera danych OPeNDAP. Analizuje
pliki NcML w celu dodania metadanych do innych lokalnych zbiorów
danych na lokalnym serwerze Hyrax. Ponadto pozwala autorom na
tworzenie agregatów joinNew i union innych zbiorów danych.

%prep
%setup -q -n ncml_module-%{version}
%patch -P0 -p1

%build
# rebuild autotools for -as-needed to work
%{__libtoolize}
%{__aclocal} -I conf
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/bes/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYRIGHT ChangeLog NEWS README
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bes/modules/ncml.conf
%attr(755,root,root) %{_libdir}/bes/libncml_module.so
%dir %{_datadir}/hyrax/data/nc
%{_datadir}/hyrax/data/nc/*.nc
%dir %{_datadir}/hyrax/data/ncml
%{_datadir}/hyrax/data/ncml/*.nc
%{_datadir}/hyrax/data/ncml/*.ncml
%dir %{_datadir}/hyrax/data/ncml/agg
%{_datadir}/hyrax/data/ncml/agg/*.ncml
%dir %{_datadir}/hyrax/data/ncml/agg/dated
%{_datadir}/hyrax/data/ncml/agg/dated/*.nc
%dir %{_datadir}/hyrax/data/ncml/agg/grids
%{_datadir}/hyrax/data/ncml/agg/grids/*.hdf
