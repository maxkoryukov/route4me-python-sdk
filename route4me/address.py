import xmltodict

from base import Base
from exceptions import ParamValueException


class Address(Base):
    """
    An Address is a destination in a route or optimization problem.
    Addresses can be depots, which means they are a departure points.
    Addresses can belong to only one route and one optimization problem,
    except for depots. One depot can be part of many routes if we have a
    VRP (multi-route) solution.
    """
    required = ['address', 'lat', 'lng', ]

    def __init__(self, api, addresses=[]):
        """
        Address Instance
        :param api:
        :param addresses:
        :return:
        """
        self.addresses = addresses
        Base.__init__(self, api)

    def get_route_id(self):
        """
        Return Route ID
        :return:
        """
        return self.get_response()['route_id']

    def get_route_destination_id(self):
        """
        Return Destination ID
        :return:
        """
        return self.get_response()['route_destination_id']

    def get_addresses(self):
        """
        Return Addresses
        :return:
        """
        return self.addresses

    def add_address(self, **kwargs):
        """
        Add addresses to optimization
        :param kwargs:
        :return:
        """
        if self.check_required_params(kwargs, self.required):
            self.addresses.append(kwargs)
            self.api.optimization.data['addresses'] = self.addresses
        else:
            raise ParamValueException('addresses', 'Params are not complete')

    def fix_geocodes(self, addresses):
        geocoding_error = []
        param_address = 'addresses='
        for a in addresses:
            param_address = '{0}{1}||'.format(param_address, a.get('address'))
        params = {'format': 'xml', 'addresses': param_address}
        content = self.api.get_geocodes(params)
        obj = xmltodict.parse(content)
        geocoded_addresses = []
        for i, d in enumerate(obj.get('destinations').get('destination')):
            try:
                address = dict([('lat', float(d.get('@lat'))),
                                          ('lng', float(d.get('@lng'))),
                                          ('time', addresses[i].get('time')),
                                          ('alias', addresses[i].get('alias')),
                                          ('address', d.get('@destination'))])
                if addresses[i].get('is_depot'):
                    address.update(dict([('is_depot', 1)]))
                geocoded_addresses.append(address)
            except IndexError:
                geocoding_error.append(d)
        return geocoding_error, geocoded_addresses