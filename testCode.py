test = ['a, b, c, d', 'e, f, g, h']

new = [tuple(item.split(',')) for item in test]