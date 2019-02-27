# Certbot plugin for authentication using Gandi LiveDNS

This is a plugin for [Certbot](https://certbot.eff.org/) that uses the Gandi
LiveDNS API to allow [Gandi](https://www.gandi.net/)
customers to prove control of a domain name.

1. Obtain a Gandi API token (see [Gandi LiveDNS API](https://doc.livedns.gandi.net/#step-1-get-your-api-key))

2. Install the plugin:

   ```shell
   pip install 'git+https://derdritte.net/gitea/markus/certbot_plugin_gandi.git'
   ```

3. Create a `gandi.ini` config file with the following contents:

   ```ini
   certbot_plugin_gandi:dns_api_key=APIKEY
   ```

   Replace `APIKEY` with your Gandi API key and ensure permissions are set
   to disallow access to other users.

4. Run `certbot` and direct it to use the plugin for authentication and to use
   the config file created in (3):

   ```shell
   certbot certonly -a certbot-plugin-gandi:dns --certbot-plugin-gandi:dns-credentials gandi.ini -d domain.com
   ```

   You generally want to use an absolute path to specify gandi.ini.

For more additional options, e.g. to specify an installation plugin and more, refer to the certbot [documentation](https://certbot.eff.org/docs/).  
It is especially recommended you use the `--cert-name` option to specify a name for your new certificate, because the certbot will create a config you can use for renewals later.
