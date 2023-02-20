import ts_functions
from time import sleep
from os.path import exists

def main():
    driver = ts_functions.start_selenium()
    # A good practice to access the elements in the csv is using a dict
    keys = ['age', 'numeration', 'popularity', 'country', 'num_of_comments', 'time', 'sex', 'text', 'temporales']
    while True:
        # For file to change you gotta close it first maybe?
        with open('secrets.csv', 'a', encoding='utf-8', newline='') as sf:
            secrets = ts_functions.get_secrets(driver)
            new_secrets = []
            writer_1 = ts_functions.csv.DictWriter(sf, keys)
            not_first_run = exists('last_secret.csv')
            if not_first_run:
                with open('last_secret.csv', 'r', encoding='utf-8', newline='') as rlf:
                    reader = ts_functions.csv.DictReader(rlf, fieldnames=keys)
                    for row in reader:
                        only_secret = row
            for secret in secrets:
                if not_first_run:
                    #print(secret)
                    if only_secret['numeration'] == secret['numeration']:
                        break
                new_secrets.append(secret)
            new_secrets.reverse()
            for secret in new_secrets:
                value = ts_functions.grab_temporales(secret['text'])
                secret['temporales'] = value
                writer_1.writerow(secret)
            with open('last_secret.csv', 'w', encoding='utf-8', newline='') as wlf:
                writer_2 = ts_functions.csv.DictWriter(wlf, keys)
                writer_2.writerow(new_secrets[-1])
        sleep(110)
main()
