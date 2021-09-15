from PyQt5 import QtCore, QtWidgets,QtGui, uic
from PyQt5.QtCore import *
from binance.client import Client
import time,os,sys,pythoncom,pyrebase
from datetime import datetime
import binance.exceptions
from wmi import WMI
from pushnotifier import PushNotifier as pn




apikeys = {}
with open('./bdata/apikeys') as file_object:
    for line in file_object:
        key = line.strip()
        value = file_object.readline().strip()
        apikeys[key] = value
pinfo = {}
with open('./bdata/pushnotifierinfo') as file_object:
    for line in file_object:
        key = line.strip()
        value = file_object.readline().strip()
        pinfo[key] = value
        
coinList = []
with open('./bdata/coinlist', 'r') as f:
    for line in f:
        coin = line.strip()
        coinList.append(coin)
        
pn = pn.PushNotifier(pinfo['username'],pinfo['password'],pinfo['packagename'],pinfo['papikey'])

dbconfig = {
    "apiKey": "",
    "authDomain": "",
    "databaseURL": "",
    "projectId": "",
    "storageBucket": "",
    "messagingSenderId": "",
    "appId": "",
    "measurementId": ""
}

class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainUi, self).__init__()
        uic.loadUi('./bdata/maingui.ui', self)
        self.setWindowIcon(QtGui.QIcon('./bdata/logo.ico'))
        self.label_49 = QtWidgets.QLabel(self)
        self.label_49.setGeometry(QtCore.QRect(30, 284, 370, 21))
        self.label_49.setObjectName("label_49")
        self.label_50 = QtWidgets.QLabel(self)
        self.label_50.setGeometry(QtCore.QRect(300, 472, 120, 21))
        self.label_50.setText("Powered by sametatila")
        self.ComboBox100.addItems(sorted(coinList))
        self.lineEdit100.setText("0.00000001")
        self.lineEdit100.returnPressed.connect(self.onPressed1)
        self.lineEdit101.setText("0.00000002")
        self.lineEdit101.returnPressed.connect(self.onPressed1)
        self.lineEdit102.setText("1")
        self.lineEdit102.returnPressed.connect(self.onPressed1)
        self.pushButton100.clicked.connect(self.threadingmainfunc1)
        self.pushButton101.clicked.connect(self.threadstop1)
        self.pushButton101.setEnabled(False)
        ############### BTC Eşleri : Bot 2
        self.ComboBox200.addItems(sorted(coinList))
        self.lineEdit200.setText("0.00000001")
        self.lineEdit200.returnPressed.connect(self.onPressed2)
        self.lineEdit201.setText("0.00000002")
        self.lineEdit201.returnPressed.connect(self.onPressed2)
        self.lineEdit202.setText("1")
        self.lineEdit202.returnPressed.connect(self.onPressed2)
        self.pushButton200.clicked.connect(self.threadingmainfunc2)
        self.pushButton201.clicked.connect(self.threadstop2)
        self.pushButton201.setEnabled(False)
        ############### BTC Eşleri : Bot 3
        self.ComboBox300.addItems(sorted(coinList))
        self.lineEdit300.setText("0.00000001")
        self.lineEdit300.returnPressed.connect(self.onPressed3)
        self.lineEdit301.setText("0.00000002")
        self.lineEdit301.returnPressed.connect(self.onPressed3)
        self.lineEdit302.setText("1")
        self.lineEdit302.returnPressed.connect(self.onPressed3)
        self.pushButton300.clicked.connect(self.threadingmainfunc3)
        self.pushButton301.clicked.connect(self.threadstop3)
        self.pushButton301.setEnabled(False)
        ################ Main Tab: Ayarlar ###########################
        self.lineEdit_40.setText(apikeys['apikey'])
        self.lineEdit_41.setText(apikeys['secretkey'])
        self.pushButton_40.clicked.connect(self.saveapi)
        self.pushButton_41.clicked.connect(self.updatecoinlist)
        self.lineEdit_43.setText(pinfo['username'])
        self.lineEdit_44.setText(pinfo['password'])
        self.lineEdit_45.setText(pinfo['packagename'])
        self.lineEdit_46.setText(pinfo['papikey'])
        self.lineEdit_47.setText(pinfo['deviceid'])
        self.pushButton_42.clicked.connect(self.savepushnotifier)
        self.show()

    def onPressed1(self):
        self.btcquantity2 = str(format(float(self.lineEdit100.text())*float(self.lineEdit102.text()),'.8f'))
        self.label111.setText("Kullanılacak BTC Miktarı: "+self.btcquantity2)
    
    def onPressed2(self):
        self.btcquantity2 = str(format(float(self.lineEdit200.text())*float(self.lineEdit202.text()),'.8f'))
        self.label211.setText("Kullanılacak BTC Miktarı: "+self.btcquantity2)
    
    def onPressed3(self):
        self.btcquantity3 = str(format(float(self.lineEdit300.text())*float(self.lineEdit302.text()),'.8f'))
        self.label311.setText("Kullanılacak BTC Miktarı: "+self.btcquantity3)
    
    def savepushnotifier(self):
        puser = self.lineEdit_43.text()
        ppasswrd = self.lineEdit_44.text()
        ppackage = self.lineEdit_45.text()
        papikey = self.lineEdit_46.text()
        pdevice = self.lineEdit_47.text()
        f = open( './bdata/pushnotifierinfo', 'w' )
        f.write("username\n"+str(puser)+"\npassword\n"+str(ppasswrd)+"\npackagename\n"+str(ppackage)+"\npapikey\n"+str(papikey)+"\ndeviceid\n"+str(pdevice))
        f.close()
        os.execl(sys.executable, sys.executable, *sys.argv)

    def saveapi(self):
        newapikey = self.lineEdit_40.text()
        newsecretkey = self.lineEdit_41.text()
        f = open( './bdata/apikeys', 'w' )
        f.write("apikey\n"+str(newapikey)+"\nsecretkey\n"+str(newsecretkey))
        f.close()
        os.execl(sys.executable, sys.executable, *sys.argv)
    
    def updatecoinlist(self):
        client = Client(apikeys["apikey"], apikeys["secretkey"])
        prices = client.get_all_tickers()
        coinList = []
        for price in prices:
            if price['symbol'][-3:] == 'BTC':
                coin = price['symbol']
                coinList.append(coin)
        with open('./bdata/coinlist', 'w') as f:
            for item in coinList:
                f.write("%s\n" % item)
        os.execl(sys.executable, sys.executable, *sys.argv)

    def threadingmainfunc1(self):
        self.thread = ThreadClass1(parent=None,index=0)
        self.thread.coinsymbol = self.ComboBox100.currentText()
        self.thread.buyprice = self.lineEdit100.text()
        self.thread.sellprice = self.lineEdit101.text()
        self.thread.buyquantity = self.lineEdit102.text()
        self.thread.start()
        self.pushButton100.setEnabled(False)
        self.pushButton101.setEnabled(True)
        self.label107.setText(" ")
        self.label104.setText("İşlem Başlatıldı!")
        self.thread.label104signal.connect(self.label104.setText)
        self.thread.label105signal.connect(self.label105.setText)
        self.thread.label106signal.connect(self.label106.setText)
        self.thread.label108signal.connect(self.label108.setText)
        self.thread.label109signal.connect(self.label109.setText)
        self.thread.label110signal.connect(self.label110.setText)
        self.thread.label_49signal.connect(self.label_49.setText)
        self.thread.stopsignal1.connect(self.threadstop1)
        
    def threadstop1(self):
        self.label104.setText(" ")
        self.label107.setText("İşlem Durduruldu!")
        self.pushButton100.setEnabled(True)
        self.pushButton101.setEnabled(False)
        self.thread.stop()
    
    def threadingmainfunc2(self):
        self.thread = ThreadClass2(parent=None,index=0)
        self.thread.coinsymbol = self.ComboBox200.currentText()
        self.thread.buyprice = self.lineEdit200.text()
        self.thread.sellprice = self.lineEdit201.text()
        self.thread.buyquantity = self.lineEdit202.text()
        self.thread.start()
        self.pushButton200.setEnabled(False)
        self.pushButton201.setEnabled(True)
        self.label207.setText(" ")
        self.label204.setText("İşlem Başlatıldı!")
        self.thread.label204signal.connect(self.label204.setText)
        self.thread.label205signal.connect(self.label205.setText)
        self.thread.label206signal.connect(self.label206.setText)
        self.thread.label208signal.connect(self.label208.setText)
        self.thread.label209signal.connect(self.label209.setText)
        self.thread.label210signal.connect(self.label210.setText)
        self.thread.label_49signal.connect(self.label_49.setText)
        self.thread.stopsignal2.connect(self.threadstop2)
        
    def threadstop2(self):
        self.label204.setText(" ")
        self.label207.setText("İşlem Durduruldu!")
        self.pushButton200.setEnabled(True)
        self.pushButton201.setEnabled(False)
        self.thread.stop()
        
    def threadingmainfunc3(self):
        self.thread = ThreadClass3(parent=None,index=0)
        self.thread.coinsymbol = self.ComboBox300.currentText()
        self.thread.buyprice = self.lineEdit300.text()
        self.thread.sellprice = self.lineEdit301.text()
        self.thread.buyquantity = self.lineEdit302.text()
        self.thread.start()
        self.pushButton300.setEnabled(False)
        self.pushButton301.setEnabled(True)
        self.label307.setText(" ")
        self.label304.setText("İşlem Başlatıldı!")
        self.thread.label304signal.connect(self.label304.setText)
        self.thread.label305signal.connect(self.label305.setText)
        self.thread.label306signal.connect(self.label306.setText)
        self.thread.label308signal.connect(self.label308.setText)
        self.thread.label309signal.connect(self.label309.setText)
        self.thread.label310signal.connect(self.label310.setText)
        self.thread.label_49signal.connect(self.label_49.setText)
        self.thread.stopsignal3.connect(self.threadstop3)
    
    def threadstop3(self):
        self.label304.setText(" ")
        self.label307.setText("İşlem Durduruldu!")
        self.pushButton300.setEnabled(True)
        self.pushButton301.setEnabled(False)
        self.thread.stop()
       
