from source.ihep_edu import IHEPEDUSource
from compile.LLM import LLMCompiler

def test_llm_compiler_list():
    ihep = IHEPEDUSource()
    l = LLMCompiler({'personal_info': "我是小学生"})
    info = ihep.get_list()[:2]
    compiled = [l.compile_info(i) for i in info]
    print(l.compile_list(compiled))