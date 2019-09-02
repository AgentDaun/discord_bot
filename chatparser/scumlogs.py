# -*- coding: utf-8 -*-
import traceback
import json
from datetime import datetime

from aiocfscrape import CloudflareScraper

from bs4 import BeautifulSoup
from configparser import ConfigParser


def log(text):
    print('[%s] %s' % (datetime.strftime(datetime.now(), '%H:%M:%S'), text))


def load_configini():
    config = ConfigParser()
    with open('scumlogs.ini', 'r') as f:
        config.read_file(f)
    global configini
    configini = dict(config['GPORTAL'])


def save_configini():
    parser = ConfigParser()
    parser.add_section('GPORTAL')
    for key in configini.keys():
        parser.set('GPORTAL', key, configini[key])
    with open('scumlogs.ini', 'w') as f:
        parser.write(f)


async def read_logs():
    result_chat_lines = []
    result_kill_lines = []
    values = ('user', 'password', 'serverid', 'loc', 'folder', 'admin_file',
              'admin_line', 'chat_file', 'chat_line', 'kill_file',
              'kill_line', 'login_file',
              'login_line', 'violations_file', 'violations_line')

    try:
        load_configini()
    except Exception:
        global configini
        configini = {}
    for value in values:
        if value not in configini:
            configini[value] = ''
    if configini['folder'] != '':
        if configini['folder'][-1:] != '/' and configini['folder'][-1:] != '\\':
            configini['folder'] = configini['folder'] + '/'
    save_configini()

    URL_LOGIN = 'https://id2.g-portal.com/login?redirect=https://www.g-portal.{}/en/gportalid/login?'.format(configini['loc'])
    URL_LOGS = 'https://www.g-portal.{}/en/scum/logs/{}'.format(configini['loc'], configini['serverid'])

    async with CloudflareScraper() as session:
        try:
            log('connecting g-portal...')
            payload = {'_method': 'POST',
                       'login': configini['user'],
                       'password': configini['password'],
                       'rememberme': '1'}

            async with session.post(URL_LOGIN, data=payload) as raw_response:
                response = await raw_response.text()
            async with session.get(URL_LOGS) as raw_response:
                response = await raw_response.text()

            html = BeautifulSoup(response, 'html.parser')
            select = html.find('div', {'class': 'wrapper logs'})
            loglist = select['data-logs']
            logs = json.loads(loglist)

            for i in range(len(logs)):
                getid = logs["file_" + str(i + 1)]
                id = (getid[int(getid.find('Logs')) + 5:])
                type = id.split('_')[0]

                if type in ['chat', 'kill']:
                    if configini[type + '_file'] != '':
                        if id < configini[type + '_file']:
                            continue

                    payload = {'_method': 'POST',
                               'load': 'true',
                               'ExtConfig[config]': getid}
                    async with session.post(URL_LOGS,
                                            data=payload) as raw_response:
                        response = await raw_response.text()
                    content = json.loads(response)
                    lines = content["ExtConfig"]["content"].splitlines()

                    found = False
                    writing = False
                    for line in lines:
                        #  Replace all "%" symbols to ";" coz
                        # .ini files can't save "%" symbol.
                        if "%" in line:
                            ready_line = ""
                            # continue
                            for i in line:
                                if i == "%":
                                    ready_line += ";"
                                else:
                                    ready_line += i
                            index = lines.index(line)
                            lines[index] = ready_line
                        if id == configini[type + '_file'] and not found:
                            if line == configini[type + '_line']:
                                found = True
                                continue
                            # Replace all ";" symbold to ";"
                            elif line.find("%") > -1:
                                ready_line = ""
                                for i in line:
                                    if i == "%":
                                        ready_line += ";"
                                    else:
                                        ready_line += i
                                if ready_line == configini[type + "_line"]:
                                    found = True
                                    continue
                        else:
                            if type == "chat":
                                result_chat_lines.append(line)
                            else:
                                result_kill_lines.append(line)
                            writing = True
                    if writing:
                        if found:
                            log('updating {}'.format(id))
                        else:
                            log('creating {}'.format(id))
                    # file.close()
                    configini[type + '_file'] = id
                    configini[type + '_line'] = lines[-1]
            save_configini()
            if not result_chat_lines and not result_kill_lines:
                return [], False
            return [result_chat_lines, result_kill_lines], True

        except Exception:
            print(traceback.format.exc())
            return [], False
        await session.close()
