include_recipe 'collectd'
include_recipe 'collectd_plugins'

cookbook_file 'eagle.py' do
  path File.join(node['collectd-plugins']['python']['module_path'], 'eagle.py')
  notifies :restart, "collectd_service[#{node['collectd']['service_name']}]", :delayed
end

template File.join(node['collectd']['service']['config_directory'], 'eagle.conf') do
  notifies :restart, "collectd_service[#{node['collectd']['service_name']}]", :delayed
end
