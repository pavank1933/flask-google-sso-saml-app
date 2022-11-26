# flask-google-admin-sso-saml-app
This project walkthrough how to integrate Google SSO saml(Google Workspace) to flask app to have a user seamless login

## What is Google SSO?
Once you configure your users' enterprise cloud applications(Eg: Flask App) to use SAML 2.0, they can use their Google Workspace credentials to sign in to enterprise cloud applications from a single login.

## What is SAML?
SAML (Security Assertion Markup Language) is an XML-based standard for web browser single sign-on (SSO) that eliminates application-specific passwords. SAML uses single-use, expiring, digital “tokens” to exchange authentication and authorization data between an identity provider and cloud application service provider that have an established trust relationship.

## What is ACS?
The ACS URL is an endpoint on the service provider where the identity provider will redirect to with its authentication response. This endpoint should be an HTTPS endpoint because it will be used to transfer Personally Identifiable Information (PII).
	-> Here service provider(SP) is Python Flask App

SAML Python toolkit(pysaml2 library in flask) lets you turn your Python application into a SP (Service Provider) that can be connected to an IdP (Identity Provider)

## Pre-requisites for Google sso setup
-> Create a cheap domain in Amazon route53 if you have any AWS account, I see that .click domain costs 3$ per year, create one from it and use it while setting up google admin setup with just few users in google admin free trial account which is valid for 14 days for our testing. Using this domain, create google admin account with 2-3 years if required(which creates gmail accounts for users).
	-> Once done with all testing, clean all the resources
	-> Once you create a registered domain name in route53 using .click domain-> it auto creates hosted zone records stuff -> Take the MX records and paste the same during Google admin setup at MX records section.

## How to setup SSO in Google(Workspace) Admin for SAML Flask App
-> Login admin.google.com -> 
-> Go to Apps -> Web and Mobile apps -> Add app -> Add Custom Saml App -> Give App name and Description -> Click Next -> Download IDP metadata
-> Add ACS Url (Eg: https://192.168.1.5:8080) 
-> Add Entity ID (Eg: https://192.168.1.5:8080) 
-> After filling the above details, Leave default or provide values for other required params -> Click Continue 
-> Provide Attributes map if required 
-> Click Finish

## Post SSO setup
-> If required the site to be visible, Update Off to On under "User Access"

-> Configure downloaded IDP(Identity Provider) metadata for saml app config
	-> Copy downloaded "googleidpmetadata.xml" from google sso admin page during sso setup, paste it under flask app metadata directory
->
If required to to test from google admin page, click "Test saml App" to test sso login
(OR)
Start the app in terminal and open the host url from browser(https://192.168.1.5:8080)

-> Note:
 Next you can see sso saml authentication passed and did the call back to ACS URL. This happens if you had already logged in to the google admin page with correct credentials.

->
If we are not already authenticated user with google admin account in the current brower page, then it auto redirects us to "https://accounts.google.com/AccountChooser" page to select correct goole account of actual user exists in, if it succeeds, it redirects us to ACS call back url.

https://accounts.google.com/AccountChooser/signinchooser?continue=https%3A%2F%2Faccounts.google.com%2Fo%2Fsaml2%2Fidp%3Ffrom_login%3D1%26zt%3DChRNc1dDdmNUSklOcnM4V3gtOGxMahIfRTJ5bHp3RDFneHNjOEhuU1JuY2dubXF1dWFzbFN4Zw%25E2%2588%2599AD98QVYAAAAAY4Lx8ehkmWQ3Fe5mcX_UiNOAhwqSWRZF%26as%3DsZ9qlV4qM0qFD1PZS0_IRjitxt9ufzWBfDmwSSdcvKs&ltmpl=popup&btmpl=authsub&scc=1&oauth=1&flowName=GlifWebSignIn&flowEntry=AccountChooser

-> Once you had successfully authenticated to the correct Gmail account where the flask app config is configured with, it auto redirects you to ACS(Assertion Consumer Service) call back URL

## SSL setup(Self signed, not recommended for PROD)
To test this sso stuff, you need ACS url to be https, for this just change app.run to "app.run(host='0.0.0.0', port=port, ssl_context='adhoc')" which gets you the url with https just for testing purposes.

## Troubleshoot
If [xmlsec1] issue:
https://github.com/IdentityPython/pysaml2/issues/474

for more errors info from Google :
https://support.google.com/a/answer/6301076?hl=en#:~:text=To%20resolve%20the%20403%20app_not_configured_for_user,This%20value%20is%20case%2Dsensitive.

If the issue is (403 app_not_configured_for_user)
To resolve the 403 app_not_configured_for_user error:
Verify that the value in the saml:Issuer tag in the SAMLRequest matches the Entity ID value configured in the SAML Service Provider Details section in the Admin console. This value is case-sensitive.
	-> Make sure 

If the issue is(405 method not allowed)
	-> Try to update methods ->  @app.route("/swamid", methods=['GET', 'POST']) with get/post or both and test

Note: Make sure your google admin sso service provider config(Entity ID) and entity id in the get_saml_client method idp metadata Entity ID should be sameI("entityid": "https://192.168.1.5:8080")

## Flask App Install Steps
-> pip install -r requirements.txt
-> Start the server from terminal (python3 web.py)