class ThreadClass1(QtCore.QThread):
    label104signal = QtCore.pyqtSignal(str)
    label105signal = QtCore.pyqtSignal(str)
    label106signal = QtCore.pyqtSignal(str)
    label108signal = QtCore.pyqtSignal(str)
    label109signal = QtCore.pyqtSignal(str)
    label110signal = QtCore.pyqtSignal(str)
    label_49signal = QtCore.pyqtSignal(str)
    stopsignal1 = QtCore.pyqtSignal(int)
    

    def __init__(self, parent: None,index=0):
        super(ThreadClass1, self).__init__(parent)
        self.index = index
        self.is_running = True
        
    def run(self):
        while True:
            try:
                try:
                    pythoncom.CoInitialize()
                    deviceuuid = WMI().Win32_ComputerSystemProduct()[0].UUID
                    firebase = pyrebase.initialize_app(dbconfig)
                    db = firebase.database()
                    with open('./bdata/loginemail', 'r') as emailfile:
                        email = [email for email in emailfile][0]
                    fromfb = [fromfbu.val() for fromfbu in db.child(email.split("@")[0]).get().each()][0]
                    if fromfb == deviceuuid:
                        pass
                    else:
                        self.label_49signal.emit("Başka bir cihazda oturum açıldı!")
                        self.stopsignal1.emit(1)
                except:
                    pass
                try:
                    client = Client(apikeys['apikey'], apikeys['secretkey'])
                    getServerTime = client.get_server_time()
                    serverTime = str(datetime.fromtimestamp(getServerTime['serverTime']/1000))
                    os.system("time "+serverTime[11:22])
                    os.system("date "+serverTime[5:10]+"-"+serverTime[0:4])
                except:
                    pass
                
                for i in range(10):
                    try:
                        client = Client(apikeys['apikey'], apikeys['secretkey'])
                        getServerTime = client.get_server_time()
                        serverTime = str(datetime.fromtimestamp(getServerTime['serverTime']/1000))
                        now = datetime.now()
                        getSystemTime = datetime.timestamp(now)
                        systemTime = str(datetime.fromtimestamp(getSystemTime))[11:23]
                        coinsymbol = self.coinsymbol
                        buyprice = self.buyprice
                        sellprice = self.sellprice
                        buyquantity = self.buyquantity
                        
                        def bnbprice():
                            bnbavgprice = client.get_avg_price(symbol='BNBBTC')
                            bnbp = float(format(float(bnbavgprice['price']),'.6f'))+0.000010
                            return bnbp

                        def bnbbalance():
                            bnbbalance = client.get_asset_balance(asset='BNB')
                            bnbb = float(bnbbalance['free'])
                            return bnbb

                        def allballance():
                            sum_btc = 0.0
                            balances = client.get_account()
                            for _balance in balances["balances"]:
                                asset = _balance["asset"]
                                if float(_balance["free"]) != 0.0 or float(_balance["locked"]) != 0.0:
                                    try:
                                        btc_quantity = float(_balance["free"]) + float(_balance["locked"])
                                        if asset == "BTC":
                                            sum_btc += btc_quantity
                                        else:
                                            _price = client.get_symbol_ticker(symbol=asset + "BTC")
                                            sum_btc += btc_quantity * float(_price["price"])
                                    except:
                                        pass
                            sum_btc = float(format(sum_btc,'.8f'))
                            return sum_btc

                        def buyorder():
                            orderbuy = client.order_limit_buy(
                                symbol=coinsymbol,
                                quantity=buyquantity,
                                price=buyprice)
                        #BNB bakiye için alış
                        def buyorderbnb():
                            orderbuy = client.order_limit_buy(
                                symbol='BNBBTC',
                                quantity=totalassetballance*0.15*13,
                                price=bnbbuyprice)
                        #Sell order ayarı
                        def sellorder():
                            ordersell = client.order_limit_sell(
                                symbol=coinsymbol,
                                quantity=sellquantity,
                                price=sellprice)
                            
                        totalassetballance = allballance()
                        bnbbuyprice = bnbprice()
                        bnbassetbalance = bnbbalance()
                        coinbalance = client.get_asset_balance(asset=coinsymbol[:-3])
                        sellquantity = float(coinbalance['free'])+float(coinbalance['locked'])
                        openorders = client.get_open_orders(symbol=coinsymbol)
                        self.label105signal.emit("BTC Bakiyesi: "+str(totalassetballance)+" | BNB Bakiyesi: "+str(bnbassetbalance))
                        self.label106signal.emit("Sunucu Saati: "+str(serverTime[11:23])+" | Sistem Saati: "+str(systemTime))
                        if len(openorders) == 0 and sellquantity == 0:
                            buyorder()
                            self.label108signal.emit(str(systemTime)+" | "+str(coinsymbol)+" Alış Emri Verildi!")
                            pn.send_text(str(coinsymbol)+" Alış Emri Verildi!", silent=False, devices=[pinfo['deviceid']])
                        elif len(openorders) == 0 and sellquantity > 0:
                            sellorder()
                            self.label109signal.emit(str(systemTime)+" | "+str(coinsymbol)+" Satış Emri Verildi!")
                            pn.send_text(str(coinsymbol)+' Satış Emri Verildi!', silent=False, devices=[pinfo['deviceid']])
                        if bnbassetbalance < 0.005:
                            buyorderbnb()
                            self.label110signal.emit("BNB Takviyesi Yapıldı!")
                            pn.send_text('"BNB Takviyesi Yapıldı!"', silent=False, devices=[pinfo['deviceid']])
                    except binance.exceptions.BinanceAPIException as e:
                        if str(e) == "APIError(code=-1021): Timestamp for this request was 1000ms ahead of the server's time.":
                            self.label104signal.emit("Sistem saati sorunu! Saatinizi senkronize edin!")
                        else:
                            pass
                    time.sleep(45)
            except:
                pass
            
    def stop(self):
        self.is_running = False
        self.terminate()

