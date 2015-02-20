from constants import *
from exceptions import ParamValueException
import types
import re


class Base(object):
    """
    Base Class, with common methods.
    """

    def __init__(self, api):
        """
        Base instance
        :param api:
        :return:
        """
        self.response = None
        self.api = api
        self.data = {'parameters': {},
                     'addresses': {},
                     }
        self.params = {'api_key': api.key, }

    def format(self, set_format):
        """
        Add format to params.
        :param set_format:
        :return:
        :raise: ParamValueException if set_format is not in FORMAT
        """
        if set_format in FORMAT.reverse_mapping.keys():
            self._copy_param({'format': set_format})
        else:
            raise ParamValueException('format', 'Must be CSV, SERIALIZED, XML')

    def member_id(self, member_id, target='data'):
        """
        Set member_id in params or data
        :param member_id:
        :param target:
        :return:
        :raise: ParamValueException if member_id is not Integer
        """
        if isinstance(member_id, types.LongType) or isinstance(member_id,
                                                               types.IntType):
            getattr(self, '_copy_%s' % target)({'member_id': member_id})
        else:
            raise ParamValueException('member_id', 'Must be Integer or Long')

    def route_id(self, route_id):
        """
        Set route_id in params or data
        :param route_id:
        :return:
        :raise: ParamValueException if route_id is not String
        """
        if isinstance(route_id, types.StringTypes):
            self._copy_param({'route_id': route_id})
        else:
            raise ParamValueException('route_id', 'Must be String')

    def tx_id(self, tx_id):
        """
        Set tx_id param
        :param tx_id:
        :return:
        """
        if isinstance(tx_id, types.StringTypes):
            self._copy_param({'tx_id': tx_id})
        else:
            raise ParamValueException('tx_id', 'Must be String')

    def vehicle_id(self, vehicle_id):
        """
        Set vehicle_id param
        :param vehicle_id:
        :return:
        """
        if isinstance(vehicle_id, types.LongType) or isinstance(vehicle_id,
                                                                types.IntType):
            self._copy_data({'vehicle_id': vehicle_id})
        else:
            raise ParamValueException('vehicle_id', 'Must be integer or long')

    def course(self, course):
        """
        Set course param
        :param course:
        :return:
        """
        if isinstance(course, types.LongType) or isinstance(course,
                                                                types.IntType):
            self._copy_param({'course': course})
        else:
            raise ParamValueException('course', 'Must be integer or long')

    def speed(self, speed):
        """
        Set speed param
        :param speed:
        :return:
        """
        if isinstance(speed, types.LongType) or isinstance(speed,
                                                                types.IntType):
            self._copy_param({'speed': speed})
        else:
            raise ParamValueException('speed', 'Must be Float')

    def lat(self, lat):
        """
        Set lat param
        :param lat:
        :return:
        """
        if isinstance(lat, types.FloatType):
            self._copy_param({'lat': lat})
        else:
            raise ParamValueException('lat', 'Must be Float')

    def lng(self, lng):
        """
        Set lng param
        :param lng:
        :return:
        """
        if isinstance(lng, types.FloatType):
            self._copy_param({'lng': lng})
        else:
            raise ParamValueException('lng', 'Must be Float')

    def altitude(self, altitude):
        """
        Set altitude param
        :param altitude:
        :return:
        """
        if isinstance(altitude, types.FloatType):
            self._copy_param({'altitude': altitude})
        else:
            raise ParamValueException('altitude', 'Must be Float')

    def device_guid(self, device_guid):
        """
        Set device_guid param
        :param device_guid:
        :return:
        """
        if isinstance(device_guid, types.StringTypes):
            self._copy_param({'device_guid': device_guid})
        else:
            raise ParamValueException('device_guid', 'Must be String')

    def app_version(self, app_version):
        """
        Set app_version param
        :param app_version:
        :return:
        """
        if isinstance(app_version, types.StringTypes):
            self._copy_param({'app_version': app_version})
        else:
            raise ParamValueException('app_version', 'Must be String')

    def device_timestamp(self, device_timestamp):
        """
        Set device_timestamp param. Must be a vale date time
        with this format:  YYYY-MM-DD HH:MM:SS
        :param device_timestamp:
        :return:
        """
        pattern = '^(\d{4})-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01]) ' \
                  '([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])$'
        if re.match(pattern, device_timestamp):
            self._copy_param({'device_timestamp': device_timestamp})
        else:
            raise ParamValueException('device_timestamp',
                                      'Must be YYYY-MM-DD HH:MM:SS format')

    def algorithm_type(self, algorithm_type):
        """
        Set algorithm_type. Choices are:
        TSP, VRP, CVRP_TW_SD
        CVRP_TW_MD, TSP_TW,
        TSP_TW_CR and BBCVRP
        :param: algorithm_type:
        :return:
        """
        if 1 <= algorithm_type <= 7:
            self._copy_data({'algorithm_type': algorithm_type})
        else:
            raise ParamValueException('algorithm_type',
                                      'Must be ALGORITHM_TYPE: '
                                      'TSP, VRP, CVRP_TW_SD, '
                                      'CVRP_TW_MD, TSP_TW, '
                                      'TSP_TW_CR and BBCVRP')

    def route_name(self, route_name):
        """
        Set route_name param
        :param route_name:
        :return:
        """
        if isinstance(route_name, types.StringTypes):
            self._copy_data({'route_name': route_name})
        else:
            raise ParamValueException('route_name', 'Must be String')

    def optimization_problem_id(self, optimization_problem_id):
        """
        Set optimization_problem_id param
        :param optimization_problem_id:
        :return:
        """
        if isinstance(optimization_problem_id, types.StringTypes):
            self._copy_param({'optimization_problem_id':
                                  optimization_problem_id})
        else:
            raise ParamValueException('optimization_problem_id',
                                      'Must be String')

    def remote_ip(self, remote_ip):
        """
        Set remote_ip param
        :param remote_ip:
        :return:
        """
        if isinstance(remote_ip, types.LongType) or isinstance(remote_ip,
                                                               types.IntType):
            self._copy_data({'remote_ip': remote_ip})
        else:
            raise ParamValueException('remote_ip', 'Must be integer or long')

    def travel_mode(self, travel_mode):
        """
        Set travel_mode. Options are:
        DRIVING, WALKING, TRUCKING
        :param travel_mode:
        :return:
        """
        if travel_mode in TRAVEL_MODE.reverse_mapping.keys():
            self._copy_data({'travel_mode': travel_mode})
        else:
            raise ParamValueException('travel_mode', 'Must be DRIVING, '
                                                     'WALKING, TRUCKING')

    def optimize(self, optimize):
        """
        Set optimize param
        :param optimize:
        :return:
        """
        if optimize in OPTIMIZE.reverse_mapping.keys():
            self._copy_data({'optimize': optimize})
        else:
            raise ParamValueException('optimize', 'Must be DISTANCE, TIME, '
                                                  'TIME_WITH_TRAFFIC')

    def distance_unit(self, distance_unit):
        """
        Set distance_unit param
        :param distance_unit:
        :return:
        """
        if distance_unit in DISTANCE_UNIT.reverse_mapping.keys():
            self._copy_data({'distance_unit': distance_unit})
        else:
            raise ParamValueException('distance_unit', 'Must be MI or KM')

    def device_type(self, device_type, target='data'):
        """
        Set device_type. Options are: WEB, IPHONE, IPAD, ANDROID_PHONE,
        ANDROID_TABLET
        :param device_type:
        :param target:
        :return:
        """
        if device_type in DEVICE_TYPE.reverse_mapping.keys():
            getattr(self, '_copy_%s' % target)({'device_type': device_type})
        else:
            raise ParamValueException('device_type', 'Must be WEB, IPHONE, '
                                                     'IPAD, ANDROID_PHONE, '
                                                     'ANDROID_TABLET')

    def route_path_output(self, route_path_output):
        """
        Set device_type. Options are: WEB, IPHONE, IPAD, ANDROID_PHONE,
        ANDROID_TABLET
        :param route_path_output:
        :param target:
        :return:
        """
        if route_path_output in ROUTE_PATH_OUTPUT.reverse_mapping.keys():
            self._copy_param({'route_path_output': route_path_output})
        else:
            raise ParamValueException('route_path_output', 'Must be NONE or '
                                                           'POINTS')

    def route_time(self, route_time):
        """
        Set route_time param
        :param route_time:
        :return:
        """
        if isinstance(route_time, types.LongType) or isinstance(route_time,
                                                                types.IntType):
            self._copy_data({'route_time': route_time})
        else:
            raise ParamValueException('route_time', 'Must be integer or long')

    def route_max_duration(self, route_max_duration):
        """
        Set route_max_duration param
        :param route_max_duration:
        :return:
        """
        if isinstance(route_max_duration, types.LongType) or \
                isinstance(route_max_duration, types.IntType):
            self._copy_data({'route_max_duration': route_max_duration})
        else:
            raise ParamValueException('route_max_duration',
                                      'Must be integer or long')

    def vehicle_capacity(self, vehicle_capacity):
        """
        Set vehicle_capacity param
        :param vehicle_capacity:
        :return:
        """
        if isinstance(vehicle_capacity, types.LongType) or \
                isinstance(vehicle_capacity, types.IntType):
            self._copy_data({'vehicle_capacity': vehicle_capacity})
        else:
            raise ParamValueException('vehicle_capacity',
                                      'Must be integer or long')

    def parts(self, parts):
        """
        Set parts param
        :param parts:
        :return:
        """
        if isinstance(parts, types.LongType) or \
                isinstance(parts, types.IntType):
            self._copy_data({'parts': parts})
        else:
            raise ParamValueException('parts',
                                      'Must be integer or long')

    def limit(self, limit):
        """
        Set limit param
        :param limit:
        :return:
        """
        if isinstance(limit, types.LongType) or \
                isinstance(limit, types.IntType):
            self._copy_param({'limit': limit})
        else:
            raise ParamValueException('limit',
                                      'Must be integer or long')

    def offset(self, offset):
        """
        Set offset param
        :param offset:
        :return:
        """
        if isinstance(offset, types.LongType) or \
                isinstance(offset, types.IntType):
            self._copy_param({'offset': offset})
        else:
            raise ParamValueException('offset',
                                      'Must be integer or long')

    def vehicle_max_distance_mi(self, vehicle_max_distance_mi):
        """
        Set vehicle_max_distance_mi
        :param vehicle_max_distance_mi:
        :return:
        """
        if isinstance(vehicle_max_distance_mi, types.LongType) or \
                isinstance(vehicle_max_distance_mi, types.IntType):
            self._copy_data({'vehicle_max_distance_mi':
                                 vehicle_max_distance_mi})
        else:
            raise ParamValueException('vehicle_max_distance_mi',
                                      'Must be integer or long')

    def route_email(self, route_email):
        """
        Set route_email param
        :param route_email:
        :return:
        """
        if isinstance(route_email, types.StringTypes):
            self._copy_data({'route_email': route_email})
        else:
            raise ParamValueException('route_email', 'Must be String')

    def metric(self, metric):
        """
        Set metric Param. Must be:
        ROUTE4ME_METRIC_EUCLIDEA
        ROUTE4ME_METRIC_MANHATTA
        ROUTE4ME_METRIC_GEODESIC
        ROUTE4ME_METRIC_MATRIX
        ROUTE4ME_METRIC_EXACT_2D
        :param metric:
        :return:
        """
        if 1 <= metric <= 7:
            self._copy_data({'metric': metric})
        else:
            raise ParamValueException('metric',
                                      'Must be METRIC: '
                                      'ROUTE4ME_METRIC_EUCLIDEAN , '
                                      'ROUTE4ME_METRIC_MANHATTAN, '
                                      'ROUTE4ME_METRIC_GEODESIC'
                                      'ROUTE4ME_METRIC_MATRIX'
                                      'ROUTE4ME_METRIC_EXACT_2D')

    def store_route(self, store_route):
        """
        Set store_route param
        :param store_route:
        :return:
        """
        if 0 <= store_route <= 1:
            self._copy_data({'store_route': store_route})
        else:
            raise ParamValueException('store_route', 'Must be 0 or 1')

    def reoptimize(self, reoptimize):
        """
        Set reoptimize param
        :param reoptimize:
        :return:
        """
        if 0 <= reoptimize <= 1:
            self._copy_param({'reoptimize': reoptimize})
        else:
            raise ParamValueException('reoptimize', 'Must be 0 or 1')

    def share_route(self, share_route):
        """
        Set share_route param
        :param share_route:
        :return:
        """
        if 0 <= share_route <= 1:
            self._copy_data({'share_route': share_route})
        else:
            raise ParamValueException('share_route', 'Must be 0 or 1')

    def rt(self, rt):
        """
        Set rt param.
        :param rt:
        :return:
        """
        if 0 <= rt <= 1:
            self._copy_data({'rt': rt})
        else:
            raise ParamValueException('rt', 'Must be 0 or 1')

    def directions(self, directions):
        """
        Set directions param.
        :param directions:
        :return:
        """
        if 0 <= directions <= 1:
            self._copy_param({'directions': directions})
        else:
            raise ParamValueException('directions', 'Must be 0 or 1')

    def device_tracking_history(self, device_tracking_history):
        """
        Set device_tracking_history param.
        :param device_tracking_history:
        :return:
        """
        if 0 <= device_tracking_history <= 1:
            self._copy_param({'device_tracking_history': device_tracking_history})
        else:
            raise ParamValueException('device_tracking_history', 'Must be 0 or 1')

    def _copy_data(self, params):
        """
        Copy params to data
        :param params:
        :return:
        """
        self.data['parameters'].update(params)

    def _copy_param(self, params):
        """
        Copy params to params
        :param params:
        :return:
        """
        self.params.update(params)

    def get_params(self):
        """
        Get params
        :return:  params
        """
        return self.params

    def required_params(self, requirements=[]):
        """
        Check if required params are set
        :param requirements:
        :return:
        """
        return set(requirements).issubset(set(self.params.keys()))

    @staticmethod
    def check_required_params(params, requirements=[] ):
        """
        Check if required params are set
        :param requirements:
        :return:
        """
        return set(requirements).issubset(set(params.keys()))

    def validate_params(self, **kwargs):
        """
        Validate params
        :param kwargs:
        :return:
        """
        for k, v in kwargs.items():
            try:
                self.__getattribute__(k)(v)
            except AttributeError as e:
                raise e
        return True

    def add(self, params={}, data={}):
        """
        Add params and data
        :param params:
        :param data:
        :return:
        """
        self.validate_params(**params)
        self.validate_params(**data)
        self.data.update(data)
        self.params.update(params)