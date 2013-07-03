#coding: utf-8

import re
import MySQLdb as mdb
import pycurl
import StringIO
import hashlib
import time
import random
import os
import datetime


LOG_ROOT = '/home/distribution/log/curl_log/'


class MySQL(object):
    def __init__(self, host='127.0.0.1', username='', password='', database=''):
        self.conn = mdb.connect(host, username, password, database)

    def closeLink(self):
        self.conn.close()


class Curl(object):
    def __init__(self):
        self.curl = pycurl.Curl()
        self.curl.setopt(pycurl.VERBOSE, 1)
        self.curl.setopt(pycurl.HEADER, 1)
        self.curl.setopt(pycurl.MAXREDIRS, 5)
        self.curl.setopt(pycurl.FOLLOWLOCATION, 1)
        self.wf = StringIO.StringIO()
        self.curl.setopt(pycurl.HEADERFUNCTION, self.wf.write)

    def set_host_header(self, host):
        self.curl.setopt(pycurl.HTTPHEADER, ['HOST:' + host])

    def curl_url(self, url):
        self.curl.setopt(pycurl.URL, url)
        self.curl.perform()
        http_code = self.curl.getinfo(self.curl.HTTP_CODE)
        total_time = self.curl.getinfo(self.curl.TOTAL_TIME)
        content_length = self.curl.getinfo(self.curl.CONTENT_LENGTH_DOWNLOAD)

        return {
            'http_code': http_code,
            'total_time': total_time,
            'content_length': content_length,
            'response_header': self.wf.getvalue()
        }


mysql_obj = MySQL(username='root', password='redhat', database='dist')
conn = mysql_obj.conn
cursor = conn.cursor(cursorclass=mdb.cursors.DictCursor)


def get_monitor_list():
    sql = "SELECT * FROM curl_monitor_monitoritem"
    cursor.execute(sql)
    monitor_list = cursor.fetchall()

    return monitor_list


def update_monitor_item(**args):
    sql = "UPDATE curl_monitor_monitoritem SET error_count=%s, last_status='%s' WHERE id=%s" %(args['error_count'], args['last_status'], args['id'])
    cursor.execute(sql)


def insert_monitor_log(**args):
    sql = "INSERT INTO curl_monitor_monitorlog (monitor_id, log_path, datetime) VALUES (%s, '%s', '%s')" %(args['monitor_id'], args['log_path'], datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
    cursor.execute(sql)


def counter(data_list):
    return_dict = {}
    for data in data_list:
        if data in return_dict:
            return_dict[data] += 1
        else:
            return_dict[data] = 1

    return return_dict


def main():
    curl_obj = Curl()

    monitor_list = get_monitor_list()
    for item in monitor_list:
        url = item['url']
        url_pattern = r'^(http:\/\/)?([^\/]+)$'
        url_re_object = re.compile(url_pattern)
        target_list = url_re_object.find(url)
        domain = target_list[1]

        ip_list = item['ip_list'].split(';')
        new_url_list = []
        for ip in ip_list:
            new_url_list.append(url.replace(domain, ip))

        result_to_store = {
            'error_count': item.error_count,
            'error_info': '',
            'last_status': []
        }
        this_run_error_count = 0
        for new_url in new_url_list:
            curl_obj.set_host_header(domain)
            result_dict = curl_obj.curl_url(new_url)
            result_to_store['last_status'].append(result_dict['http_code'])
            if result_dict['http_code'] != 200:
                this_run_error_count += 1
                result_to_store['error_count'] += 1
                result_to_store['error_info'] += '=' * 40 + '<br />' + result_dict['response_header']
        if this_run_error_count > 0:
            log_dir = hashlib.new('md5', url).hexdigest()[0:5]
            log_file_name = 'log_' + str(time.time()) + '_' + str(random.randint(1000, 9999)) + '.log'
            log_path = LOG_ROOT + log_dir + '/'
            if not os.path.exists(log_path):
                os.mkdir(log_path)
            log_absolute_path = log_path + log_file_name
            with open(log_absolute_path, 'w') as fh:
                fh.write(result_to_store['error_info'])
            insert_monitor_log(monitor_id=item['id'], log_path=log_absolute_path)

        code_count_dict = counter(result_to_store['last_status'])
        last_status_info = ';'.join(['%s x %s' %(str(key), str(value)) for key, value in code_count_dict.iteritems()])
        update_monitor_item(id=item['id'], error_count=result_to_store['error_count'], last_status=last_status_info)

        conn.commit()

    cursor.close()
    mysql_obj.closeLink()


if __name__ == '__main__':
    main()