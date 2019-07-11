require 'ipaddr'

Puppet::Functions.create_function(:'lab_network_ironic_phobos::find_gateway') do

  dispatch :cidr_param do
    param 'String', :cidr
  end

  def cidr_param(cidr)
    iprange = IPAddr.new(cidr).to_range.to_a[1].to_s
  end

end
