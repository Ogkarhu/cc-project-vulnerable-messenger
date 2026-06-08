The vulnerabilities follow the OWASP 2021 list

LINK: https://github.com/Ogkarhu/cc-project-vulnerable-messenger

Install Instructions:

Requirements:

    Linux
    python3

Setup:

    Open a terminal in the project root.
    Create a virtual environment: python3 -m venv .venv
    Activate it: source .venv/bin/activate
    Install Django: pip install Django

Initialize Database And Admin

    Run: ./install.sh

    username: admin
    password: admin

Run The App:

    Start server: python3 manage.py runserver
    Open: http://127.0.0.1:8000/

---------------------------------------------------------------------------

FLAW 1:
https://github.com/Ogkarhu/cc-project-vulnerable-messenger/blob/main/messenger/views.py#L110


A02 cryptographic failures Plaintext passwords

In the views.py no library for password management or hashing is imported. Instead there is a handmade very simple implementation that just saves usernames and passwords to the database in plaintext. In a situation where an attacker gains access to the database, all username – password pairs can be stolen. This does not only endanger the integrity of this app but also creates a risk to users who use the same username – password combo elsewhere.

The fix in this case would be to use the Django built-in validate_password tool as fixed in the commented code. This way the password will be salted and hashed and only visible to the user. With this fix even if the database leaks, it would be much more difficult to find out the credentials of users. This also prevents the admins from seeing information they don’t need to see.



FLAW 2:
https://github.com/Ogkarhu/cc-project-vulnerable-messenger/blob/main/messenger/views.py#L110

https://github.com/Ogkarhu/cc-project-vulnerable-messenger/blob/main/messenger/views.py#L83

https://github.com/Ogkarhu/cc-project-vulnerable-messenger/blob/main/messenger/templates/messenger/register.html#L20

A01 Broken access control. Manual user creation and login

Users are created with a insecure form instead of a more secure built-in function. In the form there is a hidden field that allows the creation of an admin account if the person creating a account knows how to use devtools. In devtools anyone can just change the IS_ADMIN field to TRUE or change the field from type=”hidden” to type=”checkbox”.

The fix would be to disable generation of admin users from the web view as it is an unnecessary risk and does not have any perks other than convenience. The fix would thus be a removal of the lines from the frontend.



FLAW 3:
https://github.com/Ogkarhu/cc-project-vulnerable-messenger/blob/main/install.sh#L13

A05 broken security control

The installation script install.sh creates weak hardcoded admin credentials by default (admin/admin). The use of hardcoded credentials that the main user is not required to change is a bad practice. If the main user does not change the script, the admin user with admin/admin credentials will be a permanent open door for anyone as there is no way of removing users without manually changing them from the database.

To fix this issue one could require a ADMIN_USERNAME and ADMIN_PASSWORD to be set externally, or by generating a one time use secret. In the fixed code this is not implemented. What is implemented is a script that requires the main user to change the ADMIN_USERNAME" == "set-me-manually" || "$ADMIN_PASSWORD" == "set-a-strong-password-manually to a more secure one or the script exits. Once these credentials are changed, the script will run to completion and creates a more secure admin. I acknowledge that this is not the most secure way of solving this, and using the Django default tool for the admin page would be more secure, but I don’t want to default to the defaults in each case either.



FLAW 4:
https://github.com/Ogkarhu/cc-project-vulnerable-messenger/blob/main/messenger/views.py#L104

CSRF injection

There is a CSRF vulnerability due to irresponsible use of @csrf_exempt in the register view. The view does not check for csrf token which in return makes it vulnerable for creating a massive amount of accounts.


To fix this vulnerability, both the @csrf_exempt should be removed from the L104 and the corresponsive import from the start of the file should be removed. It’d be very rare to need to use such functionality.



FLAW 5:
https://github.com/Ogkarhu/cc-project-vulnerable-messenger/blob/main/messenger/templates/messenger/conversation.html#L22

A03 XSS injection 

The fields <strong>{{ message.user.name |safe}}:</strong> {{ message.message |safe}} allow user to run markdown unescaped. This could include malicious links or redirecting to external malicious sites. This could be used in phishing attacks or for spreading malware.

The simple fix would be to drop the safe flag from the fields and Django by default would handle the fields securely. It might be unnecessary but for the sake of demo we can fix the fields as {{ message.user.name|escape }}: {{ message.message|escape }}. This escapes the fields and effectively prevents injections. Some kind of backend sanitization would also be very necessary.



FLAW 6:
https://github.com/Ogkarhu/cc-project-vulnerable-messenger/blob/main/vulnerable_messenger/settings.py#L27

A05 Security misconfiguration

Django debug mode is on in the app. This shows a Django debug 404 page on worng or mistyped paths. The debug 404 page lists URL patterns used in the app revealing /obscure_very_secret_admin_page/. Keeping in mind that security by obscurity is not a safe approach but the debug page makes a malicious actors work way too easy. There should also be privilege checks on the admin page but those are not implemented

To fix this oversight, the Debug mode should be set as FALSE. No development features should be active in a production app.



Honorable mentions.
- Using the login name as screen name.
- No checks for duplicate usernames
- No rate limiting
- Existance of django admin panel with default credentials
