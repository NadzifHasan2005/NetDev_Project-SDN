from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet

class SniffingController(app_manager.RyuApp):
    # Menentukan versi OpenFlow yang digunakan oleh controller ini
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def _init_(self, *args, **kwargs):
        # Konstruktor untuk inisialisasi controller
        super(SniffingController, self)._init_(*args, **kwargs)
        # Menyimpan mapping MAC address ke port switch
        self.mac_to_port = {}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        # Menangani event ketika switch baru terhubung
        datapath = ev.msg.datapath
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto

        # Install table-miss flow entry yang mengarah ke controller
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions):
        # Fungsi untuk menambahkan flow entry ke switch
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Instruksi untuk menerapkan aksi yang ditentukan pada flow
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                match=match, instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        # Menangani event ketika ada paket yang masuk ke controller
        msg = ev.msg
        datapath = msg.datapath
        dpid = datapath.id
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto

        # Mengambil informasi Ethernet dari paket yang diterima
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)

        # Mendapatkan alamat tujuan dan sumber
        dst = eth.dst
        src = eth.src
        in_port = msg.match['in_port']

        # Menyimpan MAC address ke port
        self.mac_to_port.setdefault(dpid, {})
        self.mac_to_port[dpid][src] = in_port

        # Menentukan port keluar berdasarkan MAC address tujuan
        out_port = self.mac_to_port[dpid].get(dst, ofproto.OFPP_FLOOD)

        actions = []

        # Jika alamat tujuan ditemukan (tidak di flood), paket akan keluar melalui port tersebut
        if out_port != ofproto.OFPP_FLOOD:
            actions.append(parser.OFPActionOutput(out_port))

        # Logika sniffing berdasarkan dpid (ID switch):
        if dpid == 1:
            # Jika switch adalah S1, kita duplikasi paket yang menuju Host2 ke Hacker1 (port 3) dan Hacker2 (port 4)
            if out_port != 3:
                actions.append(parser.OFPActionOutput(3))  # Menyalin ke Hacker1
            if out_port != 4:
                actions.append(parser.OFPActionOutput(4))  # Menyalin ke Hacker2

        elif dpid == 2:
            # Jika switch adalah S2, kita duplikasi paket yang menuju Host1 ke Hacker3 (port 3)
            if out_port != 3:
                actions.append(parser.OFPActionOutput(3))  # Menyalin ke Hacker3

        # Membuat pesan PacketOut untuk mengirimkan paket yang telah dimodifikasi
        out = parser.OFPPacketOut(datapath=datapath,
                                  buffer_id=ofproto.OFP_NO_BUFFER,
                                  in_port=in_port,
                                  actions=actions,
                                  data=msg.data)
        datapath.send_msg(out)
