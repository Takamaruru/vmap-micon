from bluetooth import BLE
import struct
import time
import ubluetooth

class BLEPeripheral:
    def __init__(self, name="XIAO-BLE"):
        self.ble = ubluetooth.BLE()
        self.ble.active(True)
        self.ble.irq(self.ble_irq)
        self.register_services()
        self.advertise(name)
        self.conn_handle = None
        print("✅ BLEペリフェラルとして広告開始")

    def advertise(self, name="XIAO-BLE"):
        self.ble.gap_advertise(100, adv_data=self.advertise_payload(name=name))

    def advertise_payload(self, name=None):
        payload = bytearray()
        payload += struct.pack("BB", len(name) + 1, 0x09)
        payload += name.encode()
        return payload

    def register_services(self):
        # Nordic UART Service UUIDs
        UART_UUID = ubluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
        UART_TX = (
            ubluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"),
            ubluetooth.FLAG_NOTIFY,
        )
        UART_RX = (
            ubluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
            ubluetooth.FLAG_WRITE,
        )
        UART_SERVICE = (UART_UUID, (UART_TX, UART_RX,))
        SERVICES = (UART_SERVICE,)

        ((self.tx_handle, self.rx_handle),) = self.ble.gatts_register_services(SERVICES)

    def ble_irq(self, event, data):
        if event == 1:  # central connected
            conn_handle, _, _ = data
            print("🔗 接続されました")
            self.conn_handle = conn_handle

        elif event == 2:  # central disconnected
            conn_handle, _, _ = data
            print("❌ 切断されました")
            self.conn_handle = None
            self.advertise()  # 再アドバタイズ

        elif event == 3:  # write
            conn_handle, attr_handle = data
            msg = self.ble.gatts_read(attr_handle)
            decoded = msg.decode().strip()
            print("📥 受信:", decoded)

            # 💡 ここでコマンドに応じた動作を追加できる
            if decoded == "ping":
                self.send("pong")
            elif decoded.startswith("echo "):
                response = decoded[5:]
                self.send(f"echoed: {response}")
            else:
                self.send("🤖 未知のコマンド")
                
            if (decoded == "右"):
                pass
            elif (decoded == "左"):
                pass

    def send(self, data):
        if self.conn_handle is not None:
            self.ble.gatts_notify(self.conn_handle, self.tx_handle, data)

# 実行
ble_uart = BLEPeripheral()

try:
    while True:
        ble_uart.send("Hello from ESP32")
        print("...")
        time.sleep(1)
except KeyboardInterrupt:
    print("🛑 プログラム停止")