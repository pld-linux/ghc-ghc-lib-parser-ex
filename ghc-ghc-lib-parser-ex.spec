#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	ghc-lib-parser-ex
Summary:	Algorithms on GHC parse trees
Name:		ghc-%{pkgname}
Version:	8.10.0.11
Release:	1
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/ghc-lib-parser-ex
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	d6ca471d3c449e73c24fab70b05d0036
URL:		http://hackage.haskell.org/package/ghc-lib-parser-ex
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-uniplate
%if %{with prof}
BuildRequires:	ghc-prof
BuildRequires:	ghc-uniplate-prof
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
Requires:	ghc-uniplate
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
The ghc-lib-parser-ex package contains GHC API parse tree utilities.
It works with or without ghc-lib-parser.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-uniplate-prof

%description prof
Profiling %{pkgname} library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc ChangeLog.md README.md %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/GhclibParserEx
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/GhclibParserEx/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/GhclibParserEx/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/GhclibParserEx/GHC
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/GhclibParserEx/GHC/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/GhclibParserEx/GHC/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/GhclibParserEx/GHC/Driver
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/GhclibParserEx/GHC/Driver/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/GhclibParserEx/GHC/Driver/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/GhclibParserEx/GHC/Hs
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/GhclibParserEx/GHC/Hs/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/GhclibParserEx/GHC/Hs/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/GhclibParserEx/GHC/Types
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/GhclibParserEx/GHC/Types/Name
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/GhclibParserEx/GHC/Types/Name/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/GhclibParserEx/GHC/Types/Name/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/GhclibParserEx/GHC/Utils
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/GhclibParserEx/GHC/Utils/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/GhclibParserEx/GHC/Utils/*.dyn_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/include

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/GhclibParserEx/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/GhclibParserEx/GHC/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/GhclibParserEx/GHC/Driver/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/GhclibParserEx/GHC/Hs/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/GhclibParserEx/GHC/Types/Name/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/GhclibParserEx/GHC/Utils/*.p_hi
%endif