class ThreadClass2(QtCore.QThread):
    label204signal = QtCore.pyqtSignal(str)
    label205signal = QtCore.pyqtSignal(str)
    label206signal = QtCore.pyqtSignal(str)
    label208signal = QtCore.pyqtSignal(str)
    label209signal = QtCore.pyqtSignal(str)
    label210signal = QtCore.pyqtSignal(str)
    label_49signal = QtCore.pyqtSignal(str)
    stopsignal2 = QtCore.pyqtSignal(int)

    def __init__(self, parent: None,index=0):
        super(ThreadClass2, self).__init__(parent)
        self.index = index
        self.is_running = True
        
    def run(self):
        while True:
            try:
                try:
                    pythoncom.CoInitialize()
                    deviceuuid = WMI().Win32_ComputerSystemProduct()[0].UUID
                    firebase = pyrebase.initialize_app(dbconfig)
                    db = firebase.database()
                    with open('./bdata/loginemail', 'r') as emailfile:
                        email = [email for email in emailfile][0]
                    fromfb = [fromfbu.val() for fromfbu in db.child(email.split("@")[0]).get().each()][0]
                    if fromfb == deviceuuid:
                        pass
                    else:
                        self.label_49signal.emit("Başka bir cihazda oturum açıldı!")
                        self.stopsignal2.emit(1)
                except:
                    pass
                try:
                    client = Client(apikeys['apikey'], apikeys['secretkey'])
                    getServerTime = client.get_server_time()
                    serverTime = str(datetime.fromtimestamp(getServerTime['serverTime']/1000))
                    os.system("time "+serverTime[11:22])
                    os.system("date "+serverTime[5:10]+"-"+serverTime[0:4])
                except:
                    pass
                
                for i in range(10):
                    try:
                        client = Client(apikeys['apikey'], apikeys['secretkey'])
                        getServerTime = client.get_server_time()
                        serverTime = str(datetime.fromtimestamp(getServerTime['serverTime']/1000))
                        now = datetime.now()
                        getSystemTime = datetime.timestamp(now)
                        systemTime = str(datetime.fromtimestamp(getSystemTime))[11:23]
                        coinsymbol = self.coinsymbol
                        buyprice = self.buyprice
                        sellprice = self.sellprice
                        buyquantity = self.buyquantity
                        
                        def bnbprice():
                            bnbavgprice = client.get_avg_price(symbol='BNBBTC')
                            bnbp = float(format(float(bnbavgprice['price']),'.6f'))+0.000010
                            return bnbp

                        def bnbbalance():
                            bnbbalance = client.get_asset_balance(asset='BNB')
                            bnbb = float(bnbbalance['free'])
                            return bnbb

                        def allballance():
                            sum_btc = 0.0
                            balances = client.get_account()
                            for _balance in balances["balances"]:
                                asset = _balance["asset"]
                                if float(_balance["free"]) != 0.0 or float(_balance["locked"]) != 0.0:
                                    try:
                                        btc_quantity = float(_balance["free"]) + float(_balance["locked"])
                                        if asset == "BTC":
                                            sum_btc += btc_quantity
                                        else:
                                            _price = client.get_symbol_ticker(symbol=asset + "BTC")
                                            sum_btc += btc_quantity * float(_price["price"])
                                    except:
                                        pass
                            sum_btc = float(format(sum_btc,'.8f'))
                            return sum_btc

                        def buyorder():
                            orderbuy = client.order_limit_buy(
                                symbol=coinsymbol,
                                quantity=buyquantity,
                                price=buyprice)
                        #BNB bakiye için alış
                        def buyorderbnb():
                            orderbuy = client.order_limit_buy(
                                symbol='BNBBTC',
                                quantity=totalassetballance*0.15*13,
                                price=bnbbuyprice)
                        #Sell order ayarı
                        def sellorder():
                            ordersell = client.order_limit_sell(
                                symbol=coinsymbol,
                                quantity=sellquantity,
                                price=sellprice)
                            
                        totalassetballance = allballance()
                        bnbbuyprice = bnbprice()
                        bnbassetbalance = bnbbalance()
                        coinbalance = client.get_asset_balance(asset=coinsymbol[:-3])
                        sellquantity = float(coinbalance['free'])+float(coinbalance['locked'])
                        openorders = client.get_open_orders(symbol=coinsymbol)
                        self.label205signal.emit("BTC Bakiyesi: "+str(totalassetballance)+" | BNB Bakiyesi: "+str(bnbassetbalance))
                        self.label206signal.emit("Sunucu Saati: "+str(serverTime[11:23])+" | Sistem Saati: "+str(systemTime))
                        if len(openorders) == 0 and sellquantity == 0:
                            buyorder()
                            self.label208signal.emit(str(systemTime)+" | "+str(coinsymbol)+" Alış Emri Verildi!")
                            pn.send_text(str(coinsymbol)+" Alış Emri Verildi!", silent=False, devices=[pinfo['deviceid']])
                        elif len(openorders) == 0 and sellquantity > 0:
                            sellorder()
                            self.label209signal.emit(str(systemTime)+" | "+str(coinsymbol)+" Satış Emri Verildi!")
                            pn.send_text(str(coinsymbol)+' Satış Emri Verildi!', silent=False, devices=[pinfo['deviceid']])
                        if bnbassetbalance < 0.005:
                            buyorderbnb()
                            self.label210signal.emit("BNB Takviyesi Yapıldı!")
                            pn.send_text('"BNB Takviyesi Yapıldı!"', silent=False, devices=[pinfo['deviceid']])
                    except binance.exceptions.BinanceAPIException as e:
                        if str(e) == "APIError(code=-1021): Timestamp for this request was 1000ms ahead of the server's time.":
                            self.label204signal.emit("Sistem saati sorunu! Saatinizi senkronize edin!")
                        else:
                            pass
                    time.sleep(45)
            except:
                pass
            
    def stop(self):
        self.is_running = False
        self.terminate()

