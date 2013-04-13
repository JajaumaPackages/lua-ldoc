%global luaver 5.1
%global luapkgdir %{_datadir}/lua/%{luaver}

Name:		lua-ldoc
Version:	1.3.11
Release:	1%{?dist}
BuildArch:	noarch
Summary:	Lua documentation generator
# the included css code is BSD licensed
License:	MIT and BSD
URL:		https://github.com/stevedonovan/ldoc
Source0:	https://github.com/stevedonovan/LDoc/archive/%{version}/LDoc-%{version}.tar.gz
BuildRequires:	lua >= %{luaver}
BuildRequires:	lua-markdown
BuildRequires:	lua-penlight
Requires:	lua >= %{luaver}
Requires:	lua-markdown
Requires:	lua-penlight

%global __requires_exclude_from %{_docdir}

%description
LDoc is a second-generation documentation tool that can be used as a
replacement for LuaDoc. It is mostly compatible with LuaDoc, except
that certain workarounds are no longer needed. For instance, it is not
so married to the idea that Lua modules should be defined using the
module function.


%package doc
Summary:	Docs for lua-ldoc
Requires:	%{name} = %{version}-%{release}

%description doc
%{summary}


%prep
%setup -q -n LDoc-%{version}


%build
# nothing to do here


%install
mkdir -p %{buildroot}%{luapkgdir}
mkdir -p %{buildroot}%{_bindir}
make install \
  "LUA_SHAREDIR=%{luapkgdir}" \
  "LUA_BINDIR=%{_bindir}" \
  "DESTDIR=%{buildroot}"

# fix scripts
sed -i %{buildroot}%{_bindir}/ldoc -e '1i#!/bin/sh'
sed -i %{buildroot}%{luapkgdir}/ldoc.lua -e '1{/^#!/d}'

# create documentation
lua ldoc.lua .
markdown.lua readme.md > readme.html

# fix permissions
chmod u=rwX,go=rX -R out

# fix line-endings
sed -i 's/\r//' COPYRIGHT


%files
%doc COPYRIGHT readme.html
%{_bindir}/ldoc
%{luapkgdir}/ldoc
%{luapkgdir}/ldoc.lua


%files doc
%doc out/*


%changelog
* Sat Apr 13 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.3.11-1
- Update to 1.3.11.

* Thu Mar 21 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.3.7-2
- Require lua-markdown also at run time.

* Thu Mar 21 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.3.7-1
- Update to 1.3.7.

* Sat Feb 16 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.3.4-1
- Update to 1.3.4.

* Wed Jan 30 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.3.3-1
- Update to 1.3.3.

* Wed Jan  9 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.3.1-2
- Fix requirements.
- Move docs to a separate package.

* Fri Jan  4 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.3.1-1
- New package.
