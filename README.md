# wshare

List Windows File Sharing shares and reconnect bookmarks.

## Introduction

I wrote this tool because I have a problem with my Windows File Sharing (SMB / CIFS) connections to my development VM dying and not reconnecting on their own.

`wshare` parses the output of the `net use` command and then reads in your `wshare_config.py` file. Then it allows you to list connections and bookmarks (merged together) with their connection status, and reconnect paths listed in your bookmarks.

## Requirements

* Windows
* Python 3.x

## Installation

1. Copy `wshare.py` to a path in your `%PATH%` environment variable. (For example, you could create a `C:\bin` folder and [edit your %PATH% variable](http://www.digitalcitizen.life/how-edit-or-delete-environment-variables-windows-7-windows-8).

2. If you have more than one Python installed, you should probably create a `wshare.cmd` file in the same folder with something like this:

        @echo off
        "C:\Programs\Python34\python.exe" %~dp0wshare.py %*

  (Edit the path to Python as needed.)

3. Create a `wshare_config.py` in the same folder:

        config = {
            'NAME1': {
                'drive_letter': 'N:',
                'path': '//SERVER1.EXAMPLE.COM/PATH1',
                'username': 'USER',
                'password': 'PASSWORD',
            },
            'NAME2': {
                'drive_letter': None,  # None for no drive letter; just connection
                'path': '//SERVER2.EXAMPLE.COM/PATH2',
                'username': 'USER',
                'password': 'PASSWORD',
            },
        }

## Usage

Use Windows' Run command (WIN + R key) and enter `wshare.py` (or `wshare` if you created a `wshare.cmd` launcher).

With no parameters, `wshare` will merge the output of `net use` with your bookmarks from `wshare_config.py` and show you a list of connections and bookmarks. Enter a number or a name of a bookmark to reconnect; it will be completely dropped and then reconnected. Then the program will loop until you make no selection. (Enter an empty string.)

You can also call `wshare.py NAME` or `wshare NAME` to skip listing the connections and immediately drop and reconnect the bookmark called `NAME`.

## Example Run

    C:\>wshare

    Network shares:

    :: G: \\files.mycorp.example.com\users$\bkidwell (not in config)
            Unavailable
    :: H: \\files.mycorp.example.com\itgroup\Common (not in config)
            Unavailable
    3 [devbox]:: T: \\devbox.local.example.com\Code
            Unavailable

    Reconnect which share number or name? (ENTER to quit) 3

    The command completed successfully.


    Network shares:

    :: G: \\files.mycorp.example.com\users$\bkidwell (not in config)
            Unavailable
    :: H: \\files.mycorp.example.com\itgroup\Common (not in config)
            Unavailable
    3 [devbox]:: T: \\devbox.local.example.com\Code
            OK

    Reconnect which share number or name? (ENTER to quit)
