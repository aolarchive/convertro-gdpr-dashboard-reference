**Please Note**: This repo contains known security vulnerabilities and is no longer maintained. Use at your own risk!

# convertro-gdpr-dashboard-reference

This project is a reference implementation for a privacy dashboard that uses Convertro's GDPR APIs.

The code is very minimal and simplistic and is written with [Flask](http://flask.pocoo.org/).

Please see the full GDPR API documentation at [Convertro Knowledge Base](https://convertro.zendesk.com/)
-> GDPR Center -> API Documentation.

## Set up
Clone this repo, rename the `.env.example` file to `.env` and set your private keys.

## Run with Docker
Run `docker-compose up` and open [http://localhost:5000/](http://localhost:5000/) to view it in the browser.

> Note: this code is not intended for production. It will run in debug mode, and the server will reload itself on code changes.

## The Flask app 

- The index page contains a link to the Cookie Reflection API to retrieve the cookies.
- The `/cookie-handler` route is passed as the `redirect_url` parameter to the Cookie Reflection API. 
The function `handler` is bound to this URL and will handle the redirect.
- `handler` redirects to an error page in case the Cookie Reflection API encountered an error (the returned query param
`status_code` is not 200). You may handle this case differently.
- Otherwise, it makes a server-side request to the `/v1/requests` API, 
and redirects to a success or an error page according to the http status code of the response. 
Here too your logic may vary.
- This example doesn't utilize other existing APIs. Please see the full API documentation for more details
about those endpoints. 
- In addition, you may want to provide a notification mechanism to notify your users when their data is ready,
such as email, sms or push notification.

## Contributing
See [Contributing.md](Contributing.md) for more information.

## License
convertro-gdpr-dashboard-reference is [MIT licensed](LICENSE).



