
default['collectd-plugins']['python']['module_path'] = File.join(
  node['collectd']['service']['config_directory'], 'python')

default['collectd-plugins']['eagle']['Host'] = '172.17.2.105'
default['collectd-plugins']['eagle']['Port'] = 5002
default['collectd-plugins']['eagle']['Verbose'] = true

default['collectd-plugins']['write_graphite']['Host'] = '172.17.2.80'
default['collectd-plugins']['write_graphite']['Protocol'] = 'TCP'
default['collectd-plugins']['write_graphite']['Port'] = 2003
default['collectd-plugins']['write_graphite']['LogSendErrors'] = true
