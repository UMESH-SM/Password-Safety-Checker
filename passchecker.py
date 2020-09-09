import requests, hashlib

def req_api_data(query_str):
    url = 'https://api.pwnedpasswords.com/range/' + query_str
    res = requests.get(url)
    hashes = (line.split(':') for line in (res.text).splitlines())
    return hashes

def check_count(hashes, pass_tail):
    for h, count in hashes:
        if h == pass_tail:
            return count
    return 0

def pass_input(password):
    sha1_pass = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5chars, tail = sha1_pass[:5], sha1_pass[5:]
    hashes = req_api_data(first5chars)
    count = check_count(hashes, tail)
    return count

@app.route('/passcheck', methods=['POST', 'GET'])
def pass_check():
    if request.method == 'POST':
        password = request.form['password']
    count = pass_input(password)
    if count:
        return render_template("passwordchecker.html", msg1 = f'The Password has been hacked {count} times!')
    else:
        return render_template("passwordchecker.html", msg2 = 'The Password is Safe to Use.') 
