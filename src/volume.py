import json


def get_price(data):
    Open = data[0]['시가']

    high_list = []
    low_list = []
    for i in data:
        high_list.append(i['고가'])
        low_list.append(i['저가'])
    close = i['종가']
    high = max(high_list)
    low = min(low_list)
    return (Open, high, low, close)


stock_info = [
    ('053580', '웹케시'),
    ('011000', '진원생명과학'),
    ('014990', '인디에프'),
    ('032940', '원익'),
    ('089150', '케이씨티'),
]
for code, name in stock_info:
    with open(f'data/{code}.txt', 'r', encoding='utf-8') as txt:
        data: dict[str, str|int] = json.load(txt)
    Open, high, low, close = get_price(data)

    hsub = high - close
    hh, hm, hl = (round(high-hsub/4), round(high-hsub/2), round(close+hsub/4))
    lsub = close - low
    lh, lm, ll = (round(close-lsub/4), round(close-lsub/2), round(low+lsub/4))

    volume = sum([i['거래량'] for i in data])
    print()
    print(f'종목코드 : {code}')
    print(f'종목명 : {name}')
    print(f'시가 : {Open:,}원, 고가 : {high:,}원, 저가 : {low:,}원, 종가 : {close:,}원')
    print(f'전체 거래량 : {volume:,}주')
    print('\n거래량 분포')

    hh_list = []
    hm_list = []
    hl_list = []
    ch_list = []
    cl_list = []
    lh_list = []
    lm_list = []
    ll_list = []
    for i in data:
        L, H = (i['저가'], i['고가'])

        a = 0
        b = 0
        c = 0
        d = 0
        e = 0
        f = 0
        g = 0
        h = 0

        for p in (L, H):
            if hh < p:
                a += 1
            if hm < p:
                b += 1
            if hl < p:
                c += 1
            if close < p:
                d += 1
            if lh < p:
                e += 1
            if lm < p:
                f += 1
            if lh < p:
                g += 1
            if L <= H:
                h += 1

        v = i['거래량'] / (a+b+c+d+e+f+g+h)

        if a:
            hh_list.append(v * a)
        if b:
            hm_list.append(v * b)
        if c:
            hl_list.append(v * c)
        if d:
            ch_list.append(v * d)
        if e:
            cl_list.append(v * e)
        if f:
            lh_list.append(v * f)
        if g:
            lm_list.append(v * g)
        if h:
            ll_list.append(v * h)

    for n, l in {
        '고가 75% ~ 고가 100%': hh_list,
        '고가 50% ~ 고가 75%': hm_list,
        '고가 25% ~ 고가 50%': hl_list,
        '종가 ~ 고가 25%': ch_list,
        '저가 25% ~ 종가': cl_list,
        '저가 50% ~ 저가 25%': lh_list,
        '저가 75% ~ 저가 50%': lm_list,
        '저가 100% ~ 저가 75%': ll_list
    }.items():
        print(f'  {n}')
        s = sum([round(i) for i in l])
        print(f'    {s:,}주')
        print(f'    {round(s * 100 / volume, 2)}%')
