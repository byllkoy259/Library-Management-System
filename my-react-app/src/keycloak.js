import Keycloak from 'keycloak-js';

const keycloak = new Keycloak({
    url: 'http://127.0.0.1:8080',
    realm: 'library-realm',
    clientId: 'react-keycloak',
});

export default keycloak;