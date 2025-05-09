from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel

class LoadBalancingTopo(Topo):
    def build(self):
        # Tambah hosts
        h1 = self.addHost('h1', ip='10.0.0.1/24')
        h2 = self.addHost('h2', ip='10.0.0.2/24')
        h3 = self.addHost('h3', ip='10.0.0.3/24')
        h4 = self.addHost('h4', ip='10.0.0.4/24')

        # Tambah switches
        s1 = self.addSwitch('s1')  # Switch untuk H1
        s2 = self.addSwitch('s2')  # Switch untuk H4
        s3 = self.addSwitch('s3')  # Switch untuk H3
        s4 = self.addSwitch('s4')  # Switch untuk H2

        # Hubungkan host ke switch sesuai dengan permintaan
        self.addLink(h1, s1)
        self.addLink(h2, s4)
        self.addLink(h3, s3)
        self.addLink(h4, s2)

        # Inter-switch connections (middle mesh)
        self.addLink(s1, s2)  # s1 ke s2
        self.addLink(s1, s3)  # s1 ke s3
        self.addLink(s2, s4)  # s2 ke s4
        self.addLink(s3, s4)  # s3 ke s4

def run():
    topo = LoadBalancingTopo()
    net = Mininet(topo=topo,
              controller=lambda name: RemoteController(name, ip='10.0.0.4', port=6653),
              link=TCLink)
    net.start()
    print("Testing connectivity...")
    net.pingAll()
    CLI(net)
    net.stop()

if _name_ == '_main_':
    setLogLevel('info')
    run()
