from source.ihep_edu import IHEPEDUSource
from store.sqlite import SQLiteStore

def test_get_list():
    ihep = IHEPEDUSource()
    sql = SQLiteStore({
        "db_path": "test.sqlite"
    })
    sql.update_list(ihep.get_list())