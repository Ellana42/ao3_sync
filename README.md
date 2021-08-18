# AO3-SYNC

This is a program which aims to sync an archive of our own work with a local folder. It would allow to push the modifications made locally on to AO3 and pull changes made online.

## Installation instructions

- Clone package 
- Create a credential file with this template
{
    "username":"YOURUSERNAME",
    "password":"YOURPASSWORD"
}
- modify the path in config.py 
- use the pull function where you want your files to be to initialise your fanfic directory 

Then you can pull/push as you like !

**Warning** these actions are not reversible nor intelligent ! Pulling will overwrite your local files and pushing will overwrite your published fanfic ! Use with care and create backups


## Features

- post chapter
- pull chapter

## TODO

- push changes to existing chapter
- sync work
