from threading import Lock
from flask import Flask, render_template, session, request, jsonify, url_for
from flask_socketio import SocketIO, emit, disconnect  
import math
import time
import random     
import serial

async_mode = None

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock() 

ser = serial.Serial("/dev/ttyACM0", 9600)
ser.baudrate=9600

read_ser = ser.readline()

def background_thread(args):
    count = 0  
    dataCounter = 0 
    dataList = []            
    while True:
        if args:
          A = dict(args).get('A')
          dbV = dict(args).get('btn_value')
        else:
          A = 0
          dbV = 'nic'
          
        dbV = dict(args).get('btn_value')  
        print(args)  
        socketio.sleep(2)
        count += 1
        
        print(float(ser.readline()))
        recCount=0
        if dbV == 1:
          recCount = dict(args).get('receive_count',0) + 1
          args['receive_count'] = recCount
          dataDict = {
            "x": recCount,
            "y": float(ser.readline())}
          dataList.append(dataDict)
          socketio.emit('my_response',
                  {'data': float(ser.readline()), 'count': recCount},
                  namespace='/test')  

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)
    
@socketio.on('my_event', namespace='/test')
def test_message(message):   
    session['receive_count'] = session.get('receive_count', 0) + 1 
    session['A'] = message['value']
    #print("TOTO je hodnota ktoru by som mal poslať", message['value'])
    #ser.write((str)(2.5))
    ser.write(str(message['value']).encode())
    emit('my_response',
        {'data': message['value'], 'count': session['receive_count']})

@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()

@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread, args=session._get_current_object())
   # emit('my_response', {'data': 'Connected', 'count': 0})

@socketio.on('click_eventStart', namespace='/test')
def db_message(message):   
    session['btn_value'] = 1
    #print(session['click_eventStart'])
    #print(session)

@socketio.on('click_eventStop', namespace='/test')
def db_message(message):   
    session['btn_value'] = 0
    #print(session['click_eventStop'])
    #print(session)

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)