import requests
import json

from .Config import Config
from .Logger import Logger



class GodaddyDomainsApiException(Exception):
    def __init__(self, message, *args):
        self.message = message
        super(GodaddyDomainsApiException, self).__init__(self.message, *args) 



class GodaddyDomainsApi:

    # these are public for test purposes
    instance = None


    # constructor is not intended to be called from outside the module, only fo test purposes
    def __init__(self):

        if GodaddyDomainsApi.instance is not None:
            return

        GodaddyDomainsApi.instance = self
        self.__setup()


    @staticmethod
    def __get_instance():

        if GodaddyDomainsApi.instance is None:
            GodaddyDomainsApi()

        return GodaddyDomainsApi.instance


    def __setup(self):
        self.__config = Config.get('godaddy_domains_api')


    @staticmethod
    def retrieve_dns_records(q_domain, q_type, q_name):
        return GodaddyDomainsApi.__get_instance().__retrieve_dns_records(q_domain, q_type, q_name)


    @staticmethod
    def replace_dns_records(q_domain, q_type, q_name, dns_records):
        return GodaddyDomainsApi.__get_instance().__replace_dns_records(q_domain, q_type, q_name, dns_records)



    def __retrieve_dns_records(self, q_domain, q_type, q_name):

        url = '{base_url}/{version}/domains/{domain}/records/{type}/{name}'.format(base_url=self.__config['base_url'],
                                                                                   version=self.__config['version'],
                                                                                   domain=q_domain,
                                                                                   type=q_type,
                                                                                   name=q_name)

        response = self.__request_get(url)

        if response.status_code == 200:
            return response.json()

        if response.status_code == 404:
            Logger.log(__name__, 'not found <{reason}>'.format(reason=response.text.strip()), type='debug')
            return None
                
        Logger.log(__name__, 'request failed with status code <{status_code}> and <{reason}>'.format(status_code=response.status_code,
                                                                                                     reason=response.text.strip()), type='debug')

        raise GodaddyDomainsApiException('could not retrieve dns records')


    def __replace_dns_records(self, q_domain, q_type, q_name, dns_records):

        url = '{base_url}/{version}/domains/{domain}/records/{type}/{name}'.format(base_url=self.__config['base_url'],
                                                                                    version=self.__config['version'],
                                                                                    domain=q_domain,
                                                                                    type=q_type,
                                                                                    name=q_name)

        response = self.__request_put(url, dns_records)

        if response.status_code != 200:
            raise GodaddyDomainsApiException('request failed with status code <{status_code}> and <{reason}>'.format(status_code=response.status_code,
                                                                                                                     reason=response.text.strip()))

        return True


    def __request_get(self, url):

        Logger.log(__name__, 'requesting GET url <{url}>'.format(url=url), type='debug')

        headers = {
            'Authorization': 'sso-key {key}:{secret}'.format(key=self.__config['key'], secret=self.__config['secret'])
        }

        try:
            return requests.get(url, headers=headers, timeout=self.__config['request_timeout'])
        except Exception as ex:
            Logger.log(__name__, str(ex), type='debug')
            raise GodaddyDomainsApiException('could not request GET <{url}>'.format(url=url))


    def __request_put(self, url, dns_records):

        Logger.log(__name__, 'requesting PUT url: <{url}>'.format(url=url), type='debug')

        headers = {
            'Authorization': 'sso-key {key}:{secret}'.format(key=self.__config['key'], secret=self.__config['secret']),
            'content-type': 'application/json'
        }

        try:
            return requests.put(url, headers=headers, timeout=self.__config['request_timeout'], data=json.dumps(dns_records))
        except Exception as ex:
            Logger.log(__name__, str(ex), type='debug')
            raise GodaddyDomainsApiException('could not request PUT <{url}>'.format(url=url))

