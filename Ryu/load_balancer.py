from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, ipv4, arp
from ryu.lib import hub
import itertools

class LoadBalancer(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def _init_(self, *args, **kwargs):
        super(LoadBalancer, self)._init_(*args, **kwargs)
        self.mac_to_port = {}
        self.datapaths = {}
        self.monitor_thread = hub.spawn(self._monitor)

        # Konfigurasi virtual IP dan backends
        self.virtual_ip = '10.0.0.100'
        self.virtual_mac = 'aa:bb:cc:dd:ee:ff'
        self.backends = {
            '10.0.0.2': {'mac': '00:00:00:00:00:02', 'port': 2},
            '10.0.0.3': {'mac': '00:00:00:00:00:03', 'port': 3},
        }

        # Round-robin iterator untuk backend
        self.backend_iter = itertools.cycle(self.backends.items())

    def _monitor(self):
        while True:
            for dp in self.datapaths.values():
                self._request_stats(dp)
            hub.sleep(5)

    def _request_stats(self, datapath):
        parser = datapath.ofproto_parser
        req = parser.OFPFlowStatsRequest(datapath)
        datapath.send_msg(req)

    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def flow_stats_reply_handler(self, ev):
        for stat in ev.msg.body:
            self.logger.info("Flow stats: %s", stat)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto

        self.logger.info("Switch connected: datapath_id=%s", datapath.id)

        # Flow default ke controller
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

        # Flow untuk komunikasi ARP dan IP Traffic antar host
        match = parser.OFPMatch(eth_type=0x0806)  # ARP untuk IP lokal
        actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]  # Flood ARP request ke semua port
        self.add_flow(datapath, 10, match, actions)

        # Flow untuk komunikasi IP antar host (tanpa controller)
        match = parser.OFPMatch(eth_type=0x0800)  # Semua paket IP
        actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]  # Flood IP traffic antar host
        self.add_flow(datapath, 20, match, actions)

    def add_flow(self, datapath, priority, match, actions, idle_timeout=60, hard_timeout=0):
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(datapath=datapath,
                                priority=priority,
                                match=match,
                                instructions=inst,
                                idle_timeout=idle_timeout,
                                hard_timeout=hard_timeout)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)
        if eth is None:
            return

        arp_pkt = pkt.get_protocol(arp.arp)
        ip_pkt = pkt.get_protocol(ipv4.ipv4)

        # Handle ARP request untuk virtual IP
        if arp_pkt and arp_pkt.opcode == arp.ARP_REQUEST and arp_pkt.dst_ip == self.virtual_ip:
            self.logger.info("Received ARP request for virtual IP")
            self.reply_arp(datapath, arp_pkt, in_port)
            return

        # Handle trafik yang ditujukan ke virtual IP
        if ip_pkt and ip_pkt.dst == self.virtual_ip:
            # Pilih backend berdasarkan round-robin
            selected_ip, backend = next(self.backend_iter)

            self.logger.info("Routing traffic to backend: %s", selected_ip)

            match = parser.OFPMatch(
                in_port=in_port,
                eth_type=0x0800,
                ipv4_dst=self.virtual_ip,
                ipv4_src=ip_pkt.src
            )

            actions = [
                parser.OFPActionSetField(ipv4_dst=selected_ip),
                parser.OFPActionSetField(eth_dst=backend['mac']),
                parser.OFPActionOutput(backend['port'])
            ]

            self.add_flow(datapath, 10, match, actions, idle_timeout=30)

            out = parser.OFPPacketOut(
                datapath=datapath,
                buffer_id=ofproto.OFP_NO_BUFFER,
                in_port=in_port,
                actions=actions,
                data=msg.data
            )
            datapath.send_msg(out)

    def reply_arp(self, datapath, arp_request, port):
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto

        ether = ethernet.ethernet(
            dst=arp_request.src_mac,
            src=self.virtual_mac,
            ethertype=0x0806
        )

        arp_reply = arp.arp(
            opcode=arp.ARP_REPLY,
            src_mac=self.virtual_mac,
            src_ip=self.virtual_ip,
            dst_mac=arp_request.src_mac,
            dst_ip=arp_request.src_ip
        )

        pkt = packet.Packet()
        pkt.add_protocol(ether)
        pkt.add_protocol(arp_reply)
        pkt.serialize()

        out = parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=ofproto.OFP_NO_BUFFER,
            in_port=ofproto.OFPP_CONTROLLER,
            actions=[parser.OFPActionOutput(port)],
            data=pkt.data
        )
        datapath.send_msg(out)
