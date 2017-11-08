# Change Log
All notable changes to this project will be documented in this file.

## 1.0.5 / 2017-11-06

### New Features
- Fixed setting config environment variables so they now merge with the exsisting environment instead of overriding.
- Adding cwd kwarg to the Task and Engine classes.  Tasks can now query its information in another working directory.