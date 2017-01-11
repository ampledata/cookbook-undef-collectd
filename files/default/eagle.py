#!/home/gba/.pyenv/shims/python


import socket
import time
import xml.etree.ElementTree

import collectd


PLUGIN_NAME = 'eagle'
VERBOSE_LOGGING = 1
EAGLE_HOST = ''
EAGLE_PORT = 0


def configure_callback(conf):
    log_verbose('configure_callback()')

    global EAGLE_HOST, EAGLE_PORT, VERBOSE_LOGGING

    for node in conf.children:
        if 'Host' in node.key:
            EAGLE_HOST = node.values[0]
        elif 'Port' in node.key:
            EAGLE_PORT = int(node.values[0])
        elif 'Verbose' in node.key:
            VERBOSE_LOGGING = bool(node.values[0])
        elif 'PresenceHash' in node.key:
            VERBOSE_LOGGING = node.values[0]
        else:
            collectd.warning(
                "%s plugin [warning]: Unknown config key: %s" %
                (PLUGIN_NAME, node.key))


def read_callback():
    log_verbose('read_callback()')

    sendstr = (
        '<LocalCommand>\n <Name>get_instantaneous_demand</Name>\n '
        '<MacId>0xd8d5b90000000fc4</MacId>\n</LocalCommand>\n'
    )
    x_data = ''

    eagle_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    eagle_sock.connect((EAGLE_HOST, EAGLE_PORT))
    time.sleep(1)
    eagle_sock.send(sendstr)
    time.sleep(1)

    while 1:
        buf = eagle_sock.recv(1000)
        if not buf:
            break
        x_data += buf

    time.sleep(1)
    eagle_sock.close()

    root = xml.etree.ElementTree.fromstring(x_data)

    demand = root.findall('Demand')[0].text
    multiplier = root.findall('Multiplier')[0].text
    divisor = root.findall('Divisor')[0].text

    demand_f = float(int(demand, 16))
    multiplier_f = float(int(multiplier, 16))
    divisor_f = float(int(divisor, 16))

    current_demand = demand_f * multiplier_f / divisor_f

    log_verbose("demand_f=%s" % demand_f)
    log_verbose("multiplier_f=%s" % multiplier_f)
    log_verbose("divisor_f=%s" % divisor_f)
    log_verbose("current_demand=%s" % current_demand)

    val = collectd.Values(plugin=PLUGIN_NAME)
    val.type = 'gauge'
    val.type_instance = 'demand_f'
    val.values = [demand_f]
    val.dispatch()

    val = collectd.Values(plugin=PLUGIN_NAME)
    val.type = 'gauge'
    val.type_instance = 'multiplier_f'
    val.values = [multiplier_f]
    val.dispatch()

    val = collectd.Values(plugin=PLUGIN_NAME)
    val.type = 'gauge'
    val.type_instance = 'divisor_f'
    val.values = [divisor_f]
    val.dispatch()

    val = collectd.Values(plugin=PLUGIN_NAME)
    val.type = 'gauge'
    val.type_instance = 'current_demand'
    val.values = [current_demand]
    val.dispatch()


def log_verbose(msg):
    if VERBOSE_LOGGING:
        collectd.info("%s plugin [verbose]: %s" % (PLUGIN_NAME, msg))


# register callbacks
collectd.register_config(configure_callback)
collectd.register_read(read_callback)
