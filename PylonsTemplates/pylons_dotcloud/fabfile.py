## Copyright (c) 2010 dotCloud Inc.
##
## Permission is hereby granted, free of charge, to any person obtaining a copy
## of this software and associated documentation files (the "Software"), to deal
## in the Software without restriction, including without limitation the rights
## to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
## copies of the Software, and to permit persons to whom the Software is
## furnished to do so, subject to the following conditions:
##
## The above copyright notice and this permission notice shall be included in
## all copies or substantial portions of the Software.
##
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
## OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
## THE SOFTWARE.

from __future__ import with_statement

import os
import contextlib

import yaml
from fabric.contrib.files import exists
from fabric.context_managers import settings
from fabric.api import local, env, run, prompt, put


class _Config(dict):

    def __getattr__(self, key): 
        value = self[key]
        if isinstance(value, dict):
            return self.__class__(value)
        return value

    def __setattr__(self, key, value): 
        self[key] = value

    def __delattr__(self, key):
        del self[key]

    def __repr__(self):     
        return '<Config ' + dict.__repr__(self) + '>'


config_file = os.environ.get('DOTCLOUD_CONFIG_FILE', './dotcloud.yml')
config = yaml.load(file(config_file))
if config is None:
    config = {}
config = _Config(config)

env.user = "dotcloud"
env.disable_known_hosts = True
env.hosts.append("{0}:{1}".format(config.host, config.port))


def hostname():
    """ Show remote hostname """
    run("hostname")


def _get_maintenance_file(revision):
    if revision is not None:
        return "revisions/%s/maintenance" % revision
    return "current/maintenance"


def maintenance_mode(revision=None):
    """ Check if maintenance mode is set """
    return exists(_get_maintenance_file(revision))


def set_maintenance(revision=None):
    """ Set maintenance mode (The server will return 503 and show /static/503.html) """
    run("touch " + _get_maintenance_file(revision))


def unset_maintenance(revision=None):
    """ Unset maintenance mode """
    run("rm -f " + _get_maintenance_file(revision))


def reset():
    """ Reset virtualenv and revisions (deletes all remote files!) """
    sure = prompt("Are you sure? [yes/no]", validate="(yes)|(no)")
    if sure == "yes":
        run("rm -rf *")
        run("mkdir revisions")
        run("virtualenv env")
    reload_wsgi()


def install_requirements():
    """ Install all python requirements specified in the config file (requirements: [...]) """
    for r in config.get('requirements', []):
        run("pip install " + r)


def deployed():
    """ Show currently deployed revision """
    return run("readlink current | cut -d/ -f2")


def _get_scm():
    scm = None
    if os.path.exists(".hg"):
        scm = "hg"
    elif os.path.exists(".git"):
        scm = "git"
    return config.get("scm", scm)


def _get_revision():
    scm = _get_scm()
    if scm == "hg" or scm == "mercurial":
        return local("hg tip --template '{node|short}'")
    elif scm == "git":
        return local("git show --format=%h master | head -1")
    else:
        import time
        return time.strftime('%Y%m%d%H%M%S')


def deploy():
    """ Deploy application """
    revision = _get_revision()
    upload(revision)
    switch_current(revision)
    reload_wsgi()


def switch_current(revision):
    """ Switch current application to specific revision """
    with settings(warn_only=True):
        run("mv -f current previous")
    run("ln -s revisions/%s current" % revision)


def rollback():
    """ Rollback to previous deployment """
    run("mv current _previous")
    run("mv previous current")
    run("mv _previous previous")
    reload_wsgi()


def _create_tar(revision):
    tar = revision + ".tar.bz2"
    scm = _get_scm()
    if scm == "hg" or scm == "mercurial":
        local("hg archive --type tbz2 --prefix './' --rev %s %s" % (revision, tar))
    elif scm == "git":
        local("git archive --format=tar %s | bzip2 > %s" % (revision, tar))
    else:
        local("tar cjf %s *" % tar)
    return tar


def upload(revision):
    """ Upload application """
    remote_dir = "revisions/" + revision
    run("mkdir -p " + remote_dir)
    tar = _create_tar(revision)
    put(tar, tar)
    run("tar xjf %s -C %s" % (tar, remote_dir))
    run("rm " + tar)
    os.unlink(tar)


def reload_wsgi():
    """ Restart uwsgi gracefully """
    run("kill -HUP `cat /var/dotcloud/uwsgi.pid`")


def restart_wsgi():
    """ Restart uwsgi """
    run("supervisorctl restart uwsgi")


def reload_supervisor():
    """ Reload supervisor config """
    run("supervisorctl reload")


def restart_supervisor():
    """ Restart supervisor """
    run("/etc/init.d/supervisor stop")
    run("/etc/init.d/supervisor start")
