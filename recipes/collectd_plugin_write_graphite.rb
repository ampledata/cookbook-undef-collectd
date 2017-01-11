include_recipe 'collectd'
include_recipe 'collectd_plugins'

template File.join(node['collectd']['service']['config_directory'], 'write_graphite.conf') do
  notifies :restart, "collectd_service[#{node['collectd']['service_name']}]", :delayed
end
