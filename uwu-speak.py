
if __name__ == '__main__':
    input_text = input("Wut to say senpai?     ")
    words = input_text.split(" ")
    rep_map = {'l': 'w',
               'r': 'w',
               'on': 'ony',
               'no': 'nyo'}

    out_text = ''
    for word in words:
        new = word
        for orig in rep_map:
            new = new.replace(orig, rep_map[orig])
        out_text += new + ' '
    print(out_text)
