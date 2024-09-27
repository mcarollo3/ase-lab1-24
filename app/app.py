from flask import Flask, json, request, make_response, jsonify
import random

app = Flask(__name__, instance_relative_config=True)

last_operation = None

@app.route('/')
def home():
    return '<h1>Hello!</h1>'  # Puoi restituire anche un template HTML

@app.route('/add')
def add():
    global last_operation
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    if a is not None and b is not None:
        result = a + b
        last_operation = f"add({a},{b})={result}"
        return make_response(jsonify(s=result), 200)  # HTTP 200 OK
    else:
        return make_response('Invalid input\n', 400)  # HTTP 400 BAD REQUEST

@app.route('/sub')
def sub():
    global last_operation
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    if a is not None and b is not None:
        result = a - b
        last_operation = f"sub({a},{b})={result}"
        return make_response(jsonify(s=result), 200)  # HTTP 200 OK
    else:
        return make_response('Invalid input\n', 400)  # HTTP 400 BAD REQUEST

@app.route('/mul')
def mul():
    global last_operation
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    if a is not None and b is not None:
        result = a * b
        last_operation = f"mul({a},{b})={result}"
        return make_response(jsonify(s=result), 200)  # HTTP 200 OK
    else:
        return make_response('Invalid input\n', 400)  # HTTP 400 BAD REQUEST

@app.route('/div')
def div():
    global last_operation
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    if a is not None and b is not None:
        if b == 0:
            return make_response('Invalid input, you cannot divide by zero\n', 400)
        else:
            result = a / b
            last_operation = f"div({a},{b})={result}"
            return make_response(jsonify(s=result), 200)  # HTTP 200 OK
    else:
        return make_response('Invalid input\n', 400)  # HTTP 400 BAD REQUEST

@app.route('/mod')
def mod():
    global last_operation
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    if a is not None and b is not None:
        if b == 0:
            return make_response('Invalid input, you cannot modulo by zero\n', 400)
        else:
            result = a % b
            last_operation = f"mod({a},{b})={result}"
            return make_response(jsonify(s=result), 200)  # HTTP 200 OK
    else:
        return make_response('Invalid input\n', 400)  # HTTP 400 BAD REQUEST

@app.route('/random')
def rand():
    global last_operation
    a = request.args.get('a', type=int)
    b = request.args.get('b', type=int)
    if a is not None and b is not None:
        if a > b:
            random_value = random.randint(b, a)
        else:
            random_value = random.randint(a, b)
        last_operation = f"rand({a},{b})={random_value}"
        return make_response(jsonify(s=random_value), 200)  # HTTP 200 OK
    else:
        return make_response('Invalid input\n', 400)  # HTTP 400 BAD REQUEST

@app.route('/upper')
def up():
    global last_operation
    a = request.args.get('a', type=str)
    if a:
        result = a.upper()
        last_operation = f"upper({a})={result}"
        return make_response(jsonify(s=result), 200)  # HTTP 200 OK
    else:
        return make_response('Invalid input\n', 400)  # HTTP 400 BAD REQUEST

@app.route('/lower')
def low():
    global last_operation
    a = request.args.get('a', type=str)
    if a:
        result = a.lower()
        last_operation = f"lower({a})={result}"
        return make_response(jsonify(s=result), 200)  # HTTP 200 OK
    else:
        return make_response('Invalid input\n', 400)  # HTTP 400 BAD REQUEST

@app.route('/concat')
def concat():
    global last_operation
    a = request.args.get('a', type=str)
    b = request.args.get('b', type=str)
    if a and b:
        result = a + b
        last_operation = f"concat({a},{b})={result}"
        return make_response(jsonify(s=result), 200)  # HTTP 200 OK
    else:
        return make_response('Invalid input\n', 400)  # HTTP 400 BAD REQUEST

@app.route('/reduce')
def reduce_list():
    global last_operation
    op = request.args.get('op')
    lst = request.args.get('lst')

    try:
        lst = json.loads(lst)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid list format"}), 400

    result = None

    if op == 'add':
        result = sum(lst)
    elif op == 'sub':
        result = lst[0] - sum(lst[1:])
    elif op == 'mul':
        result = 1
        for number in lst:
            result *= number
    elif op == 'div':
        try:
            result = lst[0]
            for number in lst[1:]:
                result /= number
        except ZeroDivisionError:
            return jsonify({"error": "Division by zero"}), 400
    elif op == 'concat':
        result = ''.join(map(str, lst))
    else:
        return jsonify({"error": "Invalid operator"}), 400

    last_operation = f"reduce('{op}',{lst})={result}"
    
    return jsonify({"s": result})

@app.route('/last')
def last_operation_endpoint():
    if last_operation is None:
        return jsonify({"error": "No operation performed"}), 404
    return jsonify({"last_operation": last_operation})

if __name__ == '__main__':
    app.run(debug=True)