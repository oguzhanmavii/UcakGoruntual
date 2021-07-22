from dronekit import connect,VehicleMode,Command,Vehicle,LocationGlobalRelative

import  time

from  pymavlink import  mavutil

print("Bağlandı..")
baglanti_adresi="tcp:127.0.0.1:5762"
ucak= connect(baglanti_adresi,wait_ready=True,timeout=100)


def arm_et():
    while ucak.is_armable==False:
        print("Arm olamıyor !")
        time.sleep(1)
    ucak.mode = VehicleMode("GUIDED")
    while ucak.mode == 'GUIDED':
        print("GUIDED moda geçiliyor..")
        time.sleep(1)
    print("GUIDED moda geçildi.")
    ucak.armed=True
    while ucak.armed is False:
        print("Arm için bekleniyor..")
        time.sleep(1)
    print("Arm oldu.")

def kalkis(kalkisAcisi,irtifa):
    kalkis_komutu= Command(0,0,0,3,mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,0,0,kalkisAcisi,0,0,0,0,0,irtifa)
    print("Kalkış komutu oluşturuldu")
    return  kalkis_komutu

def hedefNoktayaGidildi(enlem,boylam,irtifa):
    komut_git= Command(0,0,0,3,mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,0,0,0,0,0,0,enlem,boylam,irtifa)
    print("Hedef Noktaya gidiliyor..")
    return  komut_git

def goruntuTespiti(mesafe,goruntuAl): #girilen mesafe aralıklarında görüntü almaya yarıyor..
    goruntu_Al= Command(0,0,0,3,mavutil.mavlink.MAV_CMD_DO_SET_CAM_TRIGG_DIST,0,0,mesafe,0,goruntuAl,0,0,0,0)
    print("Görüntü alma işlemi yapılıyor..")
    return goruntu_Al

def inis(enlem, boylam):
    komut_inis = Command(0, 0, 0, 3, mavutil.mavlink.MAV_CMD_NAV_LAND, 0, 0, 0, 0, 0, 0, enlem, boylam, 0)
    print("İniş için hazırlanıyor..")
    return komut_inis

komut= ucak.commands
komut.download()""
komut.wait_ready()
komut.clear()


komut1=kalkis(15,25)
komut2=hedefNoktayaGidildi(39.9039341,41.23604,20)
komut3=goruntuTespiti(115,1) ## burada 115 m aralıkla görüntü alıyor
komut4=hedefNoktayaGidildi(39.9049876,41.2362438,20)
komut5=inis(39.9049629,41.2372765)


komut.add(komut1)
komut.add(komut2)
komut.add(komut3)
komut.add(komut4)
komut.add(komut5)

ucak.flush()
ucak.mode=VehicleMode("AUTO")
arm_et()

ucak.mode=VehicleMode("AUTO")