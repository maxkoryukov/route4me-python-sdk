# -*- coding: utf-8 -*-

"""
An Optimization Problem refers to a collection of addresses that need to be
visited.

The optimization problem takes into consideration all of the addresses that
need to be visited and all the constraints associated with each address and
depot.

It is preferable to create an optimization problem with as many orders in it
as possible, so that the optimization engine is able to consider the entire
problem set.

This is different from a :class:`~route4me.sdk.models.Route`, which
is a sequence of addresses that need to be visited by a single vehicle and
driver in a fixed time period. Solving an Optimization Problem results in
a number of routes. (Possibly recurring in the future)

.. seealso:: https://route4me.io/docs/#optimizations

"""

import pydash

from ..models import Optimization
from ..enums import OptimizationStateEnum

from ..errors import Route4MeApiError
from route4me.sdk.utils import PagedList

from route4me.sdk._internals import add_limit_offset_to_query_string
from route4me.sdk._internals.typeconv import bool201
from route4me.sdk._internals.net import NetworkClient


class Optimizations(object):
	"""
	Optimizations endpoint
	"""

	def __init__(self, api_key=None, _network_client=None):
		nc = _network_client
		if nc is None:
			nc = NetworkClient(api_key)
		self.__nc = nc

	def create(self, optimization_data, optimized_callback_url=None):
		"""
		Create a new optimization through the Route4Me API

		You could pass any valid URL as :paramref:`optimized_callback_url`
		parameter.

		The callback URL is a URL that gets called when the optimization is
		solved, or if there is an error. The callback is called with a
		**POST** request. The example of the POST data sent:

		.. code-block:: javascript

			{
				"timestamp": 1500111222,        // seconds
				"state": 4,                     // ID of the optimization state

				// ID of Optimization Problem
				"optimization_problem_id": "1EDB78F63556D99336E06A13A34CF139"
			}

		The ``state`` is a value from the enumeration
		:class:`~route4me.sdk.enums.OptimizationStateEnum`

		.. seealso::

			Route4Me API: https://route4me.io/docs/#create-an-optimization

		:param optimization_data: Optimization data
		:type optimization_data: ~route4me.sdk.models.Optimization or dict
		:param optimized_callback_url: Optimization done callback URL, defaults \
			to None
		:type optimized_callback_url: str or None, optional
		:returns: New optimization
		:rtype: ~route4me.sdk.models.Optimization
		"""

		query = None
		if optimized_callback_url:
			query = {
				'optimized_callback_url': optimized_callback_url,
			}

		data = optimization_data

		# if isinstance(optimization_data, BaseModel):
		# 	data = optimization_data.raw

		res = self.__nc.post(
			'/api.v4/optimization_problem.php',
			subdomain='www',
			query=query,
			data=data,
		)
		return Optimization(res)

	def get(self, ID):
		"""
		GET a single optimization by ID.

		.. seealso::

			Route4Me API: https://route4me.io/docs/#get-an-optimization

		:param ID: Optimization Problem ID
		:type ID: str
		:returns: Optimization data
		:rtype: ~route4me.sdk.models.Optimization

		:raises ~route4me.sdk.errors.Route4MeEntityNotFoundError: if \
			optimization was not found
		"""

		res = self.__nc.get(
			'/api.v4/optimization_problem.php',
			subdomain='www',
			query={
				'optimization_problem_id': ID,
			}
		)

		return Optimization(res)

	def list(self, states=None, limit=None, offset=None):
		"""
		GET all optimizations belonging to a user.

		Optionally filtered

		.. seealso::

			Route4Me API: https://route4me.io/docs/#get-optimizations

		:param states: Comma separated list of states, you can pass one CSV \
			string or any enumerable of state IDS (string and enums are \
			supported), defaults to None
		:type states: str or list(str) or list(OptimizationStateEnum), optional
		:param limit: Search limitation, defaults to None
		:type limit: int, optional
		:param offset: Search starting position, defaults to None
		:type offset: int, optional
		"""
		qs = {}
		add_limit_offset_to_query_string(limit, offset, qs)

		if states:
			s = OptimizationStateEnum.parse_many(states)
			qs['state'] = ','.join([str(i.value) for i in s])

		res = self.__nc.get(
			'/api.v4/optimization_problem.php',
			subdomain='www',
			query=qs
		)

		return PagedList(
			total=res['totalRecords'],
			limit=limit,
			offset=offset,
			items=[Optimization(item) for item in res['optimizations']],
		)

	def update(
		self,
		ID,
		optimization_data=None,
		reoptimize=False,
		# TODO: try to implement or remove!
		# optimized_callback_url=None,
	):
		"""
		Update existing optimization problem, by changing some parameters or
		addresses. Optionally you can re-run the optimization engine for the
		optimization problem

		Notice, that you can re-run optimization without modifications.

		.. seealso::

			Route4Me API: https://route4me.io/docs/#re-optimize-an-optimization

		:param ID: Optimization problem ID
		:type ID: str
		:param optimization_data: Optimization data, defaults to None
		:type optimization_data: ~route4me.sdk.models.Optimization or dict, \
			optional
		:param reoptimize: Whether to re-run optimization, defaults to \
			:data:`False`
		:type reoptimize: bool, optional
		:returns: Updated optimization
		:rtype: ~route4me.sdk.models.Optimization
		"""
		query = {
			'optimization_problem_id': ID,
			'reoptimize': bool201(reoptimize),
		}

		data = optimization_data if optimization_data else {}

		res = self.__nc.put(
			'/api.v4/optimization_problem.php',
			subdomain='www',
			query=query,
			data=data,
		)
		return Optimization(res)

	def remove(self, ID):
		"""
		Remove an existing optimization belonging to an user.

		.. seealso::

			Route4Me API: https://route4me.io/docs/#remove-an-optimization

		:param ID: Optimization Problem ID
		:type ID: str
		:returns: Always :data:`True`
		:rtype: bool

		:raises ~route4me.sdk.errors.Route4MeApiError: if Route4Me API \
			returned not expected response
		:raises ~route4me.sdk.errors.Route4MeEntityNotFoundError: if \
			optimization was not found
		"""

		res = self.__nc.delete(
			'/api.v4/optimization_problem.php',
			subdomain='www',
			query={
				'optimization_problem_id': ID,
			}
		)

		if not pydash.get(res, 'status'):
			# TODO: this exception should contain METHOD and URL fields
			raise Route4MeApiError(
				'Not expected response',
				code='route4me.sdk.api_error',
				details={
					'res': res,
				},
				method='DELETE',
				# url=''
			)

		return True

	def reoptimize(
		self,
		ID,
		# optimization_data=None,
		# optimized_callback_url=None,
	):
		"""
		An alias for :meth:`.update`, with ``reoptimize`` set to :data:`True`
		"""
		return self.update(ID=ID, reoptimize=True)
