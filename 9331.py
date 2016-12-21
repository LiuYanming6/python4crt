
import struct

global DOWNLOAD_PATH, FIRMWARE_PATH, NEXFI_STD, NEXFI_STD_PATH, IP_1_3, IP_4, PC_IP

###############################################
PC_IP = '192.168.1.222' 			# 电脑的ip
IP_1_3 = '192.168.102.'
IP_4 = 9						# 板子起始ip
FIRMWARE = 'firmware.bin'			# 固件名
NEXFI_STD = "nexfi-std-2.3.tar.gz"	# 程序名
###############################################

DOWNLOAD_PATH='http://%s/automate/' % PC_IP
FIRMWARE_PATH='%s/%s' % (DOWNLOAD_PATH, FIRMWARE)
NEXFI_STD_PATH='%s/%s' % (DOWNLOAD_PATH, NEXFI_STD)

# equel to printf "\xdd\xdd\xdd\xdd\xdd\xdd" | dd conv=notrunc of=breed.cat.bin bs=1 seek=$((0x1fc00))
def createBreed():
	mac = crt.Dialog.Prompt("Enter mac:","mac addr", "", False)
	b=b''	#定义一个buffer，放6字节的mac地址
	for i in range(0, len(mac), 2):
	    byte_dat = struct.pack('B', int(mac[i: i + 2], 16))
	    b = b + byte_dat

	f = open("breed.bin", "r+b")
	f.seek(0x1fc00)
	f.write(b)
	f.close()

def comBreed():
	#Network started on eth0
	createBreed()
	crt.Screen.WaitForString('Please press Enter to activate this console')
	crt.Screen.Send("\r")
	crt.Screen.Send("reboot\r")
	crt.Screen.WaitForString("Hit any key to stop autoboot:")
	crt.Screen.Send("\r")
	# crt.Screen.Send('setenv ipaddr 192.168.1.111\r')
	crt.Screen.WaitForString("ar7240>")
	crt.Screen.Send('setenv serverip %s\r' % PC_IP)
	crt.Screen.WaitForString("ar7240>")
	crt.Screen.Send("tftp 0x80060000 breed.bin\r") 
	crt.Screen.WaitForString("ar7240>")
	crt.Screen.Send("erase 0x9f000000 +0x20000\r") 
	crt.Screen.WaitForString("ar7240>")
	crt.Screen.Send("cp.b 0x80060000 0x9f000000 0x20000\r") 
	crt.Screen.WaitForString("ar7240>")
	crt.Screen.Send("reset\r>")

### after 
def comBreedTo9331():
	crt.Screen.WaitForString("Press any key to interrupt autoboot")
	crt.Screen.Send("\r")
	crt.Screen.WaitForString("breed>")
	crt.Screen.Send('wget %s\r' % FIRMWARE_PATH)
	crt.Screen.WaitForString("breed>")
	crt.Screen.Send('flash erase 0x20000 0x7e0000\r')
	crt.Screen.WaitForString("breed>")
	crt.Screen.Send("flash write 0x20000 0x80000000 0x660004\r")
	crt.Screen.WaitForString("breed>")
	crt.Screen.Send("reset\r>")


def comNexfiStd():
	global FILE, IP_1_3, IP_4
	
	crt.Screen.WaitForString("Please press Enter to activate")
	crt.Sleep(100000)
	crt.Screen.Send('\r')
	crt.Screen.Send('ifconfig br-lan 192.168.1.111 netmask 255.255.255.0\r')
	crt.Screen.WaitForString("root@OpenWrt")
	crt.Screen.Send('cd /root/\r')
	crt.Screen.WaitForString("root@OpenWrt")
	crt.Screen.Send("wget -c %s\r" % NEXFI_STD_PATH)
	crt.Screen.WaitForString("root@OpenWrt")
	crt.Screen.Send("tar -zxvf %s\r" %NEXFI_STD)
	crt.Screen.WaitForString("root@OpenWrt")
	crt.Screen.Send("sed -i 's/192.168.102.XX/%s%d/' config/netconfig\r" % (IP_1_3,IP_4))
	crt.Screen.WaitForString("root@OpenWrt")
	crt.Screen.Send("./install.sh\r")
	crt.Screen.Send('\r')
	crt.Screen.WaitForString('Starting kernel at 0x80060000')
	crt.Dialog.MessageBox("ok换一台板子，插点后快速点击该按钮")
	IP_4 = IP_4+1


def main():

	crt.Screen.Synchronous = True
	while True:
		comBreed()
		comBreedTo9331()
		comNexfiStd()


	crt.Screen.Synchronous = False

#############main############
main()
