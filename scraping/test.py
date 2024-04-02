import websocket
import json
 
def on_message(ws, message):
    print(message)
 
def on_error(ws, error):
    print(error)
 
def on_close(ws):
    print("### closed ###")
 
def on_open(ws):

    ws.send(json.dumps({
        "type": "hello",
        "apikey": "YOUR_API_KEY",
        "subscribe_data_type": ["trade"],
        "subscribe_filter_symbol_id": [ "BITSTAMP_SPOT_BTC_USD$", "BITFINEX_SPOT_BTC_USD$" ]
    }))
 
ws = websocket.WebSocketApp("wss://ws.coinapi.io/v1",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
ws.on_open = on_open
ws.run_forever()