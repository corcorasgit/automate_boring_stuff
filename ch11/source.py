#!/usr/bin/python3
r1 = '''
version 15.2

service timestamps debug datetime msec localtime
service timestamps log datetime msec localtime
service password-encryption
!
hostname [[hostname]] 
!
boot-start-marker
boot system flash0:c2900-universalk9-mz.SPA.152-4.M5.bin
boot-end-marker
!
card type t1 0 0
card type t1 0 2
logging buffered 128000
enable secret 4 testsecretpassword
!
aaa new-model
!
aaa authentication login local_auth local
aaa authorization exec default local 
!
aaa session-id common
clock timezone [[timezone]] [[timezone offset]] 0
clock summer-time [[timezone]] recurring
network-clock-participate wic 0 
no network-clock-participate wic 2 
network-clock-select 1 T1 0/0/0
!
no ip gratuitous-arps
ip cef
!
no ip domain lookup
ip domain name [[domain name]]
ip host aspdms [[server ip]]
ip wccp source-interface GigabitEthernet0/0.75
ip wccp 61
ip wccp 62
no ipv6 cef
multilink bundle-name authenticated
!
isdn switch-type primary-ni
!
key chain eigrp48
 key 48
  key-string 7 1043081E0C1C4653
!
voice-card 0
 dspfarm
 dsp services dspfarm
!
voice call send-alert
voice call carrier capacity active
voice rtp send-recv
!
voice service pots
!
voice service voip
 ip address trusted list
 allow-connections h323 to h323
 allow-connections h323 to sip
 allow-connections sip to h323
 allow-connections sip to sip
 supplementary-service media-renegotiate
 signaling forward unconditional
 fax protocol pass-through g711ulaw
 h323
  h225 display-ie ccm-compatible
  call start slow
  call preserve 
 modem passthrough nse codec g711ulaw redundancy
 sip
  registrar server
!
voice class codec 1
 codec preference 1 g711ulaw
 codec preference 2 g729r8
!
voice class codec 2
 codec preference 1 g729r8
!
voice class h323 1
  h225 timeout tcp establish 3
  h225 timeout setup 3
!
!
voice class cause-code 1
 no-circuit
!
license udi pid CISCO2921/K9 sn TTF123456
hw-module pvdm 0/0
!
hw-module pvdm 0/1
!
archive
 log config
  logging enable
  logging size 500
  notify syslog contenttype plaintext
  hidekeys
 path flash:archived.config
 maximum 7
 time-period 1440
username admin secret 4 testpassword123
!
redundancy
!
controller T1 0/0/0
 shutdown
 cablelength long 0db
!
controller T1 0/0/1
 shutdown
 cablelength long 0db
!
controller T1 0/2/0
 shutdown
 cablelength long 0db
 channel-group 0 timeslots 1-24
!
controller T1 0/2/1
 shutdown
 cablelength long 0db
 channel-group 0 timeslots 1-24
!
ip telnet source-interface GigabitEthernet0/0.75
ip ftp source-interface GigabitEthernet0/0.75
ip tftp source-interface GigabitEthernet0/0.75
ip ssh version 2
ip scp server enable
lldp run
!
class-map match-any ENT_APPS
 match ip dscp cs2 
 match access-group name ENT_APPS
class-map match-any INTERACTIVE
 match ip dscp cs4 
 match access-group name INTERACTIVE
class-map match-any VOICE
 match ip dscp ef 
 match access-group name VOICE
 match ip dscp cs3 
 match ip dscp af31 
 match ip dscp af41 
!
policy-map WAN-EDGE
 description Outbound QoS Parameters
 class VOICE
  priority percent 60
  set ip precedence 5
 class INTERACTIVE
  bandwidth percent 10 
  set ip precedence 4
 class ENT_APPS
  bandwidth percent 15 
  set ip precedence 2
 class class-default
  set ip dscp default
  random-detect
policy-map WAN-EDGE-SHAPE-ASP
 class class-default
  shape average 5000000
   service-policy WAN-EDGE
!
interface Loopback0
 description [[loopback voice description]]
 ip address [[loopback voice]] 255.255.255.255
 no ip redirects
 h323-gateway voip interface
 h323-gateway voip bind srcaddr [[loopback voice]]
!
interface Loopback10
 description [[loopback data description]]
 ip address [[loopback data ip]] 255.255.255.255
!
interface Embedded-Service-Engine0/0
 no ip address
 shutdown
!
interface GigabitEthernet0/0
 description trunk port
 no ip address
 no ip redirects
 load-interval 30
 duplex auto
 speed auto
 no shut
!
interface GigabitEthernet0/0.75
 description [[lan description]]
 encapsulation dot1Q 75
 ip address [[lan ip address]] [[lan mask]]
 no ip redirects
 ip nat inside
 no ip virtual-reassembly in
 no shut
!
interface GigabitEthernet0/1
 description [[wan description]]
 dampening 30 3 1000 255 restart 255
 bandwidth 5000
 ip address [[wan ip address]] [[wan mask]]
 no ip redirects
 no ip proxy-arp
 ip wccp 61 redirect out
 ip wccp 62 redirect in
 ip nat outside
 no ip virtual-reassembly in
 duplex full
 speed 100
 service-policy output WAN-EDGE-SHAPE-ASP
 no shut
!
interface GigabitEthernet0/2
 no ip address
 shutdown
 duplex auto
 speed auto
!
interface Serial0/2/0:0
 no ip address
 shutdown
!
interface Serial0/2/1:0
 no ip address
 shutdown
!
!
router eigrp 48
 network 172.17.0.1 0.0.0.0
 network 192.191.180.145 0.0.0.0
 network 199.194.157.0 0.0.0.31
 redistribute bgp 65002 metric 1540000 0 255 1 1500 route-map BGP-TO-EIGRP
 no eigrp log-neighbor-changes
!
router bgp 65002
 bgp log-neighbor-changes
 network 10.27.23.0 mask 255.255.255.0
 network 10.42.0.0 mask 255.255.255.0
 network 172.16.0.0 mask 255.255.255.0
 network 172.17.0.1 mask 255.255.255.255
 network 172.30.3.0 mask 255.255.255.0
 network 172.30.4.0 mask 255.255.255.0
 network 192.191.180.145 mask 255.255.255.255
 network 198.249.107.192 mask 255.255.255.224
 network 199.194.157.0 mask 255.255.255.224
 network 199.194.208.64 mask 255.255.255.240
 neighbor 65.152.7.85 remote-as 209
 neighbor 65.152.7.85 send-community
 neighbor 65.152.7.85 soft-reconfiguration inbound
 neighbor 65.152.7.85 route-map MPLS-INBOUND in
 neighbor 65.152.7.85 route-map MPLS-OUTBOUND out
!
ip forward-protocol nd
!
ip bgp-community new-format
no ip http server
ip http authentication local
no ip http secure-server
ip http timeout-policy idle 600 life 86400 requests 10000
!
ip nat translation udp-timeout 180
no ip nat service sip udp port 5060
ip nat inside source route-map NAT-TO-ABCD interface GigabitEthernet0/0.75 overload
ip nat inside source route-map NAT-TO-HOSTED interface GigabitEthernet0/0.75 overload
ip route 0.0.0.0 0.0.0.0 [[wan gateway]]
ip route 172.30.249.0 255.255.255.0 199.194.157.24 name ASA_VPN_Pool
!
ip access-list extended ENT_APPS
 remark Enterprise Applications
 deny   tcp any eq cmd any
 permit tcp any host 207.186.55.63 eq www
 permit tcp any host 207.186.55.63 eq 443
 permit tcp any eq www host 207.186.55.63
 permit tcp any eq 443 host 207.186.55.63
 permit tcp any eq 771 host 207.186.55.63
 permit tcp any range 1900 1994 host 207.186.55.63
 permit tcp any host 207.186.55.63 range 1900 1994
 permit tcp any 65.59.112.0 0.0.0.255 eq www
 !
ip access-list extended INTERACTIVE
 remark Interactive 
 permit tcp any any eq telnet
 permit tcp any eq telnet any
 permit tcp any 207.186.54.0 0.0.1.255 range 50001 53100
 permit tcp any range 50001 53100 207.186.54.0 0.0.1.255
 permit tcp any range 9001 12100 207.186.54.0 0.0.1.255
 permit tcp any 207.186.54.0 0.0.1.255 range 9001 12100
 permit tcp any 207.186.54.0 0.0.1.255 eq telnet
 permit tcp any eq telnet 207.186.54.0 0.0.1.255
 !
ip access-list extended INTERNET_IN
 remark DHCP server offer
 permit udp any eq bootps any eq bootpc
 permit udp host 65.59.112.70 eq 5060 any
 permit udp host 65.59.112.70 range 1024 65535 host 63.233.40.134 range 1024 65535
 permit udp host 65.59.112.25 host 63.233.40.134 eq snmp
 permit udp host 65.59.112.60 eq 1967 host 63.233.40.134
 permit udp host 65.59.112.60 eq 20000 host 63.233.40.134
 permit esp any any
 permit icmp any any echo
 permit icmp any any echo-reply
 permit udp any any eq isakmp
 permit icmp any any unreachable
 permit icmp any any time-exceeded
 permit ip host 65.59.112.41 any
 permit icmp any any administratively-prohibited
 permit icmp any any packet-too-big
 permit udp any any eq non500-isakmp
 permit gre any any
 !
ip access-list extended NAT-TO-ABCD
 permit ip 172.30.0.0 0.0.255.255 207.186.41.0 0.0.0.15
 permit ip 10.0.0.0 0.255.255.255 192.110.68.0 0.0.0.255
 permit ip 172.30.0.0 0.0.255.255 192.110.68.0 0.0.0.255
 permit ip 10.0.0.0 0.255.255.255 207.186.41.0 0.0.0.15
 permit ip 10.0.0.0 0.255.255.255 207.186.55.0 0.0.0.255
 permit ip 172.30.0.0 0.0.255.255 207.186.55.0 0.0.0.255
 permit ip 10.3.1.0 0.0.0.255 207.186.41.0 0.0.0.15
 permit ip 10.3.1.0 0.0.0.255 192.110.68.0 0.0.0.255
 permit ip 10.27.23.0 0.0.0.255 any
 permit ip 10.0.0.0 0.255.255.255 192.224.101.0 0.0.0.255
 permit ip 172.30.0.0 0.0.255.255 192.224.101.0 0.0.0.255
 permit ip 10.3.1.0 0.0.0.255 192.224.101.0 0.0.0.255
 permit ip 172.30.3.0 0.0.0.255 192.110.68.0 0.0.0.255
 permit ip 172.30.3.0 0.0.0.255 192.224.101.0 0.0.0.255
 permit ip 172.30.3.0 0.0.0.255 host 207.186.55.63
 permit ip 172.30.4.0 0.0.0.255 192.110.68.0 0.0.0.255
 permit ip 172.30.4.0 0.0.0.255 192.224.101.0 0.0.0.255
 permit ip 172.30.4.0 0.0.0.255 host 207.186.55.63
 !
ip access-list extended NAT-TO-HOSTED
 permit ip 172.16.0.0 0.0.0.255 65.59.112.0 0.0.0.255
 permit ip 172.16.0.0 0.0.0.255 206.22.222.0 0.0.0.255
 !
ip access-list extended RTP
 remark ************ RTP QOS ACL *************
 permit udp any gt 1023 any gt 1023
 !
ip access-list extended STATIC-NAT-TO-ABCD
 permit ip host 10.42.0.110 host 207.186.55.63
 permit ip host 10.42.0.110 192.110.68.0 0.0.0.255
 permit ip host 10.42.0.110 192.224.101.0 0.0.0.255
 !
ip access-list extended TELNET
 deny   tcp any eq cmd any
 permit tcp any any eq telnet
 permit tcp any range 1001 1255 any
 permit tcp any any range 50001 53100
 permit tcp any range 9001 12100 any
 permit tcp any eq 771 any
 permit tcp any any range 9001 12100
 permit tcp any range 1900 1994 any
 permit tcp any eq telnet any
 permit tcp any any range 1900 1994
 permit tcp any any range 1001 1255
 permit tcp any range 50001 53100 any
 permit tcp any any eq 771
ip access-list extended VOICE
 remark ***ACL below here is specific for Hosted Voice/CC****
 deny   tcp any 65.59.112.0 0.0.0.255 eq www
 deny   tcp any 65.59.112.0 0.0.0.255 eq 2208
 deny   tcp any 206.22.222.0 0.0.0.255 eq www
 deny   tcp any 206.22.222.0 0.0.0.255 eq 2208
 permit udp any 65.59.112.0 0.0.0.255
 permit udp 65.59.112.0 0.0.0.255 any
 permit udp any 206.22.222.0 0.0.0.255
 permit udp 206.22.222.0 0.0.0.255 any
 remark ***ACL below here is for VoIP General****
 permit udp any any range 16384 32767
 permit tcp any any range 2000 2002
 permit tcp any range 2000 2002 any
 permit tcp any any eq 5060
 permit tcp any eq 5060 any
 permit udp any any eq 5060
 permit udp any eq 5060 any
 permit tcp any any eq 1720
 permit tcp any eq 1720 any
 permit udp any any eq 2427
 permit udp any eq 2427 any
 remark ***  CAD agent traffic  ***
 permit tcp host 207.185.52.15 any
 permit tcp any host 207.185.52.15
 permit tcp host 192.224.36.15 any
 permit tcp any host 192.224.36.15
 remark *** Cisco Unified Attendant console
 permit tcp any eq 1859 any
 permit tcp any any eq 1859
 permit tcp any eq 11859 any
 permit tcp any any eq 11859
 permit tcp any eq 1864 any
 permit tcp any any eq 1864
 permit tcp any eq 1863 any
 permit tcp any any eq 1863
 remark *** CTI Desktop traffic  ***
 permit tcp host 207.185.52.25 eq 11717 any
 permit tcp any host 207.185.52.25 eq 11717
 permit tcp host 192.224.36.25 eq 11717 any
 permit tcp any host 192.224.36.25 eq 1171
 remark *** Fidelus Attendant Console ***
 permit tcp any any eq 2748
 permit tcp any eq 2748 any
ip access-list extended wccp_61_lan
 deny   ip any 192.224.36.0 0.0.0.255
 deny   ip any 207.185.52.0 0.0.0.255
 deny   tcp host 199.194.157.7 host 207.186.55.63
 remark exclude Call Manger traffic from WCCP Redirection
 deny   tcp any host 199.194.208.65
 deny   tcp any host 192.110.68.15
 deny   tcp any any eq 2000
 deny   tcp any any eq telnet
 deny   tcp any eq telnet any
 deny   tcp any any eq 22
 deny   tcp any eq 22 any
 deny   tcp any any eq 161
 deny   tcp any eq 161 any
 deny   tcp any any eq 162
 deny   tcp any eq 162 any
 deny   tcp any any eq 123
 deny   tcp any eq 123 any
 deny   tcp any any eq bgp
 deny   tcp any eq bgp any
 deny   tcp any any eq tacacs
 deny   tcp any eq tacacs any
 deny   tcp any any eq 5060
 deny   tcp any eq 5060 any
 deny   tcp any any range 1718 1719
 deny   tcp any range 1718 1719 any
 deny   tcp any any eq 8443
 deny   tcp any any eq 5222
 deny   tcp any eq 5222 any
 deny   tcp any eq 8443 any
 permit tcp any any
ip access-list extended wccp_62_wan
 deny   ip 192.224.36.0 0.0.0.255 any
 deny   ip 207.185.52.0 0.0.0.255 any
 deny   tcp host 207.186.55.63 host 199.194.157.7
 remark exclude Call Manger traffic from WCCP Redirection
 deny   tcp host 199.194.208.65 any
 deny   tcp host 192.110.68.15 any
 deny   tcp any eq 2000 any
 deny   tcp any host 192.110.68.15
 deny   tcp any any eq telnet
 deny   tcp any eq telnet any
 deny   tcp any any eq 22
 deny   tcp any eq 22 any
 deny   tcp any any eq 161
 deny   tcp any eq 161 any
 deny   tcp any any eq 162
 deny   tcp any eq 162 any
 deny   tcp any any eq 123
 deny   tcp any eq 123 any
 deny   tcp any any eq bgp
 deny   tcp any eq bgp any
 deny   tcp any any eq tacacs
 deny   tcp any eq tacacs any
 deny   tcp any any eq 5060
 deny   tcp any eq 5060 any
 deny   tcp any any range 1718 1719
 deny   tcp any range 1718 1719 any
 deny   tcp any any eq 5222
 deny   tcp any eq 5222 any
 deny   tcp any any eq 8443
 deny   tcp any eq 8443 any
 permit tcp any any
!
ip prefix-list ADVERTISE_ARH_TO_MPLS seq 15 permit 10.27.23.0/24
ip prefix-list ADVERTISE_ARH_TO_MPLS seq 20 permit 10.42.0.0/24
ip prefix-list ADVERTISE_ARH_TO_MPLS seq 25 permit 172.17.0.1/32
ip prefix-list ADVERTISE_ARH_TO_MPLS seq 30 permit 172.16.0.0/24
ip prefix-list ADVERTISE_ARH_TO_MPLS seq 31 permit 172.30.3.0/24
ip prefix-list ADVERTISE_ARH_TO_MPLS seq 32 permit 172.30.4.0/24
ip prefix-list ADVERTISE_ARH_TO_MPLS seq 35 permit 10.3.1.0/24
!
ip prefix-list ADVERTISE_ABCD_TO_MPLS seq 5 permit 192.191.180.145/32
ip prefix-list ADVERTISE_ABCD_TO_MPLS seq 15 permit 199.194.157.0/27
ip prefix-list ADVERTISE_ABCD_TO_MPLS seq 20 permit 199.194.208.64/28
ip prefix-list ADVERTISE_ABCD_TO_MPLS seq 25 permit 198.249.107.192/27
!
ip prefix-list MPLS-BGP-INBOUND seq 1 deny 199.194.157.0/27
ip prefix-list MPLS-BGP-INBOUND seq 2 deny 198.249.107.192/27
ip prefix-list MPLS-BGP-INBOUND seq 5 deny 192.191.180.145/32
ip prefix-list MPLS-BGP-INBOUND seq 10 deny 199.194.208.64/28
ip prefix-list MPLS-BGP-INBOUND seq 15 deny 10.27.23.0/24
ip prefix-list MPLS-BGP-INBOUND seq 20 deny 10.42.0.0/24
ip prefix-list MPLS-BGP-INBOUND seq 25 deny 172.16.0.0/24
ip prefix-list MPLS-BGP-INBOUND seq 31 deny 172.30.3.0/24
ip prefix-list MPLS-BGP-INBOUND seq 32 deny 172.30.4.0/24
ip prefix-list MPLS-BGP-INBOUND seq 75 permit 0.0.0.0/0 le 32
kron occurrence DAILY-AUTO-SAVE at 1:00 recurring
 policy-list NIGHTLY-AUTO-SAVE
!
kron policy-list NIGHTLY-AUTO-SAVE
 cli write memory
!
no logging trap
access-list 1 permit any
access-list 50 permit 65.59.112.25
access-list 50 permit 198.249.84.65
access-list 50 permit 206.93.76.78
access-list 50 permit 192.110.68.11
access-list 50 permit 192.110.68.15
access-list 50 deny   any
access-list 50 permit 192.224.101.0 0.0.0.255
!
route-map BGP-TO-EIGRP permit 10
 set tag 50
!
route-map NAT-TO-ABCD deny 5
 match ip address STATIC-NAT-TO-ABCD
!
route-map NAT-TO-ABCD permit 7
 match ip address NAT-TO-ABCD
 match interface GigabitEthernet0/1
!
route-map NAT-TO-ADP deny 5
 match ip address STATIC-NAT-TO-ABCD
!
route-map MPLS-OUTBOUND permit 10
 match ip address prefix-list ADVERTISE_ABCD_TO_MPLS
 set community 65248:1
!
route-map MPLS-OUTBOUND permit 20
 match ip address prefix-list ADVERTISE_ARH_TO_MPLS
 set community 65000:1
!
route-map STATIC-NAT-TO-ABCD permit 10
 match ip address STATIC-NAT-TO-ABCD
!
route-map NAT-TO-HOSTED permit 10
 match ip address NAT-TO-HOSTED
 match interface GigabitEthernet0/1
!
route-map MPLS-INBOUND permit 10
 match ip address prefix-list MPLS-BGP-INBOUND
!
snmp-server group hvgroup v3 auth access 50
snmp-server community adp RO 50
snmp-server community adprw RW 50
snmp-server ifindex persist
snmp-server trap-source GigabitEthernet0/0.75
snmp-server packetsize 1024
snmp-server location Arrowhead Honda, Peoria AZ
snmp-server contact Dan Lowe
snmp-server chassis-id "Cisco 2851"
snmp-server enable traps snmp authentication linkdown linkup coldstart warmstart
snmp-server enable traps tty
snmp-server enable traps envmon
snmp-server enable traps entity-sensor threshold
snmp-server enable traps entity
snmp-server enable traps syslog
snmp-server enable traps dsp card-status
snmp-server enable traps voice poor-qov
snmp-server host 192.110.68.11 adptraps 
snmp-server host 192.110.68.15 adptraps 
tftp-server flash0:vg224-i6s-mz.151-4.M5.bin
!
control-plane
!
voice-port 0/1/0
!
voice-port 0/1/1
!
voice-port 0/1/2
!
voice-port 0/1/3
!
no ccm-manager fax protocol cisco
ccm-manager music-on-hold
!
mgcp fax t38 ecm
!
mgcp profile default
!
sccp local Loopback0
sccp ccm 207.185.52.2 identifier 1 priority 1 version 7.0 
sccp ccm 192.224.36.1 identifier 2 priority 2 version 7.0 
sccp ip precedence 3
sccp
!
sccp ccm group 1
 bind interface Loopback0
 associate ccm 1 priority 1
 associate ccm 2 priority 2
 associate profile 1 register AZPEORHON-XCODE
 registration retries 20
 registration timeout 30
 keepalive retries 10
 connect retries 30
 connect interval 30
 switchback method immediate
 switchback interval 15
!
dspfarm profile 1 transcode  
 codec g711ulaw
 codec g711alaw
 codec g729ar8
 codec g729abr8
 maximum sessions 10
 associate application SCCP
!
dial-peer voice 2 voip
 tone ringback alert-no-PI
 description USED FOR PAGING TO FXO From IP Phones
 modem passthrough nse codec g711ulaw
 incoming called-number .
 voice-class codec 1  
 voice-class h323 1
 dtmf-relay h245-alphanumeric
 fax rate disable
 no vad
!
dial-peer voice 999 pots
 description paging interface
 max-conn 1
 destination-pattern #2390[0-3]
 port 0/1/0
 forward-digits 2
!
gatekeeper
 shutdown
!
banner exec ^C
*****************************************************************




*****************************************************************
Client Name =               [[dealer name]]
Client City =               [[city]]
Client State =              [[state]]
Client CNumber =            [[client number]]
Client Contact =            [[contact]]
Client Phone Number =       [[phone]]
-----------------------------------------------------------------
          Router - Paging connected to FXO
-----------------------------------------------------------------
^C
banner login ^C
************************************************************
*  WARNING! WARNING! WARNING! WARNING! WARNING! WARNING!   *
************************************************************
* Access to and use of this device and/or other devices is *
* restricted to authorized users only. Unauthorized        *
* individuals attempting to access this device may be      *
* subject to prosecution.                                  *
*                                                          *
************************************************************
^C
!
line con 0
 exec-timeout 30 0
 logging synchronous
 transport preferred none
 transport output all
line aux 0
 session-timeout 10 
 no motd-banner
 no exec-banner
 exec-timeout 0 0
 logging synchronous
 modem InOut
 no exec
 transport preferred none
 transport input all
 transport output none
 flowcontrol hardware
line 2
 no activation-character
 no exec
 transport preferred none
 transport output pad telnet rlogin lapb-ta mop udptn v120 ssh
 stopbits 1
line vty 0 4
 exec-timeout 120 0
 privilege level 15
 logging synchronous
 length 0
 transport preferred none
 transport input all
 transport output all
line vty 5
 exec-timeout 120 0
 privilege level 15
 logging synchronous
 transport preferred none
 transport input telnet ssh
line vty 6 15
 privilege level 15
 logging synchronous
 transport preferred none
 transport input telnet ssh
!
scheduler allocate 20000 1000
ntp server 65.59.112.41 prefer
ntp server 199.165.76.11
!
end
'''
