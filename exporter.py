from urllib import response
from flask import Flask, request
import re
import getopt, sys


def parameters(argv):

    # defaults
    _metric_name="custom_metrics"
    _defauft_labels = 'custom-metrics=app'
    _port = 5081

    try:
        opts, args = getopt.getopt(argv,"h",["name=","labels=","port="])
    except getopt.GetoptError:
        print("invalid parameter")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h"):
            print("--name=metricname, --labels=key1=value1,key2=value2, --port=5081")
            exit(1)
        elif opt in ("--name"):
            _metric_name = arg
        elif opt in ("--labels"):
            _defauft_labels = arg
        elif opt in ("--port"):
            _port = arg
        
    return (_metric_name,_defauft_labels,_port)

_metric_value={}
_metric_name,_defauft_labels,_port = parameters(sys.argv[1:])
print("name: %s, labels: %s, port: %s" % (_metric_name,_defauft_labels,_port))
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "try:\n /metrics\n /payload?foo1=bar1&foo2=bar2\n"

@app.route('/payload', methods=['GET'])
def payload():

    # construct default label
    _payload_labels=[]
    for _label in _defauft_labels.split(','): 
        _key,_value=_label.split('=')
        _payload_labels.append(_key + '="' +_value + '"')

    # construct labels
    _args = request.args
    for _key in sorted(_args.keys()):
        try:
            _value = _args.get(_key,'')
            print("%s=%s" % (_key,_value))
            _payload_labels.append(_key + '="' +_value + '"')
        except:
            print('no value \n')
            pass

    # join labels
    _labels=','.join(_payload_labels)
    
    # update counter
    try:
        _metric_value[_labels]+=1
    except:
        _metric_value[_labels]=1
        pass
    
    # logging
    print("%s{%s} %s" % (_metric_name,_labels,_metric_value[_labels]))
    print("Headers:\n",request.headers)
    print("Request:",request)

    # return response  
    _result=""
    if re.match("(Mozilla|AppleWebKit|Chrome|Safari)", str(request.headers.get('User-Agent'))):
        _result='ok' + '<br>' + str(request) + '<br>' + str(request.headers.get('User-Agent')) + "<br>"    
    else:
        _result="\nok" + '\n' + str(request) + '\n' + str(request.headers.get('User-Agent')) + "\n"

    return _result 

@app.route('/metrics', methods=['GET'])
def metrics():

    # create metric header
    _metrics=[]
    _metrics.append('# HELP ' + _metric_name + ' Number of events')
    _metrics.append('# TYPE ' + _metric_name + ' counter')

    # Contruct metrics
    for _labels in _metric_value:
        _metrics.append(_metric_name + '{' + _labels + '} ' + str(_metric_value[_labels]) )

    print("Headers:\n",request.headers)
    print("Request:",request)

    # join metrics
    _result=""
    if re.match("(Mozilla|AppleWebKit|Chrome|Safari)", str(request.headers.get('User-Agent'))):
        _result="<br>".join(_metrics) + '<br>'
    else:
        _result="\n".join(_metrics) + '\n'
    
    return _result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=_port)