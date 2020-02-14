def drawSaveButton():
    buttonFont = pygame.font.Font(r"C:\Windows\Fonts\REFSAN.TTF", 40)
    saveText = buttonFont.render("СОХРАНИТЬ", True, purple)
    drawSaveButton.saveButtonRect = saveText.get_rect(center=(485, 565))
    pygame.draw.rect(window, purple, drawSaveButton.saveButtonRect, 5)
    window.blit(saveText, drawSaveButton.saveButtonRect)
