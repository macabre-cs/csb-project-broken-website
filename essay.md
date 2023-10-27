# Cyber Security Base Project Essay
This essay pinpoints the flaws of the application and describes how they can be fixed.

## FLAW 1 Missing CSRF protection:
https://github.com/macabre-cs/csb-project-broken-website/blob/f9069e556806e82306979e08915829cb04f3b7e8/users/views.py#L12

This website is missing CSRF protection in various places and here is an example of it. When we are using Django’s ```@csrf_exempt``` decorator this view is exempt from the protection that is ensured by the Django middleware.

Since the CSRF protection is missing it is possible for an attacker to stage a denial-of-service attack. The attacker can send a huge amount of register requests to overload the server. Let me explain how to do it in steps:

- Open the website and developer tools. Go to the network tab.
- Register as a user.
- Copy register/ as a cURL

You will get something like this:
```bash
curl 'http://127.0.0.1:8000/register/' \
  -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
  -H 'Accept-Language: en-GB,en-US;q=0.9,en;q=0.8,fi;q=0.7,ja;q=0.6' \
  -H 'Cache-Control: no-cache' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H 'Cookie: csrftoken=FYUJhTvcHclfl0KxwniEEHi4UJXmysBR; sessionid=3g6swxl0ytk6m24svzf58tgyjmow7ll6' \
  -H 'Origin: http://127.0.0.1:8000' \
  -H 'Pragma: no-cache' \
  -H 'Referer: http://127.0.0.1:8000/register/' \
  -H 'Sec-Fetch-Dest: document' \
  -H 'Sec-Fetch-Mode: navigate' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'Sec-Fetch-User: ?1' \
  -H 'Upgrade-Insecure-Requests: 1' \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  --data-raw 'username=testi&email=testi%40testi.com&password1=testi&password2=testi' \
  --compressed
```
Now how to use this:
- You are able to change the username and other register information (second last row of the cURL).
- In this example let’s change it to testi2.
```bash
'username=testi2&email=testi2%40testi.com&password1=testi&password2=testi' \
```
- You can now replace the edited row with the original one in the cURL.
  
To make a new user without CSRF token simply open terminal and paste your edited cURL into it. This is only possible because of the decorator.

This flaw can be simply fixed by removing the decorators. This attack is not enabled by the absence of CSRF protection alone. It would be good to add spam protection to the register form by adding a captcha.

## FLAW 2 Broken access control:
https://github.com/macabre-cs/csb-project-broken-website/blob/f9069e556806e82306979e08915829cb04f3b7e8/users/views.py#L28

Some temporary code from development was accidentally deployed so users are given admin privileges when they are registered. This is a huge flaw since any user can now access the admin panel simply typing http://127.0.0.1:8000/admin/ into their browser. The correct way to register a new user is commented in the code: https://github.com/macabre-cs/csb-project-broken-website/blob/f9069e556806e82306979e08915829cb04f3b7e8/users/views.py#L35

## FLAW 3 Server-side request forgery:
https://github.com/macabre-cs/csb-project-broken-website/blob/f9069e556806e82306979e08915829cb04f3b7e8/users/views.py#L50
https://github.com/macabre-cs/csb-project-broken-website/blob/f9069e556806e82306979e08915829cb04f3b7e8/users/views.py#L52

This web application has a feature that makes a HTTP request to an URL provided by the user. Sometimes an application that combines data from multiple sources (like a dashboard or an RSS reader) might have a feature like this. An SSRF flaw occurs when the application is making a request to an URL without validating it first. This can lead to leaking sensitive data or might allow the attacker to execute commands. This could also be used to do a port scan through the vulnerable server. One way to make the implemented feature safer would be to use an allow list or allow only specific symbols. In the code it is fixed by making a list of allowed websites: https://github.com/macabre-cs/csb-project-broken-website/blob/f9069e556806e82306979e08915829cb04f3b7e8/users/views.py#L60

If you would like to try this feature out simply type http://127.0.0.1:8000/userurl/ into your browser. You could input an url and the server will make a request to the url and display the data. You do not have to even log in to use this which is also a security flaw. To fix this simply remove the comment from the ```@login_required``` decorator.

## FLAW 4 Identification and authentication failure:
https://github.com/macabre-cs/csb-project-broken-website/blob/f9069e556806e82306979e08915829cb04f3b7e8/broken_website/settings.py#L100

Users are able to register with weak and common passwords. Accounts with weak passwords are known to be weak to brute force attacks. This can lead to accounts being compromised because once the attacker gets the password they will have control of the account. Compromised accounts lead to compromised data. Once the attacker has control of the account they can access information stored on the account. However in this web application this does not have many consequences  since there is not much functionality. Though it would be quite sad if someone else logged on my personal account just for the sake of it. If this was a bank application for example the attacker would get unauthorized access to the victims financial account. They could for example transfer money to someone else without permission (if there isn’t any other authentication method).

Fortunately Django enforces strong passwords to make user accounts less prone to attacks. To fix the flaw simply remove the comments from the password validators. If you were to use a framework without built-in password strength checks you might have to program them yourself or use a library.

## FLAW 5 Security misconfiguration:
https://github.com/macabre-cs/csb-project-broken-website/blob/f9069e556806e82306979e08915829cb04f3b7e8/broken_website/settings.py#L25

This web app has quite many security misconfigurations if you look for them. Here we are intentionally exposing and making our project's secret key very weak. It is weak because it is simple and in plain text and stored in the application source code (therefore also available in git). Django's premade secret key that is commented in the code is more secure but still not secure enough for a ‘’real’’ application.

If an attacker is able to obtain our secret key they are able to do various malicious things with it. In this Django app secret key is used as a cryptographic signature. In summary the key is most commonly used to sign session cookies. With the key you (or the attacker) is able to modify the cookies which are sent by the application. In Django cryptographic signing is for example used in signing serialized data (for example JSON documents) and in unique tokens for a user session.

To fix this security misconfiguration we should not store our secret key directly in our code. Instead it could be stored in an environment variable. An example of how to implement this is commented in the code: https://github.com/macabre-cs/csb-project-broken-website/blob/f9069e556806e82306979e08915829cb04f3b7e8/broken_website/settings.py#L30
We also need to generate a new secret key for example with:
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
You must store the output of this command securely. In the future when running the application you must pass the secret key for example with:
```bash
SECRET_KEY=<REAL SECRET> python3 manage.py runserver
```
