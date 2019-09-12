#!/usr/bin/env python3

from colorama import Fore
from functools import partial
from multiprocessing import Pool
import argparse
import requests
import sys



def fetch_git(output_f, domains):
    """
    This function will tell us about vulnerable domains
    :param output_f: name of the output file
    :param domains: domain name
    """
    domain = domains.strip()

    # checking if there is empty string in domain or new line at the end.
    if domain == "":
        return

    if not (domain.startswith('http://') or domain.startswith('https://')):
        domain = 'http://' + domain

    if not domain.endswith('/'):
        domain += '/.git/HEAD'
    else:
        domain += '.git/HEAD'

    try:
        # Testing if url is valid or not
        response = requests.get(domain, timeout=5)
        response_value = response.text
    except (requests.Timeout, requests.ConnectionError, requests.HTTPError) as err:
        print(Fore.RED + domain)
        return

    if 'refs/head' not in response_value:
        print(Fore.RED + domain)
        return

    print(Fore.GREEN+domain)

    # Writing final output to the file
    try:
        with open(output_f, 'a') as f:
            f.write(''.join([domain, '\n']))
    except Exception as e:
        print(Fore.RED + e)




def read_file(filename):
    """
    It will read the file and return the content.
    :param filename: name of the file
    """
    with open(filename) as f:
        return f.readlines()


def main():
    print("""
    It will look for the domains which are vulnerable to git misconfiguration.
    """)

    # Argument Parsing
    parser = argparse.ArgumentParser(usage='%(prog)s -i input_file [-o output_file]')
    parser.add_argument('-i', '--inputfile', default='input.txt', help='input file')
    parser.add_argument('-o', '--outputfile', default='output.txt', help='output file')
    parser.add_argument('-t', '--threads', default=20, help='threads')
    args = parser.parse_args()

    domain_f = args.inputfile
    output_f = args.outputfile
    try:
        max_processes = int(args.threads)
    except ValueError as err:
        sys.exit(err)

    try:
        domains = read_file(domain_f)
    except FileNotFoundError as err:
        sys.exit(err)

    fun = partial(fetch_git, output_f)
    with Pool(processes=max_processes) as pool:
        pool.map(fun, domains)
    print('Finished')


if __name__ == '__main__':
    main()
