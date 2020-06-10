from berserker_resolver import Resolver
import logging
import threading

NAMESERVERS=['8.8.8.8','8.8.4.4','9.9.9.9']

def resolve_domain(domain, app_log, error_log, record='A', retry=10, timeout=10):
    ''' Query using resolver class and return a dictionary with its results '''
    results = {}
    try:
        resolver = Resolver(
            nameservers=NAMESERVERS,
            tries=retry,
            timeout=timeout,
            qname=record,
            verbose=True
        )
        results = resolver.resolve([domain])
    except Exception as error:
        error_log.error(f'Failed to query domain: {domain} with error: {error}')
    finally:
        if results:
            app_log.info(results['success'])
            error_log.error(results['error'])
        else:
            error_log('Failed to get a response for the resolver')

def setup_log(name, filename, level=logging.DEBUG):
    ''' Create a log file for the application '''
    handler = logging.FileHandler(filename)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger

if __name__ == "__main__":
    error_log = setup_log('error_log', 'resolver.err')
    resolver_log = setup_log('resolver_log', 'resolver.log')

    domain = input('Which domain do I have to resolve? ')
    times = input('How many times do I have to resolve the domain? ')
    try:
        times = int(times)
    except ValueError:
        times = 1
        resolver_log.error('Times to resolve was not defined as integer, using default value of 1')
    for i in range(times):
        thread = threading.Thread(target=resolve_domain, args=(domain, resolver_log, error_log, ))
        thread.start()