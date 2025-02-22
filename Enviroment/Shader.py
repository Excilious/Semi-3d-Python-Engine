from Settings import *
from Enviroment.TextureID import ID

class ShaderProgram:
    def __init__(self,Engine):
        self.Engine = Engine
        self.Context = Engine.Context
        self.Player = Engine.Player

        self.Level = self.GetProgram(Shader='level')
        self.InstancedDoor = self.GetProgram(Shader='instanced_door')
        self.InstancedBillboard = self.GetProgram(Shader='instanced_billboard')
        self.InstancedHud = self.GetProgram(Shader='instanced_hud')
        self.Weapon = self.GetProgram(Shader='weapon')
        self.Default = self.GetProgram(Shader='Default')
        self.Shadow = self.GetProgram(Shader="ShadowProgram")
        self.SetUniform()

    def SetUniform(self):
        self.Level['m_proj'].write(self.Player.MatrixProjection)
        self.Level['u_texture_array_0'] = TEXTURE_UNIT

        self.InstancedDoor['m_proj'].write(self.Player.MatrixProjection)
        self.InstancedDoor['u_texture_array_0'] = TEXTURE_UNIT

        self.InstancedBillboard['m_proj'].write(self.Player.MatrixProjection)
        self.InstancedBillboard['u_texture_array_0'] = TEXTURE_UNIT

        self.InstancedHud['u_texture_array_0'] = TEXTURE_UNIT
        self.Weapon['u_texture_array_0'] = TEXTURE_UNIT

    def Update(self):
        self.Level['m_view'].write(self.Player.MatrixView)
        self.InstancedDoor['m_view'].write(self.Player.MatrixView)
        self.InstancedBillboard['m_view'].write(self.Player.MatrixView)


    def GetProgram(self,Shader):
        with open(f'Shaders/{Shader}.vert') as File:
            VertexShader = File.read()

        with open(f'Shaders/{Shader}.frag') as File:
            FragmentShader = File.read()

        Program = self.Context.program(vertex_shader=VertexShader, fragment_shader=FragmentShader)
        return Program
