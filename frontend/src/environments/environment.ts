
export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'thedevscott', // the auth0 domain prefix
    audience: 'localhost:5000', // the audience set for the auth0 app
    clientId: 'I67b3U2Nr1MTBBn0nGQlDOkKvG68gBi1', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application.
  }
};
