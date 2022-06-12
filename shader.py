from OpenGL.GL import *


class ShaderSource:
    def __init__(self, vertex_path: str, fragment_path: str):
        vertex_file = open(vertex_path)
        self.vertex_src = vertex_file.read()
        vertex_file.close()

        fragment_file = open(fragment_path)
        self.fragment_src = fragment_file.read()
        fragment_file.close()


class Shader:
    def __init__(self, vertex_path: str, fragment_path: str):
        self.vertex_path = vertex_path
        self.fragment_path = fragment_path
        source = ShaderSource(self.vertex_path, self.fragment_path)
        self.id = self.create_shader(source.vertex_src, source.fragment_src)
        self.uniform_cache = dict()

    def __del__(self):
        glDeleteProgram(self.id)

    def bind(self):
        glUseProgram(self.id)

    def unbind(self):
        glUseProgram(0)

    def get_uniform_location(self, uniform_name: str):
        if uniform_name in self.uniform_cache:
            return self.uniform_cache[uniform_name]

        location = glGetUniformLocation(self.id, uniform_name)
        if location == -1:
            print("경고! 유니폼 " + uniform_name + " 은(는) 존재하지 않습니다!")
        else:
            self.uniform_cache[uniform_name] = location
        return location

    def compile_shader(self, shader_type, source: str):
        shader_id = glCreateShader(shader_type)
        glShaderSource(shader_id, source)
        glCompileShader(shader_id)

        result = glGetShaderiv(shader_id, GL_COMPILE_STATUS)
        if result == GL_FALSE:
            log = glGetShaderInfoLog(shader_id)
            if log:
                print("쉐이더 컴파일 오류!")
                if shader_type == GL_VERTEX_SHADER:
                    print("Vertex shader")
                elif shader_type == GL_FRAGMENT_SHADER:
                    print("Fragment shader")
                glDeleteShader(shader_id)
                raise Exception(log)

        return shader_id

    def create_shader(self, vertex_src: str, fragment_src: str, ):
        shader_program = glCreateProgram()
        vertex_shader = self.compile_shader(GL_VERTEX_SHADER, vertex_src)
        fragment_shader = self.compile_shader(GL_FRAGMENT_SHADER, fragment_src)

        glAttachShader(shader_program, vertex_shader)
        glAttachShader(shader_program, fragment_shader)
        glLinkProgram(shader_program)
        glValidateProgram(shader_program)

        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)

        program_log = glGetProgramInfoLog(shader_program)

        if program_log:
            print("쉐이더 프로그램 링크 오류")
            if "unsuccessful" in program_log:
                raise Exception(program_log)
            else:
                print(program_log)
        return shader_program

    def set_uniform4f(self, uniform_name: str, v0: float, v1: float, v2: float, v3: float):
        location = self.get_uniform_location(uniform_name)
        glUniform4f(location, v0, v1, v2, v3)

    def set_uniform2f(self, uniform_name: str, v0: float, v1: float):
        location = self.get_uniform_location(uniform_name)
        glUniform2f(location, v0, v1)

    def set_uniform1f(self, uniform_name: str, value: float):
        location = self.get_uniform_location(uniform_name)
        glUniform1f(location, value)

    def set_uniform1fv(self, uniform_name: str, size: int, values):
        location = self.get_uniform_location(uniform_name)
        glUniform1fv(location, size, values)

    def set_uniform1iv(self, uniform_name: str, size: int, values):
        location = self.get_uniform_location(uniform_name)
        glUniform1iv(location, size, values)

    def set_uniform1i(self, uniform_name: str, value: int):
        location = self.get_uniform_location(uniform_name)
        glUniform1i(location, value)










