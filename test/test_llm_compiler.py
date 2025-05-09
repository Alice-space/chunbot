from source.ihep_edu import IHEPEDUSource
from compile.LLM import LLMCompiler

def test_llm_compiler():
    ihep = IHEPEDUSource()
    l = LLMCompiler({'personal_info': "我是小学生"})
    print(l.compile_info(ihep.get_list()[0]))