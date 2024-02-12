import sys

from .core.Config import Config
from .core.Logger import Logger
from .core.PublicIP import PublicIP
from .core.GodaddyDomainsApi import GodaddyDomainsApi




def needs_update(dns_records, current_ip):

    if dns_records is None:
        Logger.log(__name__, 'dns records do not exist', type='warning')
        return True

    record_ip = dns_records[0]['data']

    if record_ip == current_ip:
        Logger.log(__name__, 'dns record ip <{record_ip}> is up to date'.format(record_ip=record_ip))
        return False
    
    Logger.log(__name__, 'dns_record ip <{record_ip}> is outdated'.format(record_ip=record_ip), type='warning')
    return True



def main():

    dns_record = Config.get('dns_record')

    Logger.log(__name__, 'updating dns record < | {domain} | {type} | {name} |>'.format(domain=dns_record['domain'],
                                                                                   type=dns_record['type'],
                                                                                   name=dns_record['name']))

    current_ip = PublicIP.get()

    if current_ip == '127.0.0.1':
        Logger.log(__name__, 'could not get public ip, exiting', type='error')
        sys.exit(1)

    Logger.log(__name__, 'public ip is <{ip}>'.format(ip=current_ip))

    try:

        dns_records = GodaddyDomainsApi.retrieve_dns_records(q_domain='panosrcng.com', q_type='A', q_name='@')

        if not needs_update(dns_records, current_ip):
            sys.exit(0)
    
        updated_dns_records = [{
            'data': current_ip,
            'ttl': 600
        }]

        GodaddyDomainsApi.replace_dns_records(q_domain='panosrcng.com', q_type='A', q_name='@', dns_records=updated_dns_records)

        Logger.log(__name__, 'dns record ip updated to <{current_ip}>'.format(current_ip=current_ip))
        sys.exit(0)

    except Exception as ex:
        Logger.log(__name__, str(ex), type='error')
        Logger.log(__name__, 'could not update dns record ip to <{current_ip}>'.format(current_ip=current_ip), type='error')
        sys.exit(1)





if __name__ == '__main__':
    main()