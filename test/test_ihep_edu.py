from source.ihep_edu import IHEPEDUSource

def test_get_list():
    ihep = IHEPEDUSource()
    print(ihep.get_list())