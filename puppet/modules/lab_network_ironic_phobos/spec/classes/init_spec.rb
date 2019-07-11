require 'spec_helper'
describe 'lab_network_ironic_phobos' do
  context 'with default values for all parameters' do
    it { should contain_class('lab_network_ironic_phobos') }
  end
end
