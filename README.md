## About Ntbykeyword

Ntbykeyword is a python script written to avoid looking for specific [nuclei templates](https://github.com/projectdiscovery/nuclei-templates) when using [Nuclei](https://github.com/projectdiscovery/nuclei), you can do something similar with the '-tags' option. Anyway, I didn't know about this option before doing this.

The script will do a search using the github api in the nuclei templates repository, then it concatenates the templates paths to your HOME path to append each template local path to the nuclei command that will run.

## Screenshots

![Ntbykeyword](https://i.imgur.com/xedkrNQ.png)

### Examples

* Look for xxs related templates in one specific domain:

`python ntbykeyword.py -d https://example.com -q xss`

* Look for sqli related templates in list of domains:

`python ntbykeyword.py -l phpdomains.txt -q sqli`

* Add extra arguments to nuclei command:

`python ntbykeyword.py -l phpdomains.txt -q sqli -ea ' -vv'`

### TODO

* Only retrieves first 50 items from github api search. It should return all the items.