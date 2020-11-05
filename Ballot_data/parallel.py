import requests
import json
import os
from pathlib import Path
import pandas as pd
import sys

def get_deaths(start_death_year):
    PATH = Path(__file__).parent.resolve()
    SAVE_PATH = os.path.join(PATH, f'wayne-{start_death_year}.csv') 
    print(f'File will be saved to: {SAVE_PATH}')
    data_list = []
    counter = 0
    for birthyear in range(start_death_year, start_death_year + 21):
        for deathyear in range(1950, 2019):
            for page in range(1, 500000):
                try:

                    r = requests.get('https://www.ancestry.com/api/search-results?event=_Wayne-Michigan-USA_3093&pg={0}&birth={1}&death={2}_Michigan-USA_25&birth_x=0-0-0&count=50&death_x=0-0-0&event_x=_1-0-a&types=r&categories=&collections=&debug=&searchState=Pagination&testCaseId='.format(page, birthyear, deathyear)).json()
                    counter += 1
                    if r['results']['items'] == []:
                        print(birthyear, deathyear, page, r['results']['hitCount'], counter)
                        if counter % 100 == 0:
                            df_data = pd.DataFrame.from_dict(data_list)
                            df_data.to_csv(SAVE_PATH, index=False)
                        break

                    for person in r['results']['items']:
                        temp_dict = {'recordID':person['recordId']}
                        a = {k['label']:k['text'] for k in person['fields']}
                        temp_dict.update(a)
                        data_list.append(a)

                    print(birthyear, deathyear, page, r['results']['hitCount'], counter)
        
                    if counter % 100 == 0:
                        df_data = pd.DataFrame.from_dict(data_list)
                        df_data.to_csv(SAVE_PATH, index=False)
                except Exception as e:
                        with open(os.path.join(PATH, 'Errors', f'error-{birthyear}-{counter}.txt'), '+w') as f:
                            f.write(str(e))

    df_data = pd.DataFrame.from_dict(data_list)
    df_data.to_csv(SAVE_PATH, index=False)

    return

if __name__ == "__main__":
    get_deaths(int(sys.argv[1]))