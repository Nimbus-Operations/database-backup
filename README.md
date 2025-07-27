## Database Backup

An application for doing coordinated dumps of multiple SQL databases.

This tool will connect to local or remote SQL servers and initiate dumps of
multiple databases, either on a predefined schedule or on demand.

This is currently pre-alpha code.

The project lacks a good name.  This repository will probably be renamed once
I pick one.

## Rationale

Why am I writing this?  There are almost certainly other tools out there that
will do the same job.  

1. I have some specific requirements in mind and trying to search for and
   evaluate a bunch of other open source projects sounds boring right now.

2. I've been looking for a project that lends itself to learning the
   [textualize/rich](https://github.com/Textualize/rich) framework, and this
   seems ideal.

This isn't just a toy project.  I fully intend to run this in production, when
it's ready.

## Features and Support

A rundown of the things I have in mind to support in version 1.0:

- PostgreSQL:  I'm intending to write this in a way that it could be extended
  to support other common databases, but I only need PostgreSQL support right
  now, so that's what I'm including.

- Local Dump: Dumps can be obtained from remote servers, but are written to a
  specified directory on the local server.

- Multiple Servers: Each database configured for dump can have its own server
  specified, or inherit the default from the global configuration, allowing
  multiple SQL servers in the same network to all be dumped to one central
  place.

- Dump Scheduling: Each database configured can have its own schedule,
  inherit from a default, or be configured to dump on every execution of the
  application.  Schedules are expressed as every every 1 days, every 5 days,
  every 2 weeks, etc.

- Cron Execution: To support backups with varying schedules, the application
  can be run from cron frequently (e.g. every 30 minutes).  It will check its
  schedule and history, determine if anything needs backing up, and exit if
  not.

- Terminal Execution: This is the fun part.  When run from the terminal it
  will display a
  [TUI](https://en.wikipedia.org/wiki/Text-based_user_interface) showing
  expected operations, progress, and some activity detail.

- Environment: Initially this will only be developed/tested on posix
  (unix-like) operating systems.  Mostly Linux and MacOS.  I see no reason it
  shouldn't work on Windows and other places that Python runs, but (at least
  at first) my testing will be confined to the environments I need to run it
  in.  I welcome anyone who wants to test it in other environments and provide
  feedback.
