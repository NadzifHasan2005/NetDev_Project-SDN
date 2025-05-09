from mininet.topo import Topo

class SniffTopo(Topo):
    def build(self):
        # Tambah switch
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        # Tambah host
        h1 = self.addHost('h1')  # host1
        h2 = self.addHost('h2')  # host2
        h3 = self.addHost('h3')  # hacker1
        h4 = self.addHost('h4')  # hacker2
        h5 = self.addHost('h5')  # hacker3

        # Urutan link memengaruhi penomoran port

        # Switch s2
        self.addLink(s2, s1, port1=1, port2=1)  # s2-eth1
        self.addLink(s2, h1, port1=2, port2=1)  # s2-eth2
        self.addLink(s2, h5, port1=3, port2=1)  # s2-eth3

        # Switch s1
        self.addLink(s1, h2, port1=2, port2=1)  # s1-eth2
        self.addLink(s1, h3, port1=3, port2=1)  # s1-eth3
        self.addLink(s1, h4, port1=4, port2=1)  # s1-eth4

topos = {'snifftopo': (lambda: SniffTopo())}
