# TODO
# - check py3 tests, are they ran?
# - rename to python-markdown (after current python-markdown) is trashed

# Conditional build:
%bcond_without	tests	# do not perform "make test"
%bcond_without	py3	# do not build python3 package

%define		srcname	Markdown
Summary:	Markdown implementation in Python
Name:		python-Markdown
Version:	2.2.1
Release:	1
License:	BSD
Group:		Development/Languages/Python
URL:		http://packages.python.org/Markdown/
Source0:	http://pypi.python.org/packages/source/M/%{srcname}/%{srcname}-%{version}.tar.gz
# Source0-md5:	9e002c8051fb346cae75060f3302048a
BuildRequires:	python-devel
BuildRequires:	python-elementtree
BuildRequires:	python-nose
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
%if %{with py3}
BuildRequires:	python3-devel
BuildRequires:	python3-nose
# for converting before running the tests:
BuildRequires:	python-2to3
%endif
Requires:	python-elementtree
Obsoletes:	python-markdown = 2.2.1
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a Python implementation of John Gruber's Markdown. It is
almost completely compliant with the reference implementation, though
there are a few known issues.

%package -n python3-markdown
Summary:	Markdown implementation in Python
Group:		Development/Languages/Python

%description -n python3-markdown
This is a Python implementation of John Gruber's Markdown. It is
almost completely compliant with the reference implementation, though
there are a few known issues.

%prep
# install does not support --build-base. so create two different trees
%setup -qc
mv %{srcname}-%{version} py2
cd py2

# remove shebangs
find markdown -type f -name '*.py' -exec sed -i -e '/^#!/{1D}' {} ';'

# fix line-ending
sed -i 's/\r//' docs/release-2.2.0.txt

cd ..
cp -a py2 py3

%build
cd py2
%{__python} setup.py build

%if %{with py3}
cd ../py3
%{__python3} setup.py build
%endif

%if %{with tests}
cd ../py2
./run-tests.py

%if %{with py3}
cd ../py3
2to3 -d -w -n markdown tests run-tests.py > /dev/null
# FIXME: run-tests.py shebang points to python2, is that correct?
./run-tests.py
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT
# somewhy --build-base not supported in install
cd py2
%{__python} setup.py install \
	--optimize=2 \
	--skip-build \
	--root $RPM_BUILD_ROOT

%py_postclean

# rename binary
mv $RPM_BUILD_ROOT%{_bindir}/markdown_py{,-%{py_ver}}

%if %{with py3}
cd ../py3
%{__python3} setup.py install \
	--optimize=2 \
	--skip-build \
	--root $RPM_BUILD_ROOT

# rename binary
mv $RPM_BUILD_ROOT%{_bindir}/markdown_py{,-%{py3_ver}}
%endif

# 2.X binary is called by default for now
ln -s markdown_py-%{py_ver} $RPM_BUILD_ROOT%{_bindir}/markdown_py

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc py2/docs/*
%attr(755,root,root) %{_bindir}/markdown_py
%attr(755,root,root) %{_bindir}/markdown_py-%{py_ver}
%{py_sitescriptdir}/markdown
%{py_sitescriptdir}/Markdown-%{version}-py*.egg-info

%if %{with py3}
%files -n python3-markdown
%defattr(644,root,root,755)
%doc py3/docs/*
%attr(755,root,root) %{_bindir}/markdown_py-%{py3_ver}
%{py3_sitescriptdir}/Markdown-%{version}-py*.egg-info
%{py3_sitescriptdir}/markdown
%endif
