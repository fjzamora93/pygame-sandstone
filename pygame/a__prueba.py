def salto(self):    
        if self.jumping:
            if self.jump_count <= 10 and not self.parabola: #Parabola de subida del salto
                self.rect.y -= (self.jump_count * self.jump_count * 0.8)
                self.jump_count += 0.2 #Velocidad de subida y bajada
            elif self.jump_count >= 0: #Parabola de bajada del dalto
                self.rect.y -= (self.jump_count * self.jump_count * 0.8)
                self.jump_count -= 0.2
                self.parabola= True
            if self.jump_count < 5: #Restablecimiento del salto
                self.jump_count=10
                self.jumping = False
                self.parabola= False