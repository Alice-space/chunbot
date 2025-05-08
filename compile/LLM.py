from compile.base import Compiler


class LLMCompiler(Compiler):
    def compile_info(self, source_description, title, url):
        return source_description + title + url

    def compile_list(self, info_list):
        r = ""
        for info in info_list:
            r += "\n".join(info)
        return r
