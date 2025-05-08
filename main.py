from source.ihep_edu import IHEPEDUSource
from store.sqlite import SQLiteStore

ihepsource = IHEPEDUSource()
sqliteStore = SQLiteStore()

print(sqliteStore.update_list(ihepsource.get_list()))