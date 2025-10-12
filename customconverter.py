import sys, csv, json, pycountry

def cname(code):
    code = (code or '').strip()
    if not code:
        return ''
    #if code.upper() == 'UK':
    #    code = 'GB'
    c = pycountry.countries.get(alpha_2=code) or pycountry.countries.get(alpha_3=code)
    return getattr(c, 'common_name', c.name) if c else ''

def norm_row(r):
    r = [(x or '').strip() for x in r]
    n = len(r)
    if n == 0:
        return []
    if n == 6:
        return r
    if n > 6:
        iso = r[2]
        return [r[0], r[1], iso, cname(iso), r[3], r[5]]
    # n < 6: 右侧补空
    r += [''] * (6 - n)
    return r

def main():
    if len(sys.argv) < 4:
        print('Usage: python script.py in1.csv[,in2.csv,...] out.csv out.json')
        return
    inputs = [p.strip() for p in sys.argv[1].split(',') if p.strip()]
    out_csv, out_json = sys.argv[2], sys.argv[3]

    with open(out_csv, 'w', newline='', encoding='utf-8') as ocsv, \
         open(out_json, 'w', encoding='utf-8') as ojson:
        w = csv.writer(ocsv)
        for path in inputs:
            with open(path, newline='', encoding='utf-8') as f:
                for r in csv.reader(f):
                    if not r:
                        continue
                    a = norm_row(r)
                    if not a:
                        continue
                    w.writerow(a)
                    obj = {
                        "start_ip": a[0],
                        "end_ip": a[1],
                        "country": {"iso_code": a[2], "names": {"en": a[3]}},
                        "subdivisions": [{"names": {"en": a[4]}}],
                        "city": {"names": {"en": a[5]}}
                    }
                    ojson.write(json.dumps(obj, ensure_ascii=False, separators=(',', ':')) + '\n')

if __name__ == '__main__':
    main()