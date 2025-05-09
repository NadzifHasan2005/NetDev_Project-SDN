from mininet.topo import Topo

class QoSTopo(Topo):
    def __init__(self):
        Topo.__init__(self)

        # Add switches
        s1 = self.addSwitch('s1', protocols='OpenFlow13')
        s2 = self.addSwitch('s2', protocols='OpenFlow13')

        # Add hosts with MAC and IP
        h1 = self.addHost('h1', mac='00:00:00:00:00:01', ip='10.0.0.1/24')  # V>
        h2 = self.addHost('h2', mac='00:00:00:00:00:02', ip='10.0.0.2/24')  # H>
        h3 = self.addHost('h3', mac='00:00:00:00:00:03', ip='10.0.0.3/24')  # V>
        h4 = self.addHost('h4', mac='00:00:00:00:00:04', ip='10.0.0.4/24')  # H>

        # Add links
        self.addLink(h1, s1, port1=1, port2=1)  # h1 --> port 1 s1
        self.addLink(h2, s1, port1=1, port2=2)  # h2 --> port 2 s1
        self.addLink(s1, s2, port1=3, port2=1)  # s1 port3 --> s2 port 2
        self.addLink(h3, s2, port1=1, port2=2)  # h3 --> port 2 s2
        self.addLink(h4, s2, port1=1, port2=3)  # h4 --> port 3 s2

topos = {'QoS_topo': (lambda: QoSTopo())}
