# Changelog

## 1.0.0

- Dropped support for Python 2.6
- Added Python 3 support
- Dropped support for Django < 1.8
- Django 1.8 & Django 1.9 are now supported
- Tests are run using tox (for all Python and Django versions)
- Switched to more semantic versioning
- Removed old south migrations, added Django migrations
- Refactoring and cleanup

## 0.5:

- Fixed DateTimeField RuntimeWarning (thanks to [yurtaev](https://github.com/yurtaev>))
- Tests are using Django 1.4.10 now

## 0.4:

- Usage of `AUTH_USER_MODEL` instead of `auth.models.User` (thanks to [timbutler](https://github.com/timbutler))

## 0.3:

- Removed south as dependency
- Small cleanups (thanks to [gwrtheyrn](https://github.com/gwrtheyrn>))

## 0.2:

- Updated `related_name` to avoid namespace clashes
- Added south as dependency
