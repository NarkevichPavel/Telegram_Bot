def test(request: dict):
    data  = {**request}
    print(data)

a = {
    'a': 'hello',
}

test(a)
