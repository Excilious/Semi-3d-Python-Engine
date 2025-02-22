from Meshes.QuadMesh import *

class WeaponMesh(QuadMesh):
    def __init__(self,Engine,Shader,WeaponInstance):
        super().__init__(Engine,Shader)
        self.Weapon = WeaponInstance

    def SetUniform(self):
        self.Program['m_model'].write(self.Weapon.MatrixModel)
        self.program['tex_id'] = self.Weapon.Frame + self.WeaponInstance.WeaponID

    def Render(self):
        self.SetUniform()
        self.VertexArray.render()
