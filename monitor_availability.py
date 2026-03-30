import requests, time, csv
from datetime import datetime

ALB_URL  = 'http://flask-app-alb-808434288.eu-west-2.elb.amazonaws.com'
INTERVAL = 30
OUTPUT   = 'availability_log.csv'

print(f'Monitoring {ALB_URL} every {INTERVAL}s')
print('Press Ctrl+C to stop\n')

with open(OUTPUT, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['timestamp', 'status_code',
                     'response_ms', 'available'])
    total = 0
    available = 0
    try:
        while True:
            try:
                t0 = time.time()
                r  = requests.get(f'{ALB_URL}/health', timeout=5)
                ms = round((time.time() - t0) * 1000, 1)
                ok = 1 if r.status_code == 200 else 0
                writer.writerow(
                    [datetime.now(), r.status_code, ms, ok])
                f.flush()
                total += 1
                available += ok
                pct = 100 * available / total
                print(f'[{datetime.now().strftime("%H:%M:%S")}] '
                      f'HTTP {r.status_code}  {ms}ms  '
                      f'Availability: {pct:.1f}%')
            except Exception as e:
                writer.writerow([datetime.now(), 0, 0, 0])
                total += 1
                print(f'ERROR: {e}')
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        pct = 100 * available / total
        print(f'\nFinal availability: {pct:.1f}%')
        print(f'Saved to: {OUTPUT}')