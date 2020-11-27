This program, if run as an administrator, will create a new full access account on a remote computer.
It will also write the computer's public name, IPv4, and IPv6 in a specified Google document.

In the credentials.txt file, write the username on the first line and the password on the second line.
If the account already exists on the target computer, the new one will not be created.
The Chrome browser is also required to connect to the internet to write to the Google Document (as a Chrome driver is used for internet connection).

Depending on the version and settings of the target computer, attackers can possibly use this information to establish a remote connection.
This has only been tested on Windows, and will most likely not work with other operating systems.

NOTE: Do not edit the cleartext.txt file

Use this program responsibly (only for tests and personal use).  Enjoy :)