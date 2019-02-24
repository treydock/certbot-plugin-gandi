import zope.interface
import logging

from certbot import interfaces
from certbot.errors import PluginError
from certbot.plugins import dns_common

from . import gandi_api


logger = logging.getLogger(__name__)


@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for Gandi (using LiveDNS)."""

    description = ('Obtain certificates using a DNS TXT record (if you are '
                   'using Gandi for DNS).')

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None

    @classmethod
    def add_parser_arguments(cls, add):  # pylint: disable=arguments-differ
        super(Authenticator, cls).add_parser_arguments(add)
        add('credentials', help='Gandi credentials INI file.')

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        return ('This plugin configures a DNS TXT record to respond to a '
                'dns-01 challenge using the Gandi LiveDNS API.')

    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            'credentials',
            'Gandi credentials INI file',
            {
                'api-key': 'API key for Gandi account'
            }
        )

    def _perform(self, domain, validation_name, validation):
        previous_values = gandi_api.get_txt_records(
            self._get_gandi_config(), domain, validation_name)
        previous_values.append(validation)
        error = gandi_api.add_txt_record(
            self._get_gandi_config(), domain, validation_name, previous_values)
        if error is not None:
            raise PluginError(
                'An error occurred adding the DNS TXT record: {}'.format(
                    error))

    def _cleanup(self, domain, validation_name, validation):
        error = gandi_api.del_txt_record(
            self._get_gandi_config(), domain, validation_name)
        if error is not None:
            logger.warn(
                ('Unable to find or delete the DNS TXT record: {}, this '
                 'is normal if you had multiple challenges in the same '
                 'zone.').format(error))

    def _get_gandi_config(self):
        return gandi_api.get_config(api_key=self.credentials.conf('api-key'))
