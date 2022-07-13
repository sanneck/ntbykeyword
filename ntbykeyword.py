#!/usr/bin/env python

import requests
import os
import getopt
import sys
import argparse


def show_options():
	print("""

		this is the help

		""")

def ntbkeywork():
	
	# Parse command line
	parser = argparse.ArgumentParser()
	parser.add_argument("-d", "--domain",
                        help="Input a domain to scan with Nuclei",
                        action="store")
	parser.add_argument("-l", "--list",
                        help="List of domains to scan with Nuclei",
                        action="store")
	parser.add_argument("-q", "--query",
                        help="Keyword to look for related nuclei templates",
                        required=True, action="store")
	parser.add_argument("-ea", "--extra-arguments",
						dest="extraArguments",
                        help="Add Nuclei extra arguments (i.e. -ea ' -vv')",
                        action='store')
	args = parser.parse_args()

	url =""
	host_list =""
	query =""
	extra_arguments =""

	if args.domain:
		url = args.domain
	if args.list:
		host_list = args.list
	if args.query:
		query = args.query
	if args.extraArguments:
		extra_arguments = args.extraArguments

	try:
		res = requests.get(f'https://api.github.com/search/code?q={query}+in:file+repo:projectdiscovery/nuclei-templates')
		res.raise_for_status()
		json_results = res.json()

	except requests.exceptions.HTTPError as err:
		sys.exit(err)

	home_dir = os.getenv('HOME', default=None)

	nuclei_templates_dir = f'{home_dir}/nuclei-templates/'

	if not os.path.isdir(nuclei_templates_dir):
		sys.exit('nuclei templates directory not found.')

	nuclei_command = 'nuclei'

	if extra_arguments:
		nuclei_command += f' {extra_arguments}'

	if host_list:
		nuclei_command += f' -l {host_list}'
	elif url:
		nuclei_command += f' -u {url}'

	if json_results:
		for result in json_results['items']:
			path = result['path']
			extenstion = path.split('.')[1:][0]
			first_dir = path.split('/')[:1][0]
			if extenstion == 'yaml':
				if first_dir != 'workflows':
					nuclei_command += f' \\\n -t {nuclei_templates_dir}{path}'
				else:
					nuclei_command += f' \\\n -w {nuclei_templates_dir}{path}'


	print(f'\nNuclei command: \n{nuclei_command}')
	if nuclei_command and (host_list or url):
		os.system(nuclei_command)


if __name__ == '__main__':

	ntbkeywork()
