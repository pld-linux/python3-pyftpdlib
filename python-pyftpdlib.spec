#
# Conditional build:
%bcond_without	tests		# unit tests (can fail under heavy system load)
%bcond_with	tests_net	# functional tests, localhost networking required
%bcond_without	python2		# CPython 2.x module
%bcond_without	python3		# CPython 3.x module

Summary:	Very fast asynchronous FTP server library for Python 2
Summary(pl.UTF-8):	Bardzo szybka biblioteka asynchronicznego serwera FTP dla Pythona 2
Name:		python-pyftpdlib
# keep 1.x here for python2 support
Version:	1.5.10
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.python.org/simple/pyftpdlib/
Source0:	https://files.pythonhosted.org/packages/source/p/pyftpdlib/pyftpdlib-%{version}.tar.gz
# Source0-md5:	a07bad18db605c1e1a38087c170fddb8
URL:		https://github.com/giampaolo/pyftpdlib/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-pyOpenSSL
BuildRequires:	python-pysendfile >= 1.5
BuildRequires:	python-pytest
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pyOpenSSL
BuildRequires:	python3-pytest
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-modules >= 1:2.7
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

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python} -m pytest pyftpdlib/test \
%if %{without tests_net}
	--ignore pyftpdlib/test/test_functional.py \
	--ignore pyftpdlib/test/test_functional_ssl.py \
	--ignore pyftpdlib/test/test_servers.py
%endif
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest pyftpdlib/test \
	--ignore pyftpdlib/test/test_functional.py \
	--ignore pyftpdlib/test/test_functional_ssl.py \
	--ignore pyftpdlib/test/test_servers.py
%if %{without tests_net}
%endif
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

%if %{with python2}
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a demo/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
%{__sed} -i -e '1s,/usr/bin/env python3,%{__python},' \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/*.py
%endif
%if %{with python3}
install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-pyftpdlib-%{version}
cp -a demo/* $RPM_BUILD_ROOT%{_examplesdir}/python3-pyftpdlib-%{version}
%{__sed} -i -e '1s,/usr/bin/env python3,%{__python3},' \
	$RPM_BUILD_ROOT%{_examplesdir}/python3-pyftpdlib-%{version}/*.py
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
