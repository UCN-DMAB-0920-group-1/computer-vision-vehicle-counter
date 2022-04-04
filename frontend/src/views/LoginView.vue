<template>
    <div>
  
     
    </div>
</template>

<script setup>
    oauthSignIn();
    /*
     * Create form to request access token from Google's OAuth 2.0 server.
     */
    function oauthSignIn() {
        // Google's OAuth 2.0 endpoint for requesting an access token
        var oauth2Endpoint = 'https://accounts.google.com/o/oauth2/v2/auth';

        // Create <form> element to submit parameters to OAuth 2.0 endpoint.
        var form = document.createElement('form');
        form.setAttribute('method', 'GET'); // Send as a GET request.
        form.setAttribute('action', oauth2Endpoint);

        // Parameters to pass to OAuth 2.0 endpoint.
        var params = {
            'client_id': '512124053214-vpk9p42i9ls413asejsa9bg7j1b4nq61.apps.googleusercontent.com',
            'redirect_uri': 'http://localhost:8080',
            'response_type': 'code',
            'scope': 'profile openid email',
            'nonce': '0394852-3190485-2490358',
        };

        // Add form parameters as hidden input values.
        for (var p in params) {
            var input = document.createElement('input');
            input.setAttribute('type', 'hidden');
            input.setAttribute('name', p);
            input.setAttribute('value', params[p]);
            form.appendChild(input);
        }

        // Add form to page and submit it to open the OAuth 2.0 endpoint.
        document.body.appendChild(form);
        form.submit();
    }
</script>

<style lang="scss" scoped>

</style>