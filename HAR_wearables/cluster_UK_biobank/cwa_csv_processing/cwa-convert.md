helper commands:

find /home/aayush/accelerometer/random-22/random-22/left_cwa/ -type f | xargs -I{} sh -c '../cwa-convert "{}" -out "$(basename "{}").csv"'


ls /home/aayush/accelerometer/random-22/random-22/left_cwa/* | xargs -I{} basename {}

