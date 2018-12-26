from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import os
import re


bindPath=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/named.conf'
# pattern(s)
rePattern = '^(([^ ]*\\.)[ ]*([^ ]*)[ ]*([^ ]*)[ ]*([^ ]*)[ ]*([^\\n ]*)(?:[ ]*\\(([^\\)]*)\\))*[^\\n]*|^[\\;][^\\n]*|^([\\$][^ \\n]*) ([^\\n]*))'

rePatternCompiled = re.compile(rePattern, re.MULTILINE)
rePatternOptions = '^([^;]*)([^\\n]*)'
rePatternOptionsCompiled = re.compile(rePatternOptions, re.MULTILINE)

# Create your views here.
@login_required
def index(req):
    bindFile = open(bindPath, 'r')
    bindContent = bindFile.read()
    bindOptions = {
        "bindDomainEntries": [],
        "globalOptions": [],
        "path": bindPath
    }
    for match in rePatternCompiled.finditer(bindContent):
        full_line, para1, para2, para3, para4, para5, options, glob_option, glob_option_val = match.groups()
        entryVal = {
        }
        if glob_option:
            bindOptions['globalOptions'].append({glob_option: glob_option_val})
            entryVal['type'] = 'global options'
        elif not para1:
            entryVal['type'] = 'comment'
        elif para3 == 'SOA':
            entryVal['type'] = 'start of authority'
            entryVal['subdomain'] = para1
            entryVal['entrydir'] = para2
            entryVal['entrytype'] = para3
            entryVal['target'] = para4
            entryVal['target2'] = para5
            entryVal['parameters_raw'] = options
            entryVal['parameters_list'] = []
            for matchOptions in rePatternOptionsCompiled.finditer(options):
                optionVal, optionComment = matchOptions.groups()
                entryVal['parameters_list'].append({'value': optionVal, 'comment': optionComment})
        else:
            if para1.startswith(";"):
                entryVal['type'] = 'disabled-entry'
            else:
                entryVal['type'] = 'entry'
            entryVal['subdomain'] = para1
            entryVal['ttl'] = para2
            entryVal['entrydir'] = para3
            entryVal['entrytype'] = para4
            entryVal['target'] = para5

        entryVal['full_line'] = full_line

        bindOptions['bindDomainEntries'].append(entryVal)
    return render(req,'dns/dnsView.html', {"bindOptions": bindOptions})
