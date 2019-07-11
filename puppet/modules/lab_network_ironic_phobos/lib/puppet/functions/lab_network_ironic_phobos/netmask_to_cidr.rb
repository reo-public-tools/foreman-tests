require 'ipaddr'

Puppet::Functions.create_function(:'lab_network_ironic_phobos::netmask_to_cidr') do

  dispatch :netmask_param do
    param 'String', :netmask
  end

  def netmask_param(netmask)
    IPAddr.new(netmask).to_i.to_s(2).count("1")
  end

end
