#!/usr/bin/env python

import casperfpga, time, struct, sys, logging, socket, numpy

fabric_port= 4000         
mac_base= (2<<40) + (2<<32)
ip_base = 192*(2**24) + 168*(2**16) + 200*(2**8)

tx_core_name = 'onehundred_gbe'

fpgfile = 'test_vcu128_100g.fpg'
fpga=[]

def exit_fail():
    sys.exit()

def exit_clean():
    try:
        for f in fpgas: f.stop()
    except: pass
    sys.exit()

if __name__ == '__main__':

    fpga_address = sys.argv[1]


try:
    print('Connecting to server %s... '%(fpga_address)),
    fpga = casperfpga.CasperFpga(fpga_address, transport=casperfpga.TapcpTransport)
    time.sleep(1)

    print ('------------------------')
    print ('Reading FPGA fpg file...',
    fpga.get_system_information(fpgfile))
    print ('ok')

    fpga.write_int('packet_len',99999992-16)
    print ('Configuring transmitter core...')
    #Set IP address of snap and set arp-table

    gbe_tx = fpga.gbes[tx_core_name]
    gbe_tx.set_arp_table(mac_base+numpy.arange(256))
    gbe_tx.configure_core(mac_base+30,ip_base+30,fabric_port)
    print ('done')

    print ('Setting-up destination addresses...')
    fpga.write_int('dest_ip',ip_base+101)
    fpga.write_int('dest_port',fabric_port+1)
    print ('done')

    

#
except KeyboardInterrupt:
    exit_clean()
except Exception as inst:
    raise

exit_clean()