class ThreadClass3(QtCore.QThread):
    label304signal = QtCore.pyqtSignal(str)
    label305signal = QtCore.pyqtSignal(str)
    label306signal = QtCore.pyqtSignal(str)
    label308signal = QtCore.pyqtSignal(str)
    label309signal = QtCore.pyqtSignal(str)
    label310signal = QtCore.pyqtSignal(str)
    label_49signal = QtCore.pyqtSignal(str)
    stopsignal3 = QtCore.pyqtSignal(int)

    def __init__(self, parent: None,index=0):
        super(ThreadClass3, self).__init__(parent)
        self.index = index
        self.is_running = True
        
    def run(self):
        while True:
            try:
                try:
                    pythoncom.CoInitialize()
                    deviceuuid = WMI().Win32_ComputerSystemProduct()[0].UUID
                    print(deviceuuid)
                    firebase = pyrebase.initialize_app(dbconfig)
                    db = firebase.database()
                    with open('./bdata/loginemail', 'r') as emailfile:
                        email = [email for email in emailfile][0]
                    fromfb = [fromfbu.val() for fromfbu in db.child(email.split("@")[0]).get().each()][0]
                    if fromfb == deviceuuid:
                        pass
                    else:
                        self.label_49signal.emit("Başka bir cihazda oturum açıldı!")
                        self.stopsignal3.emit(1)
                except:
                    pass
                try:
                    client = Client(apikeys['apikey'], apikeys['secretkey'])
                    getServerTime = client.get_server_time()
                    serverTime = str(datetime.fromtimestamp(getServerTime['serverTime']/1000))
                    os.system("time "+serverTime[11:22])
                    os.system("date "+serverTime[5:10]+"-"+serverTime[0:4])
                except:
                    pass
                
                for i in range(10):
                    try:
                        client = Client(apikeys['apikey'], apikeys['secretkey'])
                        getServerTime = client.get_server_time()
                        serverTime = str(datetime.fromtimestamp(getServerTime['serverTime']/1000))
                        now = datetime.now()
                        getSystemTime = datetime.timestamp(now)
                        systemTime = str(datetime.fromtimestamp(getSystemTime))[11:23]
                        coinsymbol = self.coinsymbol
                        buyprice = self.buyprice
                        sellprice = self.sellprice
                        buyquantity = self.buyquantity
                        
                        def bnbprice():
                            bnbavgprice = client.get_avg_price(symbol='BNBBTC')
                            bnbp = float(format(float(bnbavgprice['price']),'.6f'))+0.000010
                            return bnbp

                        def bnbbalance():
                            bnbbalance = client.get_asset_balance(asset='BNB')
                            bnbb = float(bnbbalance['free'])
                            return bnbb

                        def allballance():
                            sum_btc = 0.0
                            balances = client.get_account()
                            for _balance in balances["balances"]:
                                asset = _balance["asset"]
                                if float(_balance["free"]) != 0.0 or float(_balance["locked"]) != 0.0:
                                    try:
                                        btc_quantity = float(_balance["free"]) + float(_balance["locked"])
                                        if asset == "BTC":
                                            sum_btc += btc_quantity
                                        else:
                                            _price = client.get_symbol_ticker(symbol=asset + "BTC")
                                            sum_btc += btc_quantity * float(_price["price"])
                                    except:
                                        pass
                            sum_btc = float(format(sum_btc,'.8f'))
                            return sum_btc

                        def buyorder():
                            orderbuy = client.order_limit_buy(
                                symbol=coinsymbol,
                                quantity=buyquantity,
                                price=buyprice)
                        #BNB bakiye için alış
                        def buyorderbnb():
                            orderbuy = client.order_limit_buy(
                                symbol='BNBBTC',
                                quantity=totalassetballance*0.15*13,
                                price=bnbbuyprice)
                        #Sell order ayarı
                        def sellorder():
                            ordersell = client.order_limit_sell(
                                symbol=coinsymbol,
                                quantity=sellquantity,
                                price=sellprice)
                            
                        totalassetballance = allballance()
                        bnbbuyprice = bnbprice()
                        bnbassetbalance = bnbbalance()
                        coinbalance = client.get_asset_balance(asset=coinsymbol[:-3])
                        sellquantity = float(coinbalance['free'])+float(coinbalance['locked'])
                        openorders = client.get_open_orders(symbol=coinsymbol)
                        self.label305signal.emit("BTC Bakiyesi: "+str(totalassetballance)+" | BNB Bakiyesi: "+str(bnbassetbalance))
                        self.label306signal.emit("Sunucu Saati: "+str(serverTime[11:23])+" | Sistem Saati: "+str(systemTime))
                        if len(openorders) == 0 and sellquantity == 0:
                            buyorder()
                            self.label308signal.emit(str(systemTime)+" | "+str(coinsymbol)+" Alış Emri Verildi!")
                            pn.send_text(str(coinsymbol)+" Alış Emri Verildi!", silent=False, devices=[pinfo['deviceid']])
                            print("Alış Emri verildi1")
                        elif len(openorders) == 0 and sellquantity > 0:
                            sellorder()
                            self.label309signal.emit(str(systemTime)+" | "+str(coinsymbol)+" Satış Emri Verildi!")
                            pn.send_text(str(coinsymbol)+' Satış Emri Verildi!', silent=False, devices=[pinfo['deviceid']])
                        if bnbassetbalance < 0.005:
                            buyorderbnb()
                            self.label310signal.emit("BNB Takviyesi Yapıldı!")
                            pn.send_text('"BNB Takviyesi Yapıldı!"', silent=False, devices=[pinfo['deviceid']])
                    except binance.exceptions.BinanceAPIException as e:
                        if str(e) == "APIError(code=-1021): Timestamp for this request was 1000ms ahead of the server's time.":
                            self.label304signal.emit("Sistem saati sorunu! Saatinizi senkronize edin!")
                        else:
                            pass
                    time.sleep(45)
            except:
                pass
            
    def stop(self):
        self.is_running = False
        self.terminate()
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainUi()
    sys.exit(app.exec_())
