# pylint:disable=global-statement
from websocket import WebSocket
from fn_reflection.json import extend_dumps

# サーバーの状態に関わらずひたすらデータをプッシュするクライアント
# コネクション接続に失敗したらデータをプッシュしない
# BrokenPipeになったら接続を切って再接続(データロストは許容する)
class UDPLikeWebSocketClient:
    def __init__(self, url) -> None:
        self.ws = WebSocket()
        self.url = url

    def try_to_connect(self):
        try:
            self.ws.connect(url=self.url)
        except ConnectionRefusedError:
            pass

    def try_to_send(self, d):
        try:
            self.ws.send(extend_dumps(d))
        except BrokenPipeError:
            self.ws.close()


    def silent_send(self, channel, msg):
        if not self.ws.connected:
            self.try_to_connect()
        if not self.ws.connected:
            return
        self.try_to_send(dict(msg=msg, channel=channel))
        