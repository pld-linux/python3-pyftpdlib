#
# Conditional build:
%bcond_with	tests	# unit tests (can fail under heavy system load)
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Very fast asynchronous FTP server library for Python 2
Summary(pl.UTF-8):	Bardzo szybka biblioteka asynchronicznego serwera FTP dla Pythona 2
Name:		python-pyftpdlib
Version:	1.5.5
Release:	2
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.python.org/simple/pyftpdlib/
Source0:	https://files.pythonhosted.org/packages/source/p/pyftpdlib/pyftpdlib-%{version}.tar.gz
# Source0-md5:	7f8089520d60171bee5dab2b721e8d00
Patch0:		%{name}-tests.patch
Patch1:		%{name}-sendfile.patch
URL:		https://github.com/giampaolo/pyftpdlib/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.6
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-pyOpenSSL
BuildRequires:	python-pysendfile >= 1.5
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pyOpenSSL
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-modules >= 1:2.6
Suggests:	python-pyOpenSSL
Suggests:	python-pysendfile >= 1.5
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python FTP server library provides a high-level portable interface to
easily write very efficient, scalable and asynchronous FTP servers
with Python. It is the most complete RFC-959 FTP server implementation
available for Python programming language.

%description -l pl.UTF-8
Biblioteka serwera FTP dla Pythona udostępnia wysokopoziomowy,
przenośny interfejs do łatwego tworzenia bardzo wydajnych,
skalowalnych i asynchronicznych serwerów FTP w Pythonie. Jest to
najpełniejsza implementacja serwera FTP wg RFC-959 dostępna dla tego
języka programowania.

%package -n python3-pyftpdlib
Summary:	Very fast asynchronous FTP server library for Python 3
Summary(pl.UTF-8):	Bardzo szybka biblioteka asynchronicznego serwera FTP dla Pythona 3
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4
Suggests:	python3-pyOpenSSL

%description -n python3-pyftpdlib
Python FTP server library provides a high-level portable interface to
easily write very efficient, scalable and asynchronous FTP servers
with Python. It is the most complete RFC-959 FTP server implementation
available for Python programming language.

%description -n python3-pyftpdlib -l pl.UTF-8
Biblioteka serwera FTP dla Pythona udostępnia wysokopoziomowy,
przenośny interfejs do łatwego tworzenia bardzo wydajnych,
skalowalnych i asynchronicznych serwerów FTP w Pythonie. Jest to
najpełniejsza implementacja serwera FTP wg RFC-959 dostępna dla tego
języka programowania.

%prep
%setup -q -n pyftpdlib-%{version}
%patch0 -p1
%patch1 -p1

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTHONPATH=$(pwd)/build-2/lib \
%{__python} pyftpdlib/test/runner.py
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd)/build-3/lib \
%{__python3} pyftpdlib/test/runner.py
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%{__rm} $RPM_BUILD_ROOT%{_bindir}/ftpbench
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/pyftpdlib/test
%endif

%if %{with python3}
%py3_install
%{__rm} $RPM_BUILD_ROOT%{_bindir}/ftpbench
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/pyftpdlib/test
%endif

# in case there are examples provided
%if %{with python2}
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a demo/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
%endif
%if %{with python3}
install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-pyftpdlib-%{version}
cp -a demo/* $RPM_BUILD_ROOT%{_examplesdir}/python3-pyftpdlib-%{version}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CREDITS HISTORY.rst LICENSE README.rst
%{py_sitescriptdir}/pyftpdlib
%{py_sitescriptdir}/pyftpdlib-%{version}-py*.egg-info
%{_examplesdir}/%{name}-%{version}
%endif

%if %{with python3}
%files -n python3-pyftpdlib
%defattr(644,root,root,755)
%doc CREDITS HISTORY.rst LICENSE README.rst
%{py3_sitescriptdir}/pyftpdlib
%{py3_sitescriptdir}/pyftpdlib-%{version}-py*.egg-info
%{_examplesdir}/python3-pyftpdlib-%{version}
%endif
