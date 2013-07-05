#coding:utf-8

# **************************************
# Author: shuangluo
# Created: 13-7-5 上午10:20
# **************************************

import re


pattern1 = r'^Publish/(\w+)/([\w\.]+)/(\w+)'
pattern2 = r'^/cygdrive/e/Publish/(\w+)/([\w\.]+)/(\w+)'
pattern3 = r'^(\w+)\\([\w\.]+)\\(\w+)'
pattern4 = r'^Publish\\(\w+)\\([\w\.]+)\\(\w+)'
pattern5 = r'^E:\\Publish\\(\w+)\\([\w\.]+)\\(\w+)'
pattern6 = r'^(\w+)\\\\([\w\.]+)\\\\(\w+)'
pattern7 = r'^E:\\\\Publish\\\\(\w+)\\\\([\w\.]+)\\\\(\w+)'


def test_re():
    m1 = re.match(pattern1, 'Publish/website/Icson.CS/CS')
    m2 = re.match(pattern2, '/cygdrive/e/Publish/website/Icson.CS/CS')
    m3 = re.match(pattern3, 'website\Icson.CS\CS')
    m4 = re.match(pattern4, 'Publish\website\Icson.CS\CS')
    m5 = re.match(pattern5, 'E:\Publish\Website\Icson.CS\CS')
    m6 = re.match(pattern6, r'website\\Icson.CS\\CS')
    m7 = re.match(pattern7, r'E:\\Publish\\Website\\Icson.CS\\CS')
    print m1.groups()[0]
    print m2.groups()[0]
    print m3.groups()[0]
    print m4.groups()[0]
    print m5.groups()[0]
    print m6.groups()[0]
    print m7.groups()[0]


import pysvn
import os


class LocalSvnManipulate(object):
    def __init__(self, path):
        self._path = path
        self._repo = pysvn.Client(self._path.rstrip(os.path.sep))
        self._repo.set_default_username = 'publishtest'
        self._repo.set_default_password = 'publishtest'

    def latest_rev_by(self, timestamp):
        rev = pysvn.Revision(pysvn.opt_revision_kind.date, timestamp)
        logs = self._repo.log(self._path, revision_start=rev)
        latest = -1
        if logs:
            latest = logs[0]['revision'].number
        return latest

    def update_to_revnum(self, revnum):
        rev = self._repo.update(
            path=self._path,
            revision=pysvn.Revision(pysvn.opt_revision_kind.number, revnum)
        )
        return rev[0].number

    def diff_by_time(self, timestamp1, timestamp2):
        rev1 = pysvn.Revision(pysvn.opt_revision_kind.date, timestamp1)
        rev2 = pysvn.Revision(pysvn.opt_revision_kind.date, timestamp2)
        return self._do_diff(rev1, rev2)

    def diff_by_revnum(self, revnum1, revnum2):
        rev1 = pysvn.Revision(pysvn.opt_revision_kind.number, revnum1)
        rev2 = pysvn.Revision(pysvn.opt_revision_kind.number, revnum2)
        return self._do_diff(rev1, rev2)

    def _do_diff(self, rev1, rev2):
        diffs = self._repo.diff_summarize(
            url_or_path1=self._path,
            revision1=rev1,
            revision2=rev2,
        )
        diff_files = []
        for diff in diffs:
            path = diff.data['path']
            text = diff(
                tmp_path="/tmp",
                url_or_path=path,
                revision1=rev1,
                revision2=rev2,
            )
            diff_files.append((path, text))
        return diff_files


def checkout_or_update_to_revnum(remote, local, revnum):
    cl = pysvn.Client()
    try:
        cl.status(local)
    except pysvn.ClientError:
        cl.set_default_username = 'publishtest'
        cl.set_default_password = 'publishtest'
        rev = cl.checkout(
            url=remote,
            path=local,
            revision=pysvn.Revision(pysvn.opt_revision_kind.number, revnum)
        )
        return rev[0].number
    else:
        lsm = LocalSvnManipulate(local)
        return lsm.update_to_revnum(revnum)