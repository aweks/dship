--------------------------------------------------------------------------------
NOTE: When initially syncing the database you must comment out the line
with start_listeners() on it in payment/models.py (currently line 7) otherwise
the database won't sync correctly due to the database tables not
existing at the time of syncing.

As soon as you have done the first round of syncing and migrations you
can then uncomment those lines and the code will work perfectly.

--------------------------------------------------------------------------------
NOTE: When registering the very first user (the initial admin user) you
must set the username to be the same as the email address of the user
otherwise the login forms won't work. This is the only user this applies
to and happens because the admin user is created before the registration
module is loaded.

--------------------------------------------------------------------------------
NOTE: You must update the MEDIA_URL setting to the correct URL of your
website.
