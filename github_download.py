import glob, json, codecs, sqlite3, json, datetime
import csv
import src.tor_spider as TOR
    
class GITHUB_API(object):

    def __init__(self, name, API_KEY, sesson = None):
        self.name = name
        self.TOKEN = API_KEY
        
        if session == None:
            self.session = TOR._local_session
        else:
            self.session = sesson
            
    def check_limits():
        rate_limit_url = "https://api.github.com/rate_limit"
        payload = {"access_token":self.TOKEN,}
        r = self.session.get(rate_limit_url,params=payload)

        print r.text
        
        #limit_js = ast.literal_eval(R.text)
        #remaining = limit_js["rate"]["remaining"]
        #if not remaining:
        #    print "Overloaded requests MUST WAIT!"
        #    return 0
        #return remaining


f_credentials = "db/credentials.csv"
USERS = []
with open(f_credentials) as FIN:
    for api_token, name in csv.reader(FIN):
        user = GITHUB_API(name, api_token)
        USERS.append(user)
       

exit()


f_repo_info = "db/repo_info.db"
conn = sqlite3.connect(f_repo_info)

# Get the column names
cursor = conn.execute('SELECT * FROM repo_info LIMIT 1')
cols = list(map(lambda x: x[0], cursor.description))

# Remove ID from cols, we don't want to change it
cols.remove("id")

cols_dates = [1 if "_at" in name else 0 for name in cols]

cmd_select = '''
SELECT id, full_name FROM repo_info
WHERE created_at IS NULL AND fork=0
LIMIT 20
'''

cursor = conn.execute(cmd_select)

for item in cursor:
    print item
