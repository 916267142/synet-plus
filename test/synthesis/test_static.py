#!/usr/bin/env python
import unittest

from ipaddress import ip_interface

from synet.synthesis.static import CannotSynthesizeStaticRoute
from synet.synthesis.static import StaticSyn


from synet.topo.bgp import Announcement
from synet.topo.bgp import BGP_ATTRS_ORIGIN
from synet.topo.bgp import Community
from synet.topo.graph import NetworkGraph

from synet.utils.common import PathProtocols
from synet.utils.common import PathReq
from synet.utils.smt_context import VALUENOTSET
from synet.utils.topo_gen import gen_mesh


__author__ = "Ahmed El-Hassany"
__email__ = "a.hassany@gmail.com"


class StaticTest(unittest.TestCase):
    def get_two_nodes(self):
        g = NetworkGraph()
        g.add_router('R1')
        g.add_router('R2')
        g.add_router_edge('R1', 'R2')
        g.add_router_edge('R2', 'R1')
        return g

    def test_two_nodes(self):
        g = self.get_two_nodes()
        prefix = 'P0'
        reqs = [PathReq(PathProtocols.BGP, prefix, ['R1', 'R2'], 10)]
        g.set_static_routes_empty('R1')
        static_syn = StaticSyn(reqs, g)
        static_syn.synthesize()
        self.assertEquals(g.get_static_routes('R1')[prefix], 'R2')

    def test_not_empty(self):
        g = self.get_two_nodes()
        prefix = 'P0'
        reqs = [PathReq(PathProtocols.BGP, prefix, ['R1', 'R2'], 10)]
        static_syn = StaticSyn(reqs, g)
        with self.assertRaises(CannotSynthesizeStaticRoute):
            static_syn.synthesize()

    def test_two_existing(self):
        g = self.get_two_nodes()
        prefix = 'P0'
        reqs = [PathReq(PathProtocols.BGP, prefix, ['R1', 'R2'], 10)]
        g.add_static_route('R1', prefix, 'R2')
        static_syn = StaticSyn(reqs, g)
        static_syn.synthesize()
        self.assertEquals(g.get_static_routes('R1')[prefix], 'R2')
